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
import wikipediaapi
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# Import the Google Cloud client library
from google.cloud import vision_v1
from google.cloud.vision_v1 import types, ImageAnnotatorClient, Image

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST', 'GET'])
def process_image():
        labelslist = []
    # You either get a text or a picture
    # Check for what you got!
        if request.files['image']:
            try:
                uploaded_image = request.files['image']
                # Authenticate with Google Cloud Vision using your API key
                client = ImageAnnotatorClient.from_service_account_json('makeuc-hackathon-2023-467a19918a38.json')
                # Read the image file
                content = uploaded_image.read()
                # Perform image analysis using Google Cloud Vision API
                image = Image(content=content)
                response = client.label_detection(image=image) # Taking most time to process
                return render_template('results.html', mode = "1", wiki_url = "", labels="", uploaded_images=uploaded_image, animal_data="", genus_data="")
            except Exception as e:
                return render_template('error.html')
        
        elif request.form['animal']:
            uploaded_text = request.form['animal']
            print("Processing text...")

            for words in str(uploaded_text).split():
                if is_animal(words):
                    labelslist.append(words)
            print("Processing text...")

            if labelslist == []:
                return render_template('error.html')
    
            api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(uploaded_text)
            response = requests.get(api_url, headers={'X-Api-Key': 'ig9ASDgHx/G7qjaEMjc20w==IKOpR2YWR7NvUA1w'})
            randAnimal = random.randint(0, len(response.json())-1)

            print(response.json()[randAnimal]['name'])
            print("Processing text...")
            # Render the results page
            if response.status_code == requests.codes.ok:
                animal_data = wiki(str(response.json()[randAnimal]['name']).lower())
                if (str(response.json()[randAnimal]['name']).lower() != str(labelslist[0]).lower()):
                    genus_data = wiki(labelslist[0].lower())
                else:
                    genus_data = ""
                genus = str(response.json()[randAnimal]['taxonomy']['genus']).lower()
                for section in wiki_species(genus):
                    print(section.title)
                print("Processing text...")
                wiki_url = "https://en.wikipedia.org/wiki/{}".format(str(response.json()[randAnimal]['name']).lower())
                return render_template('results.html', mode = "2", wiki_url = wiki_url, labels=response.json()[randAnimal], uploaded_images="", animal_data=animal_data, genus_data=genus_data)
            else:
                print("Error:", response.status_code, response.text)
                return render_template('error.html')

# Define Functions From Here
def wiki(query):
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='MakeUCHackathon')
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary
    else:
        return ""

def page_exists(query):
    wiki_wiki = wikipediaapi.Wikipedia(user_agent='MakeUCHackathon')
    page = wiki_wiki.page(query)
    return page.exists()

# Function to check if a label is related to an animal
def is_animal(label):
    animal_keywords = ["Fox", "Ox", "Aardvark", "Albatross", "Alligator", "Alpaca", "Ant", "Anteater", "Antelope", "Ape", "Armadillo", "Donkey", "Baboon", "Badger", "Barracuda", "Bat", "Bear", "Beaver", "Bee", "Bison", "Boar", "Buffalo", "Butterfly", "Camel", "Capybara", "Caribou", "Cassowary", "Cat", "Caterpillar", "Cattle", "Chamois", "Cheetah", "Chicken", "Chimpanzee", "Chinchilla", "Chough", "Clam", "Cobra", "Cockroach", "Cod", "Cormorant", "Cow", "Coyote", "Crab", "Crane", "Crocodile", "Crow", "Curlew", "Deer", "Dinosaur", "Dog", "Dogfish", "Dolphin", "Dotterel", "Dove", "Dragonfly", "Duck", "Dugong", "Dunlin", "Eagle", "Echidna", "Eel", "Eland", "Elephant", "Elk", "Emu", "Falcon", "Ferret", "Finch", "Fish", "Flamingo", "Fly", "Fox", "Frog", "Gaur", "Gazelle", "Gerbil", "Giraffe", "Gnat", "Gnu", "Goat", "Goldfinch", "Goldfish", "Goose", "Gorilla", "Goshawk", "Grasshopper", "Grouse", "Guanaco", "Gull", "Hamster", "Hare", "Hawk", "Hedgehog", "Heron", "Herring", "Hippopotamus", "Hornet", "Horse", "Human", "Hummingbird", "Hyena", "Ibex", "Ibis", "Jackal", "Jaguar", "Jay", "Jellyfish", "Kangaroo", "Kingfisher", "Koala", "Kookabura", "Kouprey", "Kudu", "Lapwing", "Lark", "Lemur", "Leopard", "Lion", "Llama", "Lobster", "Locust", "Loris", "Louse", "Lyrebird", "Magpie", "Mallard", "Manatee", "Mandrill", "Mantis", "Marten", "Meerkat", "Mink", "Mole", "Mongoose", "Monkey", "Moose", "Mosquito", "Mouse", "Mule", "Narwhal", "Newt", "Nightingale", "Octopus", "Okapi", "Opossum", "Oryx", "Ostrich", "Otter", "Owl", "Oyster", "Panther", "Parrot", "Partridge", "Peafowl", "Pelican", "Penguin", "Pheasant", "Pig", "Pigeon", "Pony", "Porcupine", "Porpoise", "Quail", "Quelea", "Quetzal", "Rabbit", "Raccoon", "Rail", "Ram", "Rat", "Raven", "Red deer", "Red panda", "Reindeer", "Rhinoceros", "Rook", "Salamander", "Salmon", "Sand Dollar", "Sandpiper", "Sardine", "Scorpion", "Seahorse", "Seal", "Shark", "Sheep", "Shrew", "Skunk", "Snail", "Snake", "Sparrow", "Spider", "Spoonbill", "Squid", "Squirrel", "Starling", "Stingray", "Stinkbug", "Stork", "Swallow", "Swan", "Tapir", "Tarsier", "Termite", "Tiger", "Toad", "Trout", "Turkey", "Turtle", "Viper", "Vulture", "Wallaby", "Walrus", "Wasp", "Weasel", "Whale", "Wildcat", "Wolf", "Wolverine", "Wombat", "Woodcock", "Woodpecker", "Worm", "Wren", "Yak", "Zebra", "Aardwolf", "Bactrian Camel", "Beluga Whale", "Chimpanzee", "Dik-dik", "Echidna", "Fennec Fox", "Gila Monster", "Hamadryas Baboon", "Iguana", "Jerboa", "Kakapo", "Lemming", "Manatee", "Narwhal", "Ocelot", "Pangolin", "Quokka", "Red Fox", "Stoat", "Tasmanian Devil", "Uakari", "Vaquita", "Wombat", "X-ray Tetra", "Yellow Tang", "Zorse"]    
    for keyword in animal_keywords:
        if keyword.lower() == label.lower():
            return True
    return False 

def wiki_species(query):
    wiki_wiki = wikipediaapi.Wikipedia(user_agent="Kartavya")  # You can change the language code if needed.
    page = wiki_wiki.page(query)
    if page.exists():
        print("Page: ", page)
        print("Section Data:", page.sections)
        # for section in page.sections:
        #     if section.
        return page.sections
    else:
        return ""


if __name__ == '__main__':
    app.run(debug=True)