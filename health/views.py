import os, sys, re
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from listorm import Listorm
from tqdm import tqdm

try:
	from settings import REQUEST_HEADER, MAX_WORKERS, JINJA_ENV
	from forms import DRUG_SEARCH_FORM, DRUG_SEARCH_MORE_FORM
	from urls import SEARCH_DRUG, SEARCH_DRUG_MORE
	from parsers import parse_search_drug, parse_detail_api, parse_detail
	from retrieves import retrieve_search_drug
except:
	from .settings import REQUEST_HEADER, MAX_WORKERS, JINJA_ENV
	from .forms import DRUG_SEARCH_FORM, DRUG_SEARCH_MORE_FORM
	from .urls import SEARCH_DRUG, SEARCH_DRUG_MORE
	from .parsers import parse_search_drug, parse_detail_api, parse_detail
	from .retrieves import retrieve_search_drug



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

def get_drug_list(*criterias, **kwargs):
	drug_list = Listorm()
	for crit in tqdm(criterias, total=len(criterias)):
		drug_list += get_drug_search_list(**crit)
	drug_codes = drug_list.column_values('drug_cd')
	detail_list = Listorm()
	print('collecting {} items....'.format(len(drug_codes)))
	for drug_code in tqdm(drug_codes, total=len(drug_codes)):
		detail_list += get_drug_detail(drug_code, **kwargs)
	ret = detail_list.join(drug_list, left_on='drug_code', right_on='drug_cd')
	records = [dict(row) for row in ret]
	return records


def get_drug_list_thread(*criterias, max_workers=MAX_WORKERS, **kwargs):
	drug_code_sets = []
	workers = min(max_workers, len(criterias))
	with ThreadPoolExecutor(workers) as executor:
		todo_list = []
		print('Searching for {} keywords...'.format(len(criterias)))
		for crit in criterias:
			future = executor.submit(get_drug_search_list, **crit)
			todo_list.append(future)
		done_iter = tqdm(as_completed(todo_list), total=len(todo_list))
		for future in done_iter:
			drug_code_sets += future.result()

	drug_codes = [row.get('drug_cd', '') for row in drug_code_sets]

	records = []
	workers = min(max_workers, len(drug_codes))
	with ThreadPoolExecutor(workers) as executor:
		todo_list = []
		print('Retrieving {} items(workers: {})'.format(len(drug_codes), workers))
		for drug_code in drug_codes:
			future = executor.submit(get_drug_detail, drug_code, **kwargs)
			todo_list.append(future)
		done_iter = tqdm(as_completed(todo_list), total=len(todo_list))
		for future in done_iter:
			records += future.result()
	records = [dict(row) for row in records]
	return records


def drug_picture_view(records, columns=5, env=JINJA_ENV, output_html=None):
	records = Listorm(records)
	records = records.distinct('drug_code')
	template = env.get_template('drug_pictures.html')
	object_lists = []
	for i in range(0, len(records), columns):
		object_lists.append(records[i:i+columns])

	html = template.render(object_lists=object_lists)
	if output_html:
		with open(output_html, 'wt', encoding='utf-8') as fp:
			fp.write(html)
	else:
		return html