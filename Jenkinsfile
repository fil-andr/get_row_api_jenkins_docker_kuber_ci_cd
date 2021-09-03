pipeline {
    agent { label 'master' }
    environment {
        VENV_DIR = "/docker_test/venv_jenkins"
        JENKINS_MANIFEST_KUBER_HOST = "/kuber_manifests/jenkins_manifests/get_row_api"
    }
    triggers {pollSCM('* * * * *')}
    stages {
        stage ('clone from git repo'){
            steps{
                git 'https://github.com/fil-andr/get_row_api_jenkins_docker_kuber_ci_cd.git'
            }
        }
        stage ('unit tests'){
           steps{
                sh 'cd ${VENV_DIR} && source venv_jenkins/bin/activate && pytest ${WORKSPACE}/app/tests.py -v'
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
                sh 'cd ${WORKSPACE} && /usr/bin/bash tag_ver_replace.sh v${BUILD_NUMBER}'
                sh 'ansible-playbook ${WORKSPACE}/copy_files_get_row_api_ansible.yml -e "path=${JENKINS_MANIFEST_KUBER_HOST}" -e "src_path=${WORKSPACE}"'
                sh 'ansible-playbook ${WORKSPACE}/get_row_api_kuber_deploy_ansible.yml -e "yml_file_path=${JENKINS_MANIFEST_KUBER_HOST}"'
            }
        }
        stage ('application health test'){
            steps{
                sh 'ansible-playbook ${WORKSPACE}/health_check_ansible.yml -e "path=${JENKINS_MANIFEST_KUBER_HOST}"'
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
