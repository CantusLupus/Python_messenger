from datetime import datetime
from flask import Flask, request, abort
import time

app = Flask(__name__)

db = []

@app.route("/status", methods=['get'])

def status():
    return {
        'status': True,
        'name': 'Messanger',
        'time1': time.asctime(),
        'time2': time.time(),
        'time3': datetime.now(),
        'time4': str(datetime.now()),
        'time5': datetime.now().strftime('%Y/%m/%d time: %H/%M/%S'),
        'time6': datetime.now().isoformat(),
        'users': len(set([db[i]['name'] for i in range(len(db))]))
    }


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)
    # if set(data.keys()) != {'name', 'text'}:
    #     return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)
    if len(data) != 2:
        return abort(400)

    name = data['name']
    text = data['text']

    if not isinstance(name, str) or \
            not isinstance(text, str) or \
            name == '' or \
            text == '':
        return abort(400)

    message = {
        'time': time.time(),
        'name': name,
        'text': text,
    }
    db.append(message)
    return {'ok': True}


@app.route("/messages")
def get_message():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(result) >= 1:
                break

    return {'messages': result}


app.run()
