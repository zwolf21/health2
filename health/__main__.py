import argparse, os, platform

from views import get_drug_search_list, get_drug_list
from utils import gen_search_query


def main():
	argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="약학정보원유틸")
	argparser.add_argument('-q', '--query', help='검색필드명=검색어 또는 개행으로 구분 된 검색어리스트파일 ex:)search_bohcode=626700072 input_drug_name=약품명.txt' , nargs='*')
	argparser.add_argument('-o', '--output', help='검색 결과 엑셀파일로 저장',  nargs='?')
    argparser.add_argument('-x', '--excel', help='엑셀 파일에서 EDI코드 찾아내어 검색하기', nargs='+')
	
	args = argparser.parse_args()

	if args.query:
		querys = gen_search_query(args.query)
		records = get_drug_list(*querys, ret_kpic=True)
		if args.output:
			records.to_excel(args.output)

if __name__ == '__main__':
	main()