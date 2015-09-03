from datetime import datetime
from time import sleep

import serial
import Adafruit_DHT
from TSL2561 import TSL2561

__author__ = 'laurogama'

# Example of sensor connected to Raspberry Pi pin 23
DHT_PIN = 4
SDA_1 = 2
SCL1 = 3


class Sensor():
    def __init__(self):
        self.dht22_sensor = Adafruit_DHT.DHT22
        self.tsl = TSL2561()
        self.data = {}
        self.response = {}
        self.gas_threshold = 100

    def read_sensors(self):
        # print "reading temperature and humidity"
        self.read_temperature_humidity()
        self.read_lux()
        self.read_gas_presence()
        self.read_sound_level()
        self.response['data'] = self.data
        self.response['timestamp'] = str(datetime.now())
        # print self.response
        return self.response

    def read_temperature_humidity(self):
        # Sensor should be set to Adafruit_DHT.DHT11,
        # Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.

        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(self.dht22_sensor,
                                                        DHT_PIN)
        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        if humidity is not None and temperature is not None:
            # print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature,
            #                                                    humidity)
            self.data.update({"temperature": temperature, "humidity": humidity})
            return (True, {"temperature": temperature, "humidity": humidity})
        else:
            print 'Failed to get reading. Try again!'
            return (False, None)

    def read_lux(self):
        lux = self.tsl.readLux()
        # print "Lux: {}".format(lux)
        self.data.update({"luminance": lux})

    def read_gas_presence(self):
        ser = serial.Serial(

            port='/dev/ttyAMA0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        ser.write('S')
        sleep(1)
        data = ser.readline()
        self.data.update({"gas": int(data)})
        # print "Gas presence: {}".format(data)
        ser.write('g')
        if int(data) > self.gas_threshold:
            ser.write('r')
        ser.close()

    def read_sound_level(self):
        pass


if __name__ == '__main__':
    sensors = Sensor()
    sensors.read_sensors()
