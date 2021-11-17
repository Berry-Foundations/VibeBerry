# PackedBerry Server

from flask import Flask
from threading import Thread
import logging
import time

app = Flask('')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def home():
	f = open('index.html', 'r')
	d = f.read()
	f.close()
	html = str(d)
	return html

def run():
	try:
		app.run(host='0.0.0.0',port=2021)
	except Exception as e:
		print(e)

def status():
	t = Thread(target=run)
	t.start()

def super_run():
	def super():
		while True:
			status()
			time.sleep( 60 * 60 )
	super_thread = Thread(target=super)
	super_thread.start()
