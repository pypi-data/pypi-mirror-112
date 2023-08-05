#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import urllib
import getpass
import textwrap

from lims.tools.login import login
from lims.tools.utils import get_logger

import bs4


class Project(object):

    def __init__(self, **kwargs):

        self.kwargs = kwargs
        self.session = login(kwargs)
        self.logger = get_logger(**kwargs)

        self.kwargs['analyst_person_code'] = getpass.getuser()

    def start(self, fields=None):

        if self.kwargs.get('change_status'):
            if not self.kwargs['stage_code']:
                print('请提供要修改状态的分期编号')
            else:
                self.change_display_status()
            exit(0)

        rows = self.get_project_list(**self.kwargs)
        # rows = self.get_project_list()

        if self.kwargs['show_sops']:
            product_code = rows[0]['PRODUCTCODE'] if self.kwargs['stage_code'] and rows else None
            product_code = self.kwargs.get('product_code') or product_code
            if not product_code:
                self.logger.warn('请指定要查询的分期编号或产品编号')
            else:
                self.show_sop_methods(product_code)
            exit()

        if rows:

            self.logger.info('There are {} projects'.format(len(rows)))
            fields = fields or 'STAGECODE STAGES SUBPROJECTCODE CONTRACTNO DISPSTATUS ANALYSTPERSON DOUBLECHECKERNAME OPERATIONSMANAGER PROJECTNAME PRODUCTCODE REMARK'.split()
            if self.kwargs.get('show_information'):
                fields.append('INFORMATIONCONTENT')
            # print('\t'.join(fields))

            for n, row in enumerate(rows, 1):
                # for k,v in row.items():
                #     print(k, v)
                if self.kwargs.get('show_information'):
                    info = row['INFORMATIONCONTENT']
                    if info and info.startswith('<'):
                        try:
                            soup = bs4.BeautifulSoup(info)
                            trs = soup.select('tbody tr')
                            info_new = []
                            for tr in trs:
                                tds = [each.text.strip() for each in tr.select('td')]
                                info_new.append('\t'.join(tds))
                            info = '\n' + '\n'.join(info_new)
                        except:
                            pass
                    row['INFORMATIONCONTENT'] = '\033[32m{}\033[0m'.format(info)

                print('\033[36m----- {n}. {STAGECODE} {PROJECTNAME} -----\033[0m'.format(n=n, **row))
                linelist = [row[field] for field in fields]
                for field, value in zip(fields, linelist):
                    print('{:20}\t{}'.format(field, value))
                    yield {field: value}
        else:
            print('没有项目信息')

    def get_project_list(self, **kwargs):

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.dgStagingTask_H&Type=json&p1=Draft'.format(**self.kwargs)

        self.logger.debug('GET {}'.format(url))
        rows = self.session.get(url).json()['Tables'][0]['Rows']

        if not kwargs:
            return rows

        # keys_map = {'stage_code': 'STAGES'}

        for key in ('stage_code', 'sub_project_code', 'sub_project_name', 'analyst_person_code'):
            if not kwargs.get(key):
                continue

            # KEY = keys_map[key]
            KEY = key.replace('_', '').upper()
            # print(key, KEY)
            new_rows = []
            for row in rows:

                if kwargs.get('search_status') and kwargs.get('search_status') != row['DISPSTATUS']:
                    continue

                if row.get(KEY) == kwargs.get(key):
                    new_rows.append(row)
                elif (key == 'sub_project_name') and kwargs.get(key) in row.get(KEY):
                    self.logger.debug('fuzzy matching sub project name: {}'.format(row.get(KEY)))
                    new_rows.append(row)

            return new_rows

    def change_display_status(self):

        row = self.get_project_list(stage_code=self.kwargs['stage_code'])

        if not row:
            print('no such project with stage code {stage_code}'.format(**self.kwargs))
            exit(1)


        old_status = row[0]['DISPSTATUS']
        new_status = self.kwargs['change_status']

        if new_status == old_status:
            print('the current status is already "{new_status}"'.format(**locals()))
            exit(0)

        # keys = '''
        #     ORIGREC STAGECODE STAGES PROJECTCODE PROJECTNAME SUBPROJECTCODE SUBPROJECTNAME CONTRACTNO
        #     CONTRACTNAME SALEMANCODE SALEMAN ANALYSTPERSONCODE ANALYSTPERSON OPERATIONSMANAGERCODE STATUS
        #     DISPSTATUS RETURNCRM PRODUCTCODE OPERATIONSMANAGER DOUBLECHECKER DOUBLECHECKERNAME FTP_URL
        #     INFORMATIONCONTENT FILENAME REMARK COMMENTS SELECTED
        # '''.split()

        # *** bugs here: all fields can be modified
        fields = [
            ['DISPSTATUS', new_status, 'S', old_status],
        ]

        payload = [
            'dgStagingTask1', 'KF_GENETICANALYSIS', fields, row[0]['ORIGREC'],
            None
        ]

        url = '{base_url}/WS_UPDATEPROVIDER.lims'.format(**self.kwargs)
        print('[change_display_status POST]', url)
        resp = self.session.post(url, json=payload).json()

        if resp:
            print('display status changed: {old_status} ==> {new_status}'.format(**locals()))
        else:
            print('change display status failed:', resp)

    def show_sop_methods(self, product_code):
        self.logger.info('获取产品编号\033[3;36m{}\033[0m可选的SOP方法'.format(product_code))

        url = '{base_url}/RUNTIME_SUPPORT.GetData.lims?Provider=KF_DataAnalysis.DS_TestRelMethod_H&Type=json&p1=&p2={product_code}'.format(
            **dict(self.kwargs, **locals()))
        rows = self.session.get(url).json()['Tables'][0]['Rows']
        if not rows:
            self.logger.warn('指定的产品编号不存在，请检查！')
            exit(1)

        for row in rows:
            print('{VALUE:15} {TEXT}'.format(**row))


def parser_add_project(parser):

    parser.description = '\033[1;32m   项目查看，搜索或状态更改  \033[0m'

    parser.add_argument(
        '-stage',
        '--stage-code',
        help='search the stage code')

    parser.add_argument(
        '-project',
        '--sub-project-code',
        help='search the sub project code')

    parser.add_argument(
        '-name',
        '--sub-project-name',
        help='search the sub project name')

    parser.add_argument(
        '-status',
        '--search-status',
        help='only search the given status from (%(choices)s)',
        choices=['新建', '进行中', '完成'])

    parser.add_argument(
        '-info',
        '--show-information',
        help='show the information content',
        action='store_true')

    parser.add_argument(
        '-change',
        '--change-status',
        help='change the display status for a stage code, choose from (%(choices)s)',
        choices=['新建', '进行中', '完成'])

    parser.add_argument(
        '-sop',
        '--show-sops',
        help='show the available sop methods for given stage_code',
        action='store_true')

    parser.add_argument(
        '-product',
        '--product-code',
        help='show the available sop methods for given product_code')

    parser.set_defaults(func=main)


def main(**args):

    for each in Project(**args).start():
        pass


# if __name__ == "__main__":

#     main()
