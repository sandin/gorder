'''
Created on 2011-12-2

@author: lds
'''

def fixGlassCSV(data):
    newStr = "";
    line = data.split("\n")
    lastLine = []
    for l in line:
        if l.startswith('#'):
            continue
        if not l or l == '\r\n': 
            newStr += '\r\n'
            continue
    
        l = l.replace("\r\n", "")
        data = l.split(',')
        if (len(data) == 3):
            data = [lastLine[0], lastLine[1], data[0], data[1], data[2], lastLine[5]]
        elif (len(data) == 4):
            data = [lastLine[0], lastLine[1], data[0], data[1], data[2], data[3]]
            newStr += ','.join(data) + '\r\n'
    
        lastLine = data
    
    return newStr
