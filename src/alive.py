from flask import Flask
from threading import Thread

app = Flask('')
app.logger.disabled = True
app.debug = False

@app.route('/')
def home():
	return 'Mićko is alive!'

def run():
	app.run(host='0.0.0.0', port=8080)

def keep_alive():
	t = Thread(target=run)
	t.start()