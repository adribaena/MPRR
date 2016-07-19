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

def crearlistaFinal (lista, lCues) :
    lst = {'U': [], 'NU': []}
    for i in [i for i,x in enumerate(lCues) if x == 'U']:
        lst['U'] = lst['U'] + [i] 
    for i in [i for i,x in enumerate(lCues) if x == 'NU']:
        lst['NU'] = lst['NU'] + [i]
        
    listaCues = ['U','NU']
    for i in range(72) : 
        item = listaCues[i % 2]
        dummyTrial = random.choice(lst[item])
        lst[item].remove(dummyTrial)
        lCues[dummyTrial] = lista[i] + [lCues[dummyTrial]]
    return lCues
    


def angleInDegrees(pt, pt2):
    x2, y2 = pt2
    if x2 == 0.0 and y2 == 0.0:
        return 404
    angleDeg = angleInRads(pt, pt2)*180/math.pi
    return round(angleDeg,3)

def darPrimeraLista (lista, n) : 
    listaF = []
    for i in range(n):
        listaF = listaF + lista
    return listaF


def esPseudoRandom(lista) :
    
    res = True
    for i in range(len(lista)-2) : 
        if lista[i] == lista[i+1] and lista[i+1] == lista[i+2] :
            res = False
            break
    return res 
    
def darListaCompleta(lc, lAux, n):
    
    listaCFin = []
    for i in range(n):
        lc, lAux = darSiguientePseudoRandom(lc, lAux)
        listaCFin = listaCFin + lc
    return listaCFin, [listaCFin[len(listaCFin)-2], listaCFin[len(listaCFin)-1]]


def darSiguientePseudoRandom(lista, anteriores):
    random.shuffle(lista)
    anterioresIguales = 0
    if anteriores[0] == anteriores[1]:
        anterioresIguales = anteriores[0]
    anterioresIguales = anterioresIguales == lista[0] and anterioresIguales == lista[1]
    
    while anterioresIguales == 1 or esPseudoRandom(lista) == False : 
        random.shuffle(lista)
        anterioresIguales1 = anteriores[1] == lista[0] and anteriores[1] == lista[1]
        anterioresIguales2 = anteriores[0] == anteriores[1] and anteriores[1] == lista[0]
        anterioresIguales = anterioresIguales1 or anterioresIguales2
        
    return lista, [lista[len(lista)-2], lista[len(lista)-1]]


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
    