import numpy as np
import random
import cv2

def get_table_data(qu):
    '''Changing data of the data base into matrix table'''
    fname = [i.first_name for i in qu]
    sname = [i.middle_name for i in qu]
    lname = [i.last_name for i in qu]
    sex = [i.sex for i in qu]
    no = [i.candidate_number for i in qu]
    darasa = [i.darasa for i in qu]
    sn = []
    cand_no = []
    for i in sname:
        if i == None:
            sn.append(' ')
        else:
            sn.append(i)
    for i in no:
        if i == None:
            cand_no.append(' ')
        else:
            cand_no.append(i)
    dat =  np.concatenate([np.array(i).reshape(-1, 1) for i in
                           [fname, sn, lname, sex, cand_no, darasa]], axis=1)
    #return sorted data
    return dat[dat[:, 0].argsort()]


def user_table(qu):
    fname = [i.first_name for i in qu]
    sname = [i.second_name for i in qu]
    role = [i.role for i in qu]
    ukey = [i.value_key for i in qu]

    dat = np.concatenate([np.array(i).reshape(-1, 1) for i in
                           [fname, sname, role, ukey]], axis=1)
    #return sorted data
    return dat[dat[:, 0].argsort()]

def generate_key(val, role='TE'):
    ls = 'ADBNMKTECSPKLJ23458679XZVQRF'
    l = [i for i in ls]
    req = role[0]
    for i in range(6):
        req += str(random.choice(l))
    dat = req + role[1] + str(val)

    for i in range(5):
        dat += str(random.choice(l))
    return dat

def required_key(val):
    role = val[0] + val[7]
    pk = int(val[8:-5])
    return (role, pk)

def validate_key(val):
    try:
        role = val[0] + val[7]
        if role in ['TE', 'AC', 'SE']:
            try:
               if int(val[8:-5]):
                   return True
            except:
                return False
        else:
            return False
    except:
        return False

def profile_logo(file_path, name):
    img = cv2.imread(file_path)
    img = img.resize((100, 100))
    cv2.imwrite(name, img)

def encode(dt):
    if dt == 'AC':
        return 1
    elif dt == 'TE':
        return 2
    elif dt == 'SE':
        return 3
    else:
        return None

