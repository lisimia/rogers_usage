from django.http import HttpResponse
from django.core.cache import cache

from lxml import html, etree
import requests
import os


def usage(request):

    rt = cache.get('usage')
    if rt:
        print 'rt pulled from redis'
        return HttpResponse(rt)

    # based on reverse enginnering the rogers login portal
    login_post_url = 'https://www.rogers.com/siteminderagent/forms/login.fcc'
    pwd = os.environ.get('PASS')
    user = os.environ.get('USER')
    login_post_data = {
        'USER': user,
        'password': pwd,
        'SMAUTHREASON': '0',
        'target': '/web/RogersServices.portal/totes/#/accountOverview'
    }
    s = requests.Session()
    # login
    s.post(login_post_url, data=login_post_data)

    # This req will set your sessions correctly then use JS to refresh
    s.get('https://www.rogers.com/web/myrogers/internetUsageBeta')
    # mimic the refresh
    res2 = s.get('https://www.rogers.com/web/myrogers/internetUsageBeta')

    # pull the information from available xpath
    doc = html.fromstring(res2.content)
    t = doc.xpath('//table[@id="usageInformation"]')[0]

    # based on page from october
    tr = t.getchildren()[-1]
    if not tr.values():
        t.remove(tr)
    rt = etree.tostring(t)
    # clean the information and re-render

    cache.set('usage', rt, 60 * 60 * 4)
    return HttpResponse(rt)
