import re

from bs4 import BeautifulSoup

def _extract(soup, recorded=True):
	regex = re.compile(r"javascript:drug_detailHref\(\'(?P<drug_cd>.+)\'\)")
	records = []
	soup = soup or BeautifulSoup('', 'html.parser')
	visited = set()
	for td in soup('td', onclick=regex):
		g = regex.search(td['onclick'])
		drug_cd = g.group('drug_cd')
		if drug_cd in visited:
			continue
		visited.add(drug_cd)
		record = {
			'drug_cd': drug_cd,
			'drug_nm': td.text.strip(),
		}
		records.append(record)
	return records

def get_count(html):
	soup = BeautifulSoup(html, 'html.parser')
	tags = ['proy_cnt', 'pron_cnt']
	ret = {}
	for tag in tags:
		cnt_soup = soup.find('span', id=tag)
		cnt = 0
		if cnt_soup:
			cnt = int(cnt_soup.text.replace('개', '').strip())
		ret[tag[:4]] = cnt
	return ret


def parse_default(html, **kwargs):
	soup = BeautifulSoup(html, 'html.parser')

def parse(html, *args, **kwargs):
	soup = BeautifulSoup(html, 'html.parser')
	target = soup.find(*args, **kwargs)
	return _extract(target)