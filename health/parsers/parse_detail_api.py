import re, json

from bs4 import BeautifulSoup


def _parse_sunb(value, delimiter='\n'):
	if not value:
		return value
	soup = BeautifulSoup(value, 'html.parser')
	rows = []
	for a in soup('a'):
		row = a.text
		contents = row.split('　')
		if contents and len(contents)>2:
			row = contents[0] + ' ' + contents[-1]
		row = re.sub(r'\s+', ' ', row).strip()
		rows.append(row)
	return delimiter.join(rows)

def _parse_upso(value):
	if not value:
		return value

	contents = value.split('|')
	if contents:
		return contents[0]
	return value

def _parse_bohistory_price(value):
	price = 0
	if not value:
		return price

	regx = re.compile(r'(?P<price>\d+)원')
	g = regx.search(value)
	if g:
		price = int(g.group('price'))
	return price

def _parse_bohistory_bohgb(value):
	bohgb = '비급여'

	if '비급여' in value:
		return bohgb
	elif '급여' in value:
		bohgb = '급여'
	else:
		bohgb = '삭제'
	return bohgb

def _parse_kpic_atc(value):
	if not value:
		return []

	contents = value.split('|')
	kpic_categories = ['kpic_large', 'kpic_regular', 'kpic_small', 'kpice_detail']
	ret = []
	for html in contents:
		soup = BeautifulSoup(html, 'html.parser')
		atags = soup('a')
		catset  = {}
		for a, kpic_nm in zip(atags, kpic_categories):
			catset[kpic_nm] = re.sub(r'\s+', ' ', a.text).strip()
		ret.append(catset)
	return ret


def _parse_drug_pic(value):
	if not value:
		return {}
	ret = {}
	for src in value.split('|'):
		if 'pack_img' in src:
			ret['pack_img'] = src
		elif 'sb_photo' in src:
			ret['sb_photo'] = src
	return ret



def parse(content, *args, **kwargs):
	regx = re.compile(b'jQuery[\w\_]+\((?P<content>.+)\)')
	g = regx.search(content)
	if g:
		data = g.group('content')
	else:
		data = b'{}'
	ret = json.loads(data)
	if isinstance(ret, list):
		ret = ret[0]

	ret['sunb'] = _parse_sunb(ret.get('sunb', ''))
	ret['upso1'] = _parse_upso(ret.get('upso1', ''))
	ret['upso_name'] = _parse_upso(ret.get('upso_name', ''))
	ret['price'] = _parse_bohistory_price(ret.get('boh_history', ''))
	ret['bohgb'] = _parse_bohistory_bohgb(ret.get('boh_history', ''))
	ret.update(_parse_drug_pic(ret.get('drug_pic')))
	del ret['drug_pic']
	del ret['picto_img']
	return [ret]

