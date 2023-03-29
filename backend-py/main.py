import random
from flask import Flask, render_template, session, request, jsonify

app = Flask(__name__,static_folder='static',static_url_path='')
app.secret_key = 'secretkey'

user_numbers = {}

@app.route('/', methods=['GET'])
def start():
    user_id = random.randint(1, 1000000)
    img_id = random.randint(0, 1)
    session['user_id'] = user_id
    # number = random.randint(1, 10)
    number = 0 
    user_numbers[user_id] = number
    box_pos = []
    for i in range(4):
        box_pos.append((random.uniform(0, 1),random.uniform(0, 1)))
    return render_template('index.html',this=img_id,box_pos=box_pos)

@app.route('/guess', methods=['POST'])
def guess():
    user_id = session.get('user_id')
    guess = request.json['guess']
    number = user_numbers.get(user_id)
    if number is None:
        response = {
            'message': 'Please start a new game before guessing.',
        }
    elif guess == number:
        response = {
            'bool': 'true',
        }
    else:
        response = {
            'bool': 'false',
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,ssl_context=("cert.pem", "key.pem"))


