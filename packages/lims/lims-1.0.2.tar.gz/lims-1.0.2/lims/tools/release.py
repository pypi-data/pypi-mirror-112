#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import re
import sys
import time
import json
import textwrap
import socket
import dateutil.parser

try:
    from commands import getstatusoutput
except ImportError:
    from subprocess import getstatusoutput

from lims.tools.login import login
from lims.tools import utils

raw_input = __builtins__.get('raw_input', input)


class Release(object):

    def __init__(self, **kwargs):

        self.kwargs = kwargs

        self.session = login(kwargs)
        self.logger = utils.get_logger(**kwargs)

        if 'njlogin' in socket.gethostname():
            self.exe_path = '/TJPROJ1/JF/lims/GN/lims_report_upload_gn'
        else:
            self.exe_path = '/NJPROJ1/JF/lims/GN/lims_report_upload_gn'

        self.exe_path += '/d53fc91a99ed343e09a1c0df8fa72354'

    def start(self):

        if self.kwargs['release_path'] and self.kwargs['stage_code']:
            self.kwargs['release_path'] = os.path.abspath(self.kwargs['release_path'])
            if not self.kwargs.get('no_check'):
                self.check_size()
            # self.release_data()
            self.release_data2()
            self.show_release()
        elif not self.kwargs['release_path']:
            self.show_release()
        else:
            self.logger.warn('stage_code is required!')

    def show_release(self):

        fields = '''
            INSTALLMENTCODE     分期编号
            INSTALLMENTDESC     分期名称
            RELEASEADDRESS      释放集群
            RELEASETYPE         释放方式
            DATASIZE            数据大小
            FTPURL              集群路径
            CRM_RELEASETYPE     释放内容
            OPERATOR            运营经理
            COMMENTS            释放备注
            CONCLUSTATUS        结题状态
            CONCLUDATE          结题时间
            JT_ST               结题标识
            RELEASESTATUS       释放状态
            RELEASEDATE         释放时间
            SF_ST               释放标识
        '''.strip().split('\n')

        fields = [line.strip().split() for line in fields]

        rows = list(self.get_releases_result())

        if not rows:
            self.logger.info('该分期没有释放记录')
            exit(0)

        for n, row in enumerate(rows, 1):

            url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgStagingSample_H&Type=json&p1={stage_code}'.format(**self.kwargs)
            data = self.session.get(url).json()['Tables'][0]['Rows']

            for each in data:
                del each['RELEASETYPE']
                if each['RELEASESTATUS']:
                    row.update(each)
                break

            linelist = [row.get(field) for field, name in fields]

            print('\033[36m----- {n}. {PROJECTNAME} -----\033[0m'.format(n=n, **row))
            for (field, name), line in zip(fields, linelist):
                if not line:
                    continue
                if name in ('结题时间', '释放时间'):
                    line = dateutil.parser.parse(line).strftime('%Y-%m-%d %H:%M:%S')
                if name in ('释放状态', '释放备注'):
                    line = '\033[1;3;32m{}\033[0m'.format(line)
                print('\033[1m{} \033[0m\t{}'.format(name, line))

    def check_size(self):

        self.logger.info('checking checkSize.xls ...')

        check_size_xls = '{release_path}/checkSize.xls'.format(**self.kwargs)

        if not os.path.exists(check_size_xls):
            self.logger.warn('checkSize.xls文件不存在!')
            choice = raw_input('是否现在生成?(y/n):')
            if choice.lower() in ('y'):
                cmd = 'dirCheckSize.pl {release_path}'.format(**self.kwargs)
                self.logger.info('run cmd: {}'.format(cmd))
                assert not os.system(cmd)
            else:
                self.logger.error('释放路径下必须包含checkSize.xls文件！')
                exit(1)
        elif not os.path.getsize(check_size_xls):
            self.logger.error('checkSize.xls文件为空，请检查！')
            exit(1)

        files_in_xls = []
        with utils.safe_open(check_size_xls) as f:
            for line in f:
                line = line.decode()
                size, path = line.strip().split()
                path = path.lstrip('./')
                filepath = os.path.join(self.kwargs['release_path'], path)
                files_in_xls.append(path.split('/')[0])
                try:
                    filesize = os.path.getsize(filepath)
                except Exception as e:
                    self.logger.error(e)
                    exit(1)

                if filesize == 0:
                    self.logger.error('{}文件为空，请检查！'.format(path))
                    exit(1)
                elif int(size) != filesize:
                    self.logger.error('{}文件大小与checkSize.xls中不一致，请检查！'.format(path))
                    exit(1)

        for file in os.listdir(self.kwargs['release_path']):
            if file != 'checkSize.xls' and file not in files_in_xls:
                self.logger.error('文件{}不在checkSize.xls中，请检查！'.format(file))
                exit(1)

        self.logger.info('checkSize检查通过')


    def data_management(self):
        qclist = self.kwargs.get('qclist')
        if not qclist:
            self.logger.error('qc_list file is required!')
            exit(1)

        analydir = self.kwargs.get('analydir') or os.path.dirname(os.path.abspath(qclist))

        xiaji = os.path.join(analydir, 'xj_path.txt')
        
        samples = set()

        with utils.safe_open(xiaji, 'w') as out, utils.safe_open(qclist) as f:
            for line in f:
                line = line.decode()
                if line.startswith('#'):
                    continue
                linelist = line.strip().split('\t')
                novoid = linelist[4]
                libid = linelist[3]
                sampleid = linelist[2]
                samples.add(sampleid)
                path = linelist[6]
                if 'NJ' in path:
                    cluster = 'nj'
                else:
                    cluster = 'tj'
                outline = '{novoid}\t{sampleid}\t{path}/{libid}\t原路径\t{cluster}\t存在'.format(**locals())
                out.write(outline + '\n')
        
        cmd = '''
            Data_management XJ -s {stage_code} -i {xiaji}
            Data_management ML -s {stage_code} -p {analydir} -t 过程目录 -j {cluster}
            Data_management ML -s {stage_code} -p {release_path} -t 交付目录 -j {cluster}
        '''.format(**dict(self.kwargs, **locals()))

        print('run cmds: {}'.format(cmd))
        os.system(cmd)

        return list(samples)

    def release_data2(self):
        if not self.kwargs.get('xianxia'):
            self.data_management()

        info = self._get_release_info()
        cmd = '''Lims_report_uploader D --path {JFPATH} --stage_code {STAGECODE} --samplecount {sample_count} --allsamplename "{sample_names}" -m "{remark}"'''
        cmd = cmd.format(**info)
        print('run cmd:', cmd)
        assert not os.system(cmd)

    def _get_release_info(self):

        cluster = self.get_cluster()
        release_size = self._get_release_size()

        if self.kwargs.get('release_way'):
            self.logger.warn('使用自定义释放方式: {release_way}'.format(**self.kwargs))
            release_way = self.kwargs['release_way']
        else:
            release_way = '拷盘' if release_size > 100 else '阿里云'

        samples = self.data_management()

        sample_count = len(samples)

        if sample_count <= 5:
            sample_names = ','.join(samples)
        else:
            sample_names = ','.join(list(samples)[:6]) + '等{}个样品'.format(sample_count)

        info = {
            'STAGECODE': self.kwargs['stage_code'],
            'JFPATH': os.path.abspath(self.kwargs['release_path']),
            'sample_count': sample_count,
            'sample_names': sample_names,
            'remark': self.kwargs.get('remark', ''),
        }

        return info

    def _get_release_size(self):

        if self.kwargs.get('release_size'):
            if os.path.isfile(self.kwargs.get('release_size')):
                self.logger.info('从文件中读取数据大小...')
                size = open(self.kwargs.get('release_size')).read().strip().split()[0]
            else:
                size = self.kwargs.get('release_size')
        else:
            self.logger.info('释放数据大小计算中...')
            cmd = 'du -sL -B1 {release_path}'.format(**self.kwargs)
            self.logger.debug(cmd)
            status, output = getstatusoutput(cmd)
            if status:
                self.logger.error('数据大小计算失败!\n\033[3;31m{}\033[0m'.format(output))
                exit(status)
            size = output.split()[0]
            self.logger.debug('数据大小计算完毕：\033[32m{}\033[0m bytes'.format(size))

        size = float(size) * 1e-9
        size = size if size <= 0.01 else round(size, 2)

        self.logger.info('数据大小：\033[32m{}\033[0m GB'.format(size))
        return size

    def get_cluster(self):

        cluster_map = {
            'TJ': '天津集群',
            'NJ': '南京集群',
            'USA': '美国集群'
        }

        cluster_name = self.kwargs.get('cluster_name')
        if not cluster_name:
            if ('NJ' in self.kwargs['release_path']) or socket.gethostname() == 'njlogin04.local':
                cluster_name = 'NJ'
            elif ('TJ' in self.kwargs['release_path']) or  socket.gethostname() == 'login04.local':
                cluster_name = 'TJ'
            else:
                choices = ['TJ', 'NJ', 'USA']
                while True:
                    cluster_name = raw_input('请选择集群地点({}): '.format(', '.join(choices)))
                    if cluster_name in choices:
                        break

        cluster = cluster_map[cluster_name]

        self.logger.info('集群地点：\033[32m{}\033[0m'.format(cluster))
        return cluster

    def get_releases_result(self):
        '''
            现在系统中有bug，没有分期编号，只有项目编号
            正式系统已修复
        '''
        # url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_AnalysisReport.kf_GetRelease&Type=json'.format(**self.kwargs)
        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_AnalysisReport.kf_GetRelease&Type=json&p1=Y'.format(**self.kwargs)
        self.logger.debug('GetRelease:' + url)
        rows = self.session.get(url).json()['Tables'][0]['Rows']
        for row in rows:
            if not self.kwargs['stage_code']:
                yield row
            elif self.kwargs['stage_code'] == row.get('INSTALLMENTCODE'):
                yield row
            elif row['PROJECTCODE'] in self.kwargs['stage_code']:
                # 根据该row的RID，检查STAGECODE是否一致
                url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_AnalysisReport.dgSubDataReleaseInfo&Type=json&p1={RID}'.format(
                    **dict(self.kwargs, **row))
                data = self.session.get(url).json()['Tables'][0]['Rows'][0]
                if data['INSTALLMENTCODE'] == self.kwargs['stage_code']:
                    row.update(data)
                    yield row

