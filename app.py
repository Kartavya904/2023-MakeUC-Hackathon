# Backend for the web application
# Flask Application
# Made by Kartavya Singh & Shivam Kharangate
# Date: 11/04/2023
#PLEASE READ THIS BEFORE CONTINUING
# Please create a virtual environment using the following command: python3 -m venv makeucenv
# Activate the virtual environment using the following command: source makeucenv/Scripts/activate
# Install the required packages using the following command: pip install -r requirements.txt
# To Install Google-Cloud API Run makeucenv\Scripts\pip.exe install google-cloud
# To Install Google-Cloud Vision Run makeucenv\Scripts\pip.exe install google-cloud-vision 
# Run the application using the following command: python app.py

# Importing the required packages
import os, random, string, json, requests, datetime, time, re
import wikipediaapi as wiki
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# Import the Google Cloud client library
from google.cloud import vision_v1
from google.cloud.vision_v1 import types, ImageAnnotatorClient, Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST', 'GET'])
def process_image():
    # You either get a text or a picture
    # Check for what you got!
    if request.files['image']:
        uploaded_image = request.files['image']
        # Authenticate with Google Cloud Vision using your API key
        client = ImageAnnotatorClient.from_service_account_json('makeuc-hackathon-2023-467a19918a38.json')
        # Read the image file
        content = uploaded_image.read()
        # Perform image analysis using Google Cloud Vision API
        image = Image(content=content)
        response = client.label_detection(image=image) # Taking most time to process

    elif request.form['text']:
        uploaded_text = request.form['text']
        print(uploaded_text)
        data = wiki(uploaded_text)
    return render_template('results.html', data=data)


# Define Functions From Here
def wiki(query):
    wiki_wiki = wiki.Wikipedia(user_agent='MakeUCHackathon')
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary
    else:
        return ""

def page_exists(query):
    wiki_wiki = wiki.Wikipedia(user_agent='MakeUCHackathon')
    page = wiki_wiki.page(query)
    return page.exists()

if __name__ == '__main__':
    app.run(debug=True)