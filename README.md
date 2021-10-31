# Image-Colour-Palette-Generator
This simple **Flask**-based website allows you to extract colors from your image files.

Just upload an image and it will give you:
- The image color palette (up to 10 colors)
- The top 20 most common colors in that image including RGB and HEX values and the ratio for each color. 


## Local installation
- Clone this repository.
- Create a new virtual environment.
- Install the required packages `pip install -r requirements.txt`
- Set your app's secret key as `SECRET_KEY` environment variable.
- Run main.py and use the URL displayed in the console to see the application in your browser.


## Deployment
For a deployment on Heroku you will need to setup a config var :

- `HEROKU_DEPLOY_VAR` to let the app know it is running online


## Overview

![alt text](https://github.com/Julien-B-py/Image-Colour-Palette-Generator/blob/main/img/demo.png?raw=true)

Inspired from [Image Color Extract][color-extract] tool.

Deployed and hosted version available here: https://color-palette-jb.herokuapp.com/

[color-extract]: <http://www.coolphptools.com/color_extract#demo>
