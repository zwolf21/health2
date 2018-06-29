import os
from collections import OrderedDict

from jinja2 import Environment, PackageLoader, select_autoescape

JINJA_ENV = Environment(
    loader=PackageLoader('views', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

BASE_DIR = os.path.dirname(__file__)

REQUEST_HEADER = {
	"Connection":"keep-alive",
	"Cache-Control":"max-age=0",
	"Origin":"http://www.health.kr",
	"Upgrade-Insecure-Requests":"1",
	"Content-Type":"application/x-www-form-urlencoded",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"Referer":"http://www.health.kr/searchDrug/search_detail.asp",
	"Accept-Encoding":"gzip, deflate",
	"Accept-Language":"ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
}

MAX_WORKERS = 20

COLUMN_MAP = OrderedDict([
	('kpic_large', '대분류'), ('kpic_regular', '중분류'), ('kpic_small', '소분류'), ('kpice_detail', '상세분류'),
	('drug_name', '약품명'), ('drug_enm', '약품영문명'), ('upso_name', '제약회사',), ('boh_hiracode', '보험코드'), ('bohgb', '급여구분'), ('price', '약가'),
	('cls_code', '식약처분류'), ('cls_code_num', '분류번호'), ('fdacode', 'FDA등급'), ('narcotic_kind_code', '마약류구분'),
	('sunb', '성분명'), ('drug_form', '제형'), ('charact', '성상'), ('dosage_route', '투여경로'), ('drug_box', '포장'),
	('effect', '효능효과'), ('medititle', '약품설명'), ('stmt', '보관방법'),
])
INDEX = ['대분류', '중분류', '소분류', '상세분류']

