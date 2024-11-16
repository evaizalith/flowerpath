## FlowerPath Companion Planner
FlowerPath Companion Planner - a garden planning system.

## Description
Our product is for flower gardeners who are frustrated with bald patches in their carefully planned gardens and plants that fail to thrive. The FlowerPath Companion Planner is a software tool that, when provided with the dimensions and sun exposure of a garden plot, accurately creates a timeline of how the garden will look throughout the entire growing season. 

## Installation
1. Clone repository onto local device 

2. After locating the main project directory, install requirements via pip install -r requirements.txt

3. Run main program via python main.py 

Alternatively, program can be run through executable if an executable is provided 

##Directions to Create Own Executable File 
1. Create .spec file: # .Spec Generation file: pyinstaller --onefile --windowed --icon="images/flower_icon.ico" --add-data "images;images" --add-data "placeholders_assets;placeholder_assets" --name FlowerPath main.py

2. Regenerate .exe: pyinstaller FlowerPath.spec   

3. Provide images and placeholder images asset folders

## Features
- Users can create a model of their garden by specifiying garden size, sunlight exposure, and soil drainage
- Collision feature shows users full size of plants during seed sowing stage 
- Timeline feature allows users to dynamically observe how their garden will look over an entire growing season, helping them identify bald patches and times of low growth

# Credits
Planned and developed by:
- Amber Martino
- Brandon Jennings
- Eva Powlison
- Katherine Whitmoyer
