# -*- coding: utf-8 -*-
# Este fichero forma parte de airea.me
#
# Copyright 2011 Plexxoo Interactiva S.L.
# Copyright Daniel Gonzalez     <demetrio@plexxoo.com>
# Copyright Jon Latorre         <moebius@plexxoo.com>
# Copyright Silvia Martín       <smartin@plexxoo.com>
# Copyright Jesus Martinez      <jamarcer@plexxoo.com>
#
# Este fichero se distribuye bajo la licencia GPL según las
# condiciones que figuran en el fichero 'licence' que se acompaña.
# Si se distribuyera este fichero individualmente, DEBE incluirse aquí
# las condiciones expresadas allí.
#
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

def get_url_contents(url):
    """
    Gets the contents from a given URL.
    """
    import urllib
    wf = urllib.urlopen(url)
    str=wf.read()
    wf.close()
    
    return str

def parse_csv(stream, delimiter=',',header=None):
    import csv, re
    regex=re.compile('\W+')
    
    def clean(data):
        data=data.strip()
        try:            
            if str(int(data))==str(data): return int(data)
            return float(data)
        except ValueError:
            return data.strip()
        
    cols=header
    rows=[]
    for line in csv.reader(stream,delimiter=delimiter):
        if not cols:
            cols=[regex.sub('_',x.strip().lower()) for x in line]
        else:
            rows.append(dict((key,clean(line[i])) for i,key in enumerate(cols)))
    return cols, rows

def get_csv_from_list(cols,rows,needed=[]):
    n_cols=[]
    n_rows=[]
    for key in needed:
        n_cols.append(cols[key-1])
        
    for row in rows:
        tmp={}
        for col in n_cols:
            tmp[col]=row[col]
        # Calculate latitude-longitude coordinates
        (lat,lon)=convertUTM(float(row['xutm'].replace(',','.')),float(row['yutm'].replace(',','.')))
        tmp['lat']=lat
        tmp['lon']=lon
        n_rows.append(tmp)
        
    n_cols.append('lat')
    n_cols.append('lon')
        
    return n_cols, n_rows    

def get_zone_code(url):
    if url == '':
           return None
    parameters = url.split('?')
    params = parameters[1].split('&')
    zone = ''
    for param in params:
        (name, value) = param.split('=')
        if name == 'CodZona':
            zone = value
    return zone

def get_station_code(url):
    if url == '':
           return None
    parameters = url.split('?')
    params = parameters[1].split('&')
    zone = ''
    for param in params:
        (name, value) = param.split('=')
        if name == 'CodEst':
            zone = value
    return zone

def get_from_list(item,list):
    try:
        return list[item]
    except:
        return None
    
def convertUTM(xutm,yutm,zone=30,northernHemisphere=True):
    """
    Convert UTM coordinates to Latitude-Longitude coordinates
    """
    exec("from applications.%s.modules.utm2latlon import utmTolatlon"%request.application)
    #from applications.aireme.modules.utm2latlon import utmTolatlon
    return utmTolatlon(zone, xutm, yutm, northernHemisphere)