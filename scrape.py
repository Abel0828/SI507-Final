from bs4 import BeautifulSoup
import requests
import json
import re
import os
import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from db_config import *
import sys


N_PAGE=1
CACHE= 'cache_websites.json'
if not os.path.exists('./cache_websites.json'):
    with open(CACHE,'w') as c:
        c.write('{}')
        
def get_soup(url):
    headers={'User-Agent':'Mozilla/5.0'}
    f=open(CACHE,'r',encoding='utf-8')
    text=f.read()
    f.close()
    cache_dict=json.loads(text)
    try:
        soup=BeautifulSoup(cache_dict[url],'html.parser')
    except:
        text=requests.get(url,headers=headers).text
        cache_dict[url]=text
        with open(CACHE,'w',encoding='utf-8') as nf:
            nf.write(json.dumps(cache_dict))
        soup=BeautifulSoup(text,'html.parser')
    return soup
    

def scrape():
    """
    start point of scraping
    use urls, pass soup tag to Unvs
    return a list of 100 unvs(university) object
    """
    url_base='https://www.usnews.com/best-colleges/rankings/national-universities'
    unvss=[]
    for page in range(N_PAGE):
        url=url_base+'?_page={}'.format(page+1)
        soup=get_soup(url)
        unvs_tags=soup.find_all('li',id=re.compile(r'^view-.*'),class_='block-normal block-loose-for-large-up')
        for unvs_tag in unvs_tags:
            u=Unvs(unvs_tag)
            print("Collect info of {}".format(u.name))
            unvss.append(u)
    return unvss

class Unvs(object):
    def __init__(self,unvs_tag):       
        self.name=None
        self.rank=None
        self.address=None
        self.thumbnail=None
        self.n_ug=None
        self.page_url=None
        
        self.type=None
        self.year_founded=None
        self.setting=None
        self.endowment=None

        self.scrape_overview(unvs_tag)
        assert(self.page_url!=None)
        self.scrape_detail(self.page_url)
        
        """
        print(self.name)
        print(self.rank)
        print(self.address)
        print(self.thumbnail)
        print(self.n_ug)
        print(self.page_url)
        print(self.type)
        print(self.year_founded)
        print(self.setting)
        print(self.endowment)
        """

    def __repr__(self):
        return '{} in {}, ranking #'.format(self.name,self.address,self.rank)
        
    def __contains__(self,string):
        return string in self.name
        
    def scrape_overview(self,unvs_tag):
        """
        get a soup tag, scrape the basic info from tag,
        return a url directing to detailed info
        call scrpae_detail for the info
        """
        base='https://www.usnews.com'
        name_tag=unvs_tag.find('h3',class_='heading-large block-tighter').a
        assert(name_tag!=None)
        self.name=name_tag.string.strip()
        self.page_url=base+name_tag.get('href')
        assert(self.page_url!=None)
        self.address=unvs_tag.find('div',class_='block-normal text-small').string.strip()
        rank_msg=unvs_tag.find('div',style='margin-left: 2.5rem;').find('div').stripped_strings.__next__()
        match=re.search(r'\d+',rank_msg)
        assert(match)
        self.rank=int(match.group())
        self.n_ug=int(unvs_tag.find('span',string=re.compile(r'\s*Undergraduate Enrollment\s*'))\
                      .parent.strong.string.strip().replace(',',''))
        self.thumbnail=base+unvs_tag.find('a',class_='display-block right').get('href')
        
    def scrape_detail(self,url):
        """
        use the url to scrape detailed info
        """
        soup=get_soup(url)
        info_tags=soup.find_all('span',class_='heading-small text-black text-tight block-flush display-block-for-large-up')
        self.type=info_tags[0].string.strip()
        self.year_founded=int(info_tags[1].string.strip())
        self.setting=info_tags[4].string.strip()
        self.endowment=info_tags[5].string.strip()

def DB_setup():
        print("Start with existing database: postgres...")
        try:
            con= psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(db_name, db_user, db_password))
        except:
            print('Cannot establish connection, please recheck username and password.')
            sys.exit()
        print("Connection established.")        
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur=con.cursor()
        print("Create new database: si507_final_ywangdr, which might take a little time...")
        cur.execute("CREATE DATABASE si507_final_ywangdr;")

        cur.close()
        con=psycopg2.connect("dbname=si507_final_ywangdr user='{}' password={}".format(db_user,db_password))
        return con
    
def create_tables(con,cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS university_basic(
    name VARCHAR UNIQUE,
    rank INTEGER,
    web_url VARCHAR,
    PRIMARY KEY (name));"""
    )
    con.commit()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS university_detail(
    name VARCHAR UNIQUE,
    address VARCHAR,
    year_founded INTEGER,
    photos_url VARCHAR,
    n_undergraduate INTEGER,
    school_type VARCHAR,
    setting VARCHAR,
    endowment_amount VARCHAR,
    FOREIGN KEY (name) REFERENCES university_basic (name),
    PRIMARY KEY (name));"""
    )
    con.commit()
    


def insert_data(con,cur,unvss):
    for unvs in unvss:
        basic_tup=(unvs.name,unvs.rank,unvs.page_url)
        cur.execute("""INSERT INTO university_basic (name,rank,web_url) VALUES (%s,%s,%s);""",basic_tup)
        con.commit()
        detail_tup=(unvs.name,unvs.address,unvs.year_founded,unvs.thumbnail,unvs.n_ug,unvs.type,unvs.setting,unvs.endowment)
        cur.execute("""INSERT INTO university_detail (name,address,year_founded,photos_url,n_undergraduate,school_type,setting,endowment_amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);""",detail_tup)
        con.commit()
    print("finish insertion.")
    
def database_store(unvss):        
    con=DB_setup()
    cur=con.cursor()
    create_tables(con,cur)
    insert_data(con,cur,unvss)
    
if __name__=='__main__':
    unvss=scrape()
    database_store(unvss)
