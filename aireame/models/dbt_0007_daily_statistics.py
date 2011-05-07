# -*- coding: utf-8 -*- 
# Generated using ToTeS #

db.define_table('daily_statistics',
    Field('station', 'reference station', label=T('Station')),
    Field('element', 'string', length=10, label=T('Element')),
    Field('statistic_date', 'date', label=T('Date')),
    Field('value', 'double', label=T('Value')),
    format='')

