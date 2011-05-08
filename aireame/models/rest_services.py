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

def rest_station_get(code=None):
    data={}
    query=((db.zone.id==db.station.zone)&(db.town.id==db.station.town))
    if code is not None:
        query=query&(db.station.code==code)
    else:
        query=query&(db.station.id>0)
    
    rows=db(query).select(db.station.id,db.station.identifier,db.station.code,db.station.name,db.station.address,db.town.name,db.zone.code,db.station.latitude,db.station.longitude)
    num=1
    for row in rows:
        tmp={}
        tmp['id']=row.station.identifier
        tmp['name']=row.station.name
        tmp['address']="%s - %s"%(row.station.address,row.town.name)
        tmp['external_url']=ESTATION_LINK%(row.zone.code,row.station.code)
        tmp['lat']=row.station.latitude
        tmp['lon']=row.station.longitude
        data[num]=tmp
        num+=1        
    return data

def _get_station_data(query=None,ca=False):
    if query is None:
        return {}
    
    # CA elements: Elementos para calidad del aire
    ca_elems=QUALITY_ELEMENTS
    
    # Get Values
    rows=db(query).select(db.measurement.id,db.measurement.element,db.measurement.measurement_hour,db.measurement.value,orderby="measurement.element ASC,measurement.measurement_hour ASC")
    elements={}
    for row in rows:
        if ca:
            if (row.element in ca_elems) is False:
                continue
        if (row.element in elements.keys()) is False:
            elements[row.element]={}
        elements[row.element][row.measurement_hour]=row.value
    values={}
    for index in range(1,25):
        values[index]=[]
    
    for item in elements.keys():
        elem=elements[item]
        for index in range(1,25):
            values[index].append(elem[index])
            
    return {'values': values,'columns':elements.keys()}

def rest_station_last(code=None,ca=False):
    # Data
    data={}
    if code is None:
        return data
    
    # Initialize configuration
    cfg=Configure()
    cur_date = cfg.get('current_date')
    if cur_date is None:
        return data
    # Prepare date
    today=get_date_from_string(cur_date, "%Y-%m-%d")

    # Get Values
    query=(db.measurement.measurement_date==today)&(db.measurement.station==db.station.id)&(db.station.code==code)
    return _get_station_data(query,ca)

def rest_station_seven(code=None,ca=False):
    from datetime import timedelta
    
    # Data
    data={}
    if code is None:
        return data
    
    # Initialize configuration
    cfg=Configure()
    cur_date = cfg.get('current_date')
    if cur_date is None:
        return data
    # Prepare date
    today=get_date_from_string(cur_date, "%Y-%m-%d")
    seven_days = timedelta(days=7)
    last7_date=today-seven_days
    

    # Get Values
    query=(db.daily_statistics.statistic_date>=last7_date)&(db.daily_statistics.statistic_date<=today)&(db.daily_statistics.station==db.station.id)&(db.station.code==code)
    rows=db(query).select(db.daily_statistics.element,db.daily_statistics.statistic_date,db.daily_statistics.value,orderby="daily_statistics.element ASC,daily_statistics.statistic_date ASC")

    counter=0
    for row in rows:
        tmp={}
        tmp['name']=row.element
        tmp['date']=row.statistic_date
        tmp['value']=row.value
        tmp['element']=row.element
        data[counter]=tmp
        counter+=1
    return data


def rest_quality(code=None,type=None):
    # Data
    data={}
    if code is None:
        return data
    if type is None:
        type='current'
        
    if type=='current':
        return rest_station_last(code,True)
    else:
        return data