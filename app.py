from flask import Flask
from flask import render_template
from flask import request
from model import predict

app = Flask(__name__)


# @app.route("/", methods=['GET', 'POST'])
# def index():    
#     if request.method == 'POST':
#         return "none"
#     else:
#         return render_template("index.html")

@app.route("/index", methods=['GET', 'POST'])
def index():    
    if request.method == 'POST':
        return render_template("index.html", prediction = 100)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
