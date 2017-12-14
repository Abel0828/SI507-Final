import unittest
from SI507F17_finalproject import *
from plot import *
from config import *
import os
import csv
import json


class testDependencies(unittest.TestCase):
    def setUp(self):
        #this setUp is omitted
        #for setUp and tearDown function, see next subclass's setUp
        pass
    def test_dependent_files(self):
        self.assertTrue(os.path.exists("./README.md"))
        self.assertTrue(os.path.exists("./config.py"))
        self.assertTrue(os.path.exists('./cache_websites.json'))
        
    def test_dependent_credentials(self):
        self.assertTrue(db_password!='')
        self.assertTrue(plotly_api_key!='')
        self.assertTrue(geo_api_key!='')

    def test_dependent_global_variables(self):
        self.assertTrue(CACHE, 'cache_websites.json')
        self.assertTrue(len(zips)==0)

class testMethodsAndResults(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(CACHE):
            with open(CACHE,'w') as c:
                c.write('{}')
        self.url='https://www.usnews.com/best-colleges/rankings/national-universities?_page=1'
        self.soup=get_soup(self.url)
        self.unvs_tags=self.soup.find_all('li',id=re.compile(r'^view-.*'),class_='block-normal block-loose-for-large-up')
        
    def test_get_soup(self):
        self.assertTrue(self.soup!=None)
        self.assertTrue(len(self.unvs_tags)>1)

    def test_get_coordinate(self):
        url='https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key={}'.format(geo_api_key)
        lat,lng=get_coordinate(url)
        self.assertTrue(lat>37 and lat<38)
        self.assertTrue(lng<-121 and lng>-123)

    def test_Unvs_scrape_overview(self):
        u=Unvs(self.unvs_tags[0])
        u.scrape_overview(self.unvs_tags[1])
        self.assertEqual(u.name,'Harvard University')
        self.assertEqual(u.n_ug,6710)
        
    def test_Unvs_scrape_detail(self):
        u=Unvs(self.unvs_tags[0])
        u.scrape_detail('https://www.usnews.com/best-colleges/harvard-university-2155')
        self.assertEqual(u.year_founded,1636)
        self.assertEqual(u.zip,'02138')

    def test_Unvs_get_location(self):
        u=Unvs(self.unvs_tags[0])
        u.get_location()
        self.assertTrue(u.lat<41 and u.lat>40)
        
    def test_Unvs_repr(self):
        u=Unvs(self.unvs_tags[0])
        self.assertEqual(u.__repr__(),'{} in {}, ranking #'.format('Princeton University','Princeton, NJ',1))
        
    def test_Unvs_contains(self):
        u=Unvs(self.unvs_tags[0])
        self.assertTrue('Princeton' in u)
        self.assertTrue('princeton' not in u)
        
    def test_output_csv(self):
        output_csv([Unvs(self.unvs_tags[0]),Unvs(self.unvs_tags[1])])
        self.assertTrue(os.path.exists(UNVSS))
        
    def test_scrape(self):
        unvss=scrape(1)
        self.assertEqual(len(unvss),10)
        self.assertEqual(type(unvss),list)

    def test_Unvs_init(self):
        u=Unvs(self.unvs_tags[0])
        self.assertEqual(u.name,"Princeton University")
        self.assertEqual(u.address,"Princeton, NJ")
        self.assertEqual(u.n_ug,5400)
        self.assertEqual(u.rank,1)

    def test_cache_system(self):
        f=open(CACHE,'r',encoding='utf-8')
        text=f.read()
        f.close()
        cache_dict=json.loads(text)
        self.assertTrue(self.url in cache_dict)
        
    def test_connect_database(self):
        success=False
        try:
            con= psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(db_name, db_user, db_password))
            success=True
        except:
            pass
        self.assertTrue(success)
        
    def tearDown(self):
        if os.path.exists('./cache_websites.json'):
            os.remove('./cache_websites.json')
        if os.path.exists(UNVSS):
            os.remove(UNVSS)
        
    
    

if __name__ == "__main__":
    unittest.main(verbosity=2)
