dataset:
	@python3 pull-data_old.py 2> pull-data.err

clean:
	@rm pull-data.err

spacy:
	cat data3.json | python3 parse-entities.py 1> data-parsed-entities.json 2> entities.csv

cleanads:
	cat data2.json | python3 clean-ads.py > data3.json

test:
	@python3 pull-links.py 2> pull-data.err | \
	python3 remove-non-news.py 2>> pull-data.err | \
	python3 pull-html.py 2>> pull-data.err | \
	python3 parse-information.py 2>> pull-data.err | \
	python3 clean-ads.py 2>> pull-data.err | \
	python3 parse-entities.py 2> entities.csv 1> data2.json
