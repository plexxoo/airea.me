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

import StringIO
import sys

# Load administration user
try:
    if db(db.auth_user.id >= 1).count() == 0:
        value=ADMIN_USER        
        crypt=CRYPT(key=auth.settings.hmac_key)
        value['password']=crypt(value['password'])[0]
        db.auth_user.insert(**value)
except:
    except_data=sys.exc_info()
    msg="Unexpected error: %s"%except_data[0]
    pass   

# Load zone,province,town and station data
try:
    if db(db.station.id >= 1).count() == 0:
        data=get_url_contents(CVS_URL)
        input=StringIO.StringIO(data)
        (cols, rows) = parse_csv(input, ';')
        (cols, rows) = get_csv_from_list(cols, rows, [1, 2, 3, 4, 5, 6, 7, 8, 9, 41, 42])
        
        # Zone table: name, code
        zones = {}
        for row in rows:
            name = row['zona']
            code = get_zone_code(row['link_zona'])
            if code is not None:
                if code in zones.keys():
                    continue
                else:
                    ident=code.lstrip('@')
                    value={'name': name, 'code': ident}
                    zones[name]=db.zone.insert(**value)
        
        # Province table: name, code
        provinces = {}
        for row in rows:
            def get_code(name):
                if name == '':
                    return None
                else:
                    return name
            name = row['provcod'].capitalize()
            code = get_code(name)
            if code is not None:
                if code in provinces.keys():
                    continue
                else:
                    value={'name': name, 'code': code}
                    provinces[code]=db.province.insert(**value)
                    
        
        # Town table: name
        towns = {}
        for row in rows:
            def get_code(name):
                if name == '':
                    return None
                else:
                    return name
            name = row['poblacion']
            code = get_code(name)
            if code is not None:
                if code in towns.keys():
                    continue
                else:
                    value={'name': name, 'code': code}
                    towns[code]=db.town.insert(name=name)
                    
        
        # Station table: identifier, zone, province, town, name, code, address, latitude, longitude
        for row in rows:        
            value= { 'identifier': float(row['idest'].replace(',','.')),
                     'zone': get_from_list(row['zona'],zones),
                     'province': get_from_list(row['provcod'].capitalize(),provinces),
                     'town': get_from_list(row['poblacion'],towns),
                     'name': row['estacion'],
                     'code': get_station_code(row['link_estac']),
                     'address': row['direcc'],
                     'latitude': row['lat'],
                     'longitude': row['lon']}
            db.station.insert(**value)
except:
    except_data=sys.exc_info()
    msg="Unexpected error: %s"%except_data[0]
    pass