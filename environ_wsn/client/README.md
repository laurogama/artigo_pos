## install

install the dependencies
```python
    sudo apt-get install python-pip build-essential python-dev python-smbus i2c-tools
```
 clone the DHT sensor library
 ```python
    git clone https://github.com/adafruit/Adafruit_Python_DHT.git
 ```
 from inside the cloned project
 ```python
    sudo python setup.py install
 ```
 ## Pins
 
Sensor      | Pin
--------------------
|temperature | GPIO 4
|Light sensor| GPIO2 GPIO3
|Gas sensor  |GPIO14(tx); GPIO15(rx) |send "S" throught serial and read a string
|LED         |"r" o led vermelho acende, e "g" o lede verde acende   
 


 
 