from __future__ import division
import random , csv, funcionesExtras, itertools
from psychopy import visual, gui,core, data,  event, logging, prefs
from psychopy.hardware import joystick
from scipy.spatial import distance
from numpy import angle
import math
from labjack import u3
import numpy as np
import time






# se giran todos los circulos 5 grados en sentido de las agujas del reloj por lo que se les restan 5 grados
angleDist = -15

# el tiempo en segundos durante el que se escribe un valor en DAC1_REGISTER durante el cue 

tiempoEsperaU3Cue = 0.2

timeInSecondsOfCueShown = 0.3

# opacidades de solar_cell100_reg , solar_cell75_reg , solar_cell50_reg , solar_cell100_nreg , solar_cell75_nreg y solar_cell50_nreg


# valor entre 0 y 1 
# indica la inclinacion del joystick para poder tener movimiento (sensibilidad)
inclinacionJoy = 0.85



opacidades = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 0.9, 1]


intensityLabjackFix = 0.1

intensitylabJackUniform = [0.45, 0.40, 0.35]

intensitylabJackNonUniform = [0.85, 0.80,0.75]

#define the number of pieces
numCircles = 5;



intensityU3TargetUniform =[1.3,1.25 ,1.2]
intensityU3TargetNoUniform = [1.7, 1.65 , 1.6]





# la aceleracion que se usa mas abajo para mover el Joystick

miu3 = u3.U3()
miu3.getCalibrationData

DAC1_REGISTER = 5002
miu3.writeRegister(DAC1_REGISTER,0)

DAC0_REGISTER = 5000
miu3.writeRegister(DAC0_REGISTER, 0)


# otros valores de otros screens
cuetime = 1.1
targetOnSet = 0.75
interstimulusInterval = 3.5






#define the angles of the pieces
lista = [round(360*random.random(),4) for i in xrange(numCircles)]


x = [0] * numCircles
y = [0] * numCircles



# define x and y as the movement distance of the pieces

for i in range(len(lista)):
    x[i]= np.cos(math.radians(lista[i]))*2
    y[i]=np.sin(math.radians(lista[i]))*2



#define the movement vector of every circle
listMoves = [0] * 10
elemental = 0
while elemental < 10 :
    listMoves[elemental] = elemental*0.3
    elemental = elemental + 1


clock = core.Clock()
#declare cont for every movement piece


listaIntensities = np.linspace(0.04, 2.0, num=181)



globalTime = core.Clock()


listaCues = ['U','NU']
lc = funcionesExtras.darPrimeraLista(listaCues, 6)

lAux = [random.choice(lc),random.choice(lc)]

listaCFin = []



listNone = list(csv.reader(open('conditionsNone.csv',"rU")))[1:]
listMedium = list(csv.reader(open('conditionsMedium.csv',"rU")))[1:]
listHigh = list(csv.reader(open('conditionsHigh.csv',"rU")))[1:]



listNone = listNone *3
listMedium = listMedium * 2
listHigh = listHigh *3


lista = listNone + listMedium + listHigh

listaFinal = []

#print lista

total = 4
heTerminado = total
twoLast = lAux
while heTerminado > 0 :
    
    #random.shuffle(lista)
    lCompleted, twoLast = funcionesExtras.darListaCompleta(lc, twoLast, 6)
    #print('lCompleted', lCompleted)
    lFinal = funcionesExtras.crearlistaFinal (lista, lCompleted)
    #print('lista : ', lista,'---')
    #print(lFinal)
    #print('bloque :', 5 - heTerminado)
    lista2 = [lista[i] + [lCompleted[i]] for i in range(len(lista))]
    listaFinal = listaFinal + lFinal
    heTerminado = heTerminado - 1
    



bloque1 = listaFinal[0 : 72]
bloque2 = listaFinal[72 : 144]
bloque3 = listaFinal[144 : 216]
bloque4 = listaFinal[216 : 288]

