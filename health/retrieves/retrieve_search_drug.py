import requests

try:
	from ..urls import SEARCH_DRUG, SEARCH_DRUG_MORE, API_DETAIL_DRUG, DETAIL_DRUG
	from ..forms import DRUG_SEARCH_FORM, DRUG_SEARCH_MORE_FORM
	from ..settings import REQUEST_HEADER	
except:
	from urls import SEARCH_DRUG, SEARCH_DRUG_MORE, API_DETAIL_DRUG, DETAIL_DRUG
	from forms import DRUG_SEARCH_FORM, DRUG_SEARCH_MORE_FORM
	from settings import REQUEST_HEADER	



def get_search(**kwargs):
	form = DRUG_SEARCH_MORE_FORM.copy()
	form.update(kwargs)
	r = requests.post(SEARCH_DRUG, data=form, headers=REQUEST_HEADER)
	return r.content

def get_search_more(fixed_cnt, **kwargs):
	form = DRUG_SEARCH_MORE_FORM.copy()
	form['fixed_cnt'] = fixed_cnt
	form.update(kwargs)
	r = requests.post(SEARCH_DRUG_MORE, data=form, headers=REQUEST_HEADER)
	return r.content

def get_detail_api(drug_cd):
	params = {
		'drug_cd': drug_cd,
		'callback': 'jQuery16209083411218851807_1529809120441',
	}
	r = requests.get(API_DETAIL_DRUG, params=params, headers=REQUEST_HEADER)
	return r.content

def get_detail(drug_cd):
	params = {
		'drug_cd': drug_cd
	}
	r = requests.get(DETAIL_DRUG, params=params, headers=REQUEST_HEADER)
	return r.content
