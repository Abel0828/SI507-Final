from bs4 import BeautifulSoup
import requests
import re
import sys
class haha(object):
    def __init__(self):
        self.a=1
        self.b=9
        self.hb()
    
    def hb(self):
        self.b=10
url_base='https://www.usnews.com/best-colleges/rankings/national-universities'
unvss=[]
for page in range(1):
    url=url_base+'?_page={}'.format(page+1)
    print(url)
    headers={'User-Agent':'Mozilla/5.0'}
    soup=BeautifulSoup(requests.get(url,headers=headers).text,'html.parser')
    print(soup.head)
    unvs_tags=soup.find_all('li',id=re.compile(r'^view-.*'),class_='block-normal block-loose-for-large-up')
    print(len(unvs_tags))
    for unvs_tag in unvs_tags[:1]:
        print(unvs_tag.text)
sys.exit(1)
