dataset:
	@python3 pull-data_old.py 2> pull-data_old.err

clean:
	@rm pull-data.err

spacy:
	cat data1.json | python3 parse-entities.py 2> spacy.err

cleanads:
	cat data.json | python3 clean-ads.py > data1.json

test:
	@python3 pull-links.py 2> pull-data.err | \
	python3 remove-non-news.py 2>> pull-data.err | \
	python3 pull-html.py 2>> pull-data.err | \
	python3 parse-information.py 2>> pull-data.err | \
	python3 clean-ads.py 2>> pull-data.err | \
	python3 parse-entities.py 2>> pull-data.err 1> data.json
