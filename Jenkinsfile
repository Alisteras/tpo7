pipeline {
    agent any
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
            steps{
                echo 'Start qemu'
                sh 'rm -rf romulus romulus.zip'
                sh 'apt update'
                sh 'apt install -y qemu-system'
                sh 'apt install -y wget'
                sh 'apt install -y unzip'
                sh 'apt install -y expect'
                sh 'wget https://jenkins.openbmc.org/job/ci-openbmc/lastSuccessfulBuild/distro=ubuntu,label=docker-builder,target=romulus/artifact/openbmc/build/tmp/deploy/images/romulus/*zip*/romulus.zip'
                sh 'unzip romulus.zip'
                sh ''' 
                LATEST_MTD=$(ls romulus/obmc-phosphor-image-romulus-*.static.mtd | sort -V | tail -1)
                expect -c "
                log_file -a qemu_result.txt
                spawn qemu-system-arm -m 256 -M romulus-bmc -nographic -drive file=$LATEST_MTD,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu
                sleep 300
                send "root\r"
                sleep 4
                send "0penBmc\r"
                expect \"root@romulus:\"
                interact" &
                QEMU_PID=$!
                echo "QEMU запущен с PID: $QEMU_PID"
                echo $QEMU_PID > qemu.pid
                '''
            }
        }

        stage('API Tests') {
            steps {
                sh 'apt install -y python3'
                sh 'apt install -y python3-pytest'
                sh 'apt install -y python3-selenium'
                sh 'apt install -y python3.13-venv'
                sh 'apt install -y python3-pip'
                sh '''
                        chmod +x ./scripts/run_pytest_tests.sh
                        ./scripts/run_pytest_tests.sh
                    '''
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
                sh 'apt install -y python3 locust'
                sh '''
                    chmod +x ./scripts/run_locust_tests.sh
                    ./scripts/run_locust_tests.sh
                '''
            }
        }
        stage('Stop Qemu') {
            steps {
                sh '''
                    echo "Stop Qemu..."
                    if [ -f "qemu.pid" ]; then
                        QEMU_PID=$(cat qemu.pid)
                        kill $QEMU_PID 2>/dev/null || true
                        rm -f qemu.pid
                        echo "Qemu shutted down"
                    fi
                    rm -rf romulus/ romulus.zip || true
                    rm -f *.log *.pid *.json *.csv || true
                    rm -f qemu.pid image_path.txt config.env || true
                    du -sh . | awk '{print $1}'
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

