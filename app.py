import requests
from flask import Flask, request, render_template
from flask_cors import cross_origin
import json
from threading import Timer

app=Flask(__name__)

##############################################################################

with open('./config.json') as file:  
  config=json.load(file)

##############################################################################

global api_counter; #in order to control maximum requests per minute

def init_api_counter():
  global api_counter
  api_counter=0
  Timer(60.0, init_api_counter).start()

def check_api_counter():
  global api_counter
  api_counter+=1
  return True if api_counter<60 else False

init_api_counter()

##############################################################################

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/api/weather", methods=['GET'])
@cross_origin()
def weather():
  try:
    if not check_api_counter():
      raise Exception('Api requests overloaded: ', api_counter)

    lang=request.args.get('lang') if request.args.get('lang') else 'en'
    latitude=request.args.get('latitude')
    longitude=request.args.get('longitude')
    res=requests.get(f'http://api.openweathermap.org/data/2.5/weather?lang={lang}&lat={latitude}&lon={longitude}&units=metric&appid={config["openweathermap-api-key"]}').text
    return res
  except Exception as e:
    print("ERROR: "+str(e))
    return ''

@app.route("/api/clock", methods=['GET'])
@cross_origin()
def clock():
  try:
    if not check_api_counter():
      raise Exception('Api requests overloaded: ', api_counter)

    latitude=request.args.get('latitude')
    longitude=request.args.get('longitude')
    res=requests.get(f'http://api.timezonedb.com/v2.1/get-time-zone?key={config["timezonedb-api-key"]}&format=json&by=position&lat={latitude}&lng={longitude}').text
    return res
  except Exception as e:
    print("ERROR: "+str(e))
    return ''

@app.route("/api/translate", methods=['GET'])
@cross_origin()
def translate():
  try:
    if not check_api_counter():
      raise Exception('Api requests overloaded: ', api_counter)

    lang=request.args.get('lang')
    text=request.args.get('text')
    res=requests.get(f'https://translate.yandex.net/api/v1.5/tr.json/translate?key={config["yandex-translate-api-key"]}&lang={lang}&text={text}').text
    return res
  except Exception as e:
    print("ERROR: "+str(e))
    return ''

@app.route("/api/buses", methods=['GET'])
@cross_origin()
def buses():
  try:
    if not check_api_counter():
      raise Exception('Api requests overloaded:', api_counter)
    act=request.args.get('act')
    p1=request.args.get('p1')
    res=requests.get(f'http://telematics.oasa.gr/api?act={act}&p1={p1}').text
    return res
  except Exception as e:
    print("ERROR: "+str(e))
    return ''

if __name__=='__main__':
  app.run()