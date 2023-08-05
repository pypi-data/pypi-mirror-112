#!/usr/bin/env python
# -*- coding=utf-8 -*-
import re
import os
import sys
import json
import socket
import textwrap
import tarfile
import dateutil.parser

try:
    from commands import getoutput
except ImportError:
    from subprocess import getoutput

from lims.tools.login import login
from lims.tools.project import Project
from lims.tools.release import Release
from lims.tools import utils


raw_input = __builtins__.get('raw_input', input)


class Report(object):

    def __init__(self, **kwargs):

        self.kwargs = kwargs
        self.session = login(kwargs)
        self.project = None
        self.logger = utils.get_logger(**kwargs)

        if 'njlogin' in socket.gethostname():
            self.exe_path = '/NJPROJ2/MICRO/PROJ/lidanqing/lims'
        else:
            self.exe_path = '/TJPROJ1/MICRO/lidanqing/lims'

    def start(self):

        if self.kwargs['filename']:
            if not os.path.exists(self.kwargs['filename']):
                self.logger.error('报告路径不存在：{filename}'.format(**self.kwargs))
                exit(1)

            name = re.findall(r'(?:QC|Mapping|Report)-(?:.+?)-B\d+-5.zip', os.path.basename(self.kwargs['filename']))

            if not self.kwargs['filename'].endswith('.zip'):
                self.logger.warn('请使用zip格式打包报告!')
                self.logger.info('自动执行转换...')
                self.convert2zip(self.kwargs['filename'])

            if not name:
                self.logger.error('报告命名有误，请检查！(命名规则：(QC|Mapping|Report)-分期编号-Bx-5*)')
                exit(2)

            if self.kwargs['stage_code'] and (self.kwargs['stage_code'] not in name[0]):
                self.logger.error('指定的分期编号和报告文件中的不一致，请检查！')
                print('分期编号：{stage_code}\n报告名称：{filename}'.format(**self.kwargs))
                exit(3)

            if not self.kwargs['stage_code']:
                self.kwargs['stage_code'] = name[0]

            if not self.kwargs['type']:
                if 'Mapping' in self.kwargs['filename']:
                    self.kwargs['type'] = 'mapping'
                elif 'QC' in self.kwargs['filename']:
                    self.kwargs['type'] = 'qc'

            if not self.kwargs['type']:
                self.logger.error('请指定报告类型')
                exit(1)
        elif not self.kwargs['stage_code']:
            self.logger.warn('请指定分期编号')
            exit(3)

        result = Project(**self.kwargs).get_project_list(**self.kwargs)
        if not result:
            self.logger.warn('指定分期不存在，请检查!({stage_code})'.format(**self.kwargs))
            exit(4)

        self.project = result[0]

        if self.kwargs['filename'] and self.kwargs['type']:
            res = self.upload_report()
            if res and self.kwargs['type'] == 'final':
                sample_count, data_size, sample_list = res
                if self.kwargs['release_path']:
                    Release(**self.kwargs).start()
                else:
                    self.logger.warn('\033[1;3;31m不要忘记释放项目数据：lims release -stage {stage_code} -path xxx ...\033[0m'.format(**self.kwargs))
        elif self.kwargs['delete']:
            self.delete_report()
        elif not (self.kwargs['filename']  or self.kwargs['type']):
            self.show_report_status()
        elif not self.kwargs['filename']:
            self.logger.error('请指定报告路径')
        elif not self.kwargs['type']:
            self.logger.error('请指定报告类型')

    def convert2zip(self, filename):

        basename = re.sub(r'\.tar.*', '', os.path.basename(filename))

        name = getoutput('tar -tf {}'.format(filename)).split()[0].strip('/')
        cmd = textwrap.dedent('''
            tar xf {filename}
            zip -r {basename}.zip {name}
        ''').format(**locals())

        self.logger.info(cmd)
        assert not os.system(cmd)
        self.kwargs['filename'] = basename + '.zip'

    @property
    def has_upload_final(self):
        '''
            检查是否上传过结题报告
            result: False已上传, True未上传
            return: True-已上传, False-未上传
        '''
        url = '{base_url}/KF_DataAnalysis.HasUploadFinalReport.lims'.format(**self.kwargs)
        self.logger.debug('check final: ' + url)

        payload = [self.kwargs['stage_code']]

        result = self.session.post(url, json=payload).json()

        return not result

    def upload_report(self):

        if self.project['STAGECODE'] not in self.kwargs['filename']:
            self.logger.error('报告名称和分期编号不符，请检查！')
            print('分期编号:', self.project['STAGECODE'])
            print('报告名称:', os.path.basename(self.kwargs['filename']))
            exit(1)

        # step1: 上传文件
        url = '{base_url}/Runtime_Support.SaveFileFromHTML.lims?ScriptName=QuickIntro.uploadFileProcessingScript'.format(**self.kwargs)
        self.logger.debug('upload file: ' + url)
        with utils.safe_open(self.kwargs['filename'], 'rb') as f:
            resp = self.session.post(url, files={'file': f}).json()
            # print(resp)

        if not resp['success']:
            self.logger.error('文件上传失败!')
            exit(1)

        # 获取报告邮件信息
        message = self.kwargs['message']
        if not message:
            message = ''
            url = '{base_url}/KF_DataAnalysis.kf_EmailBody.lims'.format(**self.kwargs)
            email_bodys = self.session.post(url, json=[self.kwargs['stage_code']]).json()
            idx = ['qc', 'mapping', 'final'].index(self.kwargs['type'])
            self.logger.info('请填写报告备注信息(\033[33m回车键结束输入，Ctrl+Backspace回退\033[0m)')
            for line in email_bodys[idx].strip().split('\n'):
                input_char = raw_input(line)
                message += line + input_char + '\n'

        self.logger.debug('备注信息：\n\033[33m{}\033[0m'.format(message.strip()))

        # step2: 填写报告
        payload = resp['result'] + [self.kwargs['stage_code'], self.kwargs['type'].upper(), None, message]

        # sample_count = data_size = sample_list = None
        # if not self.kwargs['xian_xia']:
            # sample_count, data_size, novoid_list, sample_list = self.parse_qcstat()
        sample_count, data_size, novoid_list, sample_list = self.parse_qcstat()

        # if not self.kwargs['xian_xia']:
        # print(sample_count, data_size, novoid_list)
        # exit()

        # if self.kwargs['type'] == 'final' and not self.has_upload_final:
        if self.kwargs['type'] == 'final':
            print('>>> 首次上传结题报告sop和产量信息为必填项，后续无需再次填写')    # 可以上传多个结题报告?
            sop_method = self.choose_sops()
            payload += [sop_method, sample_count, data_size]

            self.logger.info('\033[32m样本数：{sample_count}  数据量：{data_size}\033[0m'.format(**locals()))

        if self.kwargs['type'] == 'final':
            # 新增结题样本功能
            if self.kwargs['xian_xia']:
                self.logger.info('线下项目，不更新结题样本')
            elif self.kwargs['type'] == 'final':
                self.logger.info('\033[32m诺禾编号列表：{}\033[0m'.format(','.join(novoid_list)))
                self.update_conclustatus(novoid_list)

        # 上传报告
        self.logger.debug(payload)
        url = '{base_url}/KF_DataAnalysis.UploadReport_H.lims'.format(**self.kwargs)
        self.logger.debug('upload report: ' + url)
        resp = self.session.post(url, json=payload).json()
        self.logger.debug(resp)

        if resp[-1] == 'SUCCESS':
            report_name = resp[0]
            add_time = dateutil.parser.parse(resp[1]).strftime('%Y-%m-%d %H:%M:%S')
            self.logger.info('\033[32m报告上传成功！\033[0m')

            report_guid = self.get_reports(report_name=report_name, add_time=add_time)['REPORT_GUID']
            self.logger.debug('report guid: ' + report_guid)

        # step3: 提交给DoubleCheck
        url = '{base_url}/KF_DataAnalysis.SubmitStaging_H2.lims'.format(**self.kwargs)
        self.logger.debug('submit report: ' + url)
        payload = [report_guid, 'Draft', 'Submit']
        resp = self.session.post(url, json=payload).text

        self.logger.info('\033[32m已提交给DoubleCheck: {DOUBLECHECKERNAME}\033[0m'.format(**self.project))
        # self.show_report_status(report_guid)

        return sample_count, data_size, sample_list

    def update_conclustatus(self, novoid_list):
        '''
        更新结题样本
        '''
        self.logger.info('更新结题样本中...')
        url = '{base_url}/KF_DataAnalysis.kf_UpdateConclustatus.lims'.format(**self.kwargs)

        payload = [','.join(novoid_list), self.kwargs['stage_code']]

        print(novoid_list)

        resp = self.session.post(url, json=payload)
        if resp.status_code != 200:
            self.logger.warn('\033[31m更新失败！等待LIMS系统修复BUG ......\033[0m')
            self.logger.debug(resp.text)
            # exit(1)
            return

        # 检查是否更新成功
        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgStagingSample_H&Type=json&p1={stage_code}'.format(**self.kwargs)
        data = self.session.get(url).json()
        rows = data['Tables'][0]['Rows']

        result = {row['SAMPLEID']: row['CONCLUSTATUS'] for row in rows}

        all_samples = result.keys()
        jieti_samples = [each for each in result if result[each]]
        not_jieti_samples = [each for each in result if not result[each]]

        if not set(novoid_list).issubset(set(all_samples)):
            self.logger.error('\033[31m输入的诺禾编号有误，请检查！\033[0m')
            print('输入: {}'.format(','.join(novoid_list)))
            print('系统: {}'.format(','.join(all_samples)))
            print('有问题的诺禾编号：{}'.format(set(novoid_list).difference(set(all_samples))))
            if not self.kwargs['ignore']:
                exit(1)

        if not_jieti_samples:
            self.logger.warn('\033[33m部分样本没有结题，请注意！\033[0m')
            print('已结题样本({}): {}'.format(len(jieti_samples), ', '.join(jieti_samples)))
            print('未结题样本({}): {}'.format(len(not_jieti_samples), ', '.join(not_jieti_samples)))
        else:
            self.logger.info('{}个样本已更新为结题状态'.format(len(jieti_samples)))

    def parse_qcstat(self):
        '''
            默认从qcstat.xls中读取数据量，样本数，样本诺禾编号列表
            若指定参数，则使用指定的值
        '''
        qcstat = utils.get_qcstat(qcstat=self.kwargs['qcstat'], report=self.kwargs['filename'])

        if not qcstat:
            self.logger.warn('qcstat.xls不存在，请手动输入数据量，样本数和样本诺禾编号列表')
            sample_count = raw_input('样本数:')
            data_size = raw_input('数据量:')
            novoid_list = set(raw_input('诺禾编号(逗号分隔):').split(','))
            if not self.kwargs['remark']:
                sample_list = set(raw_input('样本名称(逗号分隔):').split(','))
            else:
                sample_list = None
        else:
            self.logger.debug('found qcstat.xls: ' + qcstat.name)
            data_size = 0
            samples = {}
            for line in qcstat:
                line = line.decode()
                linelist = line.strip().split('\t')
                if linelist[0] in ('Sample name', 'Sample_name'):
                    continue
                samples[linelist[1]] = linelist[0]
                data_size += float(linelist[4])
            novoid_list = list(samples.keys())
            sample_list = list(samples.values())

        sample_count = self.kwargs['sample_count'] or len(novoid_list)
        data_size = self.kwargs.get('data_size') or data_size

        if self.kwargs.get('novoid_list'):
            if os.path.isfile(self.kwargs['novoid_list']):
                novoid_list = open(self.kwargs['novoid_list']).read().strip().split()
            else:
                novoid_list = self.kwargs['novoid_list'].split(',')
            self.logger.info('use input novoid list: {}'.format(novoid_list))

        return sample_count, data_size, novoid_list, sample_list

    def choose_sops(self):

        avail_sops = self.get_sops(self.project['PRODUCTCODE'])

        if self.kwargs['sop_method']:
            if all(sop in avail_sops for sop in self.kwargs['sop_method'].split(',')):
                return self.kwargs['sop_method']

        self.logger.info('请选择SOP方法:')
        print('#code\tvalue')
        print('\n'.join('{}\t{}'.format(sop[0], sop[1]) for idx, sop in enumerate(sorted(avail_sops.items()))))
        while True:
            try:
                sops = raw_input('>>> 请选择SOP编号，逗号分隔:')
                all_pass = True
                for choice in sops.split(','):
                    if choice not in avail_sops:
                        print('invalid input: {}'.format(choice))
                        all_pass = False
                        break
                if all_pass:
                    return sops
            except EOFError:
                exit()

    def get_sops(self, product_code):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.DS_TestRelMethod_H&Type=json&p1=&p2={product_code}'.format(
            **dict(self.kwargs, **locals()))
        self.logger.debug('get sop methods: ' + url)
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        sops = {sop['VALUE']: sop['TEXT'] for sop in rows}

        self.logger.debug('available sops: {}'.format(json.dumps(sops, indent=2, ensure_ascii=False)))

        return sops


    def get_reports(self, report_guid=None, report_name=None, add_time=None):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgReport&Type=json&p1={stage_code}&p2=Draft'.format(**self.kwargs)
        self.logger.debug('get reports: ' + url)
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        # print(json.dumps(rows, indent=2, ensure_ascii=False))

        if report_guid:
            for row in rows:
                if row['REPORT_GUID'] == report_guid:
                    return row
            return None
        elif (report_name and add_time):
            for row in rows:
                if row['REPORT_NAME'] == report_name and row['ADDTIME'] == add_time:
                    return row
            return None

        return rows

    def delete_report(self):

        if self.kwargs['delete'] == 'all':
            reports = [each for each in self.get_reports() if each['STATUS'] == 'Draft']
        else:
            reports = [self.get_reports(self.kwargs['delete'])]

        if not reports:
            self.logger.info('没有可删除的报告')
            exit(1)

        for report in reports:
            if not report:
                self.logger.error('ID为\033[3;35m{delete}\033[0m的报告不存在或已删除'.format(**self.kwargs))
            elif report['STATUS'] != 'Draft':
                self.logger.error('该报告为\033[1;31m{DISPSTATUS}\033[0m状态，无法删除！'.format(**report))
            else:
                url = '{base_url}/Sunway.DeleteRows.lims'.format(**self.kwargs)
                self.logger.debug('delete report: ' + url)
                payload = [
                    'kf_geneticanalysis_report',
                    [report['ORIGREC']]
                ]
                self.logger.debug(payload)
                resp = self.session.post(url, json=payload)
                if resp.text == 'true':
                    self.logger.info('已删除ID为\033[3;35m{REPORT_GUID}\033[0m的报告'.format(**report))

    def show_report_status(self, report_guid=None):

        rows = self.get_reports()
        if not rows:
            self.logger.info('该分期没有上传过报告')
        else:
            sop_methods = self.get_sops(self.project['PRODUCTCODE'])
            fields = 'REPORT_GUID STATUS DISPSTATUS STAGECODE REPORT_TYPE METHOD REPORT_NAME ANALYSTPERSON DOUBLECHECKERNAME OPERATIONSMANAGER REPORT_URL ADDTIME REMARK'.split()
            n = 0
            for row in rows:
                if report_guid and row['REPORT_GUID'] != report_guid:
                    continue
                n += 1
                print('\033[1;36m----- {n} {REPORT_NAME} -----\033[0m'.format(n=n, **row))
                for field in fields:
                    context = dict(self.project, **row)
                    info = context.get(field)
                    if field in ('DISPSTATUS', 'REPORT_URL'):
                        if info == '审核':
                            color = '1;5;31'
                        else:
                            color = '32'
                        info = '\033[{}m{}\033[0m'.format(color, info)
                    elif field in ('REPORT_TYPE', 'REMARK'):
                        info = '\033[33m{}\033[0m'.format(info)
                    elif field == 'METHOD' and context.get(field):
                        sop = context.get(field).split(',')
                        sop_new = list(map(lambda x: '{}[\033[33m{}\033[0m]'.format(x, sop_methods.get(x)), sop))
                        info = ','.join(sop_new)

                    print('{:25} {}'.format(field, info))


