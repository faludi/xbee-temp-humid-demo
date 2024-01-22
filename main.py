from machine import I2C # load the i2c functions
import shtc3 # load the sensor module
import network # load the cell network functions
import time # load the time functions
from digi import cloud # load the digi cloud functions

__version__ = "1.0.0"
print(" Digi XBee 3 Cellular DRM Getting Started Demo - Temp Humid SHT3C v%s" % __version__)

STREAM1 = "digikit/temperature" # define data stream names
STREAM2 = "digikit/humidity"
UPLOAD_RATE = 10 # upload frequency in seconds

# wait for cell modem to be connected
conn = network.Cellular()
print(" wait for cell network...")
while not conn.isconnected():
    time.sleep(2)
print(" cell ok")

# set up temperature and humidity sensor
i2c = I2C(1, freq=400000) # create i2c connection
sensor = shtc3.SHTC3(i2c) # assign i2c to sensor

# start clock with first sample immediately
t1 = time.ticks_add(time.ticks_ms(), UPLOAD_RATE * -1000)

# main loop
while True:
    t2 = time.ticks_ms() # mark current time
    if time.ticks_diff(t2, t1) >= UPLOAD_RATE * 1000: # check if it's time for a sample
        t1 = time.ticks_ms() # mark sample time
        # get samples from shtc3 sensor
        try:
            values = sensor.get_data() # obtain temp and humidity from sensor
            temperature = values[0] # temp is first value
            humidity = values[1] # humidity is second value
        except Exception as e:
            print(e) # if anything goes wrong, print the error message
        # send samples to Digi Remote Manager data streams
        try:
            data = cloud.DataPoints(cloud.TRANSPORT_TCP) # define a TCP data upload
            data.add(STREAM1,temperature) # upload temperature value to the first stream
            data.add(STREAM2,humidity) # upload humidity value to the second stream
            data.send(timeout=60) # try sending the data, but give up after 69 seconds
            print(" drm -> ", temperature, humidity)
        except Exception as e:
            print(e)  # if anything goes wrong, print the error message

