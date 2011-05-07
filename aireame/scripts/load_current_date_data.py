#!/usr/bin/env python
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

# Use:
# From web2py directory, console mode, write...
# $ ./web2py.py -S aireame -M -R applications/aireame/scripts/load_current_date_data.py

import time
import datetime

def load_data(date):
    # Get all stations
    rows=db((db.zone.id==db.station.zone)&(db.station.id>0)).select(db.station.id,db.zone.code,db.station.code,db.station.name)
    num_rows=len(rows)
    number=1
    for row in rows:
        response.flash = None
        print "Processing %i/%i - %s "%(number,num_rows,row.station.name)
        data=insert_current_data_of_station(row.zone.code,row.station.name,row.station.code,row.station.id,date)
        if response.flash is not None:
            print response.flash
        number+=1

def generate_statistical_data(date=None):
    if date is not None:
        rows=db(db.station.id>0).select(db.station.id)
        for row in rows:
            print "Processing %i "%row.id
            statistical_data_of_station(row.id,date)
    

init_time=time.time()
today=get_current_date_from_datasource()
# Initialize configuration
cfg=Configure()
cur_date = cfg.get('current_date')
get_data=False
if cur_date is None:
    get_data=True
if today!=cur_date:
    get_data=True
    
if get_data:
    print today
    load_data(today)
    generate_statistical_data(today)
    cfg.set('current_date',today)
    
end_time=time.time()
process_time=end_time-init_time
print "All data processed in %f secs.\n"%process_time