def parser_add_report(parser):

    parser.description = '\033[1;32m   报告上传，查询或删除  \033[0m'

    parser.epilog = textwrap.dedent('''\
        \033[36mexamples:
            %(prog)s -stage P101SC16122194-01-F001 -t qc(mapping) /path/to/report.zip                         [上传QC(Mapping)报告]
            %(prog)s -stage P101SC16122194-01-F001 -t final /path/to/final_report.zip                         [上传结题报告]
            %(prog)s -stage P101SC16122194-01-F001 -t final /path/to/final_report.zip -path /path/to/release  [上传结题报告同时释放数据]
            %(prog)s -stage P101SC16122194-01-F001 -t final /path/to/final_report.zip -count 4 -data 10       [手动指定]
            %(prog)s -stage P101SC16122194-01-F001 -t final /path/to/final_report.zip -xx                     [线下项目]

            %(prog)s -stage P101SC16122194-01-F001                                                       [查看指定分期的报告]
            %(prog)s -stage P101SC16122194-01-F001 -d 4FF9F182-BC50-4AED-A5E2-3CE47D276D98               [删除指定编号的报告]
            %(prog)s -stage P101SC16122194-01-F001 -d all                                                [删除指定分期所有可删除的报告]

        \033[32mPS:
            1 首次上传结题报告时需要指定SOP，样本数，数据量，结题样本诺禾编号列表，默认情况下这些数据会自动从qcstat.xls中读取，SOP会在执行过程中进行选择，也可手动传入参数
            2 无样本信息上传结题报告时(如线下项目)，指定-xx可跳过结题样本更新步骤
            3 只可删除'新建'或'审核退回'状态的报告\033[0m''')

    parser.add_argument('filename', help='the report file to upload', nargs='?')

    parser.add_argument('-stage', '--stage-code', help='the stage code')

    parser.add_argument(
        '-t',
        '--type',
        help='the type of report, choose from [%(choices)s]',
        choices=['qc', 'mapping', 'final'])

    parser.add_argument(
        '-sop', '--sop-method', help='the sop method for the product')

    parser.add_argument('-count', '--sample-count', help='the count of sample')
    parser.add_argument('-data', '--data-size', help='the total data size')
    parser.add_argument('-novoids', '--novoid-list', help='the novoid list of samples')

    parser.add_argument('-qc', '--qcstat', help='specify a qcstat.xls file')

    parser.add_argument('-msg', '--message', help='the message for this report')
    parser.add_argument('-d', '--delete', help='the report_id to delete, use "all" to delete all deletable reports')
    parser.add_argument('-xx', '--xian-xia', help='the xian xia project, do not check samples', action='store_true')

    parser.add_argument('-i', '--ignore', help='ignore the additional samples', action='store_true')


    release_parser = parser.add_argument_group('release arguments')
    release_parser.add_argument('-path', '--release-path', help='the path to release')
    release_parser.add_argument('-qclist', '--qclist', help='the qclist file for this release')
    release_parser.add_argument('-r', '--remark', help='the remark for this release')

    parser.set_defaults(func=main)


def main(**args):

    Report(**args).start()


# if __name__ == "__main__":

#     main()
