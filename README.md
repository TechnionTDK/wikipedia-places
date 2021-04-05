# Wikipedia-places  
#### This project was done in the TDK - Technion Data & Knowledge Lab of the CS faculty.  
By Nerya Hadad under the supervision of Dr. Oren Mishali.  
  
#### This project's final product is a server - http request returning json.  
  
#### The server input is:  
Area - location on earth and radius.  
  * location - latitude and longitude ("lat, lon").  
  * radius - number and its unit [mm, cm, m, km...] ("radius").  
  
#### The server output is:  
All Wikipedia entries in Hebrew with location (coordinates) at the defined area.  
Every entry consists of the following data:  
"label" - headline of the Wikipedia page.  
"url" - url of the Wikipedia page.  
"abstract" - this name is taken from Wikipedia dump files and contain the same data. This data is based on the information in the Wikipedia page.Some labels have no abstract.  
  
"pin" - describing the coordinates by {"location" "distance[km]"} where:
  * "location" - location that appears on this Wikipedia page (latitude & longitude).  
  * "distance[km]" - precise distance from the input's location.  

  
""" HTML request would be (2 options):  
http://132.69.8.7/wiki_by_place?radius=xxx&lat,lon=xxx,xxx  
http://132.69.8.7/wiki_by_place?lat,lon=xxx,xxx&radius=xxx  
Examples - up to 1km from the Technion:  
http://132.69.8.7/wiki_by_place?radius=1km&lat,lon=32.7775,35.02166667  
http://132.69.8.7/wiki_by_place?radius=1000m&lat,lon=32.7775,35.02166667  
http://132.69.8.7/wiki_by_place?lat,lon=32.7775,35.02166667&radius=100000cm  
"""
    
    
Entry example (by running http://132.69.8.7/wiki_by_place?lat,lon=31.26373189,34.81106043&radius=1cm):  
[{"label": "פארק גב ים נגב",  
 "pin": {"location": {"lat": 31.26373189, "lon": 34.81106043}, "distance[km]": 0.0},  
 "url": "https://he.wikipedia.org/wiki/פארק_גב_ים_נגב",  
 "abstract": "פארק גב ים נגב הוא פארק תעשיות היי-טק הנבנה בבאר שבע, סמוך לאוניברסיטת בן-גוריון בנגב ולמרכז התקשוב העתידי של צה\"ל."}]  

  
  
## Getting Started

#### These instructions will get you a copy of the project up and running on your machine:

###### 1. Clone:  
Download this repository to your local machine.  
On command line:  
	git clone https://github.com/TechnionTDK/wikipedia-places  
###### 2. Install Python:  
*You can try another version if you already have it  
Windows:  
Download python3 latest version from python official website.  
Linux:  
Install python3 with these commands:  
	sudo apt-get update  
	sudo apt-get install python3.6  
	
###### 3. Python packages:  
Install the following python packages:  
(Versions number are not necessary, but guaranteed to do the job)  
elasticsearch==7.6.0  
Flask==1.1.2  
geopy==1.21.0  
requests==2.23.0  
  
Install a package using the following command:  
	python3 -m pip install packageName  
	
###### 4. Input directory:  
Input was generated by following the instructions [here](https://github.com/TechnionTDK/dbpedia-hebrew)  
And taking it's relevant output as our input (our "input" directory):  
At the mentioned project, under "usage" - there are 3 scripts, only 2 are relevant for our input:  
labels_generator.py, abstract_generator.py. (anchor_texts_generator.py is not relevant)  
You can rerun it to generate updated input.  

###### 5. Install [Elasticsearch](https://github.com/TechnionTDK/project-guidelines/wiki/ElasticSearch)  
Use port 9200 (or change this number on the scripts to your port number)  

###### 6. Build the Elasticsearch:  
Run elastic_builder.py  
Use [screen](https://github.com/TechnionTDK/project-guidelines/wiki/HowTo#how-to-execute-a-long-running-process-on-linux) command to prevent it from stopping, since the download is long.  
  
For testing - after succesfull build:  
Run elasticTestAll.py  

###### 7. Install [Flask](https://github.com/TechnionTDK/project-guidelines/wiki/ExecuteFlaskAppOnLinux)  
Use port 80 (or change the number on server.py to your port)  

###### 8. Run server.py:  
Use [screen](https://github.com/TechnionTDK/project-guidelines/wiki/HowTo#how-to-execute-a-long-running-process-on-linux) command to prevent it from stopping.  
  
  
  
  
##### Other scripts:  
###### poc.py :  
This script is using the files in "poc" folder to prove that elasticsearch is a good fit to our porpuse.

###### search.py :  
Implementation of the actual search for specific area on elastic.  
It's main is running an examples.  
  
##### Other folder:  
###### Output:  
Contains some examples for files that was generated by lines 99-102 at elastic_builder.py. Those lines in comment as it's unnecessary.  
  
    

## Challenges I have faced:  
  * Finding the best solution.  
  The project was defined by the excepted result (this server).  
  Part of the job was to find the best implementation. It's included:  
	  * Finding way to extract coordinates out of wikipedia label.  
	  * Find the best solution for search by area and proof it (POC).  
  * Fixing an older project in order to extract the right abstract.  
  * Trying to get better abstract directly from wikipedia pages.  
  