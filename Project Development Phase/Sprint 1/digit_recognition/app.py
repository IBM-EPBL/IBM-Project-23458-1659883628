import os
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/recognise', methods=['GET','POST'])
def recognise():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('recognise.html')
    

if __name__ == "__main__":
    app.run(debug = False,)


