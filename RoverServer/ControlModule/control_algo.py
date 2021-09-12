import socket
import serial
import json
import time
import threading

class Control:
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0
        self.fan1 = 0
        self.fan2 = 0
        self.kill = 0
        self.s = socket.socket()
        self.host = ""
        self.port = 9996
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
                self.control(dataFromBase, index1)
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
        data.update({"red" : str(self.r)})
        data.update({"green" : str(self.g)})
        data.update({"blue" : str(self.b)})
        data.update({"fan1" : str(self.fan1)})
        data.update({"fan2": str(self.fan2)})
        data.update({"relay": str(self.kill)})
        data.update({"req": "1"})
        return data

    def control(self, dataFromBase, index1):
            
        index2 = dataFromBase.index(',',index1 + 1)
            
        r = dataFromBase[index1 + 1 : index2]
        self.r = self.strToInt(r)
        
        index3 = dataFromBase.index(',', index2+1)
        g = dataFromBase[index2 + 1 : index3]
        self.g = self.strToInt(g)

        index4 = dataFromBase.index(',', index3+1)
        b = dataFromBase[index3+1 : index4]
        self.b = self.strToInt(b)

        index5 = dataFromBase.index(',', index4+1)
        fan1 = dataFromBase[index4+1 : index5]
        self.fan1 = self.strToInt(fan1)

        index6 = dataFromBase.index(',', index5+1)
        fan2 = dataFromBase[index5+1 : index6]
        self.fan2 = self.strToInt(fan2)

        kill = dataFromBase[index6+1 :]
        self.kill = self.strToInt(kill)
            
        data = json.dumps(self.getData())
        print(data)
        #self.sendtoard(data)


