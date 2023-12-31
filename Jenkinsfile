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
      image: 'alpine/helm:3.13.2', 
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
        def HELM_APP_NAME_1 = "amazonishv2"
        def HELM_CHART_DIRECTORY_1 = "helm/postgres"
        def HELM_APP_NAME_2 = "amazonishv2app"
        def HELM_CHART_DIRECTORY_2 = "helm/app"
        def HELM_APP_NAME_3 = "ingress-service"
        def HELM_CHART_DIRECTORY_3 = "helm/ingress"

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
                sh 'helm repo add stable https://charts.helm.sh/stable'
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

        stage('Deploy postgres helm chart to k8s'){
            container('helm'){
                sh 'helm list'
                sh "helm lint ./${HELM_CHART_DIRECTORY_1}"
                sh "helm upgrade --set image.tag=${BUILD_NUMBER} ${HELM_APP_NAME_1} ./${HELM_CHART_DIRECTORY_1}"
                sh "helm list | grep ${HELM_APP_NAME_1}"
            }
        }   

        stage('Deploy app helm chart to k8s'){
            container('helm'){
                sh 'helm list'
                sh "helm lint ./${HELM_CHART_DIRECTORY_2}"
                sh "helm upgrade --set image.tag=${BUILD_NUMBER} ${HELM_APP_NAME_2} ./${HELM_CHART_DIRECTORY_2}"
                sh "helm list | grep ${HELM_APP_NAME_2}"
            }
        }   

        stage('Deploy Image to k8s'){
            container('helm'){
                sh 'helm list'
                sh "helm lint ./${HELM_CHART_DIRECTORY_3}"
                sh "helm upgrade --set image.tag=${BUILD_NUMBER} ${HELM_APP_NAME_3} ./${HELM_CHART_DIRECTORY_3}"
                sh "helm list | grep ${HELM_APP_NAME_3}"
            }
        }      
    }
}