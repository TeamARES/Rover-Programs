import socket
import serial
import json
import time
import threading

class Propulsion:
    def __init__(self):
        self.motorspeed1 = 0
        self.motorspeed2 = 0
        self.s = socket.socket()
        self.host = ""
        self.port = 9999
        while True:
            try:  
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
        self.ser.close()

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
                self.propulsion(dataFromBase, index1)
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
        data.update({"fl" : str(self.motorspeed2)})
        data.update({"fr" : str(self.motorspeed1)})
        data.update({"bl" : str(self.motorspeed2)})
        data.update({"br" : str(self.motorspeed1)})
        data.update({"kill": "0"})
        data.update({"req": "1"})
        return data

    def propulsion(self, dataFromBase, index1):
            
        index2 = dataFromBase.index(',',index1 + 1)
            
        motorspeed = dataFromBase[index1 + 1 : index2]
        a = self.strToInt(motorspeed)
        self.motorspeed1 = a
        self.motorspeed2 = a
        
        motorspeed = dataFromBase[index2 + 1 :]
            
        print(motorspeed)
        b = self.strToInt(motorspeed)
            
        self.motorspeed1 -= b
        self.motorspeed2 += b
        if (self.motorspeed1 > 100):
            self.motorspeed1 = 100
        elif (self.motorspeed1 < -100):
            self.motorspeed1 = -100
            
        if (self.motorspeed2 > 100):
            self.motorspeed2 = 100
        elif (self.motorspeed2 < -100):
            self.motorspeed2 = -100
        
        print('motorspeed1',self.motorspeed1)
        print('motorspeed2',self.motorspeed2)
            

        data = json.dumps(self.getData())
        #self.sendtoard(data)


