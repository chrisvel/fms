from flask import Flask, render_template

from controllers.penalties import PenaltyList

from services.kafka import consume_messages_from_kafka
import threading
from operator import itemgetter

from tinydb import TinyDB, Query
db = TinyDB('db.json')

import time 
time.sleep(20)

print('Starting Kafka listeners')

consumer1_thread = threading.Thread(target=consume_messages_from_kafka)
consumer1_thread.start()

print ('Starting http api')

app = Flask(__name__, static_folder='static', static_url_path='')
@app.route("/penalties")
def index():
    pagetitle = "HomePage"
    penalties = db.all()
    return render_template("index.html",
                            mytitle=pagetitle,
                            penalties=sorted(penalties, key=itemgetter('driver_id')) )

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5001, debug=False, threaded=True)