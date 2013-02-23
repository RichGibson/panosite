# just play with tag stuff.
from django.core.management import setup_environ
from panosite import settings
setup_environ(settings)

from gigapan.models import Gigapan 

import json
import sys

def one() :
    list = []
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    start_year = 2007
    end_year = 2014
    for year in range(start_year, end_year):
        for month in range(1,13):
            m={}
            m['month'] = month
            m['month_name'] = months[month-1]
            m['year'] = year
            m['cnt'] = 0
            m['gigapan_id'] = 0
            list.append(m)
            print "a: month: %i month_name: %s year: %i" % (month, months[month-1], year)
            print "b: month: %i month_name: %s year: %i" % (m['month'],m['month_name'],m['year'])
            i= len(list)-1
            print "c: month: %i month_name: %s year: %i" % (list[i]['month'],list[i]['month_name'],list[i]['year'])
            print len(list)

    

    from django.db import connection, transaction
    cursor = connection.cursor()

    # Data modifying operation - commit required
    sql = """
            select strftime('%%Y-%%m', taken) as d, count(strftime('%%Y-%%m',taken)) as cnt ,
            strftime('%%Y',taken) as year,
            strftime('%%m',taken) as month,
            max(gigapan_id) as gigapan_id
            from gigapan_gigapan 
            where month > 0
            and year >= 0 
            group by d order by cnt
          """
    print "excecute this sql: %s" % sql
    cursor.execute(sql, [])
    desc = cursor.description
    counts = [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

    for m in counts:
        if (int(m['year']) >= start_year):
            index = (int(m['year']) - start_year) * 12 + int(m['month'])
            list[index]['cnt'] = m['cnt'] 
            list[index]['gigapan_id'] = m['gigapan_id'] 
        
 
    for x in list:
        print "index: %i  %s %i\t%i %i" % (index, x['month_name'], x['year'], x['cnt'], x['gigapan_id']) 



one()

