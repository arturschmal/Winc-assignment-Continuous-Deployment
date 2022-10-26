# Import what we need from flask
from flask import Flask
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", title="Index")
