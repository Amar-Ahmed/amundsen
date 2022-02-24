def handleSCMRepoCheckout(urlToUse, branchToGet) {     
	    
	git  url: urlToUse, branch: branchToGet		
	
}
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
    stage('Cloning EUDC Git repo') {
      steps {
        git([url: 'https://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@github.cms.gov/EDL/edl-eudc-code.git', branch: 'develop'])
      }
    }  
    
    stage('EUDC workspace') {
      steps {
        sh 'pwd'
        sh 'ls' 
      }
    } 
    stage('Build image using Dockerfile & upload to Artifactory') {      
	  steps 
	  {
        // get the dockerfile checked out to the Kaniko container, so it can find it  does $WORKSPACE mount here?
		container(name: 'kaniko', shell: '/busybox/sh') {
      container('jfrogcli'){
      withCredentials([usernamePassword(credentialsId: 'JFROG_CLI_CREDS', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
      sh '/usr/local/bin/jfrog config add cms-artifactory --artifactory-url=https://artifactory.cloud.cms.gov/artifactory --user="${USER}" --password="${PASS}"'
          }
      echo 'loggined into jFrog'
      sh '''
        echo "Building metadata image from docker file"
        apk add docker
			  ls -al
        pwd
			  echo "List docker images"
        /usr/local/bin/jfrog config show cms-artifactory 
        echo "Server info"
			  /usr/local/bin/jfrog rt docker-pull artifactory.cloud.cms.gov/edl-docker-prod-local/images/python:3.7-slim edl-docker-prod-local
        ls -al
        cd metadata
        docker build --no-cache -f public.Dockerfile .
        image_ID=$(docker images --format='{{.ID}}' | head -1)
        docker save -o amundsenmetadatalibrary-test.tar "$image_ID"
        echo "uploading metadata build to jFrog Artifactory"
        /usr/local/bin/jfrog rt del edl-docker-prod-local/latest/metadata/latest/
        docker tag "$image_ID" artifactory.cloud.cms.gov/edl-docker-prod-local/latest/metadata:latest
        docker push artifactory.cloud.cms.gov/edl-docker-prod-local/latest/metadata:latest
        /usr/local/bin/jfrog rt u amundsenmetadatalibrary-test.tar edl-docker-prod-local/latest/
		  '''  
      }
        echo "Metadata build was sucessfully pushed to Artifactory"
		}
	  }
	  
	}  
} 
}