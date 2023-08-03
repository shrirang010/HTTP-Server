# To break the url in request messages
from urllib.parse import * # to parse URL/URI
import os

def breakdown(entity):
    u = urlparse(entity)
    entity = unquote(u.path)
    if entity == '/':
        entity = os.getcwd()
    query = parse_qs(u.query)
    return (entity, query)