# run app on localhost
runserver:
	dev_appserver.py .

# deploy to appspot.com
deploy:
	appcfg.py update .    
