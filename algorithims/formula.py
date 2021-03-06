

def formula_1(p1, p2=None, p3=None):
    '''Returning a single array for practical
     and theory subject for ordinary level and advanced level
     note: formula 1 =((p1 + p2) / 150) x 100%
    '''
    list_data = []
    if p1 != None and p2 != None and p3 == None:
        '''
        For o level - form four who have p1 and p2
        '''
        for i in range(len(p1)):
            try:
                #To handle wrong data
                list_data.append(round(((float(p1[i]) + float(p2[i])) / 150) * 100, 1))
            except:
                list_data.append('')

    elif p1 != None and p2 != None and p3 != None:
        '''
        for a level - form six with p1 p2 and p3
        '''
        for i in range(len(p1)):
            try:
                #To handle wrong data
                list_data.append((round((float(p1[i]) + float(p2[i]) + float(p3[i])) / 250, 1) * 100))
            except:
                list_data.append('')
    else:
        '''
        for p1 only
        '''
        for i in p1:
            try:
                list_data.append(round(float(i), 1))
            except:
                list_data.append('')
    return list_data


def formula_2(p1, p2=None, p3=None):
    '''Returning a single array for practical
     and theory subject for ordinary level and advanced level
     note: formula 1 =((p1 + p2 x 2) / 2)
    '''
    list_data = []
    for i in range(len(p1)):
        if p1 != None and p2 != None and p3 == None:
            '''
            For o level - form four who have p1 and p2
            '''
            try:
                #To handle wrong data
                list_data.append(round((float(p1[i]) + float(p2[i]) * 2) / 2, 1))
            except:
                list_data.append('')
        elif p1 != None and p2 != None and p3 != None:
            '''
            for a level - form six with p1 p2 and p3
            '''
            try:
                list_data.append(round((float(p1[i]) + float(p2[i]) + float(p3[i]) * 2) / 3, 1))
            except:
                list_data.append('')
        else:
            '''
            for p1 only
            '''
            try:
                list_data.append(round(float(p1[i]), 1))
            except:
                list_data.append('')
    return list_data

def formula_3(p1, p2=None, p3=None):
    '''Returning a single array for practical
     and theory subject for ordinary level
     note: formula 1 =(p1 + p2) / 2
    '''
    list_data = []
    for i in range(len(p1)):
        if p1 != None and p2 != None and p3 == None:
            '''
            For a level - form six who have p1 and p2
            '''
            try:
                #To handle wrong data
                list_data.append(round((float(p1[i]) + float(p2[i])) / 2, 1))
            except:
                list_data.append('')
        else:
            '''
            for p1 only
            '''
            try:
                list_data.append(round(float(p1[i]), 1))
            except:
                list_data.append('')
    return list_data
#print(formula_3(p1=['12.594736', '54', '23', '43', '98']))

