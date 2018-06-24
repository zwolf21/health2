import os, sys, re
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from listorm import Listorm

from settings import REQUEST_HEADER
from forms import DRUG_SEARCH_FORM, DRUG_SEARCH_MORE_FORM
from urls import SEARCH_DRUG, SEARCH_DRUG_MORE
from parsers import parse_search_drug, parse_detail_api, parse_detail
from retrieves import retrieve_search_drug


def get_drug_search_list(**kwargs):
	search_result_page = retrieve_search_drug.get_search(**kwargs)
	drug_countset = parse_search_drug.get_count(search_result_page)

	ret = Listorm()

	for pro, cnt in drug_countset.items():
		if pro == 'proy':
			attr_id = 'result_recorded'
			pro_yn = 'Y'
		else:
			attr_id = 'result_unrecorded'
			pro_yn = 'N'

		records = Listorm(parse_search_drug.parse(search_result_page, 'article', id=attr_id))
		retrieve_count = len(records)

		if cnt > retrieve_count:
			search_more_result_page = retrieve_search_drug.get_search_more(cnt, proYN=pro_yn, **kwargs)
			records = Listorm()
	
			for page in range(1, cnt//DRUG_SEARCH_MORE_FORM['rowLength']+2):
				search_more_result_page = retrieve_search_drug.get_search_more(cnt, proYN=pro_yn, pageNo=page, **kwargs)
				page_records = Listorm(parse_search_drug.parse(search_more_result_page, 'article', id='resultMoreTable'))
				records+=page_records
					
		records = records.add_columns(pro_yn=lambda row: pro_yn)
		ret += records

	return ret.distinct('drug_cd')


def get_drug_detail(drug_code, ret_kpic=False):
	api_content = retrieve_search_drug.get_detail_api(drug_code)
	records = Listorm(parse_detail_api.parse(api_content))
	if ret_kpic:
		html_content = retrieve_search_drug.get_detail(drug_code)
		kpic_records = Listorm(parse_detail.parse(html_content, drug_code))
		if kpic_records:
			ret = kpic_records.join(records, on='drug_code', how='left')
			return ret
	return records


def get_drug_list_by_edi(*edi_codes, **kwargs):
	drug_list = Listorm()
	for edi in edi_codes:
		drug_list += get_drug_search_list(search_bohcode=edi)
	drug_codes = drug_list.column_values('drug_cd')
	detail_list = Listorm()
	for drug_code in drug_codes:
		detail_list += get_drug_detail(drug_code, **kwargs)
	ret = detail_list.join(drug_list, left_on='drug_code', right_on='drug_cd')
	return ret