#print (bloque1)
#print (' ::: -- :::')
#
#print (bloque2)
#print (' ::: -- :::')
#
#print (bloque3)
#print (' ::: -- :::')
#
#print (bloque4)
#print (' ::: -- :::')
listatypeTrial = [0,'U','NU']



info = {'Session': 1, 'Subject':'', 'gender':['male','female']}
dialog = gui.DlgFromDict(dictionary= info, title='MPRR with Joystick')


if dialog.OK:
    infoUser = dialog.data
    #Subject's data is saved in infoUser and are ready to print them on each file
else:
    print('user cancelled')
    core.quit()
    

#Date is saved on each trial

info['dateStr'] = data.getDateStr()



#We create a screen on which our program will run
#We also set up the internal clock meanwhile the remaining functions are ready to use

mywin = visual.Window([1366,768], fullscr = False, monitor='testMonitor', color='black',units='deg', allowGUI = False)
respClock = core.Clock()


joystick.backend='pyglet'
nJoysticks=joystick.getNumJoysticks()

if nJoysticks>0:
    joy = joystick.Joystick(0)
else:
    print("You don't have a joystick connected!?")
    mywin.close()
    core.quit()
    



solar_cellFixation = visual.Circle(mywin, radius=0.5, edges=30, fillColor = 'white', opacity = opacidades[0], pos=[-14,7.5], interpolate= True)

solar_cellHigh_reg = visual.Circle(mywin, radius=0.5, edges=30, fillColor = 'white', opacity = opacidades[5], pos=[-14,7.5], interpolate= True)
solar_cellHigh_nreg = visual.Circle(mywin, radius=0.5, edges=30, fillColor = 'white', opacity = opacidades[8], pos=[-14,7.5], interpolate= True)


solar_cellCueRegular = visual.Circle(mywin, radius=0.5, edges=30, fillColor = 'white', opacity = opacidades[1], pos=[-14,7.5], interpolate= True)
solar_cellCueNoRegular = visual.Circle(mywin, radius=0.5, edges=30, fillColor = 'white', opacity = opacidades[2], pos=[-14,7.5], interpolate= True)



solar_cellMedium_reg = visual.Circle(mywin, radius=0.5, edges=30, fillColor = 'white', opacity = opacidades[4], pos=[-14,7.5], interpolate= True)
solar_cellMedium_nreg = visual.Circle(mywin, radius=0.5, edges=30, fillColor = 'white', opacity = opacidades[7], pos=[-14,7.5], interpolate= True)

solar_cellNoCert_reg = visual.Circle(mywin, radius=0.5, edges=30, fillColor = 'white', opacity = opacidades[3], pos=[-14,7.5], interpolate= True)
solar_cellNoCert_nreg = visual.Circle(mywin, radius=0.5, edges=30, fillColor = 'white', opacity = opacidades[6], pos=[-14,7.5], interpolate= True)

#solar_celltarget = visual.Circle(mywin, radius=0.5, edges=30, lineColor = 'white',fillColor = 'white', opacity = opacidades[7], pos=[-14,7.5], interpolate= True)
#preparamos la celula del punto de fijacion, de color blanco, y la cruz del punto de fijacion
black_solarCell = visual.Circle(mywin, radius= 0.6, edges=30, lineColor = 'black',fillColor = 'black', pos=[-14,7.5], interpolate= True) 


cellsreg = [solar_cellHigh_reg,solar_cellMedium_reg,solar_cellNoCert_reg]
cellsNreg = [solar_cellHigh_nreg,solar_cellMedium_nreg,solar_cellNoCert_nreg]


#declaramos el resto de items, los circulos superiores de espera, y el rojo inferior

redJoystickButton = visual.Circle(mywin, radius=0.3, edges=30, lineColor = 'red', fillColor = 'red', pos=(0, 0), interpolate=True)

CueBlackCircle = visual.Circle(mywin, radius=0.5, edges=30, lineColor = 'white', fillColor = 'black', pos=(0, 0), interpolate=True)
CueBlackCircle = visual.Circle(mywin, radius=0.5, edges=30, lineColor = 'white', fillColor = 'black', pos=(0, 0), interpolate=True)
CueBlackCircle = visual.Circle(mywin, radius=0.5, edges=30, lineColor = 'white', fillColor = 'black', pos=(0, 0), interpolate=True)

