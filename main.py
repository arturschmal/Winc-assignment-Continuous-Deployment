# Import what we need from flask
from flask import Flask
from flask import Flask, redirect, render_template, request, session, url_for

# Create a Flask app inside `app`
app = Flask(__name__)

# Assign a function to be called when the path `/` is requested
@app.route('/')
def index():
    return render_template("index.html", title="Index")
