import serial
import time

def turnOn(com):
    COMName = 'COM' + str(com)
    ser = serial.Serial(port=COMName, baudrate=9600, stopbits=1)
    dataToSend = ':OUTPut:STATe CH1,ON\n'.encode()
    ser.write(dataToSend)
    ser.close()

def turnOff(com):
    COMName = 'COM' + str(com)
    ser = serial.Serial(port=COMName, baudrate=9600, stopbits=1)
    dataToSend = ':OUTPut:STATe CH1,OFF\n'.encode()
    ser.write(dataToSend)
    ser.close()
    
    
while(True):
    turnOn(4)
    time.sleep(1.7)
    turnOff(4)
    time.sleep(0.2)
    
