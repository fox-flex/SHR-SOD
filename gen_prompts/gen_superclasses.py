import json
from pprint import pprint


mapper = {
    'objects': [
        'accessory',
        'ball',
        'clothing',
        'container',
        'cooking',
        'decor',
        'electronics',
        'hat',
        'instrument',
        'musicinstruments',
        'lab equipment',
        'paper',
        'technology',
        'tool',
        'toy',
        'weapon',
        'other',
        'sports equipment',
    ],
    'big vehicle': [
        'aircraft',
        'boat',
        'train',
        'transport',
    ],
    'vehicle': [
        'bus',
        'vehicle',
        'car',
    ],
    'person': [
        'person',
    ],
    'animal': [
        'arachnid',
        'armadillo',
        'bear',
        'dinosaur',
        'cat',
        'dog',
        'marsupial',
        'ferret',
        'mongoose',
        'monotreme',
        'primate',
        'rabbit',
        'rodent',
        'sloth',
        'ungulate',
        'wild cat',
        'wild dog',
        'wildanimals',
        'herbivorous animal',
        'hog',

        'bird',
        'crustacean',
        'bug',
        'butterfly',
        'echinoderms',

        'crocodile',
        'frog',
        'snake',
        'turtle',
        'salamander',
        'lizard',
    ],
    'water animal': [
        'fish',
        'trilobite',
        'marinemammals',
        'shark',
        'crocodile',
        'frog',
        'snake',
        'turtle',
        'salamander',
        'mollusk',
        'lizard',
    ],
    'plant': [
        'flower',
        'plant',
        'tree',
    ],
    'food': [
        'dry fruit',
        'fruit',
        'food',
        'fungus',
        'vegetable',

    ],
    'place': [
        'building',
        'fence',
        'furniture',
        'outdoor scene',
    ],
    'water place': [
        'coral',
    ],
}

class2sups = {}
for sup, clss in mapper.items():
    for cls in clss:
        class2sups[cls] = class2sups.get(cls, []).append(sup)


if __name__ == '__main__':
    with open('classes.json') as f:
        d = json.load(f)
    res = {}
    for class_name, names in d.items():
        sup_names = class2sups[class_name]
        for sup_name in sup_names:
            if sup_name not in res:
                res[sup_name] = {}
            res[sup_name][class_name] = names
    
    with open('supclasses.json', 'w') as f:
        json.dump(res, f, indent=4, sort_keys=True)
    
    # for k in res:
    #     res[k] = []
    # pprint(res)
