# Jenkins Example 2. Pipeline Job

## Requisitos

- Java
- Docker
- Jenkins

## Pipeline

- Crea un Tarea de Pipeline

- En Pipeline, elige Pipeline Script e introduce el siguiente código:

```
pipeline {

    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
           }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
            }
        }
    }
}
```

En el enlace Pipeline Syntax puedes acceder a un generador de código que te puede ayudar a completar la sistaxis de la pipeline.

- Pulsa en Guardar

- Ejecuta la tarea y comrpueba el resultado. Navega por las diferentes opciones de la ejecución.

## Jenkinsfile

Crea el fichero Jenkinsfile con el contenido anterior, crea un repositorio en Github y sube este fichero. 

Modifica la tarea para que utilice el repositorio git, obtenga la pipeline de este fichero Jenkinsfile y se ejecute cada vez que hagas un push en el repositorio.

Para ello:

- En "Configurar el origen del código fuente": Repositorio Git

- En "Disparadores de ejecuciones": GitHub hook trigger for GITScm polling.
NOTA: Es necesario añadir un WebHook a este repositorio de Github, con URL http://<jenkins_server>/github-webhook/, par que se ejecute con cada PUSH.

- En Pipeline, elige Pipeline Script fron SCM; en Repository URL incluye la URL del repositorio; no son necesarias credenciales si en un repositorio público; en Branch escribe el nombre de la rama y en Script Path indica la ruta al fichero Jenkinsfile.

## Jenkinsfile: contenerizar app y subir imagen a Docker Hub

Ahora, cada vez que subamos una nueva versión a nuestro repositorio Github se activará la tarea y se ejecutará la Pipeline tal como se describa en el fichero Jenkinsfile. 

Cambia ahora el contenido del fichero Jenkinsfile a:

```
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
                echo 'Deploying...'
            }
        }
    }
}
```

Sube la nueva versión al repositorio git, comprueba que la tarea de ejecuta y que los resultados son los esperados



## GKE

pipeline {
    agent any

    stages {
        stage('File contenet') {
            steps {
                withCredentials([file(credentialsId: 'gcp_credentials', variable: 'GC_KEY')]) {
                    withEnv(["KUBECONFIG=/var/lib/jenkins/.kube/config"]) {
                      sh("gcloud auth activate-service-account --key-file=${GC_KEY}")
                      sh("kubectl version")
                    }
                }
                     
            }
        }
    }
}
