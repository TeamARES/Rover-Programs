import socket
import serial
import json
import time
import threading

class Robotic_Arm:
    def __init__(self):
        self.baseMotorSpeed = 0
        self.baseActuator = 0
        self.armActuator = 0
        self.clawPitch = 0
        self.clawRoll= 0
        self.clawOpenClose = 0
        self.s = socket.socket()
        self.host = ""
        self.port = 9998
        while True:
            try:  
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                print("Binding the Port: " + str(self.port))
                self.s.bind((self.host, self.port))
                self.s.listen(5)
                break
            except socket.error as msg:
                print("Socket Binding error" + str(msg) + "\n" + "Retrying...")

        self.conn, self.address = self.s.accept()
        print("Connection has been established! |" + " IP " + self.address[0] + " | Port" + str(self.address[1]))
        '''
        self.ser  = serial.Serial("COM3", baudrate= 9600, 
               timeout=2.5, 
               parity=serial.PARITY_NONE, 
               bytesize=serial.EIGHTBITS, 
               stopbits=serial.STOPBITS_ONE
            )
        '''
        self.read_commands()

    def Stop(self):
        self.send_commands('Stopping!')
        self.s.close()
        self.conn.close()
        #self.ser.close()

    def read_commands(self):
        while True:
            dataFromBase = str(self.conn.recv(1024),"utf-8")
            print("\n Received Data = " + dataFromBase)
            if(len(dataFromBase) > 3):
                if dataFromBase == "stop":
                    self.Stop()
                    break
                self.send_commands('YES')
                index1 = dataFromBase.index(',')
                modeStr = dataFromBase[0:index1]
                self.roboticArm(dataFromBase, index1)
            else:
                self.send_commands('NO')

    def send_commands(self, data):
        self.conn.send(str.encode(data))

    def strToInt(self, string):
        if(len(string) == 0):
            return 0;
        x = 0
        flag = 1
        if(string[0] == '-'):
            flag = -1
            
        for i in range (0,len(string)):
                        if string[i].isdigit():
                            x += int(string[i]) * 10 ** int(len(string) - i - 1)
        return flag * x
    '''
    def sendtoard(self, data):
        return
        print(data)
        if self.ser.isOpen():
            self.ser.write(data.encode('ascii'))
            self.ser.flush()
            try:
                incoming = self.ser.readline().decode("utf-8")
                print(incoming)
            except Exception as e:
                print (e)
                pass
        else:
            print ("opening error")
    '''

    def getData(self):
        data = dict()
        motors = list()
        motors.append(str(self.baseMotorSpeed))
        motors.append(str(self.baseActuator))
        motors.append(str(self.armActuator))
        motors.append(str(self.clawPitch))
        motors.append(str(self.clawRoll))
        motors.append(str(self.clawOpenClose))
        motors.append("0")
        motors.append("0")
        motors.append("0")
        data.update({"m" : motors})
        data.update({"kill" : "0"})
        data.update({"req" : "1"})
        return data

    def printRoboticArmVariables(self):
        print(self.baseMotorSpeed, self.baseActuator, self.armActuator, self.clawPitch, self.clawRoll, self.clawOpenClose)

    def roboticArm(self,dataFromBase, index1):
        
        index2 = dataFromBase.index(',',index1+1)
        StrbaseMotorSpeed = dataFromBase[index1+1:index2]
        self.baseMotorSpeed = self.strToInt(StrbaseMotorSpeed);
        
        index3 = dataFromBase.index(',',index2+1)
        StrbaseActuator = dataFromBase[index2+1:index3]
        self.baseActuator = self.strToInt(StrbaseActuator);

        index4 = dataFromBase.index(',',index3+1)
        StrarmActuator = dataFromBase[index3+1:index4]
        self.armActuator = self.strToInt(StrarmActuator);
        
        index5 = dataFromBase.index(',',index4+1)
        StrclawPitch = dataFromBase[index4+1:index5]
        self.clawPitch = self.strToInt(StrclawPitch);
        
        index6 = dataFromBase.index(',',index5+1)
        StrclawRoll = dataFromBase[index5+1:index6]
        self.clawRoll = self.strToInt(StrclawRoll);
        
        index7 = dataFromBase.index(',',index6+1)
        StrclawOpenClose = dataFromBase[index6+1:index7]
        self.clawOpenClose = self.strToInt(StrclawOpenClose);
        
        self.printRoboticArmVariables();
        data = json.dumps(self.getData())
        # self.sendtoard(data)

