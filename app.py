# Backend for the web application
# Flask Application
# Made by Kartavya Singh & Shivam Kharangate
# Date: 11/04/2023
#PLEASE READ THIS BEFORE CONTINUING
# Please create a virtual environment using the following command: python3 -m venv makeucenv
# Activate the virtual environment using the following command: source makeucenv/Scripts/activate
# Install the required packages using the following command: pip install -r requirements.txt

# Importing the required packages
import os, random, string, json, requests, datetime, time, re
import wikipediaapi as wiki
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)