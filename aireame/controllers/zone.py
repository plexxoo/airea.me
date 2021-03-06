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

crud.settings.create_next = URL('index')
crud.settings.delete_next = URL('index')
crud.settings.update_next = URL('index')

@auth.requires_login()
def index(): 
    db.zone.id.represent = lambda id: DIV(A(T("Edit"), _href=URL(r=request, f='update', args=(id)))," ",  A(T("Show"), _href=URL(r=request, f='read', args=(id))))
    form = crud.select(db.zone, fields = ['zone.id', 'zone.name',  'zone.code', ], headers = {'zone.id': T("Actions"), 'zone.name': 'Name',  'zone.code': 'Code', })
    return dict(form=form,auser=auth.user)


@auth.requires_login()
def create():
    return dict(form=crud.create(db.zone),auser=auth.user)

@auth.requires_login()
def update():
    return dict(form=crud.update(db.zone, request.args(0)),auser=auth.user)
 
@auth.requires_login()       
def read():
    return dict(form=crud.read(db.zone, request.args(0)),auser=auth.user)
