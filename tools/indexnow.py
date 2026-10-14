#!/usr/bin/env python3
"""Meldt alle URL's uit sitemap.xml bij IndexNow (Bing, DuckDuckGo, Ecosia, Yandex). Gratis, geen account."""
import json, re, sys, urllib.request, os
KEY = "9a7bd066b1ef421bb698f3e20a840a06"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urls = re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "sitemap.xml")).read())
body = json.dumps({"host": "watkoopik.nl", "key": KEY, "keyLocation": "https://watkoopik.nl/%s.txt" % KEY, "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
try:
    r = urllib.request.urlopen(req, timeout=20)
    print("IndexNow: %d URL's gemeld, status %d" % (len(urls), r.status))
except Exception as ex:
    print("IndexNow mislukt (niet erg, volgende deploy opnieuw):", ex)
