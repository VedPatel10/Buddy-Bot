from flask import Flask
from threading import Thread
import random
import time
import requests
import logging
import datetime
app = Flask('')
@app.route('/')
def home():
    return "Buddy bot is so good!"
def run():
  app.run(host='0.0.0.0',port=random.randint(2000,9000)) 
def ping(target, debug):
    while(True):
        r = requests.get(target)
        if(debug == True):
            print(f'{r.status_code} at {datetime.datetime.utcnow() - datetime.timedelta(hours=4)}')
        time.sleep(random.randint(180,300)) #alternate ping time between 3 and 5 minutes
def awake(target, debug=False):  
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.logger.disabled = True  
    t = Thread(target=run)
    r = Thread(target=ping, args=(target,debug,))
    t.start()
    r.start()