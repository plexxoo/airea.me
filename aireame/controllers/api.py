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

@request.restful()
def station():
    def GET(id=None):
        return rest_station_get(id)
    return locals()

@request.restful()
def last():
    def GET(id=None):
        return rest_station_last(id)
    return locals()

@request.restful()
def seven():
    def GET(id=None):
        return rest_station_seven(id)
    return locals()

@request.restful()
def month():
    def GET(id=None):
        return rest_station_month(id)
    return locals()

@request.restful()
def year():
    def GET(id=None):
        return rest_station_year(id)
    return locals()


@request.restful()
def quality():
    def GET(id=None,type=None):
        return rest_quality(id,type)
    return locals()

@request.restful()
def stationqa():
    def GET(id=None):
        return rest_station_qa_get(id)
    return locals()
