dataset:
	@python3 pull-data.py 2> pull-data.err

clean:
	@rm pull-data.err

test:
	@python3 pull-links.py 2> pull-data.err | 
	python3 remove-non-news.py 2>> pull-data.err | 
	python3 pull-html.py 2>> pull-data.err | 
	python3 parse-information.py 2>> pull-data.err 1> data2.json