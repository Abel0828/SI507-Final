import plotly
import plotly.plotly as py
from plotly.graph_objs import *
import csv
import pandas as pd
from config import *
UNVSS='universities.csv'

def output_csv(unvss):
    with open(UNVSS,'w',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=['name','lat','lng','rank','address','thumbnail',
                                            'n_ug','page_url','zip','type','year_founded',
                                            'setting','endowment'],
                              extrasaction='ignore',delimiter=',',quotechar='"')
        writer.writeheader()
        for unvs in unvss:
            line={}
            line['name']=unvs.name
            line['lat']=unvs.lat
            line['lng']=unvs.lng
            line['rank']=unvs.rank
            line['address']=unvs.address
            line['thumbnail']=unvs.thumbnail
            line['n_ug']=unvs.n_ug
            line['page_url']=unvs.page_url
            
            line['zip']=unvs.zip
            line['type']=unvs.type
            line['year_founded']=unvs.year_founded
            line['setting']=unvs.setting
            line['endowment']=unvs.endowment
            
            writer.writerow(line)

def visualize(unvss):
    output_csv(unvss)
    plotly.tools.set_credentials_file(username='ywangdr', api_key=plotly_api_key)
    df = pd.read_csv(UNVSS)
    df['text'] = df['name'] + '<br>' +\
                 'national rank: '+df['rank'].astype(str)+'<br>'+\
                 'founded time: '+df['year_founded'].astype(str)+'<br>'+\
                 'university type: ' + df['type']+'<br>'+\
                 'setting: ' + df['setting']+'<br>'+\
                 '2017 endowment: '+df['endowment']

    data = Data([
        Scattermapbox(
            lat=df['lat'],
            lon=df['lng'],
            mode='markers',
            marker=Marker(
                size=9
            ),
            text=df['text'],
        )
    ])
    layout = Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=40,
                lon=-94
            ),
            pitch=0,
            zoom=3,
            style='streets'
        ),
        
        title='2018 US Universities Ranking top-100<br>Source:\
<a href="https://www.usnews.com/best-colleges/rankings/national-universities">\
   US News Ranking</a>',
    )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='final project')
