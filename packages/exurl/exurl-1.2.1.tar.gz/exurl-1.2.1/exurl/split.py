
from urllib.parse import urlparse
from exurl import Filter

# Take url , return query
def parseUrl(url):
	return urlparse(url)


# Take query , return PV list , PV => parameter:value
def splitQueryToPV(queryInput):
	return queryInput.query.split('&')

# Take PV list return [param=] all in list 
def pEqual(paramValue):
	pEqual_list = []
	for pv in paramValue:
		pEqual = pv.split('=')
		pEqual_list.append(str(pEqual[0]+'='))	
	return pEqual_list


# Final => Take url replace and return many of urls
def split_url(url, replaceMe):
	final_list = []
	global pEqual
	if Filter.urlHaveParam(url):		
		query 	   = parseUrl(url) 			# return query from url
		pv 	  	   = splitQueryToPV(query)	# return param:value list from query
		_pEqual    = pEqual(pv) 				# return param= list from param:value
		
		for pv, paramEqual in zip(pv, _pEqual):
			split_url = url.replace(pv, paramEqual+replaceMe)
			final_list.append(split_url)
		
		return final_list
	else:
		return ""

def split_urls(urls, replaceMe):
	final_list = []
	for primaryUrl in urls:
		split_urls_1 = split_url(str(primaryUrl), replaceMe)
		
		for url_2 in split_urls_1:
			final_list.append(url_2)
		
	return final_list
