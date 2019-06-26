pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checkout..'
                checkout scm
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
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
