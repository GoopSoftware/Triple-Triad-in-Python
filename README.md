# Triple Triad Remake

## Description
This project is a remake of final fantasy 8's triple triad card game. This project was intended to test out pyautogui.
However it evolved into learning scraping, tesseract, classes, image detection, and pygame. 

## Features
- Player turns
- Random card drawing
- Cards with number values
- Ability to take other players cards
- Score system based on who has more cards


## Scraping
In order to download the cards I made a program to scrape all images from a website. I learned how to interact
with the html of the website.

## Tesseract
This was my first time using tesseract. I used tesseract to read the number values on the top left of each card. 
Unfortunately at first I could only get about 15% accuracy. I learned how to filter a picture in order to get a better
read of numbers resulting in a slightly higher accuracy. Finally I split the cards into 3 and ran it though the program
a final time and got about 55% accuracy. I was happy with this number so I went and input the rest of the numbers myself.

## Classes
This was my first time using classes. I created a card class that takes input from a txt file that I saved my tesseract
reading into. This applied the numbers to the __init__ of the card class. I added the ability to tell if a card with
a higher number can take a card with a lower number next to it. Finally I added card ownership between players so that
a player can not take their own card and increase their score.

## Image Detection
I created a couple functions to detect the image in a grid and check the folder of downloaded_images for the image.
The functions iterate through the whole folder and returns the name of the card. I then used those functions in the main
script to detect what cards are being played. It then saves the image as a temporary file, iterates through to detect
what card it is, assigns the card values, then finally stores the card in the grid for later.

## Pygame
This is my first ever game developed in pygame. It was a ton of fun giving it a test. I will admit I used chatgpt
more than I wish I did. However, I still learned so much from this project and I look forward to building future games
in python!