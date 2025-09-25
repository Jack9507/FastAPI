import os
from collections import OrderedDict
import nonjaon

print(od.getcwd())

print(10/0)

# res= int(os.getenv('MAX_CACHE_SIZE'))
# print(res)
# print(type(res))

mydict= OrderedDict()
# clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'move_to_end', 'pop', 'popitem', 'setdefault', 'update', 'values'
# print(dir(mydict))

mydict['emp1'] = 'jerry'
mydict['emp2'] = 'harry'
mydict['emp3'] = 'larry'


# print(mydict)
# mydict.move_to_end('emp2')
# print(mydict)

# res= mydict.pop("emp12", None)
# print(res)

from datetime import datetime

print(datetime.now())
print(datetime.utcnow())

import time

print("------------------")
print(time.time())
