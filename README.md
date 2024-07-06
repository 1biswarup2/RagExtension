# RagExtension
## Introduction
This Chrome extension fetches content from a webpage when activated. Users can chat or ask questions related to the webpage content, as well as engage in general or casual chats. This README will guide you through the structure of the extension and explain the functionality of each file in the project.

## Table of Contents
1. Installation
2. Usage
3. ### Folder Structure:
     i. .env 
    ii.  app.py 
   iii. background.js 
    iv. content.json 
     v. HTMLLoader.py 
    vi. icon.png 
   vii. manifest.json 
  viii. popup.html 
    ix. popup.js 
     x. requirements.txt 
## Installation
To install and use the extension, follow these steps:

1.Clone the repository to your local machine.
2.Navigate to chrome://extensions/ in your Chrome browser.
3.Enable "Developer mode" by toggling the switch in the top right corner.
4.Click on "Load unpacked" and select the extension folder.
## Usage
1. Click on the extension icon in the Chrome toolbar.
2. A popup will appear where you can chat or ask questions related to the current webpage.
3. The extension can handle both specific queries about the webpage and general/casual chats.
## Folder Structure
### .env
The .env file contains environment variables used by the extension.


### app.py
The app file is a Python source file that includes the main application logic for handling chat interactions and processing user queries.


### background.js
The background.js file is a JavaScript source file that runs in the background, handling events such as browser actions and messaging between different parts of the extension.


### content.js
The content.js file is a JavaScript source file that interacts with the webpage content. It is injected into the webpage and can extract information that is then used by the extension.


### HTMLLoader.py
The HTMLLoader.py file is a Python source file responsible for loading and processing HTML content from the webpages.


### icon.png
The icon.png file is the icon for the Chrome extension.


### manifest.json
The manifest.json file is a JSON source file that defines the extension's properties, permissions, and entry points.


### popup.html
The popup.html file is an HTML file that defines the user interface of the extension's popup.


### popup.js
The popup.js file is a JavaScript source file that manages the interaction within the popup, handling user inputs and displaying responses.


### requirements.txt
The requirements.txt file lists the Python dependencies needed to run the extension's backend.
