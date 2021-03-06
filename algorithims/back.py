import re
import numpy as np

def array_generator(data):
    '''
    Returning the list consists of int data
    and empty space for empty value
    '''
    if data != None:
        req = re.split(pattern=r",\s|\]|\[", string=data)[1:-1]
        req_data = []
        for i in req:
            try:
                req_data.append(float(i))
            except:
                req_data.append(' ')
        val = req_data
        return val
    else:
        return data



#print(dict([(12, 33), (34,54), (3,4)]))