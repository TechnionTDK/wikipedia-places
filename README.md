wikipedia-places  
This project was done in the TDK - Technion Data & Knowledge Lab of the CS faculty.  
By Nerya Hadad under the supervision of Dr. Oren Mishali.  
  
This project's final product is a server - http request returning json.  
  
The server input is:  
Area - location on earth and radius.  
location - latitude and longitude ("lat, lon").  
radius - number and it's unit [mm, cm, m, km...] ("radius").  
  
The server output is:  
All wikipedia entries in Hebrew with coordinates at the defined area.  
Every entry consists of the following data:  
"label" - headline of the wikipedia page.  
"url" - url of the wikipedia page.  
"abstract" - this name is taken from wikipedia dump files and contain the same data. This data is based on the information of the wikipedia page. 
"pin" - describing the coordinates by {"location" "distance[km]"} where:
  * "location" - location that appears on this wikipedia page.  
  * "distance[km]" - precise distance from the input's location.  
    
 
  
""" HTML request would be:  
http://132.69.8.7/wiki_by_place?radius=xxx&lat,lon=xxx,xxx  
http://132.69.8.7/wiki_by_place?lat,lon=xxx,xxx&radius=xxx  
Examples - up to 1km from the Technion:  
http://132.69.8.7/wiki_by_place?radius=1km&lat,lon=32.7775,35.02166667  
http://132.69.8.7/wiki_by_place?radius=1000m&lat,lon=32.7775,35.02166667  
http://132.69.8.7/wiki_by_place?lat,lon=32.7775,35.02166667&radius=100000cm  
"""
  


Getting Started

These instructions will get you a copy of the project up and running on your machine:

1. Clone:
download this repository to your local machine.
On command line:
	git clone https://github.com/TechnionTDK/wikipedia-places
2. Python:
U can try newer version if u already have
Windows:
download python3 latest version from python official website
Linux:
install python3 with these commands:
	sudo apt-get update
	sudo apt-get install python3.6
	
3. Python packages
install the following python packages:
(Versions number r not necessity)
elasticsearch==7.6.0
Flask==1.1.2
geopy==1.21.0
requests==2.23.0

install a package using the following command:
On command line:
	python -m pip install SomePackage
	
4. Input directory:
Input was generated by following the instructions [here](https://github.com/TechnionTDK/dbpedia-hebrew)
And taking it's output as our input ("input" directory).
U can rerun it to generate updated input.

5. Install [Elasticsearch](https://github.com/TechnionTDK/project-guidelines/wiki/ElasticSearch)
Use port 9200 (or change the number on the scripts to your port)

6. Build the Elasticsearch:
Run elastic_builder.py
For testing - after succesfull build:
Run elasticTestAll.py

7. Install [Flask](https://github.com/TechnionTDK/project-guidelines/wiki/ExecuteFlaskAppOnLinux)
Use port 80 (or change the number on server.py to your port)

8. Run server.py:
Use [screen](https://github.com/TechnionTDK/project-guidelines/wiki/HowTo#how-to-execute-a-long-running-process-on-linux) command to prevent it from stopping.

Other scripts:
poc.py :
This script is using the files in "poc" folder to prove that elasticsearch is a good fit to our porpuse.

search.py :
Implementation of the actual search for specific area on elastic.
It's main is running an example.