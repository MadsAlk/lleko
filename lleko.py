import json
from flask import Flask, render_template, request, jsonify
from gpiozero import LED, DigitalInputDevice
import RPi.GPIO as GPIO
import time
import adafruit_dht
from board import *

#DHT22
SENSOR_PIN = D21
dht22 = adafruit_dht.DHT22(SENSOR_PIN, use_pulseio=False)
 
te = dht22.temperature
print(te)

GPIO.setmode(GPIO.BCM)
 
# GPIO ports for the 7seg pins
segments =  (11,4,23,8,7,10,18,25)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline
 
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
 
# GPIO ports for the digit 0-3 pins 
digits = (22,27,17,1)
# 7seg_digit_pins (12,9,8,6) digits 0-3 respectively

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)
 
num = {' ':(0,0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0,0),
    '1':(0,1,1,0,0,0,0,0),
    '2':(1,1,0,1,1,0,1,0),
    '3':(1,1,1,1,0,0,1,0),
    '4':(0,1,1,0,0,1,1,0),
    '5':(1,0,1,1,0,1,1,0),
    '6':(1,0,1,1,1,1,1,0),
    '7':(1,1,1,0,0,0,0,0),
    '8':(1,1,1,1,1,1,1,0),
    '9':(1,1,1,1,0,1,1,0),
    '.':(0,0,0,0,0,0,0,1)}
 

def displayTime(): 
    try:
        t_end = time.time() + 5
        while time.time() < t_end:
            n = time.ctime()[11:13]+time.ctime()[14:16]
            s = str(n).rjust(4)
            for digit in range(4):
                for loop in range(0,7):
                    GPIO.output(segments[loop], num[s[digit]][loop])
                    if (int(time.ctime()[18:19])%2 == 0) and (digit == 1):
                        GPIO.output(25, 1)
                    else:
                        GPIO.output(25, 0)
                GPIO.output(digits[digit], 0)
                time.sleep(0.001)
                GPIO.output(digits[digit], 1)
    finally:
        print('done')

def displayTemp(temp):
    s = str(temp).rjust(4)
    try:
        t_end = time.time() + 5
        while time.time() < t_end:
            for digit in range(4):
                for loop in range(0,8):
                    GPIO.output(segments[loop], num[s[digit]][loop])
                GPIO.output(digits[digit], 0)
                time.sleep(0.001)
                GPIO.output(digits[digit], 1)
    finally:
        print('done')


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Default: GPIO4
led = LED(3)
moisture = DigitalInputDevice(15)

# while True:
#     print(moisture.value)
#     sleep(2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods = ['POST'])
def webhook():
    req = request.get_json(force=True)
    print(json.dumps(req, indent=4, sort_keys=True))
    print(req["queryResult"]["intent"]["displayName"])
    intent = req["queryResult"]["intent"]["displayName"]


    if intent == "LED":
        print(req["queryResult"]["outputContexts"][0]["parameters"]["status"])
        status = req["queryResult"]["outputContexts"][0]["parameters"]["status"]
        if status == 'on' or status == 'ON':
            led.on()
        else:
            led.off()
        ret = {
        "fulfillmentText":status
        }
        return jsonify(ret)

    if intent == "Temperature":
        ret = {
        "fulfillmentText":"the Temperature is: "+str(dht22.temperature)
        }
        return jsonify(ret)

    if intent == "Display temperature":
        print(dht22.temperature)
        displayTemp(dht22.temperature)
        ret = {
        "fulfillmentText":"here you go"
        }
        return jsonify(ret)

    if intent == "Show time":
        displayTime()
        ret = {
        "fulfillmentText":"here you go"
        }
        return jsonify(ret)
    
    ret = {
        "fulfillmentText":"healoo from the other side"
    }
    return jsonify(ret)



# @app.route('/dest.html', methods = ['POST', 'GET'])
# def dest():
#     if request.method == 'POST':
#         data = request.form                             # capture data submitted to form
#
#         return render_template('home.html', tick = True, val =f"{valueInDollar} USD = {newValue:.2f} {toCurrency}")
#     else:
#         return """<html><head>method of form = GET</head></html>"""




if __name__ == '__main__':
    app.run(debug=True, port=4500)



