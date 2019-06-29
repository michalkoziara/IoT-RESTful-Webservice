pipeline {
    agent any

    options {
        skipDefaultCheckout()
        skipStagesAfterUnstable()
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
                echo 'Checkout..'
            }
        }
        stage('Build') {
            steps {
                echo 'Building..'
                sh "mkdir env"
                sh "virtualenv -p python3 env"
                sh ". env/bin/activate"
                sh "python3 -m pip install -r requirements.txt"
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                sh "coverage run --source app/main manage.py test"
                sh "coverage xml"
                post {
                    always {
                        sh "python-codacy-coverage -r coverage.xml"
                        junit 'coverage.xml'
                    }
                }
            }
        }
        stage('Deploy to dev') {
            when {
                branch 'dev'
            }

            steps {
                echo 'Deploying to development instance..'
                sh "git push -f git@heroku.com:iot-restful-webservice-dev.git HEAD:master"
            }
        }
        stage('Deploy to prod') {
            when {
                branch 'master'
            }

            steps {
                echo 'Deploying to production instance..'
                sh "git push -f git@heroku.com:iot-restful-webservice-prod.git HEAD:master"
            }
        }
    }
}
