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
# $ ./web2py.py -S aireame -M -R applications/aireame/scripts/load_range_date_data.py

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
# Initialize configuration
date_range=['2011-05-01','2011-05-02','2011-05-03','2011-05-04','2011-05-05','2011-05-06']
#date_range=['2011-04-01','2011-04-02','2011-04-03','2011-04-04','2011-04-05','2011-04-06','2011-04-07','2011-04-08','2011-04-09','2011-04-10',
#            '2011-04-11','2011-04-12','2011-04-13','2011-04-14','2011-04-15','2011-04-16','2011-04-17','2011-04-18','2011-04-19','2011-04-20',
#            '2011-04-21','2011-04-22','2011-04-23','2011-04-24','2011-04-25','2011-04-26','2011-04-27','2011-04-28','2011-04-29','2011-04-30']

for date_lit in date_range:
    date=get_date_from_string(date_lit) #"%Y-%m-%d"
    print date
    load_data(date)
    generate_statistical_data(date)
    
end_time=time.time()
process_time=end_time-init_time
print "All data processed in %f secs"%process_time