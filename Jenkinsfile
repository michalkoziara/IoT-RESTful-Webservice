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
                python3 -m pip install -r requirements.txt
                """
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                sh """
                . env/bin/activate
                pytest app/test/ --cache-clear -rxs -v --cov=. --cov-report=xml --cov-branch --cov-config=.coveragerc --junitxml=unit_test_report.xml
                """
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'unit_test_report.xml'

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
