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
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST', 'GET'])
@app.route('/process_text', methods=['POST', 'GET'])
@app.route('/result', methods=['POST', 'GET'])
def process_image():
        labelslist = []
        # You either get a text or a picture
        # Check for what you got!
        if request.files['image']:
        # try:
            uploaded_image = request.files['image']

            # Authenticate with Google Cloud Vision using your API key
            client = ImageAnnotatorClient.from_service_account_json('makeuc-hackathon-2023-467a19918a38.json')

            # Read the image file
            content = uploaded_image.read()

            # Perform image analysis using Google Cloud Vision API
            image = Image(content=content)
            response = client.label_detection(image=image) # Taking most time to process

            # Collect all detected labels
            for label in response.label_annotations:
                if is_animal(label.description):
                    labelslist.append(label.description)  
            if labelslist == []:
                return render_template('error.html', mode="2")
            api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(str(labelslist[0]).lower())
            response = requests.get(api_url, headers={'X-Api-Key': 'ig9ASDgHx/G7qjaEMjc20w==IKOpR2YWR7NvUA1w'})
            randAnimal = random.randint(0, len(response.json())-1)

            # Render the results page
            if response.status_code == requests.codes.ok:
                animal_data = wiki(str(response.json()[randAnimal]['name']).lower())
                if (str(response.json()[randAnimal]['name']).lower() != str(labelslist[0]).lower()):
                    genus_data = wiki(labelslist[0].lower())
                else:
                    genus_data = wiki(str(response.json()[randAnimal]['taxonomy']['genus']).lower())
                if page_exists(response.json()[randAnimal]['name'].lower()):
                    wiki_url = "https://en.wikipedia.org/wiki/{}".format(response.json()[randAnimal]['name'].lower())
                else:
                    wiki_url = "https://en.wikipedia.org/wiki/{}".format(uploaded_text.lower())
                try:
                    similar_species = get_similar_species(response.json()[randAnimal]['taxonomy']['scientific_name'])
                except Exception as e:
                    return render_template('error.html', mode="1")
                return render_template('results.html', mode = "1", wiki_url = wiki_url, labels=response.json()[randAnimal], uploaded_images=request.files['image'], animal_data=animal_data, genus_data=genus_data, similar_species=similar_species)
            else:
                print("Error:", response.status_code, response.text)
                return render_template('error.html', mode="1")
        # except Exception as e:
            return render_template('error.html', mode="1")
        
         # If Text is uploaded
        elif request.form['animal']:
            try:
                uploaded_text = request.form['animal']

                for words in str(uploaded_text).split():
                    print("Words: ", words)
                    if is_animal(words):
                        labelslist.append(words)
                        print ("Labels List: ", labelslist)

                check = 'https://api.api-ninjas.com/v1/animals?name={}'.format(uploaded_text.lower())
                response = requests.get(check, headers={'X-Api-Key': 'ig9ASDgHx/G7qjaEMjc20w==IKOpR2YWR7NvUA1w'})
                if labelslist == []:
                    if response.json() == []:
                        return render_template('error.html', mode="3")
                    else:
                        randAnimal = random.randint(0, len(response.json())-1)
                        for eachAnimal in response.json():
                            for eachword in eachAnimal['name'].split():
                                print(eachword.lower())
                                if eachword.lower() == uploaded_text.lower():
                                    print("Found")
                                    labelslist.append(uploaded_text)
                                    print("Found")
                                    animal_data = wiki(str(eachAnimal['name']).lower())
                                    print("Found")
                                    if (str(eachAnimal['name']).lower() != str(labelslist[0]).lower()):
                                        print("Found")
                                        genus_data = wiki(labelslist[0].lower())
                                        print("Found")
                                    else:
                                        genus_data = wiki(str(response.json()[randAnimal]['taxonomy']['genus']).lower())
                                        print("Found")
                                    if page_exists(eachAnimal['name'].lower()):
                                        wiki_url = "https://en.wikipedia.org/wiki/{}".format(eachAnimal['name'].lower())
                                    else:
                                        wiki_url = "https://en.wikipedia.org/wiki/{}".format(uploaded_text.lower())
                                    similar_species = get_similar_species(eachAnimal['taxonomy']['scientific_name'])
                                    return render_template('results.html', mode = "2", wiki_url = wiki_url, labels=eachAnimal, uploaded_images="", uploaded_text=uploaded_text, animal_data=animal_data, genus_data=genus_data, similar_species=similar_species)

                        labelslist.append(response.json()[0]['name'])
                        api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(str(labelslist[0]).lower())
                        response = requests.get(api_url, headers={'X-Api-Key': 'ig9ASDgHx/G7qjaEMjc20w==IKOpR2YWR7NvUA1w'})
                        randAnimal = random.randint(0, len(response.json())-1)

                        # Render the results page
                        if response.status_code == requests.codes.ok:
                            animal_data = wiki(str(response.json()[randAnimal]['name']).lower())
                            if (str(response.json()[randAnimal]['name']).lower() != str(labelslist[0]).lower()):
                                genus_data = wiki(labelslist[0].lower())
                            else:
                                genus_data = wiki(str(response.json()[randAnimal]['taxonomy']['genus']).lower())
                            if page_exists(eachAnimal['name'].lower()):
                                wiki_url = "https://en.wikipedia.org/wiki/{}".format(eachAnimal['name'].lower())
                            else:
                                wiki_url = "https://en.wikipedia.org/wiki/{}".format(uploaded_text.lower())                        
                            similar_species = get_similar_species(response.json()[randAnimal]['taxonomy']['scientific_name'])
                            return render_template('results.html', mode = "2", wiki_url = wiki_url, labels=response.json()[randAnimal], uploaded_images="", uploaded_text=uploaded_text, animal_data=animal_data, genus_data=genus_data, similar_species=similar_species)
                        else:
                            print("Error:", response.status_code, response.text)
                            return render_template('error.html', mode="3")
                else:
                    api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(str(labelslist[0]).lower())
                    print(api_url)

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
                            genus_data = wiki(str(response.json()[randAnimal]['taxonomy']['genus']).lower())
                        print("Processing text...")
                        if page_exists(str(response.json()[randAnimal]['name']).lower()):
                            wiki_url = "https://en.wikipedia.org/wiki/{}".format(str(response.json()[randAnimal]['name']).lower())
                        else:
                            wiki_url = "https://en.wikipedia.org/wiki/{}".format(uploaded_text.lower())
                        wiki_url = "https://en.wikipedia.org/wiki/{}".format(str(response.json()[randAnimal]['name']).lower())
                        similar_species = get_similar_species(response.json()[randAnimal]['taxonomy']['scientific_name'])
                        return render_template('results.html', mode = "2", wiki_url = wiki_url, labels=response.json()[randAnimal], uploaded_images="", uploaded_text=uploaded_text, animal_data=animal_data, genus_data=genus_data, similar_species=similar_species)
                    else:
                        print("Error:", response.status_code, response.text)
                        return render_template('error.html', mode="3")

            except Exception as e:
                return render_template('error.html', mode="1")
        else:
            return render_template('error.html', mode="1")

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
    wiki_wiki = wikipediaapi.Wikipedia(user_agent="MakeUCHackathon")  # You can change the language code if needed.
    page = wiki_wiki.page(query)
    if page.exists():
        print("Page: ", page)
        print("Section Data:", page.sections)
        # for section in page.sections:
        #     if section.
        return page.sections
    else:
        return ""

# Function to fetch similar species from GBIF API
def get_similar_species(animal_name):
    api_url = f'https://api.gbif.org/v1/species/search?q={animal_name}&limit=10'
    headers = {'Content-Type': 'application/json'}

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        similar_species = []
        similar_species_return = []
        counter = 0
        # Extract relevant information about similar species
        for result in data.get('results', []):
            if ((result['scientificName'] not in similar_species) and counter < 3):
                counter += 1
                similar_species.append(str(result['scientificName']))
                similar_species_return.append({
                    'name': result['scientificName'],
                    'wiki_url': f"https://en.wikipedia.org/wiki/{result['scientificName'].replace(' ', '_')}"
                })
        return similar_species_return
    else:
        return [{
            'name': 'No similar species found',
            'wiki_url': ''
        }]

if __name__ == '__main__':
    app.run(debug=True)