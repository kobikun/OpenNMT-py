from flask import Flask
from flask import request, jsonify

from translate import Option, online_trans_init, online_translate
from tokenizer import BITokenizer

opt = Option()
opt.model = ""

tokenizer = BITokenizer()
translator = online_trans_init(opt)

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
    output = online_translate(translator, tokenizer, src)
    
    data = {'src':src, 'tgt':output}
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

