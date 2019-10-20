# IoT-RESTful-Webservice
RESTful Webservice for IoT devices management.

## CLI commands

Create database migration file  
``python manage.py db migrate``

Update database with latest migration file   
``python manage.py db upgrade``

Run application  
``python manage.py run``

Print configured application routes  
``python manage.py get_routes``

Run all tests  
``python manage.py test``

Run unit tests  
``python manage.py test_unit``

Run integration tests  
``python manage.py test_integration``

Run all tests and generate coverage report in HTML format  
``pytest app/test/ --cov=. --cov-report=html --cov-branch --cov-config=.coveragerc --cache-clear``

Run unit tests and generate coverage report in HTML format  
``pytest app/test/unittest --cov=. --cov-report=html --cov-branch --cov-config=.coveragerc``

Run integration tests and generate coverage report in HTML format  
``pytest app/test/integrationtest --cov=. --cov-report=html --cov-branch --cov-config=.coveragerc --cache-clear``
