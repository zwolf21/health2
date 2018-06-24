import re, json

from bs4 import BeautifulSoup


def parse(html, drug_cd):
	soup = BeautifulSoup(html, 'html.parser')
	soup_kpic = soup.find('ul', id='kpic_atc')
	kpic_categories = ['kpic_large', 'kpic_regular', 'kpic_small', 'kpice_detail']
	ret = []
	for li in soup_kpic('li'):
		cats = {'drug_code': drug_cd}
		for cat, a in zip(kpic_categories, li('a')):
			cats[cat] = a.text.strip()
		ret.append(cats)
	return ret
