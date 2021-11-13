dataset:
	@python3 pull-data.py 2> pull-data.err

clean:
	@rm pull-data.err

test:
	@python pull-links.py 2> pull-data.err | python remove-non-news.py 2>> pull-data.err | python pull-html.py 2>> pull-data.err | python parse-information.py 2>> pull-data.err 1P> data2.json