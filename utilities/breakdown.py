# To break the url in request messages
from urllib.parse import * # to parse URL/URI
import os
from datetime import datetime

def breakdown(entity):
    u = urlparse(entity)
    entity = unquote(u.path)
    if entity == '/':
        entity = os.getcwd()
    query = parse_qs(u.query)
    return (entity, query)

def date():
    #  Sun, 06 Nov 1994 08:49:37 GMT  ; RFC 822, updated by RFC 1123
    now = datetime.now()
    datenow = now.strftime('%A,%d %B %Y %H:%M:%S ')
    datenow += "GMT"
    conversation = 'Date: ' + datenow
    return conversation
