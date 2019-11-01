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
                echo 'Checkout..'
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo 'Building..'
                sh """
                python3 -m venv env
                chmod 754 env/bin/activate
                . env/bin/activate
                python3 -m pip install -r requirements.txt
                """
            }
        }
        stage('Run unit tests') {
            steps {
                echo 'Running unit tests..'
                sh """
                . env/bin/activate
                pytest app/test/unittest/ --cache-clear -rxs -v --junitxml=unit_test_report.xml
                """
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'unit_test_report.xml'
                }
            }
        }
        stage('Run integration tests') {
            steps {
                echo 'Running integration tests..'
                sh """
                . env/bin/activate
                pytest app/test/integrationtest/ --cache-clear -rxs -v --junitxml=integration_test_report.xml
                """
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'integration_test_report.xml'
                }
            }
        }
        stage('Send data to static code analyser') {
            steps {
                echo 'Sending test data to static code analyser..'
                sh """
                . env/bin/activate
                pytest app/test/ --cache-clear -rxs -v --cov=. --cov-report=xml --cov-config=.coveragerc
                """
            }
            post {
                always {
                    withCredentials([string(credentialsId: 'codacy-project-token', variable: 'CODACY_PROJECT_TOKEN')]) {
                        sh """
                        . env/bin/activate
                        export CODACY_PROJECT_TOKEN=$CODACY_PROJECT_TOKEN
                        python-codacy-coverage -r coverage.xml
                        """
                    }
                }
            }
        }
        stage('Deploy to development') {
            when {
                branch 'dev'
            }

            steps {
                echo 'Deploying to development instance..'
                sh "git push -f git@heroku.com:iot-restful-webservice-dev.git HEAD:master"
            }
        }
        stage('Deploy to production') {
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
