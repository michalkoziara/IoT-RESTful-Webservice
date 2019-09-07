# IoT-RESTful-Webservice
RESTful Webservice for IoT devices management.

### CLI commands

Run application  
``python manage.py run``

Print configured application routes  
``python manage.py routes``

Run all tests  
``python manage.py test``

Run unit tests  
``python manage.py testunit``

Run integration tests  
``python manage.py testintegration``

Run all tests and generate coverage report in HTML format  
``pytest app/test/ --cov=. --cov-report=html --cov-branch --cov-config=.coveragerc --cache-clear``

Run unit tests and generate coverage report in HTML format  
``pytest app/test/unittest --cov=. --cov-report=html --cov-branch --cov-config=.coveragerc``

Run integration tests and generate coverage report in HTML format  
``pytest app/test/integrationtest --cov=. --cov-report=html --cov-branch --cov-config=.coveragerc --cache-clear``
