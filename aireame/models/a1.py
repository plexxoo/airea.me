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

from gluon.storage import Storage

def get_request_args(expected=None):
    expected_args = []
    arguments = request.args
    
    if expected is None:
        expected = len(arguments)
            
    for item in range(expected):
        try:
            value = request.args(item)
        except:
            value = None
        expected_args.append(value)
    if expected < len(arguments):
        expected_args.append(arguments[expected:])
    else:
        expected_args.append([])
    return expected_args

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

# Script facilities
def get_html_from_url(url):
    """
    Gets the HTML contents from a given URL.
    """
    import lxml.html
    f=get_url_contents(url)
    return lxml.html.document_fromstring(f)
    
def get_html_from_file(filename):
    """
    Gets the HTML contents from a file.
    """
    import lxml.html
    f=open(filename)
    html=lxml.html.parse(f)
    return html.getroot()

def get_date_from_string(str_date,format="%Y-%m-%d"):
    # Prepare date
    import time
    import datetime
    today=None
    try:
        pack=time.strptime(str(str_date), format)
        today=datetime.datetime(*pack[0:3])
    except Exception, e:
        pass
    return today

def get_current_date_from_datasource():    
    root=get_html_from_url(CURRENT_INFO_URL)
    
    date_form=root.get_element_by_id('doc24')
    date_p=[ b for b in date_form.iterfind(".//p")]
    
    for child in date_p[0]:
        child.drop_tree()
    
    date_lit=date_p[0].text.strip()
    (day,month,year)=date_lit.split('/')
    
    from datetime import date
    cur_date=date(int(year),int(month),int(day)) 
    return cur_date

def get_current_data_of_station(zone,station,date): 
    # Prepare link
    date_lit=date.strftime('%m/%d/%Y') #'04/30/2011'
    url=ESTATION_DATE_LINK%(zone,station,date_lit)
    element_code={"Benceno": 'C6H6',
                  "CO": 'CO',
                  "DV": 'DirV',
                  "DirV": 'DirV',
                  "Etilbenceno": 'C8H10',
                  "HC": 'HC',
                  "HC met": 'HCmet',
                  "HC noMet": 'HCnoMet',
                  "Humed": 'Humedad',
                  "Humedad": 'Humedad',
                  "NH3": 'NH3',
                  "NO": 'NO',
                  "NO2": 'NO2',
                  "O3": 'O3',
                  "Ortoxileno": 'O_C8H10',
                  "P": 'P',
                  "PM10": 'PM10',
                  "PM2.5": 'PM2.5',
                  "Rad": 'Rad',
                  "Rad UV": 'RadUV',
                  "SH2": 'SH2',
                  "SO2": 'SO2',
                  "T": 'T',
                  "Temp": 'T',
                  "Tolueno": 'C7H8',
                  "VelV": 'VelV'}

    try:
        # Get date from datasource
        root=get_html_from_url(url) 
        
        # Get available dates
        date_list=root.find_class("aizeflotaselect")[0]
        dates=[]
        for elem in date_list:
            dates.append(elem.text)
                
        # Get html elements needed
        elem_list=root.find_class("aizetable")
        data_table=elem_list[0]
    
        rows=[ b for b in data_table.iterfind(".//tr") ]
        
        # Process data
        data={}
        row_num=0
        def clean_value(value):
            if value==u'\xa0':
                return None
            else:
                return value
            
        for row in rows:
            if row_num == 0:
                # First row contains hour literals.
                row_num+=1
                continue
            else:
                cols=[ b for b in row.iterfind(".//td") ]
                
                elem_name=None
                tmp={}
                hour=0
                for col in cols:
                    if len(col.text) <=0:
                        continue
                    if hour == 0:
                        name=col.text.strip().split(' ')
                        if len(name)>2:
                            code="%s %s"%(name[0],name[1])
                        else:
                            code=name[0]
                        try:
                            elem_name=element_code[code]
                        except:
                            elem_name=''
                    else:
                        tmp[hour]=clean_value(col.text)
                    hour+=1
                if len(elem_name) > 0:
                    data[elem_name]=tmp
        return data
    except:
        return {}

def insert_current_data_of_station(zone,station_name,station_code,station_id,date): 
    data=get_current_data_of_station(zone,station_code,date)
    # Insert data into database
    for elem in data.keys():
        elem_data=data[elem]
        tmp={}
        tmp['station']=station_id
        tmp['element']=elem
        tmp['measurement_date']=date
        # Check if data is loaded yet
        rows=db((db.measurement.station==station_id)&(db.measurement.element==elem)&(db.measurement.measurement_date==date)).select(db.measurement.id)

        if len(rows) > 0:
            response.flash=T('Station data in table')+": '%s'"%station_name
            return data
        else:
            for hour in elem_data.keys():
                tmp['measurement_hour']=hour
                tmp['value']=elem_data[hour]
                id=db.measurement.insert(**tmp)
            db.commit()
    return data

def statistical_data_of_station(station_id,date): 
    # Get station data for date
    rows=db((db.measurement.station==station_id)&(db.measurement.measurement_date==date)).select(db.measurement.element,db.measurement.measurement_hour,db.measurement.value,orderby="measurement.element ASC,measurement.measurement_hour ASC")
    elements={}
    for row in rows:
        if row.element in elements.keys():
            elements[row.element][row.measurement_hour]=row.value
        else:
            elements[row.element]={}
            elements[row.element][row.measurement_hour]=row.value
    
    averages={}
    for elem in elements.keys():
        element=elements[elem]
        counter=0
        average=0
        for item in element.keys():
            if element[item] is not None:
                if element[item] <> 0:
                    counter+=1
                    average+=element[item]
        if average <= 0:
            averages[elem]=0
        else:
            averages[elem]=average/counter
    
    # Insert data into database
    for elem in averages.keys():
        # Checks if data in database
        myrow=db((db.daily_statistics.station==station_id)&(db.daily_statistics.element==elem)&(db.daily_statistics.statistic_date==date)).select(db.daily_statistics.id).first()
        if myrow is None:
            tmp={}
            tmp['station']=station_id
            tmp['element']=elem
            tmp['statistic_date']=date
            tmp['value']=averages[elem]
            id=db.daily_statistics.insert(**tmp)
        else:
            tmp={}
            tmp['statistic_date']=date
            tmp['value']=averages[elem]
            myrow.update(**tmp)
    
    db.commit()
    return averages

def get_station_by_code(code):
    if code is None:
        return None
    
    # Station data
    query=((db.zone.id==db.station.zone)&(db.town.id==db.station.town)&(db.station.code==code))    
    row=db(query).select(db.station.id,db.station.identifier,db.station.code,db.station.name,db.station.address,db.town.name,db.zone.code,db.station.latitude,db.station.longitude).first()
    
    tmp=Storage()
    tmp['id']=row.station.identifier
    tmp['name']=row.station.name
    tmp['code']=row.station.code
    tmp['address']="%s - %s"%(row.station.address,row.town.name)
    tmp['href']=ESTATION_LINK%(row.zone.code,row.station.code)
    tmp['lat']=row.station.latitude
    tmp['lon']=row.station.longitude
    return tmp
