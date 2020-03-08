import os
from flask import Flask, render_template, send_from_directory, redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'
    
@app.route('/name')
def name():
    return render_template("index.html", name = 'Володька')
    
@app.route('/favicon.ico')
def fav():
    return redirect(url_for('static', filename='favicon.ico'), code=302)
    

if __name__ == '__main__':
    app.run()