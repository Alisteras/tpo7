pipeline {
    options {
        skipDefaultCheckout()
    }

    stages {
        stage('Clean Workspace') {
            steps {
                sh 'rm -rf * .git* reports || true'
                sh 'mkdir -p reports'
            }
        }

        stage('Git Clone') {
            steps {
                sh '''
                    git clone --depth 1 https://github.com/Alisteras/tpo7.git tmp_repo
                    mv tmp_repo/* .
                    mv tmp_repo/.* . || true
                    rm -rf tmp_repo
                    ls -la
                '''
            }
        }

        stage('Initializing QEMU') {
            steps {
                sh '''
                    chmod +x ./scripts/start_qemu.sh
                    ./scripts/start_qemu.sh &
                    sleep 60
                '''
            }
        }

        stage('API Tests') {
            steps {
                ansiColor('xterm') {
                    sh '''
                        chmod +x ./scripts/run_pytest_tests.sh
                        ./scripts/run_pytest_tests.sh
                    '''
                }
            }

        }

        stage('UI Tests') {
            steps {
                sh '''
                    chmod +x ./scripts/run_selenium_tests.sh
                    ./scripts/run_selenium_tests.sh
                '''
            }

        }

        stage('Load Tests') {
            steps {
                sh '''
                    chmod +x ./scripts/run_locust_tests.sh
                    ./scripts/run_locust_tests.sh
                '''
            }
        }
    }

    post {
        always {
            echo "СТАТУС: ${currentBuild.currentResult}"

            archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
        }
        success {
            echo "ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО"

        }
        failure {
            echo "ТЕСТЫ ЗАВЕРШИЛИСЬ С ОШИБКАМИ"
        }
    }
}

