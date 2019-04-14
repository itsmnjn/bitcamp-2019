from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)
	
def scrape():
	result_list = []
	raw_html = simple_get('https://sentence.yourdictionary.com/'+sys.argv[1])
	html = BeautifulSoup(raw_html, 'html.parser')
	result_block = html.find_all('div', attrs={'class':'li_content'})
	for result in result_block:
		result_list.append(result.get_text())
	return(result_list)

def scrape2():
    final_list = []
    raw_html = simple_get("https://www.linguee.com/english-french/search?source=french&query="+sys.argv[1])
    html = BeautifulSoup(raw_html, "html.parser")
    result_block = html.find_all('div', attrs={'class':'wrap'})
    count = 0
    final_list = []
    for i in range(len(result_block)):
        if(i % 2 == 1):
            continue
        temp1 = result_block[i].get_text().replace("[...]", "", 10000).split()       
        temp1 = [i.strip() for i in temp1]
        temp1 = " ".join(temp1)
        new_str = ""
        for i in range(len(temp1)):
            if temp1[i] == '.' or temp1[i] == '?' or temp1[i] == '。' or temp1[i] == '？':
                new_str += temp1[i]
                break
            new_str += temp1[i]
        final_list.append(new_str)
    return final_list
        
if __name__=='__main__':
	# print(scrape())
    print(scrape2())