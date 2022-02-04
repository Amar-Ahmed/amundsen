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
"""
    }
  }
  stages {
    // Add any other stages and/or steps to complete the job
        stage('Cloning Git repo') {
      // steps {
      //   git([url: 'https://github.cms.gov/EDL/edl-eudc-code.git', branch: 'master', credentialsId: 'github-user-token'])

      // }
            steps {
       sh 'npm -v'
        }
    }  
}
  parameters {
        string(name: 'ENVIRONMENT', defaultValue:'test',description: 'Env to use')
        choice(name: 'ENVIRONMENT', choices: ['dev','test','impl','prod'],description:'')
  } 
}