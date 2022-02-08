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
    stage('Cloning Git repo') {
      steps {
        git([url: 'https://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@github.cms.gov/EDL/edl-eudc-code.git', branch: 'develop'])
      }

    }  
    
    stage('ls dir') {
      steps {
        sh 'pwd'
        sh 'ls' 
      }
      
      

    } 

    stage('Get Dockerfile From Version Control') {      
	  steps 
	  {
        // get the dockerfile checked out to the Kaniko container, so it can find it  does $WORKSPACE mount here?
		container(name: 'kaniko', shell: '/busybox/sh') {
		   echo "The Cloudbees Core execution workspace environment variable value in Kaniko container is: $WORKSPACE"
		
		   // creating image directory to place image into
		   sh '''#!/busybox/sh
		   mkdir ${WORKSPACE}/image/
		   '''
       echo "kinoko directory"
		   sh 'pwd'
       sh '''#!/busybox/sh
            /kaniko/executor --context `/home/jenkins/agent/workspace/EDL-Eudc2/frontend/public.Dockerfile` --skip-tls-verify --no-push --destination=devops-cbc-pipeline-primary:debug --tarPath=${WORKSPACE}/image/amundsen-frontend.tar
          '''
		  //  dir('definitions') {
		  //     script 
		  //     {
			//      handleSCMRepoCheckout("https://github.com/Amar-Ahmed/docker-file.git", "master")
		  //     }
			  
			  
			//   sh '''#!/busybox/sh
			//   /kaniko/executor --context `pwd` --skip-tls-verify --no-push -c /workspace --dockerfile ${WORKSPACE}/definitions/MDM-2021-Cloudbees-Core-DevOps/Dockerfile --destination=devops-cbc-pipeline-primary:debug --tarPath=${WORKSPACE}/image/amundsen-frontend.tar
			//   ls -altr
			  
			//   '''
			  
		  //  }
		   
		   // figure out where image was written to locally within Kaniko container
		   
		   sh '''#!/busybox/sh
		   ls -altr ${WORKSPACE}/image/
		   '''
        echo "last step"
		    sh 'pwd'
        sh 'ls' 
		   
		}
	  }
	  
	}  
}
  parameters {
        string(name: 'ENVIRONMENT', defaultValue:'test',description: 'Env to use')
        choice(name: 'ENVIRONMENT', choices: ['dev','test','impl','prod'],description:'')
  } 
}
