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
                sh """
                python3 -m venv env
                chmod 754 env/bin/activate
                . env/bin/activate
                which pip
                python3 -m pip -vv install -r requirements.txt
                """
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                sh """
                . env/bin/activate
                which pip
                python3 -m coverage run --source app/main manage.py test
                python3 -m coverage xml
                """
            }
            post {
                always {
                    sh """
                    . env/bin/activate
                    which pip
                    python3 -m python-codacy-coverage -r coverage.xml
                    """
                    junit allowEmptyResults: true, testResults: 'coverage.xml'
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
