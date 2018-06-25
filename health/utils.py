# -*- coding: utf-8 -*-
import re, os, platform, functools
from pprint import pprint
from random import sample
from string import ascii_letters
from unicodedata import normalize
from collections import OrderedDict
from urllib.parse import parse_qs

import xlrd
from bs4.element import Tag, NavigableString
from listorm import Listorm, read_excel, read_csv


def gen_search_query(querystrings):
    ret = []
    for qs in querystrings:
        queryset = parse_qs(qs)
        for key, values in queryset.items():
            key = key.strip()
            for val in values:
                row = {}
                val = val.strip()
                if os.path.isfile(val):
                    with open(val) as fp:
                        for keyword in fp.readlines():
                            row = {}
                            row[key] = keyword.strip()
                            ret.append(row)
                else:
                    row[key] = val
                    ret.append(row)
    return ret


def get_edi_code_from_xl(xl_file):
    edis = []
    re_compile_edi = re.compile('[A-Z\d]\d{8}')
    wb = xlrd.open_workbook(xl_file)
    for sheet_index in range(wb.nsheets):
        sheet = wb.sheet_by_index(sheet_index)
        
        for r in range(sheet.nrows):
            for cell in sheet.row(r):
                for edi in re_compile_edi.findall(str(cell.value)):
                    edis.append(edi)
    return list(OrderedDict.fromkeys(edis))


def br_to_linebreak(td):
    contents = []
    for ch in td.children:
        if isinstance(ch, Tag):
            contents.append(br_to_linebreak(ch))
        elif isinstance(ch, NavigableString):
            ch = ch.strip()
            if re.search(r'\[.+\]', ch):
                continue
            if re.match(r'\(.+\)', ch):
                continue
            contents.append(ch)
    contents = map(lambda s: normalize('NFKC', s).strip(), contents)
    return '\n'.join(contents)


def isvalid_file(file):
    fn, ext = os.path.splitext(file)
    return ext in ['.xls', '.xlsx', '.html']

def starts_file(file=None):
    if platform.system() == 'Windows' and file:
        os.startfile(file)
        