pipeline {
  environment {
    imagename = "amundsenfrontend"
    registryCredential = 'dockerhub'
    dockerImage = ''
  }
    agent {
        docker {
            image 'node:6-alpine'
            args '-p 3000:3000 -p 5000:5000'
        }
    }
  stages {
    stage('Cloning Git repo') {
      steps {
        git([url: 'https://github.cms.gov/EDL/edl-eudc-code.git', branch: 'master', credentialsId: 'github-user-token'])

      }
    }
   stage('Build') {
      steps {
       sh 'npm install'
        }
    }
    stage('Run unit test cases') {
      steps {
       sh 'npm run test'
        }
    }
    stage('Building image') {
      steps{
        script {
          dockerImage = docker.build imagename
        }
      }
    }
    stage ('Artifactory configuration') {
      steps {
            rtServer (
              id: "ARTIFACTORY_SERVER",
               url: SERVER_URL,
               credentialsId: CREDENTIALS
           )
       }
     }
    stage ('Push image to Artifactory') {
      steps {
             rtDockerPush(
                serverId: "ARTIFACTORY_SERVER",
                image: ARTIFACTORY_DOCKER_REGISTRY + '/images:latest',
                // Host:
                // On OSX: "tcp://127.0.0.1:1234"
                // On Linux can be omitted or null
                host: HOST_NAME,
                targetRepo: 'docker-local',
                // Attach custom properties to the published artifacts:
                properties: 'project-name=docker1;status=stable'
             )
        }
      }
    stage('Remove Unused docker image') {
      steps{
        sh "docker rmi $imagename:$BUILD_NUMBER"
         sh "docker rmi $imagename:latest"

      }
    }
  }
}