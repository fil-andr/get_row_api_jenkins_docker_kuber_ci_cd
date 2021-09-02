pipeline {
    agent { label 'master' }
    triggers {pollSCM('* * * * *')}
    stages {
        stage ('clone from git repo'){
            steps{
                git 'https://github.com/fil-andr/get_row_api_jenkins_docker_kuber_ci_cd.git'
            }
        }
        stage ('unit tests'){
           steps{
                sh 'cd /docker_test/venv_jenkins && source venv_jenkins/bin/activate && pytest ${WORKSPACE}/app/tests.py -v'
           }
        }
        stage ('build docker image'){
            steps{
                sh 'cd ${WORKSPACE}/ && docker build -t 239534/get_row_api:v${BUILD_NUMBER} -f dockerfile_get_row_api .'
            }
        }
        stage ('push image to docker registry'){
            steps{
                withCredentials([string(credentialsId: 'docker_hub_pswd', variable: 'dockerhubpwd')]){
                    sh 'docker login -u 239534 -p ${dockerhubpwd}'
                    sh 'docker push 239534/get_row_api:v${BUILD_NUMBER}'
                }
            }
        }
        stage ('kubernetes deploy new ver.'){
            steps{
                sh 'scp ${WORKSPACE}/get_row_api.yml root@192.168.0.42:/kuber_manifests/jenkins_manifests/get_row_api/'
                sh 'scp ${WORKSPACE}/tag_ver_replace.sh root@192.168.0.42:/kuber_manifests/jenkins_manifests/get_row_api/'
                sh 'ssh root@192.168.0.42 /usr/bin/bash /kuber_manifests/jenkins_manifests/get_row_api/tag_ver_replace.sh v${BUILD_NUMBER}'
                sh 'ssh root@192.168.0.42 kubectl apply -f /kuber_manifests/jenkins_manifests/get_row_api/get_row_api.yml'
            }
        }
        stage ('application health test'){
            steps{
                sh 'scp ${WORKSPACE}/app_health_check.sh root@192.168.0.42:/kuber_manifests/jenkins_manifests/get_row_api/'
                sh 'ssh root@192.168.0.42 /usr/bin/bash /kuber_manifests/jenkins_manifests/get_row_api/app_health_check.sh'
            }
        }
    }
    post {
        success {
            script {
                withCredentials([string(credentialsId: 'TG_TOKEN', variable: 'TOKEN'),
                string(credentialsId: 'TG_GROUP_ID', variable: 'CHAT_ID')])
                {sh "curl -s -X POST https://api.telegram.org/bot${TOKEN}/sendMessage -d chat_id=${CHAT_ID} -d text=\"job ${env.BUILD_TAG} build SUCCESS\""}
            }
        }
        failure {
            script {
                withCredentials([string(credentialsId: 'TG_TOKEN', variable: 'TOKEN'),
                string(credentialsId: 'TG_GROUP_ID', variable: 'CHAT_ID')])
                {sh "curl -s -X POST https://api.telegram.org/bot${TOKEN}/sendMessage -d chat_id=${CHAT_ID} -d text=\"job ${env.BUILD_TAG} build FAIL\""}
            }
        }
    }
}
