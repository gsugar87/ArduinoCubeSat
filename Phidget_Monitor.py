import sys
import time
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetException
from Phidgets.Devices.Bridge import Bridge, BridgeGain
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, TemperatureChangeEventArgs
from Phidgets.Devices.TemperatureSensor import TemperatureSensor, ThermocoupleType

#create data variables
data_to_be_sent_bridge = []
times_to_be_sent_bridge = []
data_to_be_sent_temperature = []
times_to_be_sent_temperature = []


# #Information Display Function
# def displayDeviceInfo():
#     print("|------------|----------------------------------|--------------|------------|")
#     print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
#     print("|------------|----------------------------------|--------------|------------|")
#     print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (bridge.isAttached(), bridge.getDeviceName(), bridge.getSerialNum(), bridge.getDeviceVersion()))
#     print("|------------|----------------------------------|--------------|------------|")
#     print("Number of bridge inputs: %i" % (bridge.getInputCount()))
#     print("Data Rate Max: %d" % (bridge.getDataRateMax()))
#     print("Data Rate Min: %d" % (bridge.getDataRateMin()))
#     print("Input Value Max: %d" % (bridge.getBridgeMax(0)))
#     print("Input Value Min: %d" % (bridge.getBridgeMin(0)))

#Event Handler Callback Functions
def BridgeAttached(e):
    attached = e.device
    print("Bridge %i Attached!" % (attached.getSerialNum()))

def BridgeDetached(e):
    detached = e.device
    print("Bridge %i Detached!" % (detached.getSerialNum()))

def BridgeError(e):
    try:
        source = e.device
        print("Bridge %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

def BridgeData(e):
    global data_to_be_sent_bridge
    global times_to_be_sent_bridge
#     source = e.device
    timeStamp = time.time()
    data_to_be_sent_bridge.append(e.value)
    times_to_be_sent_bridge.append(timeStamp)
#     print("Bridge %i: Input %i: %f Time %f" % (source.getSerialNum(), e.index, e.value, timeStamp))


class PhidgetBridge():
    def __init__(self):
        self.bridge = Bridge()
        self.bridge.setOnAttachHandler(BridgeAttached)
        self.bridge.setOnDetachHandler(BridgeDetached)
        self.bridge.setOnErrorhandler(BridgeError)
        self.bridge.setOnBridgeDataHandler(BridgeData)
#         self.data_to_be_sent_bridge = []
#         self.times_to_be_sent_bridge = []
        
    def open(self,waitTimeMS):
        self.bridge.openPhidget()
        try:
            self.bridge.waitForAttach(waitTimeMS)
            time.sleep(0.2)
            self.bridge.setDataRate(8)
            time.sleep(0.2)
            self.bridge.setGain(0, BridgeGain.PHIDGET_BRIDGE_GAIN_8)
            time.sleep(0.2)
            self.bridge.setEnabled(0, True)
            time.sleep(0.2)
            return 1
        except:
            return -1
    
#     def BridgeData(self,e):
#         timeStamp = time.time()
#         self.data_to_be_sent_bridge.append(e.value)
#         self.times_to_be_sent_bridge.append(timeStamp)
        
    def getData(self):
        global data_to_be_sent_bridge
        global times_to_be_sent_bridge
        #return the data and times and update the lists
        data_to_return = [data_to_be_sent_bridge,times_to_be_sent_bridge]
        data_to_be_sent_bridge = []
        times_to_be_sent_bridge = []
        return data_to_return
    
    def close(self):
        self.bridge.setEnabled(0,False)
        time.sleep(2)
        self.bridge.closePhidget()
#******************* END OF BRIDGE CODE*******************

#********************START OF TEMPERATURE SENSOR CODE *****************
#Event Handler Callback Functions
def TemperatureSensorAttached(e):
    attached = e.device
    print("TemperatureSensor %i Attached!" % (attached.getSerialNum()))

def TemperatureSensorDetached(e):
    detached = e.device
    print("TemperatureSensor %i Detached!" % (detached.getSerialNum()))

def TemperatureSensorError(e):
    try:
        source = e.device
        if source.isAttached():
            print("TemperatureSensor %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))        

def TemperatureSensorTemperatureChanged(e):
    global data_to_be_sent_temperature
    global times_to_be_sent_temperature
#     source = e.device
    timeStamp = time.time()
#     data_to_be_sent_temperature.append(e.value)
#     times_to_be_sent_temperature.append(timeStamp)
    
#     try:
#         ambient = temperatureSensor.getAmbientTemperature()
#     except PhidgetException as e:
#         print("Phidget Exception %i: %s" % (e.code, e.details))
#         ambient = 0.00
#     
#     source = e.device
#     print("TemperatureSensor %i: Ambient Temp: %f -- Thermocouple %i temperature: %f -- Potential: %f" % (source.getSerialNum(), ambient, e.index, e.temperature, e.potential))

class PhidgetTemp():
    def __init__(self):
        self.temperatureSensor = TemperatureSensor()
        self.temperatureSensor.setOnAttachHandler(TemperatureSensorAttached)
        self.temperatureSensor.setOnDetachHandler(TemperatureSensorDetached)
        self.temperatureSensor.setOnErrorhandler(TemperatureSensorError)
        self.temperatureSensor.setOnTemperatureChangeHandler(TemperatureSensorTemperatureChanged)
#         self.data_to_be_sent_bridge = []
#         self.times_to_be_sent_bridge = []
        
    def open(self,waitTimeMS):
        self.temperatureSensor.openPhidget()
        try:
            self.temperatureSensor.waitForAttach(waitTimeMS)
            time.sleep(0.5)
            self.temperatureSensor.setThermocoupleType(0, ThermocoupleType.PHIDGET_TEMPERATURE_SENSOR_K_TYPE)
            self.temperatureSensor.setThermocoupleType(1, ThermocoupleType.PHIDGET_TEMPERATURE_SENSOR_K_TYPE)
            self.temperatureSensor.setThermocoupleType(2, ThermocoupleType.PHIDGET_TEMPERATURE_SENSOR_K_TYPE)
            self.temperatureSensor.setThermocoupleType(3, ThermocoupleType.PHIDGET_TEMPERATURE_SENSOR_K_TYPE)
            self.temperatureSensor.setTemperatureChangeTrigger(0, 0.1)
#             self.temperatureSensor.setTemperatureChangeTrigger(1, 0.1)
#             self.temperatureSensor.setTemperatureChangeTrigger(2, 0.1)
#             self.temperatureSensor.setTemperatureChangeTrigger(3, 0.1)
            return 1
        except:
            return -1
    
#     def BridgeData(self,e):
#         timeStamp = time.time()
#         self.data_to_be_sent_bridge.append(e.value)
#         self.times_to_be_sent_bridge.append(timeStamp)
        
    def getData(self):
        #return the data and times and update the lists
        thermocouple0 = self.temperatureSensor.getTemperature(0)
        thermocouple1 = self.temperatureSensor.getTemperature(1)
        thermocouple2 = self.temperatureSensor.getTemperature(2)
        thermocouple3 = self.temperatureSensor.getTemperature(3)
        timeStamp = time.time()
        data_to_return = [thermocouple0,thermocouple1,thermocouple2,thermocouple3,timeStamp]
        data_to_be_sent_temperature = []
        times_to_be_sent_temperature = []
        return data_to_return
    
    def close(self):
        self.temperatureSensor.setEnabled(0,False)
        time.sleep(2)
        self.temperatureSensor.closePhidget()

