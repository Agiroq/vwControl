#
# Created by Rui Santos
# Complete project details: http://randomnerdtutorials.com
#

import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
from flask.ext.socketio import SocketIO, emit
app = Flask(__name__)

mqttc=mqtt.Client()
mqttc.connect("localhost",1883,60)
mqttc.loop_start()

# create the time variable
heat_time = 10

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   4 : {'name' : 'heater', 'board' : 'esp8266', 'topic' : 'esp8266/4', 'state' : heat_time},
   5 : {'name' : 'GPIO 5', 'board' : 'esp8266', 'topic' : 'esp8266/5', 'state' : 'False'}
   }

# Put the pin dictionary into the template data dictionary:
templateData = {
   'pins' : pins,
   'heat_time' : heat_time
   }

@app.route("/")
def main():
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<board>/<changePin>/<action>")

def action(board, changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   devicePin = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:

   if pins[changePin] == 4 and board == 'ep8266':
      mqttc.publish(pins[changePin]['topic'], action)

   if pins[changePin] == 5 and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'], action)
      pins[changePin]['state'] = 'True'

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
      'heat_time' : heat_time
   }

   return render_template('main.html', **templateData)

@socketio.on('heatT')
def heat_T(message):
    heat_time = message['data']
    emit('update value', message, broadcast=True)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8181, debug=True)
