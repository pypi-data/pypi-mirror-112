#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import json
import textwrap
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from lims.tools.login import login
from lims.tools import utils


class Sample(object):

    def __init__(self, **kwargs):

        self.kwargs = kwargs

        self.session = login(kwargs)

        self.logger = utils.get_logger(**kwargs)

    def start(self):

        if not self.kwargs.get('stage_code'):
            self.logger.warn('请指定分期编号！')
            exit(1)

        if self.kwargs['get_info']:
            self.get_info_file()

        if self.kwargs['get_list']:
            self.get_list_file()

        if not any([self.kwargs['get_info'], self.kwargs['get_list']]):
            rows = self.get_stage_info(self.kwargs['stage_code'])
            if not rows:
                self.logger.warn('指定的分期编号不存在，请检查！')
                exit(1)
            for row in rows:
                # print(row)
                print('{STAGECODE:25}\t{PROJECTNAME}'.format(**row))


    def get_info_file(self):

        stage_info = self.get_stage_info(self.kwargs['stage_code'])[0]

        if not stage_info.get('FTP_URL'):
            self.logger.error('信息搜集表不存在，请联系运营经理！')
            exit(1)

        ftp_url = stage_info['FTP_URL']
        self.logger.debug(ftp_url)

        url = '{base_url}/STARLIMS11.novogenetest/KF_DataAnalysis.GetFileFromFtp.lims'.format(**self.kwargs)
        self.logger.debug('GetFileFromFtp: ' + url)
        payload = [ftp_url]
        resp = self.session.post(url, json=payload).json()

        if not resp:
            self.logger.error('information file not uploaded, please concact operation manager {OPERATIONSMANAGER}!'.format(**stage_info))
            exit(1)

        file_path = quote(resp[0])

        url = '{base_url}/RUNTIME_SUPPORT.GetFile.lims?Provider=QuickIntro.EchoFileName&isHtml=true&LocalFileName=&p1={file_path}'.format(**dict(self.kwargs, **locals()))
        self.logger.debug('download info file:' + url)

        resp = self.session.get(url)

        ext = '.' + url.rsplit('.', 1)[-1]

        if self.kwargs.get('outfile'):
            outfile = self.kwargs['outfile'] + ext
        else:
            outfile = '{stage_code}.sample_info'.format(**self.kwargs) + ext

        with open(outfile, 'wb') as out:
            for chunk in resp.iter_content():
                out.write(chunk)

        self.logger.info('save info file: \033[32m{}\033[0m'.format(outfile))

    def get_stage_info(self, stage_code=None):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgStagingTask_H&Type=json&p1=Draft'.format(**self.kwargs)
        self.logger.debug('get stage info: ' + url)
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        if not stage_code:
            return rows

        for row in rows:
            if row['STAGECODE'] == stage_code:
                return [row]

        return None

    def get_list_file(self):

        rows = self.get_path_info()
        if not rows:
            self.logger.warn('该分期没有样本信息！')
            exit(1)

        self.logger.debug(json.dumps(rows[0], ensure_ascii=False, indent=2))

        if self.kwargs.get('outfile'):
            outfile = self.kwargs['outfile'] + '.xls'
        else:
            outfile = '{stage_code}.sample_list.xls'.format(**self.kwargs)

        with open(outfile, 'w') as out:
            fields = 'SORTER SAMPLENAME SAMPLENAME LIBSAMPLEID SAMPLEID QCINDEX PATH'.split()
            # print('\t'.join(fields))
            title = '#Ori_Lane	PatientID	SampleID	LibID	NovoID	Index	Path'.split()
            out.write('\t'.join(title) + '\n') 

            for row in rows:
                if not row.get('PATH'):
                    continue
                row['QCINDEX'] = row['QCINDEX'].replace(';', '-')
                line = '\t'.join(list(map(lambda x: '{%s}' % x, fields))).format(**row)
                # print(line)
                out.write(line + '\n')

        self.logger.info('save list file: \033[33m{}\033[0m'.format(outfile))

    def get_path_info(self):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgStagingSample_H&Type=json&p1={stage_code}'.format(**self.kwargs)
        self.logger.debug('get path info' + url)
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        return rows


def parser_add_sample(parser):

    parser.description = '\033[1;32m   样本信息获取(信息搜集表，下机路径)  \033[0m'

    parser.add_argument(
        '-stage', '--stage-code', help='the stage code')

    parser.add_argument(
        '-o',
        '--outfile',
        help='the prefix of output file')

    parser.add_argument(
        '-info',
        '--get-info',
        help='get the sample info file',
        action='store_true')

    parser.add_argument(
        '-list',
        '--get-list',
        help='get the sample list file',
        action='store_true')

    parser.set_defaults(func=main)


def main(**args):

    Sample(**args).start()


# if __name__ == "__main__":

#     main()
