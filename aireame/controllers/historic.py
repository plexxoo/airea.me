# -*- coding: utf-8 -*- 
# Este fichero forma parte de airea.me
#
# Copyright 2011 Plexxoo Interactiva S.L.
# Copyright Daniel Gonzalez     <demetrio@plexxoo.com>
# Copyright Silvia Martín       <smartin@plexxoo.com>
# Copyright Jon Latorre         <moebius@plexxoo.com>
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

def index():
    # Select data
    rows=db((db.zone.id==db.station.zone)&(db.station.id>=0)).select(db.station.id,db.station.name,db.zone.code,db.zone.name,db.station.code,orderby="zone.name ASC,station.name ASC")
    zones={}
    cur_zone=None
    zone=None
    for row in rows:
        if cur_zone != row.zone.name:
            if zone is not None:
                zones[row.zone.name]=zone
            zone=[]
            cur_zone = row.zone.name
            
        tmp=Storage()
        tmp['id']=row.station.id
        tmp['zone']=row.zone.name
        tmp['name']=row.station.name
        tmp['code']=row.station.code
        tmp['href']=ESTATION_LINK%(row.zone.code,row.station.code)
        zone.append(tmp)
        
    return dict(data=zones,auser=auth.user)

def current():
    [code, params] = get_request_args(1)  
    # Estation data
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
    
    return dict(station=tmp)
