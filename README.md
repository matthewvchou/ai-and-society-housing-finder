# AI and Society (CSE 40171) - Housing in NYC Model
Final Project for Notre Dame AI and Society (CSE 40171 - Spring 2025)

# Members:
* Matthew Chou
* Angel Ortiz
* Kyle Phan
* Michael Zang

# Documentation

Our NYC housing finder allows individuals to find the perfect rental unit based on their needs. We utilizes a wide variety of technologies. First, we pre-processed a NYC government crime dataset that measured varying crimes and the busyness of varying zipcodes. These two metrics allowed us to better understand the underlying nature of a specific NYC neighborhood (in any of the 5 boroughs!). We then asked our users to decide their preferences (which one they care about most). Users can choose from safety, price, and livability (busyness). 

Then, we ask our user what their estimated price range would be, and also how many individuals will be living in this rental unit. Further implementation would be to add more specific measures such as proximity to work, number of bathrooms, pet-friendly, etc. After this, each neighborhood/zipcode is assigned a composite score (lowest score wins, similar to golf!)

From here, we query [StreetEasyAPI](https://rapidapi.com/realestator/api/streeteasy-api) via RapidAPI with our designated parameters, and get back the top 10 rental units for our user. Once we receive these, we utilized [Geopy](https://geopy.readthedocs.io/en/stable/) to reverse geocode the latitude and longitude values into zipcodes, and then mapped these zipcodes to the corresponding neighborhood.

Once we get the neighborhood, we utilized [PRAW (Python's Reddit API Wrapper)](https://praw.readthedocs.io/en/stable/) to find reddit threads in the r/askNYC subreddit that gauged what living in the varying neighborhoods was like. From here, we leveraged [LangChain](https://github.com/langchain-ai/langchain) to perform a sentiment analysis on the top 5 comments from the top reddit post related to the livability of a specific neighborhood. We tagged the streeteasy listing and neighborhood with this, and offered the user a comprehensive view of what each of their options looks like.

# Running our Application

1. Create virtualenv

`python3 -m venv virtualenv`

`source virtualenv/bin/activate`

2. Download requirements.txt

`pip3 install -r requirements.txt`

3. Run file

`python3 main.py`

4. Follow instructions and happy apartment hunting!
