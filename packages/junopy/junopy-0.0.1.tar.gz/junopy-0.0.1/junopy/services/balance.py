
from junopy.utils.juno import *

def Balance():
    data = Get("/balance")
    del data['_links']
    return data