# no le ponemos direccion, antes de pintarlo se la pondremos, pero eso es mas adelante
targetWhiteCircle = visual.Circle(mywin, radius=0.5, edges=30,lineColor = 'white', fillColor = 'white', interpolate=True)

targetFinal = visual.Circle(mywin, radius=0.5, edges=30,lineColor = 'white', fillColor = 'white', interpolate=True)




valor = int(info['Subject'])
if valor < 10 : 

    elemento = '0' + str(info['Subject'])
else :
    elemento = str(info['Subject'])
    
    
filename = 'data/'+ 'Sub' + elemento +'_Psydat'

exp = data.ExperimentHandler(name='MprrSubject',
                version='0.1',
                extraInfo=info,
                runtimeInfo=None,
                originPath=None,
                savePickle=True,
                saveWideText=True,
                dataFileName=filename)
               


numeroReps = 45

training = data.TrialHandler(trialList=[], nReps=numeroReps, name='train', method='sequential')

#unimos con nuestro experimento los trials, de manera secuencial (definido arriba en el method), en forma de bucle
exp.addLoop(training)


voyPor = 0
pausa = 0

dummy = time.clock()
#para cada vez que hemos escrito en nuestro numero de trials
for trial in training:
    
    while pausa == 1:
        text = 'Paused, press p to Continue'
        stimP = visual.TextStim(mywin, text)
        stimP.draw()
        mywin.flip()
        if 'p' in event.getKeys():
            pausa = 0
        event.clearEvents()
        
        

    if voyPor % 72 == 0 :
        
        bloque = str((voyPor // 72) + 1)
        
        texto = 'Block  ' + bloque + ' is going to start, press space to continue'
        continuar = 0
        
        reloj2 = core.Clock()
        while continuar == 0  :
            
            if reloj2.getTime() < 0.3 :
                miu3.writeRegister(DAC0_REGISTER, 0.04)
            elif reloj2.getTime() > 0.3 and reloj2.getTime() < 0.6 :
                miu3.writeRegister(DAC0_REGISTER, 1)
            elif reloj2.getTime() > 0.6 and reloj2.getTime() < 0.9 :
                miu3.writeRegister(DAC0_REGISTER, 2)
            elif reloj2.getTime() > 0.9 :  
                miu3.writeRegister(DAC0_REGISTER, 0)
                stim = visual.TextStim(mywin, texto)
                stim.draw()
                mywin.flip()
                if 'space' in event.getKeys():
                    continuar = 1
                event.clearEvents()
        

        
        
    listatypeTrial = funcionesExtras.testPseudoRandom(listatypeTrial)
    
    typeTrial = listatypeTrial[0]
    elem = listaFinal[voyPor]
    
    typeTrial = elem[3]
    
    if typeTrial == 'U' :
        myList = intensitylabJackUniform
        myCells = cellsreg
        solarCue = solar_cellCueNoRegular
        listU3Target = intensityU3TargetUniform
    else :
        myList = intensitylabJackNonUniform
        myCells = cellsNreg
        solarCue = solar_cellCueRegular
        listU3Target = intensityU3TargetNoUniform
    
    
    if elem[0] == 'H' :
        valU3 = myList[0]
        cell = myCells[0]
        u3TargetVolts = listU3Target[0]
    if elem[0] == 'M' :
        valU3 = myList[1]
        cell = myCells[1]
        u3TargetVolts = listU3Target[1]
    if elem[0] == 'N' :
        valU3 = myList[2]
        cell = myCells[2]
        u3TargetVolts = listU3Target[2]
        
    training.addData('Labjack_U3',valU3)
    training.addData('cellIntensity',cell.opacity)
    #print('tipo de trial : ',typeTrial)
    listaTargets = funcionesExtras.obtenerposicionesTarget(elem,angleDist)
    training.addData('typeTrial',typeTrial)
    training.addData('Unceartinty type', elem[0])
    training.addData('sector', elem[1])
    training.addData('position', elem[2])
    
    
    #declaramos el SOA, un intervalo de tiempo entre 1 y 2 segundos que usaremos para la pantalla de fixation
    timeFixation = random.uniform(1,2)
    
    # redondeamos el SOA a un solo decimal, y colocamos el valor en el fichero de salida
    soa=round(timeFixation,1)
    training.addData('soa',soa)
    
    redJoystickButton.setPos((0, 0))
    respClock = core.Clock()
    
        # soa esta entre 1 y 2
    
    while respClock.getTime() < soa:
        if respClock.getTime() < tiempoEsperaU3Cue :
            miu3.writeRegister(DAC1_REGISTER, intensityLabjackFix)
        else :
            miu3.writeRegister(DAC1_REGISTER, 0)
        
        if 'q' in event.getKeys():
            core.quit()
        solar_cellFixation.draw()
        targetWhiteCircle.draw()
        redJoystickButton.draw()
        #timeInSecondsOfCueShown es el tiempo de espera hasta ocultar el solarCell
        
        if respClock.getTime()> timeInSecondsOfCueShown:
            black_solarCell.draw()
        mywin.flip()
        
    #print (elem)
    #second target 
    
    
    
    
    respClock = core.Clock()
    while respClock.getTime() < cuetime:
        
        if respClock.getTime() > 0.4 and respClock.getTime() < 0.6:
            miu3.writeRegister(DAC1_REGISTER, valU3)
        else :
            miu3.writeRegister(DAC1_REGISTER, 0)
        solarCue.draw()
        if respClock.getTime() > timeInSecondsOfCueShown:
            black_solarCell.draw()
        for i in listaTargets:
            CueBlackCircle.pos = i
            CueBlackCircle.draw()
        targetWhiteCircle.draw()
        redJoystickButton.draw()
        mywin.flip()
        
    
    isMax = 0
    
    nuevoXMax = 0.0
    nuevoYMax = 0.0
    
    reactionTime = 0
    respClock = core.Clock()
    #print(reactionTime)
    
    hayMovimiento = 0
    
    angleList = [0,0,0]
    
    while respClock.getTime() < targetOnSet and hayMovimiento == 0:
        
        
        if respClock.getTime() < tiempoEsperaU3Cue :
            miu3.writeRegister(DAC1_REGISTER, u3TargetVolts)
        else :
            miu3.writeRegister(DAC1_REGISTER, 0)
        
        cell.draw()
        if respClock.getTime() > timeInSecondsOfCueShown:
            black_solarCell.draw()
        
        xx = joy.getX()
        yy = joy.getY()
        
        
        if reactionTime == 0 :
            if abs(xx) > 0.01 or abs(yy) > 0.01 :
                
                reactionTime = respClock.getTime()
                
            
        
        
        nuevoX = 1* xx  # si avanzamos a la derecha, se incrementa el vector direccion X
        nuevoY = - 1* yy # el eje Y esta invertido en los joystick, si vamos hacia arriba, se decrementa el vector direccion Y
        
        distancia = distance.euclidean([nuevoX,nuevoY],[0,0])
        
        
        
        
        
        
        for i in listaTargets:
            CueBlackCircle.pos = i
            CueBlackCircle.draw()
        if elem[0] == 'N':
            targetFinal.pos = listaTargets[0]
            itemtoAddFinal = listaTargets[0]
        else :
            targetFinal.pos = listaTargets[int(elem[2])]
            itemtoAddFinal = listaTargets[int(elem[2])]
        targetFinal.draw()
        
        
        redJoystickButton.draw()
        
        
        if distancia > 0.3 and distancia < 0.5:
            theta = angle( nuevoX+nuevoY*1j )
            angleList[0] = theta
        
        if distancia > 0.5 and distancia < 0.85:
            theta = angle( nuevoX+nuevoY*1j )
            angleList[1] = theta
        
        
        if distancia > inclinacionJoy :
            theta = angle( nuevoX+nuevoY*1j )
            angleList[2] = theta
            
            
            thetaMax = min(angleList)
            if thetaMax >= 0 :
                thetaMax = max(angleList)
            nuevoXMax = math.cos(thetaMax)*5.00
            nuevoYMax = math.sin(thetaMax)*5.00
            
            redJoystickButton.setPos((nuevoXMax, nuevoYMax))
            redJoystickButton.draw()
            hayMovimiento = 1
        
        mywin.flip()
    
    if reactionTime == 0 :
        reactionTime = 0.750
    training.addData('reactionTime',round(reactionTime,3))
    respClock = core.Clock()
    
    joyFinalPos = (round(nuevoXMax,3), round(nuevoYMax,3))
    itemtoAddFinal = (round(itemtoAddFinal[0],3), round(itemtoAddFinal[1],3))
    training.addData('joyFinalPos',joyFinalPos)
    training.addData('TargetFinalPosition',itemtoAddFinal)
    
    ang = funcionesExtras.angleInRads(itemtoAddFinal, joyFinalPos)
    angD = funcionesExtras.angleInDegrees(itemtoAddFinal, joyFinalPos)
    
    training.addData('angleInRads',ang)
    training.addData('angleInDegrees',angD)
    
    
    
    #aqui debemos escribir ang en la u3 que vale 0 si no se ha movido joy y 0.05 a 3.14 si se tiene algo de error
    
    if angD == 404:
        valorAmandarP0 = 0
    else :
        valorAmandarP0 = round(listaIntensities[int(round(angD,0))],3)
    
    cont = 0
    respClock= core.Clock()
    
    while respClock.getTime() < interstimulusInterval :
        if hayMovimiento and angD < 5 :
            while cont < 10:
                for item in range(numCircles):
                    circle = visual.Circle(mywin, radius=0.20, edges=10, fillColor = 'white', pos=[itemtoAddFinal[0] + x[item]*listMoves[cont],itemtoAddFinal[1] + y[item]*listMoves[cont]], interpolate= True)
                    circle.draw()
                if respClock.getTime() < tiempoEsperaU3Cue :
                    miu3.writeRegister(DAC0_REGISTER, valorAmandarP0)
                else :
                    miu3.writeRegister(DAC0_REGISTER, 0)
                cont = cont+1
                mywin.flip()
        else : 
            if respClock.getTime() < tiempoEsperaU3Cue :
                miu3.writeRegister(DAC0_REGISTER, valorAmandarP0)
            else :
                miu3.writeRegister(DAC0_REGISTER, 0)
        
        if 'p' in event.getKeys():
            pausa = 1
            event.clearEvents()
        if pausa == 1:
            tr = str(voyPor + 1 )
            texto = 'trial  ' + tr + ' will be paused'
            stimP = visual.TextStim(mywin, texto)
            stimP.draw()
            mywin.flip()
        if 'q' in event.getKeys():
            core.quit()
        if hayMovimiento and angD < 5 :
            if cont == 10:
                mywin.flip()
                lista = [round(360*random.random(),4) for i in xrange(numCircles)]
                x = [0] * numCircles
                y = [0] * numCircles
                for i in range(len(lista)):
                    x[i]= np.cos(math.radians(lista[i]))*2
                    y[i]= np.sin(math.radians(lista[i]))*2
                listMoves = [0] * 10
                elemental = 0
                while elemental < 10 :
                    listMoves[elemental] = elemental*0.3
                    elemental = elemental + 1
                cont = cont + 1
            
            
        mywin.flip()
    voyPor = voyPor + 1
    training.addData('globalTime', round(time.clock(),4))
    event.clearEvents()
    exp.nextEntry()

# una vez terminado, imprimimos por la pantalla del psychopy nuestras variables de salida
for e in exp.entries:
    print(e)
    
print("Done. We will save data to a csv file")
