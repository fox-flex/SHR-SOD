from collections import OrderedDict
from pprint import pprint
import csv
import os

import numpy as np

import os
from pathlib import Path
from pprint import pprint
import json
import spacy
from tqdm.auto import tqdm




def get_categories_imagenet(filename):
	# cat_to_lab = OrderedDict()
	cat_to_lab = {}
	
	with open(filename) as csvfile:
		freader = csv.reader(csvfile)
		rownum = 0
		for row in freader:
			# Skip header row
			if rownum == 0:
				rownum += 1
				continue

			row = np.array(row)
			row = row[row!='']		# get rid of empty cells

			# The category is the first element in the row
			# the rest are the labels in that category
			cat = row[0]
			labs = row[1:]
			assert(1+len(labs) == len(row))

			# Store values in dictionaries if not yet there
			cat_to_lab[cat] = list(labs)


	return cat_to_lab


def get_classes_diffumask():
    # bird         https://byjus.com/english/birds-name/
    bird_sub_classes = ["Masai Ostrich","Macaw","Eagle","Duck","Hen","Parrot","Peacock","Dove","Stork","Swan","Pigeon","Goose",
                        "Pelican","Macaw","Parakeet","Finches","Crow","Raven","Vulture","Hawk","Crane","Penguin", "Hummingbird",
                        "Sparrow","Woodpecker","Hornbill","Owl","Myna","Cuckoo","Turkey","Quail","Ostrich","Emu","Cockatiel"
                        ,"Kingfisher","Kite","Cockatoo","Nightingale","Blue jay","Magpie","Goldfinch","Robin","Swallow",
                        "Starling","Pheasant","Toucan","Canary","Seagull","Heron","Potoo","Bush warbler","Barn swallow",
                        "Cassowary","Mallard","Common swift","Falcon","Megapode","Spoonbill","Ospreys","Coot","Rail",
                        "Budgerigar","Wren","Lark","Sandpiper","Arctic tern","Lovebird","Conure","Rallidae","Bee-eater",
                        "Grebe","Guinea fowl","Passerine","Albatross","Moa","Kiwi","Nightjar","Oilbird","Gannet","Thrush",
                        "Avocet","Catbird","Bluebird","Roadrunner","Dunnock","Northern cardinal","Teal",
                        "Northern shoveler","Gadwall","Northern pintail",
                        "Hoatzin","Kestrel","Oriole","Partridge","Tailorbird","Wagtail","Weaverbird","Skylark"]

    # cat         https://www.purina.com/cats/cat-breeds?page=0
    cat_sub_classes = ["Abyssinian","American Bobtail","American Curl","American Shorthair","American Wirehair",
                        "Balinese-Javanese","Bengal","Birman","Bombay","British Shorthair","Burmese","Chartreux Cat",
                        "Cornish Rex","Devon Rex","Egyptian Mau","European Burmese","Exotic Shorthair","Havana Brown",
                        "Himalayan","Japanese Bobtail","Korat","LaPerm", "Maine Coon","Manx","Munchkin",
                        "Norwegian Forest","Ocicat","Oriental","Persian","Peterbald","Pixiebob","Ragamuffin",
                        "Ragdoll","Russian Blue","Savannah","Scottish Fold","Selkirk Rex","Siamese","Siberian",
                        "Singapura","Somali","Sphynx","Tonkinese","Toyger","Turkish Angora","Turkish Van"]


    # bus         https://simple.wikipedia.org/wiki/Types_of_buses
    bus_sub_classes = ["Coach","Motor","School","Shuttle","Mini",
                        "Minicoach","Double-decker","Single-decker","Low-floor","Step-entrance","Trolley",
                        "Articulated","Guided","Neighbourhood","Gyrobus","Hybrid","Police",
                        "Open top","Electric","Transit","Tour","Commuter","Party"]

    car_sub_classes = ["SEDAN","COUPE","SPORTS","STATION WAGON","HATCHBACK",
                       "CONVERTIBLE","SPORT-UTILITY VEHICLE","MINIVAN","PICKUP TRUCK","IT DOESN'T STOP THERE",""]
    
    
    map_dict = {
        "bird": bird_sub_classes,
        "cat": cat_sub_classes,
        "bus": bus_sub_classes,
        'car': car_sub_classes
    }
    return map_dict

    more_prompt_for_bus = ["Photo of a bus in the street", "Photo of a bus in the road",   "Photo of a bus in the street at night",      "Photo of the back of a bus", "Photo of the overturn of a bus", "Photo of a bus", "Photo of a bus", "Photo of a bus", "Photo of a bus", "Photo of a bus", "Photo of a bus"]

    # train
    more_prompt_for_train = ["Photo of a train bus in the street", "Photo of a train bus in the road",   "Photo of a train bus in the street at night",      "Photo of the back of a train bus",  "Photo of a train bus", "Photo of a train bus"]

    # truck
    prompt_for_truck = ["Photo of a truck in the street", "Photo of a truck", "Photo of a truck in the road",   "Photo of a truck in the street at night",      "Photo of the back of a truck"]

    # bicycle
    prompt_for_bicycle = ["Photo of a bicycle in the street", "Photo of a bicycle", "Photo of a bicycle in the road",   "Photo of a bicycle in the street at night",      "Photo of the back of a bicycle"]

    # traffic light
    prompt_for_traffic_light = ["Photo of a traffic light in the street", "Photo of a traffic light", "Photo of a traffic light in the road",   "Photo of a traffic light in the street at night"]

    # motorcycle         https://ride.vision/blog/13-motorcycle-types-and-how-to-choose-one/
    motorcycle_sub_classes = ["Cruisers","Sportbikes","Standard & Naked ","Adventure","Dual Sports & Enduros",
                        "Dirtbikes","Electric","Choppers","Touring","Sport Touring","Vintage & Customs",
                        "Modern Classics","Commuters & Minis","Scooters",""]
    more_prompt_for_motorcycle = ["Photo of a motorcycle in the street", "Photo of a motorcycle in the road", "Photo of a motorcycle in the street", "Photo of a motorcycle in the road","Photo of a motorcycle in the street", "Photo of a motorcycle in the road",  "Photo of a motorcycle in the street at night",      "Photo of the back of a motorcycle"]


    # car         https://www.caranddriver.com/shopping-advice/g26100588/car-types/
    car_sub_classes = ["SEDAN","COUPE","SPORTS","STATION WAGON","HATCHBACK",
                        "CONVERTIBLE","SPORT-UTILITY VEHICLE","MINIVAN","PICKUP TRUCK","IT DOESN'T STOP THERE",""]
    more_prompt_for_car = ["Photo of a car in the street", "Photo of a car in the road",   "Photo of a car in the street at night",      "Photo of the back of a car", "Photo of the overturn of a car"]
    #     car_sub_classes_2 = ["photo of a car"]
    #     "photo of a car in street"

    # road
    road_sub_classes = ["Photo of street road in city", "Photo of street road at night in city"]

