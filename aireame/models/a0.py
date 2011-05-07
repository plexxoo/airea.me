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
import os

# Base path
w2p_path=request.env.web2py_path

# Parameters
W2P_APP_PATH=os.path.join(w2p_path,'applications')                                  #: Web2py applications path
APP_PATH=os.path.join(W2P_APP_PATH,request.application)                             #: Application path
HOST='http://'+request.env.http_host                                                #: Host URL
APP_URL='%s/%s' %(HOST, request.application)                                        #: Application URL base

# DAL definition
DB_DAL='sqlite://storage.db'

# Administration user data
ADMIN_USER={'first_name':'Administrador',
            'last_name':'Airea.me',
            'email': 'admin@host.ext',
            'password': 'admin'}

# Links
CVS_URL='http://opendata.euskadi.net/w79-contdata/es/contenidos/ds_geograficos/red_calidad_aire/es_opendata/adjuntos/estaciones.csv'