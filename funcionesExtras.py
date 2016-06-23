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
    


def obtenerposicionesTarget(elem, angleDist):
    
    cue_type = elem[0]
    sector = elem[1]
    position_target = elem[2]
    
    listaFin = []
    listaFinCert = [0, 45, 90, 135, 180, 225, 270, 315]
    
    if cue_type == 'H':
        listaFin = listaFinCert
    elif cue_type == 'M' :
        if sector == 'N':
            listaFin = [150, 90, 30]
        elif sector == 'E':
            listaFin = [60, 0, 300]
        elif sector == 'S':
            listaFin = [210, 270,330]
        else :
            listaFin = [240, 180, 120]
    elif cue_type == 'N':
        listaFin = [listaFinCert[int(position_target)]]
    for i in range(len(listaFin)) :
        ang = listaFin[i] + angleDist
        distorsion = ang/float(180)
        distorsion = distorsion * math.pi
        x = (5 * math.cos(distorsion), 5* math.sin(distorsion))
        
        listaFin[i] = x
    
    return listaFin
    