def read_tsv(path):
    data = []
    with open(path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        to_add = line.split('\t')
        to_add = sum([[y.strip().lower() for y in x.split('/')] for x in to_add], [])
        data += to_add
    data = sorted(list(set(data)))
    return data

def get_classes_my(data_dir):
    data = {}
    
    data_dir = Path(data_dir)
    for name in os.listdir(str(data_dir)):
        path = str(data_dir / name)
        name = ' '.join(name.lower().split('.')[0].split('_'))
        data[name] = read_tsv(path)
    
    return data


def low(some: dict):
    for k, v in some.items():
        some[k] = [' '.join(x.lower().split('_')) for x in v]
    return some
     


if __name__ == '__main__':
    cats_imnet = get_categories_imagenet('data/imagenet_categories.csv')
    cats_imnet = low(cats_imnet)

    to_add = {
		'person': ['person', 'human', 'man', 'woman', 'child',
                   'boy', 'girl', 'old man', 'teenager'],
    }
    for k, v in to_add.items():
        cats_imnet[k] = cats_imnet.get(k, []) + v
    
    cats_diffumask = get_classes_diffumask()
    cats_diffumask = low(cats_diffumask)

    cats_my = get_classes_my('data/objects')


    cats = {}
    for cats_loc in cats_imnet, cats_diffumask, cats_my:
        for k, v in cats_loc.items():
                cats[k] = cats.get(k, []) + v

    nlp = spacy.load("en_core_web_sm", disable=['parser', 'tagger', 'ner'])

    def normalize(text, lowercase=True):
        if lowercase:
            text = text.lower()
        text = nlp(text)
        lemmatized = list()
        for word in text:
            lemma = word.lemma_.strip()
            if lemma:
                if lemma.endswith('s') and len(lemmatized) > 0:
                    lemmatized[-1] += lemma
                elif lemma == '-' or (len(lemmatized) > 0 and lemmatized[-1].endswith('-')):
                    lemmatized[-1] += lemma
                else:
                    lemmatized.append(lemma)
        return " ".join(lemmatized)

    res = {}
    for k, v in tqdm(cats.items(), total = len(cats)):
        k = normalize(k)
        v = [normalize(x) for x in v]
        res[k] = v
        
    with open('classes.json', 'w') as f:
        json.dump(res, f, indent=4, sort_keys=True)

