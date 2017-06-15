from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/chat", methods=['POST'])
def api_chat():
    content = request.json
    src = None
    if 'src' in content:
        src = content['src']
    else:
        if request.method == 'POST':
            src = request.form['src']
    return src
