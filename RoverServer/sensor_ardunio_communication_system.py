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

class Sensor_data :
    def __init__(self, port, baudrate):
        self.arduino = serial.Serial(port=port, baudrate=baudrate)
    
    def read (self) :
        """ 
        reads the data from serial port and converts into Unicode
        """
        Readstring = self.arduino.readline()
        decoded = Readstring.decode() #byte string converted to Unicode 
        data= decoded.split()
        return data
     

    def sensor_data (self , read_data , required_data  ) :
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
            pressure = float(read_data[0])
            return pressure 
        elif (required_data == "altitude") :
            # unit  meters 

            # assumptions
            # 1. g = 9.807 m/s
            # 2. M (molar mass of air ) = 0.02896 kg / mole 
            # 3. T = 288.15
            # 4. R = 8.3143
            # 5. sea_pressure=101325 pascal
            pressure = float(read_data[0])
            altitude = ((math.log((pressure /101325))/0.00012)*-1)
            return altitude 
        elif (required_data == "temperature_bmp") :
            temperature = float(read_data[1])
            return temperature 
        elif (required_data == "luminosity") :  
            luminosity = float(read_data[2])
            return luminosity
        elif (required_data == "humidity") :
            humidity = float(read_data[3])  
            return humidity 
        elif (required_data == "temperature_dht") :
            humidity = float(read_data[4])  
            return temperature
        elif(required_data == "Methane" ) :
            methane = float(read_data[5])
            return methane 
        elif (required_data == "ammoina ") :
            ammonia = float(read_data[6])
            return ammonia
        elif (required_data == "moisture" ) :
            soil_moisture = float(read_data[7])

