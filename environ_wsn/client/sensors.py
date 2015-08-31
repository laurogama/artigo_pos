from datetime import datetime
from TSL2561 import TSL2561

__author__ = 'laurogama'

# Example of sensor connected to Raspberry Pi pin 23
DHT_PIN = 23


class Sensor():
    def __init__(self):
        self.dht22_sensor = Adafruit_DHT.DHT22
        self.tsl=TSL2561()
        self.data = {}
        self.response = {}

    def read_sensors(self):
        self.read_temperature_humidity()
        self.response['data'] = self.data
        self.response['timestamp'] = datetime.now()
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
            print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature,
                                                               humidity)
            self.data.update({"temperature": temperature, "humidity": humidity})
            return (True, {"temperature": temperature, "humidity": humidity})
        else:
            print 'Failed to get reading. Try again!'
            return (False, None)

    def read_lux(self):
        return self.tsl.readLux()

if __name__ == '__main__':
    sensors = Sensor()
    sensors.read_sensors()
