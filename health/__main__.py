import argparse, os, platform, pprint

from views import get_drug_search_list, get_drug_list, get_drug_list_thread, drug_picture_view
from utils import gen_search_query, get_edi_code_from_xl
from settings import MAX_WORKERS, COLUMN_MAP, INDEX
from forms import DRUG_SEARCH_FORM, DRUG_SEARCH_MORE_FORM
import pandas as pd


def main():
	argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="약학정보원유틸")
	argparser.add_argument('-q', '--query', help='검색필드명=검색어 또는 개행으로 구분 된 검색어리스트파일 ex:)search_bohcode=626700072 input_drug_name=약품명.txt' , nargs='*')
	argparser.add_argument('-o', '--output', help='검색 결과 엑셀파일로 저장',  nargs='?')
	argparser.add_argument('-x', '--excel', help='엑셀 파일에서 EDI코드 찾아내어 검색하기', nargs='?')
	argparser.add_argument('-w', '--workers', help='동시다운로드개수', default=MAX_WORKERS, nargs='?', type=int)
	argparser.add_argument('-ls', '--fields', help='검색 폼 필드명보기', action='store_true', default=False)
	argparser.add_argument('-CC', '--columns', type=int, help='html로 저장시 테이블 열수', default=5, nargs='?')
	argparser.add_argument('-i', '--img', help='사진받기', nargs='?')
	
	args = argparser.parse_args()

	if args.fields:
		print('DRUG_SEARCH_FORM')
		pprint.pprint(DRUG_SEARCH_FORM)
		print('')
		pprint.pprint(DRUG_SEARCH_MORE_FORM)
		return

	if args.query:
		querys = gen_search_query(args.query)
	elif args.excel:
		querys = get_edi_code_from_xl(args.excel)

	if args.workers == 1:
		records = get_drug_list(*querys, ret_kpic=True)
	else:
		records = get_drug_list_thread(*querys, ret_kpic=True, max_workers=args.workers)
		
	if args.output:
		df = pd.DataFrame(records)
		df = df.rename(columns=COLUMN_MAP)
		df = df[list(COLUMN_MAP.values())]
		df.set_index(INDEX, inplace=True)
		df.to_excel(args.output, index=True)
	else:
		for row in records:
			print(row.get('drug_name'), row.get('price', '0원'), row.get('boh_hiracode', ''), row.get('bohgb', ''))


	if args.img:
		return drug_picture_view(records, columns=args.columns, output_html=args.img)




if __name__ == '__main__':
	main()