pipeline {
  agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
spec:
  # Service Account Name to insert will be provided once previous steps are completed (refer to step 2)
  serviceAccountName: mdm
  restartPolicy: Never
  containers:
  # Add more containers to complete the job
  - name: python3
    image: python:3.10
    command: ['cat']
    tty: true
      - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    imagePullPolicy: Always
    command: ['/busybox/cat']
    tty: true
    resources:
      limits:
        cpu: 1000m   
        memory: 2048Mi        
  - name: jfrogcli
    image: docker.bintray.io/jfrog/jfrog-cli-go:latest
    command: ['cat']
    tty: true
    env:
      - name: DOCKER_HOST
        value: tcp://localhost:2375
    resources:
      limits:
        cpu: 1000m
        memory: 3072Mi
  - name: docker-daemon
    image: docker:19.03.1-dind
    securityContext:
      privileged: true
    env:
      - name: DOCKER_TLS_CERTDIR
        value: ""
    resources:
      limits:
        cpu: 1000m
        memory: 2048Mi   
"""
    }                             
  }
  stages {
        stage('Cloning Git repo') {
      steps {
        git([url: 'https://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@github.cms.gov/EDL/edl-eudc-code.git', branch: 'develop'])
      }

    }  
    stage('ls dir') {
      steps {
        sh 'ls' 
        sh 'sudo yum install docker-engine -y'
        sh 'sudo service docker start'
        sh 'docker --version'
        sh 'cd frontend'
        sh 'docker build --no-cache -f public.Dockerfile .'
      }
      

    }  
}
  parameters {
        string(name: 'ENVIRONMENT', defaultValue:'test',description: 'Env to use')
        choice(name: 'ENVIRONMENT', choices: ['dev','test','impl','prod'],description:'')
  } 
}
