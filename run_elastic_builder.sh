rm ~/wikipedia-places/input/wiki_hebrew_labels.json &
cd ~/dbpedia-hebrew &
python3 labels_generator.py &
cp output/wiki_hebrew_labels.json ~/wikipedia-places/input &
cd ~/wikipedia-places &
source env/bin/activate &
python elastic_builder.py &