def parser_add_release(parser):

    parser.description = '\033[1;32m   数据释放或历史查看  \033[0m'

    parser.epilog = textwrap.dedent('''\
        \033[36mexamples:
            %(prog)s -stage P101SC16122194-01-F001 -path /path/to/release_dir -qc path/to/qcstat.xls  [本次释放的qc_list文件]

            %(prog)s -stage P101SC16122194-01-F001 -path /path/to/release_dir                         [通过du命令自动计算数据大小]
            %(prog)s -stage P101SC16122194-01-F001 -path /path/to/release_dir -size 713728            [给定数据路径大小(字节数)]
            %(prog)s -stage P101SC16122194-01-F001 -path /path/to/release_dir -size ./datasize.txt    [从计算好的文件中读取]

            %(prog)s -stage P101SC16122194-01-F001 -path /path/to/release_dir -r 释放备注              [填写备注]

            %(prog)s -stage P101SC16122194-01-F001                                                    [查看指定分期释放历史]

        \033[32mPS:
            计算路径大小的命令: du -sL -B1 /path/to/release_dir > datasize.txt  [数据较大时不建议在本地操作] \033[0m''')

    parser.add_argument('-stage', '--stage-code', help='the stage code')
    parser.add_argument('-path', '--release-path', help='the path to release')
    parser.add_argument('-qclist', '--qclist', help='the qc_list file for this release')

    parser.add_argument(
        '-size',
        '--release-size',
        help='the size(bytes) of release path, default will calculate automatically')

    parser.add_argument(
        '-cluster',
        '--cluster-name',
        help='the cluster to release, choose from (%(choices)s)',
        choices=['TJ', 'NJ'])

    parser.add_argument(
        '-way',
        '--release-way',
        help='the way of release data (%(choices)s)',
        choices=['阿里云', '拷盘'])

    parser.add_argument(
        '-e',
        '--email',
        help='the email address to receive release result')

    parser.add_argument(
        '-r',
        '--remark',
        help='the remark for release')

    parser.add_argument(
        '-analydir',
        '--analydir',
        help='the analysis directory')

    parser.add_argument(
        '-no',
        '--no-release',
        action='store_true',
        help='do not release, just generate release information')

    parser.add_argument(
        '-nc',
        '--no-check',
        action='store_true',
        help='do not check CheckSize.xls')

    parser.set_defaults(func=main)


def main(**args):

    Release(**args).start()


# if __name__ == "__main__":

#     main()
