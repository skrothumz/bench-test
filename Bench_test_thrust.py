#! /usr/bin/python

__author__="Nicolas Marchand"
__date__ ="16-Sep-2016"

#Basic imports
import sys
import csv
from time import sleep
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.Bridge import Bridge, BridgeGain
from Phidgets.Phidget import PhidgetLogLevel

#---------------------------Init List--------------------------
#Titre = ["List1", "List2"]
Titre = ["List1"]
nbval = 10
List10 = [0] * nbval
#List20 = [0] * nbval
List1 = []
#List2 = []
iter = 0


#Create an accelerometer object
try:
    bridge = Bridge()
except RuntimeError as e:
    print("Runtime Exception: %s" % e.details)
    print("Exiting....")
    exit(1)

#Event Handler Callback Functions
def BridgeError(e):
    try:
        source = e.device
        print("Bridge %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

#---------------------------Add DATA--------------------------
def Moyenne(List):
    for val in List:
        moy += val
    moy /= nbval
    return moy

def BridgeData():
    if bridge.getEnabled(0) and bridge.getEnabled(1):
        List10[iter % 10] = getBridgeValue(bridge,0) #* FORMULE
        #List20[iter % 10] = getBridgeValue(bridge,1) #* FORMULE
        iter += 1

        if iter > nbval:
            List1.append(Moyenne(List10))
            #List2.append(Moyenne(list20))

#Main Program Code
try:
	#logging example, uncomment to generate a log file
    #bridge.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, "phidgetlog.log")
	
    bridge.setOnErrorhandler(BridgeError)
    bridge.setOnBridgeDataHandler(BridgeData)

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

try:
    bridge.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

#Vérifier si le Bridge est branché
if bridge.isAttached() is False:
    print("Pont débranché")
    chr = sys.stdin.read(1)
    try:
        bridge.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)

try:
    #Set data rate to 8ms
    bridge.setDataRate(16)

    #Set Gain to 8
    bridge.setGain(0, BridgeGain.PHIDGET_BRIDGE_GAIN_8)
    #bridge.setGain(1, BridgeGain.PHIDGET_BRIDGE_GAIN_8)

#-----------------Début de lecture DATA (Thread)----------------
    #Enable the Bridge input for reading data
    bridge.setEnabled(0, True)
    #bridge.setEnabled(1, True)

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        bridge.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)

#---------------------Script d'acc du moteur--------------------



#-----------------------Condition d'arrêt-----------------------

chr = sys.stdin.read(1)

print("Closing...")

try:
    #Disable the Bridge input for reading data
    bridge.setEnabled(0, False)
    #bridge.setEnabled(1, False)

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        bridge.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)

try:
    bridge.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)


#-----------------Copie des données (CSV FILE)------------------

with open("PATHFILE/Data.csv", "wb") as f
    writer = csv.writer(f)
    #writer.writerows([Titre, List1, List2])
	writer.writerows([Titre, List1])

#---------------------------Fin Script--------------------------
exit(0)