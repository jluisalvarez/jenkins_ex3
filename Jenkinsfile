pipeline {

    agent any

    environment { 
        TAG = sh (returnStdout: true, script: 'date "+%d%m%Y-%H%M%S"').trim()
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                echo "Building..."
                docker build -t jluisalvarez/flask_hello:$TAG .
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
           }
        }
        stage('Publish') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_credentials', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                        echo "Publishing..."
                        docker login -u="${USERNAME}" -p="${PASSWORD}"
                        docker push jluisalvarez/flask_hello:$TAG
                    ''' 
                
                }
            }
        }
        stage('Clean') {
            steps {
                sh '''
                echo "Cleaning..."
                docker rmi jluisalvarez/flask_hello:$TAG
                ''' 
                
           }
        }
        stage('Deploy') {
            steps {
                sh '''
                echo "Deploying..."
                kubectl version --client
                '''
            }
        }
    }
}

