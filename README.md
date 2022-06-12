# Wikipedia Places API


> This project's final product is a server- http request returning json.


## Introduction:
* This project was done in the TDK - Technion Data & Knowledge Lab of the CS faculty By Nerya Hadad under the supervision of Dr. Oren Mishali, and updated later by Tzahi Levi, and Raz Levi.


## Prerequisite:
* The app is based on [another project](https://github.com/TechnionTDK/dbpedia-hebrew) that provides all wikipedia's labels.
* The app uses [Nominatim API](https://nominatim.org/release-docs/develop/api/Overview/) for Place Details requests.


## Server Structure:
<p align="center">
    <img src="/assets/app_structure.jpeg" alt="drawing" width="200"/>
</p>


## API:
### wiki_by_place
##### Parameters:
* lat- location's latitude.
* lon- location's longitude.
* radius- a number and it's unit [mm, cm, m, km...].
* [optional] from- an index to start receiving the data from (using for pagination).
* [optional] size- number of places for receiving (using for pagination).


##### Output: All Wikipedia entries in Hebrew with location (coordinates) at the defined area-
* label- the headline of the Wikipedia page.
* url- url of the Wikipedia page.
* abstract- the first 5 sentences of the wikipedia article. some labels have no abstract.
* imageUrl- image url of the Wikipedia page. some labels have no imageUrl.
* pin- {distance[km], location: {lat, lon}} of the article.


##### Request Examples:  
* http://132.69.8.15:80/wiki_by_place?radius=xxx&lat,lon=xxx,xxx
* http://132.69.8.15:80/wiki_by_place?lat,lon=xxx,xxx&radius=xxx
* http://132.69.8.15:80/wiki_by_place?radius=1km&lat,lon=32.7775,35.02166667
* http://132.69.8.15:80/wiki_by_place?radius=1000m&lat,lon=32.7775,35.02166667


### place_details_by_name
##### Parameters:
* name- partially place's name or pattern.


##### Output: the full name and the coordinates of the given name
* name- full place's name.
* lat- place's latitude.
* lon- place's longitude.


##### Request Examples:  
* http://132.69.8.15:80/place_details_by_coordinates?name=xxx
* http://132.69.8.15:80/place_details_by_coordinates?name=ירושלים


### place_details_by_coordinates
##### Parameters:
* lat- place's latitude.
* lon- place's longitude.


##### Output: the full name of the given place
* name- full place's name.


##### Request Examples:  
* http://132.69.8.15:80/place_details_by_name?lat=xxx&lon=xxx
* http://132.69.8.15:80/place_details_by_name?lat=32.7775&lon=35.02166667


### get_suggestions
##### Parameters:
* name- full place's name.


##### Output:
* suggestions- list of full place's names that includes the given name.


##### Request Examples:  
* http://132.69.8.15:80/get_suggestions?name=xxx
* http://132.69.8.15:80/get_suggestions?name=ירושלים


## Instruction for running the server:
### 1. Clone:
* Clone this repository to your local machine.
> git clone https://github.com/TechnionTDK/wikipedia-places


### 2. Install Python:
#### Windows:
* Download python3 latest version from python official website.
#### Linux:
* Install python3 with these commands:
> sudo apt-get update
> sudo apt-get install python3.6


### 3. Fill input directory:  
* Input was generated following the instructions [here](https://github.com/TechnionTDK/dbpedia-hebrew). There are 3 scripts, only 1 is relevant for our input.
* Clone this repository.
* Run labels_generator.py only.
* Take it's output to our repository in input/all_labels directory. 


### 4. Python packages:
* Install some python packages automatically by running:
> pip install -r requirements.txt
* You can do it manually by running:
> python3 -m pip install packageName
* While the packageNames are:
* elasticsearch==7.6.0
* Flask==1.1.2
* geopy==1.21.0
* requests==2.23.0
* Jinja2==3.0.3
* itsdangerous==2.0.1
* werkzeug==2.0.2


### 5. Verify Python packages were successfully installed:
* verify that you have installed the right packages using:
> pip list


### 6. Create virtual environment
* Run the following commands for creating a virtual environment:
> python3.7 -m venv env
> source env/bin/activate
* Use port 80 (or change the number on server.py to your port)
* More information if needed: https://github.com/TechnionTDK/project-guidelines/wiki/ExecuteFlaskAppOnLinux


### 7. Setup Elasticsearch
#### Linux:
* Run the following commands in your home directory:
> cd ~
> wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.0-linux-x86_64.tar.gz
> tar -xf elasticsearch-7.6.0-linux-x86_64.tar.gz
> cd elasticsearch-7.6.0/
> bin/elasticsearch
* Use port 9200 (or change this number on the scripts to your port number).     

#### Windows:
* see: https://github.com/TechnionTDK/project-guidelines/wiki/ElasticSearch


### 8. Build the Elasticsearch:
* This phase is very long and can take several days- you should use [screen](https://github.com/TechnionTDK/project-guidelines/wiki/HowTo#how-to-execute-a-long-running-process-on-linux) command to prevent it from stopping.
* This builder takes all the wikipedia labels and parse it- filter the articles with coordinates and add the imageUrl and the first paragraph of the article. in the end, it creates the indices for Elasticsearch.
* Run the elastic_builder.py using [screen](https://github.com/TechnionTDK/project-guidelines/wiki/HowTo#how-to-execute-a-long-running-process-on-linux) command:
> screen
> python elastic_builder.py
* For checking the process, see the logs in the report_file.txt.
> cat report_file.txt
* if problem is occurred, you can continue running the script from the middle (all parsed data is saved locally). print report_file.txt and check what file the process is stopped. use the argument --file (-f) <x> for continuing from the file number <x>. use the argument --index (-i) if you have the all parsed data, and you want to pass the parsing and only index the elastic search.

### 9. Run server.py:  
* Run the Flask's server.
* Use [screen](https://github.com/TechnionTDK/project-guidelines/wiki/HowTo#how-to-execute-a-long-running-process-on-linux) command to prevent it from stopping.
> python server.py
* If you got a permission denied error, run:
> sudo env/bin/python server.py


### 10. Your server is up now and can be communicated.


## Reindex The server:
* Every time you wants to rebuild the server, run the virtual environment again:
> source env/bin/activate
* For reindex the server, you can just run elastic_builder.py again.
