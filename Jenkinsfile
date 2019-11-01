pipeline {
    agent any
    environment {
        DOCKER_IMAGE_TEST = "$BUILD_NUMBER-test"
    }

    options {
        skipDefaultCheckout()
        skipStagesAfterUnstable()
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checkout..'
                checkout scm
            }
        }
        stage('Build test env') {
            steps {
                echo 'Building..'
                sh """
                docker build --target app -t $DOCKER_IMAGE_TEST .
                """
            }
        }
        stage('Run tests') {
            parallel {
                stage('Run unit tests') {
                    agent {
                        docker {
                            alwaysPull false
                            image $DOCKER_IMAGE_TEST
                        }
                    }
                    steps {
                        echo 'Running unit tests..'
                        sh """
                        pytest app/test/unittest/ --cache-clear -rxs -v --junitxml=unit_test_report.xml
                        """
                    }
                }
                stage('Run integration tests') {
                    agent {
                        docker {
                            alwaysPull false
                            image $DOCKER_IMAGE_TEST
                        }
                    }
                    steps {
                        echo 'Running integration tests..'
                        sh """
                        pytest app/test/integrationtest/ --cache-clear -rxs -v --junitxml=integration_test_report.xml
                        """
                    }
                }
            }
            post {
                always {
                    sh """docker rmi $DOCKER_IMAGE_TEST"""
                    junit allowEmptyResults: true, testResults: '*_test_report.xml'
                }
            }
        }
        stage('Send to static code analyser') {
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
