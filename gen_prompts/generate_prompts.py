import json
from pprint import pprint
import random

class PromptGenerator:
    def __init__(self, supclasses_path):

        self.scenes = {
            'urban': [
                'street',
                'square',
                'vilage',
                'city',
                'town',
                'suburb',
                'metropolis',
                
            ],
            'nature': [
                'forest',
                'lawn',
                'grassland',
                'tundras',
                'mountain',
                'countryside',
                'park',
                'farm',
                'desert',
                'wetland',
                'islands',
            ],
            'near water': [
                'beach',
                'island',
                'waterfall',
                'river',
                'mountain river',
                'lake',
                'harbor',
                'canal',
            ],
            'water': [
                'see',
                'ocean',
                'river',
                'mountain river',
                'lake',
            ],
            'air': [
                'sky',
                'space',
                'close to the ground',
            ]
        }

        self.colors = [
            "red", "green", "blue", "purple", "orange",
            "yellow", "pink", "black", "white", "gray",
            "teal", "navy", "maroon", "olive", "lime",
            "aqua", "fuchsia", "silver", "gold", "magenta"
        ]
  
        self.adjectives = {
            "size": [
                "tiny", "small", "large", "giant", "miniature", "huge", "massive"
            ],
            "shape": [
                "round", "square", "rectangular", "triangular", "oval", "circular", 
                "cylindrical", "spherical", "cubical", "irregular", "curved", "straight"
            ],
            "color": [
                "red", "green", "blue", "purple", "orange", "yellow", "pink", "black", 
                "white", "gray"
            ],
            "material": [
                "wooden", "metal", "plastic", "glass", "ceramic", "fabric", "leather", 
                "rubber"
            ],
            "age": [
                "old", "new", "ancient", "antique", "modern", "vintage"
            ],
            "condition": [
                "clean", "dirty", "broken", "rusty", "shiny", "dull", "damaged", 
                "pristine"
            ],
            "texture": [
                "smooth", "rough", "soft", "hard", "bumpy", "silky", "fuzzy"
            ],
            "subjective": [
                "beautiful", "ugly", "interesting", "boring", "heavy", "light",
                "happy", "sad", "bright", "dark", "empty", "full",
            ]
        }

        # prompts = {
        #     'animal': '{} in',
        #     'big vehicle': [],
        #     'food': [],
        #     'objects': [],
        #     'person': [],
        #     'place': [],
        #     'plant': [],
        #     'sports': [],
        #     'vehicle': []
        # }

        with open(supclasses_path, 'r') as f:
            self.supclasses = json.load(f)
        
        self.generators = [
            self._gen_prompt_1,
            self._gen_prompt_2,
            self._gen_prompt_3,
        ]
    
    def __call__(self):
        generator = random.choice(self.generators)
        return generator()
    
    def choose_obj(self, types: list):
        obj_sup = random.choice(types)
        obj_cls = random.choice(list(self.supclasses[obj_sup].keys()))
        obj = random.choice(self.supclasses[obj_sup][obj_cls])
        return obj_sup, obj_cls, obj

    def choose_adjs(self, names: list):
        res = []
        for name in names:
            assert name in self.adjectives
            adj = random.choice(self.adjectives[name])
            res.append(adj)
        return res

    def _gen_prompt_1(self):
        doing = [
            "flying",
            "running",
            "walking",
            "crawling",
            "sitting",
            "standing",
            "sleeping",
        ]

        _, obj_cls, obj = self.choose_obj(['animal', 'person'])
        color = random.choice(self.adjectives['color'])
        doing = random.choice(doing)
        place = random.choice(['urban', 'nature', 'near water'])
        prompt = f'The {color} {obj} {obj_cls} is {doing} in the {place}.'
        return prompt

    def _gen_prompt_2(self):
        sports = [
            "archery",
            "badminton",
            "baseball",
            "basketball",
            "billiards",
            "bowling",
            "boxing",
            "bungee jumping",
            "chess",
            "cricket",
            "cycling",
            "diving",
            "dodgeball",
            "fencing",
            "figure skating",
            "football",
            "golf",
            "handball",
            "hockey",
            "horseback riding",
            "ice hockey",
            "judo",
            "karate",
            "kayaking",
            "kickboxing",
            "lacrosse",
            "mixed martialarts",
            "muay thai",
            "paintball",
            "paragliding",
            "rowing",
            "rugby",
            "shooting",
            "skateboarding",
            "surfing",
            "swimming",
            "tabletennis",
            "taekwondo",
            "volleyball",
            "water polo",
            "weight lifting",
            "wrestling"
        ]
        sport = random.choice(sports)
        _, obj_cls_1, obj_1 = self.choose_obj(['animal', 'person'])
        _, obj_cls_2, obj_2 = self.choose_obj(['animal', 'person'])
        place = random.choice(['urban', 'nature', 'near water', 'water'])
        prompt = f'The {obj_1} {obj_cls_1} is playing {sport} with {obj_2} {obj_cls_2} near the {place}.'
        return prompt
        
    def _gen_prompt_3(self):
        size, shape, age, texture, subjective = self.choose_adjs(['size', 'shape', 'age', 'texture', 'subjective'])
        _, obj_cls, obj = self.choose_obj(['person'])
        _, obj_cls2, obj2 = self.choose_obj(['plant'])
        _, obj_cls2, obj2 = self.choose_obj(['plant'])
        scene = random.choice(self.scenes['nature'])
        
        prompt = f'The {obj} {obj_cls} looks at {size}, {shape}, {age}, {texture}, {subjective} {obj2} in the {scene}.'
        return prompt
        



if __name__ == '__main__':
    random.seed(109)

    gen = PromptGenerator('supclasses.json')
    for i in range(10):
        print(gen())

    
    