from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'
    
@app.route('/name')
def name():
    return render_template("index.html", name = 'Володька')
    

if __name__ == '__main__':
    app.run()