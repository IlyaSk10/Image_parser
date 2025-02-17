from scrapper import Scrapper

import json

file_path = 'file.json'

with open(file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

obj = Scrapper(query=data['query'], number_images=data['number_images'], format=data['format'],
               min_dimension=data['min_dimension'])
obj.get_url()
