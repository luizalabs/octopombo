export PYTHONPATH=$PYTHONPATH:$(pwd)
	
MESSAGE=$(shell git log --pretty=format:'%an: %h %s' -1)

clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log

lint:
	@flake8 .
	@isort --check

check-vulnerabilities:
	safety check -r requirements.txt

release-patch:
	bumpversion patch

release-minor:
	bumpversion minor

release-major:
	bumpversion major

deploy:
	@teresa deploy create . --app octopombo --description "$(MESSAGE)" --cluster $(cluster)