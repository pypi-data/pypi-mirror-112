#!/usr/bin/env python
# -*- coding=utf-8 -*-
import re
import sys
import json
import getpass
import textwrap

from lims.tools.login import login
from lims.tools import utils
from lims.tools.project import Project
from lims.tools.report import Report


raw_input = __builtins__.get('raw_input', input)


class Check(object):

    def __init__(self, **kwargs):

        self.kwargs = kwargs

        self.session = login(kwargs)

        self.logger = utils.get_logger(**kwargs)

    def start(self):

        tasks = self.get_approve_task()
        if not self.kwargs['stage_code']:
            if tasks:
                fields = 'REPORT_GUID STAGECODE REPORT_TYPE FULLNAME ADDTIME REPORT_URL SAMPLECOUNT SUMDATA COMMENTS'.split()
                for n, row in enumerate(tasks, 1):
                    # print(row)
                    reports = self.get_approve_report(stage_code=row['STAGECODE'])
                    print('\033[36m----- {n}. {STAGECODE} {PROJECTNAME} -----\033[0m'.format(n=n, **row))
                    print('\t'.join(fields))
                    for report in reports:
                        line = '\t'.join(list(map(lambda x: '{%s}' % x, fields))).format(**report)
                        print(line)

                        if self.kwargs['report_guid'] == 'all':
                            self.operate_report(report)
            else:
                self.logger.info('没有check任务')
            exit(0)

        reports = self.get_approve_report(**self.kwargs)

        if not reports:
            self.logger.info('没有要check的报告')
            exit(0)

        # 获取指定分期的PRODUCTCODE
        for task in tasks:
            if self.kwargs['stage_code'] == task['STAGECODE']:
                productcode = task['PRODUCTCODE']
                break

        # # 获取指定PRODUCTCODE的SOPS
        sop_methods = Report(**self.kwargs).get_sops(productcode)

        if not self.kwargs['report_guid']:
            print('There are {} reports to check:'.format(len(reports)))
            fields = 'REPORT_GUID STAGECODE REPORT_TYPE FULLNAME ADDTIME REPORT_URL SAMPLECOUNT SUMDATA METHOD COMMENTS'.split()
            for n, report in enumerate(reports, 1):
                print('\033[1;36m----- {n} {REPORT_NAME} {ADDTIME} -----\033[0m'.format(n=n, **report))
                print('{:13} {}'.format('PRODUCTCODE', productcode))
                for field in fields:
                    info = report.get(field)
                    if not info:
                        # print(field)
                        continue
                    if field == 'REPORT_GUID':
                        info = '\033[35m{}\033[0m'.format(info)
                    elif field == 'METHOD' and report.get(field):
                        sop = report.get(field).split(',')
                        sop_new = list(map(lambda x: '{}[\033[33m{}\033[0m]'.format(x, sop_methods.get(x)), sop))
                        info = ','.join(sop_new)
                    print('{:13} {}'.format(field, info))

                if report.get('REPORT_TYPE') == '结题报告':
                    self.check_sample_status(report)
        else:
            self.operate_report(reports)

    def check_sample_status(self, report):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgStagingSample_H&Type=json&p1={stage_code}'.format(**self.kwargs)
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        if not rows:
            return

        jieti_samples = set()
        for row in rows:
            if not row:
                print('sfdsdfsdfsdfsdf')
                break
            if row.get('CONCLUSTATUS') and '结题' in row.get('CONCLUSTATUS'):
                jieti_samples.add(row.get('SAMPLEID'))

        if len(jieti_samples) != int(report.get('SAMPLECOUNT')):
            self.logger.warn('报告中样本数为{}, 系统中结题样本数为{}, 请注意！'.format(
                report.get('SAMPLECOUNT'),
                len(jieti_samples)))
        else:
            print('{:13} {}'.format('JT_SAMPLES', len(jieti_samples)))
            for field in 'FTPURL SF_ST RELEASESTATUS'.split():
                info = rows[0].get(field)
                if info:
                    print('{:13} {}'.format(field, info))

    def get_approve_task(self):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgStagingTask_H&Type=json&p1=Approve'.format(
            **self.kwargs)
        self.logger.debug('GET ' + url)

        rows = self.session.get(url).json()['Tables'][0]['Rows']

        return rows

    def get_approve_report(self, **kwargs):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgReport&Type=json&p1={stage_code}&p2=Approve'.format(
            **dict(self.kwargs, **kwargs))
        self.logger.debug('GET {}'.format(url))
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        if kwargs.get('report_guid'):
            for row in rows:
                if row['REPORT_GUID'] == kwargs.get('report_guid'):
                    return row
            return None

        return rows

    def operate_report(self, report):

        self.logger.info('dealing with report: {REPORT_GUID} {REPORT_NAME}'.format(**report))

        # 再次检查报告是否传错(一般是手动上传的报告)
        # if not report['REPORT_NAME'].startswith(report['STAGECODE']):
        if report['STAGECODE'] not in report['REPORT_NAME']:
            self.logger.error('上传的报告名称和分期编号不一致，请检查！')
            if self.kwargs['operation'] == 'submit':
                self.logger.error('不可以通过，请退回！')
                exit(1)
        elif not re.findall(r'(?:QC|Mapping|Report)-(?:.+?)-B\d+-5_\d+\.zip', report['REPORT_NAME']):
            self.logger.error('报告命名有误！命名规则如下：')
            print('QC|Mapping|Report-分期编号-Bn-5.zip')
            if self.kwargs['operation'] == 'submit':
                self.logger.error('不可以通过，请退回！')
                exit(1)

        payload = [report['REPORT_GUID'], 'Approve', self.kwargs['operation'].title()]
        if self.kwargs['operation'] == 'reject':
            # print(self.kwargs['password'])
            # exit()
            while True:
                reason = raw_input('请填写退回原因: ')
                if reason.strip():
                    break
            payload.append(str(reason))

            # =================================
            #   浏览器退回时需要输入密码进行认证
            #   这里取消了该步骤
            # =================================
            # while True:
            #     # password = getpass.getpass('> please input your password:')
            #     password = self.kwargs['password']

            #     url = '{base_url}/AuditTrail.Authenticate.lims'.format(**self.kwargs)
            #     self.logger.debug('authenticate {}'.format(url))
            #     context = [self.kwargs['username'].upper(), password]
            #     resp = self.session.post(url, json=context).json()

            #     if resp:
            #         break
            #     else:
            #         print('密码错误!')

        url = '{base_url}/KF_DataAnalysis.SubmitStaging_H2.lims'.format(**self.kwargs)
        self.logger.debug('POST {}'.format(url))
        self.logger.debug(str(payload))
        resp = self.session.post(url, json=payload, timeout=60).json()

        self.logger.debug(resp)

        if not resp[0]:
            self.logger.error(resp)
            self.logger.error('\033[31mfail to {operation} the report! try again or concat author: {author}\033[0m'.format(**self.kwargs))
        else:
            self.logger.info('\033[36m{operation} the report successfully\033[0m'.format(**self.kwargs))


def parser_add_check(parser):

    parser.description = '\033[1;32m   DoubleCheck通过或退回  \033[0m'

    parser.epilog = textwrap.dedent('''\
        \033[36mexamples:
            %(prog)s                                                         [查看所有check任务]
            %(prog)s -stage P101SC16122194-01-F003                           [查看指定分期的check任务]
            %(prog)s -st P101SC16122194-01-F003 -re REPORT_GUID -op submit   [通过指定GUID的报告]
            %(prog)s -st P101SC16122194-01-F003 -re REPORT_GUID -op reject   [退回指定GUID的报告]
        \033[0m''')

    parser.add_argument(
        '-stage', '--stage-code', help='the stage code')

    parser.add_argument('-report', '--report-guid', help='the report guid')

    parser.add_argument(
        '-operation',
        help='the operation to do, choose from (%(choices)s) [default=%(default)s]',
        choices=['submit', 'reject'],
        default='submit')

    parser.set_defaults(func=main)


def main(**args):

    Check(**args).start()


# if __name__ == "__main__":

#     main()
