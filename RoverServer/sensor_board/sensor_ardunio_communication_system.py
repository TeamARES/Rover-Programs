""" 
Code writtebn by Harshit Batra(9-sep-2021) 
as part Ares pegusus 1.0 rover Science Team 

Reads  serial communication with the transmitter Arduino 
at specified port and baudrate 

the following is type of data recivied from various sensors 
    1. Pressure (BMP180) (graph) unit pasacal 
    2. temprature (BMP180) (graph) unit celsius 
    3. luminosity (BH1750) (graph) unit lumins 
    4. Humidity (DHT11) (graph) percentage 
    5. temerature (DHT11) (graph) unit celsius
    4. Methane (MQ4) (graph) unit ppm 
    5. ammoina (MQ135) (graph) unit ppm 
    6. Soil Moisture (capactive soil sensor ) not confimed 

Dependencies:
	pip install pyserial

"""
import serial 
import time 
import math
import socket
import argparse

class Sensor_data :
    def __init__(self, port, baudrate, is_server_running):
        self.arduino = serial.Serial(port=port, baudrate=baudrate)
        # Initialising all the variables
        self.pressure = 0
        self.altitude = 0
        self.temperature_bmp = 0
        self.luminosity = 0
        self.humidity = 0
        self.temperature_dht = 0
        self.methane = 0
        self.ammonia = 0
        self.moisture = 0
        self.server = is_server_running
        # Making socket connection
        if self.server == True:
            self.host = '192.168.29.139'
            self.port = 9995
            self.s = socket.socket()
            self.s.connect((self.host, self.port))

    def read (self) :
        """ 
        reads the data from serial port and converts into Unicode
        """
        Readstring = self.arduino.readline()
        decoded = Readstring.decode() #byte string converted to Unicode 
        data= decoded.split()
        return data
     
    def sendDataToBase():
        if self.server == False:
            return
        stringData = '0,' + str(self.pressure) + ',' + str(self.altitude) + ',' + str(self.temperature_bmp) + ',' + str(self.luminosity) + ',' + str(self.humidity) + ',' + str(self.temperature_dht) + ',' + str(self.methane) + ',' + str(self.ammonia) + ',' + str(self.moisture)
        # Sendng this data from socket to the base station
        self.s.send(str.encode(stringData))
        # After sending we check if it was recieved or not
        checkDataTranfer = self.s.recv(1024)
        print(checkDataTranfer)

    def printData(self):
        print("pressure: " + self.pressure)
        print("altitude: " + self.altitude)
        print("temperature_bmp: " + self.temperature_bmp)
        print("luminosity: " + self.luminosity)
        print("humidity: " + self.humidity)
        print("temperature_dht: " + self.temperature_dht)
        print("methane: " + self.methane)
        print("ammonia: " + self.ammonia)
        print("moisture: " + self.moisture)

    def run(self):
        while True:
            data = self.read()
            self.pressure = sensor_data(data, 'pressure')
            self.altitude = sensor_data(data, 'altitude')
            self.temperature_bmp = sensor_data(data, 'temperature_bmp')
            self.luminosity = sensor_data(data, 'luminosity')
            self.humidity = sensor_data(data, 'humidity')
            self.temperature_dht = sensor_data(data, 'temperature_dht')
            self.methane = sensor_data(data, 'Methane')
            self.ammonia = sensor_data(data, 'ammonia')
            self.moisture = sensor_data(data, 'moisture')
            self.sendDataToBase()
            self.printData()
            time.sleep(2)

    def sensor_data (self , read_data , required_data) :
        """ 
        Returns required sensor data 

        read_data - data read from seiral port
        required data -
            pressure - returns pressure values from BMP180
            altitude - returns based on pressure
            temperature_bmp - returns temperature value from BMP180
            luminosity - returns luminocity value from BH1750
            Humidity - returns temperature value from DHT11
            temperature_dht - returns temperature value from DHT11
            methane - returns methane concentration value from MQ 4
            ammonia - returns ammoia concentration value from MQ135
            moisture -returns relative moisture of the soil from capacitve sensor

        """
        if (required_data == "pressure") :
            # umit pascal 
            pressure = round(float(read_data[0], 2))
            return pressure 
        elif (required_data == "altitude") :
            # unit  meters 

            # assumptions
            # 1. g = 9.807 m/s
            # 2. M (molar mass of air ) = 0.02896 kg / mole 
            # 3. T = 288.15
            # 4. R = 8.3143
            # 5. sea_pressure=101325 pascal
            pressure = round(float(read_data[0], 2))
            altitude = ((math.log((pressure /101325))/0.00012)*-1)
            return round(altitude, 2) 
        elif (required_data == "temperature_bmp") :
            temperature = round(float(read_data[1], 2))
            return temperature 
        elif (required_data == "luminosity") :  
            luminosity = round(float(read_data[2], 2))
            return luminosity
        elif (required_data == "humidity") :
            humidity = round(float(read_data[3], 2))
            return humidity 
        elif (required_data == "temperature_dht") :
            temperature = round(float(read_data[4], 2))
            return temperature
        elif(required_data == "Methane" ) :
            methane = round(float(read_data[5], 2))
            return methane 
        elif (required_data == "ammoina ") :
            ammonia = round(float(read_data[6], 2))
            return ammonia
        elif (required_data == "moisture" ) :
            soil_moisture = round(float(read_data[7], 2))
            return soil_moisture

if __name__ == "__main__":
    '''
    The program now takes one argument which is optional
    The argument is server which states if the base station side code is running
    The default value is False and can be used for debugging when only data from the arduino has to be taken
    '''
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--server", type = bool, default = False, help = "Is the server running")
    args = vars(ap.parse_args())
    sensors = Sensor_data('COM3', 115200, args["server"])
    sensors.run()
    del sensors
