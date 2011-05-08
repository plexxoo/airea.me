# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = 'airea.me'
response.subtitle = T('Aireate')

#http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Plexxoo Team Abredatos 2011'
response.meta.description = 'Airea.me'
response.meta.keywords = 'opendata, abredatos, web2py, python, framework'
response.meta.generator = 'Web2py Enterprise Framework'
response.meta.copyright = 'Copyright 2011'


##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    (T('Home'), False, URL('default','index'), []),
    (T('Historic'), False, URL(request.application, 'historic', 'index'),[])
    ]

##########################################
## this is here to provide shortcuts
## during development. remove in production
##
## mind that plugins may also affect menu
##########################################

#########################################
## Make your own menus
##########################################

admin_menu=[
    (T('Master'), False, None,
     [(T('Zone'), False, URL(request.application, 'zone', 'index')),
      (T('Province'), False, URL(request.application, 'province', 'index')),
      (T('Town'), False, URL(request.application, 'town', 'index')),
      (T('Station'), False, URL(request.application, 'station', 'index')),
      (T('Units'), False, URL(request.application, 'measurement_unit', 'index')),
      (T('Station Elements'), False, URL(request.application, 'station_element', 'index'))
     ]
   )]

if auth.user:
    response.menu+=admin_menu
