import os

BASE_DIR = os.path.dirname(__file__)

REQUEST_HEADER = {
	"Connection: keep-alive" ,
	"Cache-Control: max-age=0" ,
	"Origin: http://www.health.kr" ,
	"Upgrade-Insecure-Requests: 1" ,
	"Content-Type: application/x-www-form-urlencoded" ,
	"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36" ,
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8" ,
	"Referer: http://www.health.kr/searchDrug/search_detail.asp" ,
	"Accept-Encoding: gzip, deflate" ,
	"Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7" ,	
}

MAX_WORKERS = 20

