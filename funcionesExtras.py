import random, math



def angleInRads(pt1, pt2):
    
    x1, y1 = pt1
    x2, y2 = pt2
    if x2 == 0.0 and y2 == 0.0:
        return 404
    inner_product = x1*x2 + y1*y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    return round(math.acos(inner_product/(len1*len2)),3)


def angleInDegrees(pt, pt2):
    x2, y2 = pt2
    if x2 == 0.0 and y2 == 0.0:
        return 404
    angleDeg = angleInRads(pt, pt2)*180/math.pi
    return round(angleDeg,3)


def testPseudoRandom(lista):
    
    listaCues = ['U','NU']
    lista.pop(0)
    elem1= lista[0]
    elem2= lista[1]
    
    elem3= random.choice(listaCues)
    while elem1 == elem2 and elem2 == elem3:
        elem3= random.choice(listaCues)
    lista.append(elem3)
    return lista
    


def obtenerposicionesTarget(elem):
    
    cue_type = elem[0]
    sector = elem[1]
    position_target = elem[2]
    
    listaFin = []
    distance = 5 * math.sin(math.pi/4)
    distance=round(distance,2)
    listaFinCert = [(0,5),(distance,distance),(5,0),(distance, -distance),(0,-5),(-distance, -distance),(-5,0),(-distance,distance)]
    
    distanceX60N = 5 * math.cos(math.pi/6)
    distanceX60N=round(distanceX60N,2)
    
    distanceY60N = 5 * math.sin(math.pi/6)
    distanceY60N=round(distanceY60N,2)
    
    distanceX60E = 5 * math.cos(math.pi/3)
    distanceX60E=round(distanceX60E,2)
    
    distanceY60E = 5 * math.sin(math.pi/3)
    distanceY60E=round(distanceY60E,2)
    
    distanceX60S = 5 * math.cos(-math.pi/6)
    distanceX60S = round(distanceX60S,2)
    
    distanceY60S = 5 * math.sin(-math.pi/6)
    distanceY60S=round(distanceY60S,2)
    
    distanceX60W = 5 * math.cos((4* math.pi)/6)
    distanceX60W=round(distanceX60W,2)
    
    distanceY60W = 5 * math.sin((4* math.pi)/6)
    distanceY60W =round(distanceY60W,2)

    if cue_type == 'H':
        listaFin = listaFinCert
    elif cue_type == 'M' :
        if sector == 'N':
            listaFin = [(-distanceX60N,distanceY60N),(0,5),(distanceX60N,distanceY60N)]
        elif sector == 'E':
            listaFin = [(distanceX60E,distanceY60E),(5,0),(distanceX60E,-distanceY60E)]
        elif sector == 'S':
            listaFin = [(-distanceX60S,distanceY60S),(0,-5),(distanceX60S,distanceY60S)]
        else :
            listaFin = [(distanceX60W,-distanceY60W),(-5,0),(distanceX60W,distanceY60W)]
    elif cue_type == 'N':
        listaFin = [listaFinCert[int(position_target)]]
    
    return listaFin
    