import pprint
import operator
import json
import random
from branca.colormap import linear
from matplotlib.ticker import FuncFormatter
import sys
import pandas as pd
import folium
import pandas as pd
import ast
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from folium import IFrame
import os
import base64
import csv
import os
from werkzeug import secure_filename
from flask import Flask, request, jsonify, render_template, send_file, make_response  #import main Flask class and request object
import json
app = Flask(__name__) #create the Flask app
pp = pprint.PrettyPrinter(indent=4)

choropleth_map = folium.Map(location=[19.080800, 72.986576],
                    zoom_start=11,
                    tiles="openstreetmap")
folium_map = folium.Map(location=[19.076037, 72.877211],
                    zoom_start=13,
                    tiles="openstreetmap")
folium.TileLayer('CartoDB dark_matter').add_to(folium_map)
folium.TileLayer('stamenterrain').add_to(folium_map)
folium.TileLayer('stamentoner').add_to(folium_map)
folium.TileLayer('stamenwatercolor').add_to(folium_map)
folium.TileLayer('cartodbpositron').add_to(folium_map)
folium.LayerControl().add_to(folium_map)

geo_json_data = json.load(open('templates/BMC_Wards.geojson'))
geo_lis = [x['properties']['name'] for x in geo_json_data['features']]
ward_dict = {}
for each in geo_lis:
    ward_dict[each] = random.random()

ward_df = pd.DataFrame(list(ward_dict.items()))
ward_df.columns = ['ward', 'Water Reuse score']
ward_df.to_csv("templates/ward.csv", index = False)

colormap = linear.RdYlGn_11.scale(
min(ward_dict.values()),
max(ward_dict.values()))

colormap.caption = 'Reuse of waste water per BMC Wards'
colormap.add_to(choropleth_map)

@app.route('/map')
def map():
    global folium_map
    df = pd.read_csv('templates/data.csv')
    for index, row in df.iterrows():
        f, (a0, a1) = plt.subplots(1,2, figsize=(9.5,2.3), gridspec_kw = {'width_ratios':[3, 8]})
        data = ast.literal_eval(row['val'])
        total_water = random.randint(10,100)
        wdata = {'Reused water': random.randint(20,40)/100 * total_water, 'Total Water': total_water}
        names = list(data.keys())
        values = list(data.values())
        labels = list(wdata.keys())
        sizes = list(wdata.values())
        colors = ['#64dd17', '#2979ff']
        explode = (0.1, 0.0)
        a0.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
        a0.axis('equal')
        if data['ph'] >= 6.5 and data['ph'] <= 8.5 and data['solids'] < 50 and data['hardness'] < 45 and data['oil'] < 5 and data['bod'] < 5:
            a1.bar(range(len(data)),values,tick_label=names, color=['#64dd17', '#64dd17', '#64dd17', '#64dd17', '#64dd17'])
        else:
            a1.bar(range(len(data)),values,tick_label=names, color=['#ff0403', '#ff0403', '#ff0403', '#ff0403', '#ff0403'])
        image = BytesIO()
        plt.title("Industry name: {}".format(row['name']))
        f.tight_layout()
        f.savefig(image, format='png')
        encoded = base64.b64encode(image.getvalue())
        html = '<img src="data:image/png;base64,{}">'.format
        iframe = IFrame(html(encoded.decode()), 970, 250)
        popup = folium.Popup(iframe, max_width=2650)
        if data['ph'] >= 6.5 and data['ph'] <= 8.5 and data['solids'] < 50 and data['hardness'] < 45 and data['oil'] < 5 and data['bod'] < 5:
            marker = folium.Marker(location=[row['lat'], row['long']], popup=popup).add_to(folium_map)
        else:
            marker = folium.Marker(location=[row['lat'], row['long']], popup=popup, icon=folium.Icon(color='red')).add_to(folium_map)
        plt.close()
    return folium_map.get_root().render()

@app.route('/heatmap')
def heatmap():
    global choropleth_map
    global ward_dict
    global geo_json_data
    global colormap
    folium.GeoJson(
    geo_json_data,
    style_function=lambda feature: {
    'fillColor': colormap(ward_dict[feature['properties']['name']]),
    'color': 'black',
    'weight': 1,
    'dashArray': '4, 4',
    'fillOpacity': 0.5
    }).add_to(choropleth_map)
    return choropleth_map.get_root().render()

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
