error_file = pull-data.err

# Our makefile is directly connected to the pipeline descrbied in the report and can easily be 
# understood by reading that chapter.

# run "make" to execute this target that executes the whole pipeline
all: pulllinks removenonnews pullhtml parseinfo cleanads spacy jsontocsv characterization

# Old script that can still be used for debug purposes
dataset:
	@python3 pull-data_old.py 2> pull-data_old.err

clean:
	@rm pull-data.err

pulllinks:
	@python3 pull-links.py 2>$(error_file) 1>links.json
	@echo "Successfully pulled links from cdx"

removenonnews:
	@python3 remove-non-news.py 2>>$(error_file) 1>news.json <links.json
	@rm links.json
	@echo "Removed non news from links"

pullhtml:
	@python3 pull-html.py 2>>$(error_file) 1>html.json <news.json
	@rm news.json
	@echo "Obtained HTML for all websites"

parseinfo:
	@python3 parse-information.py 2>>$(error_file) 1>information.json <html.json
	@rm html.json
	@echo "Parsed information successfully"

cleanads:
	@python3 clean-ads.py 2>>$(error_file) 1>cleaned.json <information.json
	@rm information.json
	@echo "Cleaned ads from news"

spacy:
	@python3 parse-entities.py 2>>$(error_file) 1>entities.json <cleaned.json
	@rm cleaned.json
	@echo "Parsed entities from news"

jsontocsv:
	@[ -d "csv" ] || mkdir csv
	@python3 json_to_csv.py 2>>$(error_file) <entities.json
	@[ -e "entities.csv" ] && mv entities.csv csv
	@rm entities.json
	@echo "Created csv files"

characterization:
	@python3 characterization.py save 2>>$(error_file)
