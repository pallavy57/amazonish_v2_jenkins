podTemplate(label: 'mypod', serviceAccount: 'cd-jenkins', containers: [ 
    containerTemplate(
      name: 'docker', 
      image: 'docker', 
      command: 'cat', 
      resourceRequestCpu: '100m',
      resourceLimitCpu: '300m',
      resourceRequestMemory: '300Mi',
      resourceLimitMemory: '500Mi',
      ttyEnabled: true
    ),
    containerTemplate(
      name: 'kubectl', 
      image: 'allanlei/kubectl',
      resourceRequestCpu: '100m',
      resourceLimitCpu: '300m',
      resourceRequestMemory: '300Mi',
      resourceLimitMemory: '500Mi', 
      ttyEnabled: true, 
      command: 'cat'
    ),
    containerTemplate(
      name: 'helm', 
      image: 'alpine/helm:2.14.0', 
      resourceRequestCpu: '100m',
      resourceLimitCpu: '300m',
      resourceRequestMemory: '300Mi',
      resourceLimitMemory: '500Mi',
      ttyEnabled: true, 
      command: 'cat'
    )
  ],

  volumes: [
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
    // persistentVolumeClaim(
    //   mountPath: '/usr/local/bin/helm', 
    //   hostPath: '/usr/local/bin/helm', 
    //   readOnly: false
    //   )
    //hostPathVolume(mountPath: '/usr/local/bin/helm', hostPath: '/usr/local/bin/helm', accessModes: RWO)
  ]
  ) {
    node('mypod') {

        def REPOSITORY_URI = "pallavy57/amazonishapp_v2"
        def HELM_APP_NAME = "amazonish_v2_jenkins"
        def HELM_CHART_DIRECTORY = "helm/ingress"

        stage('Get latest version of code') {
          checkout scm
        }
        stage('Check running containers') {
            container('docker') {  
                sh 'hostname'
                sh 'hostname -i' 
                sh 'docker ps'
                sh 'ls'
            }
            container('kubectl') { 
                sh 'kubectl get pods -n default'  
            }
            container('helm') { 
                sh 'helm init'
                sh 'helm repo update'     
            }
        }  

        stage('Build Image'){
            container('docker'){

              withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                sh 'docker login --username="${USERNAME}" --password="${PASSWORD}"'
                sh "docker build -t ${REPOSITORY_URI}:${BUILD_NUMBER} ."
                sh 'docker image ls' 
              } 
                
            }
        } 

        // stage('Testing') {
        //     container('docker') { 
        //       sh 'whoami'
        //       sh 'hostname -i' 
        //       sh "docker run ${REPOSITORY_URI}:${BUILD_NUMBER} npm run test "                 
        //     }
        // }

        stage('Push Image'){
            container('docker'){
              withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                sh 'docker image ls'
                sh "docker push ${REPOSITORY_URI}:${BUILD_NUMBER}"
              }                 
            }
        }

        stage('Deploy Image to k8s'){
            container('helm'){
                sh 'helm list'
                sh "helm lint ./${HELM_CHART_DIRECTORY}"
                sh "helm upgrade --wait --timeout 60 --set image.tag=${BUILD_NUMBER} ${HELM_APP_NAME} ./${HELM_CHART_DIRECTORY}"
                sh "helm list | grep ${HELM_APP_NAME}"
            }
        }      
    }
}