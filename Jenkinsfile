def gv
pipeline {
    triggers {
        // Trigger hook every 5 minutes
        pollSCM('H/5 * * * *')
    }
    agent {
        // Run test on the nodes with the same label
        label 'AMD64_DESKTOP'
    }
    parameters {
        // Add parameters for test suite selection
        choice(
            choices: [
                'test_system',
                'test_unit'
            ],
            description: 'Select the test environment',
            name: 'TEST_ENVIRONMENT'
        )
        choice(
            choices: [
                'all',
                'unit',
                'system'
            ],
            description: 'My Test Suite',
            name: 'MY_SUITE'
        )
        choice(
            choices: [
                'all',
                'unit',
                'system'
            ],
            description: 'Functional Test',
            name: 'FUNCTIONAL'
        )
    }
    environment {
        MY_PRIVATE_TOKEN = credentials('gitlab-private-token')
        WORK_PATH = 'C:\\Users\\STE\\Projects\\MLAutoRAID\\workspace\\MLAutoRAID'
    }
    stages {
        stage('Setup') {
            steps {
                dir("${env.WORK_PATH}") { // 切换到指定的工作路径
                    script {
                        // 安装所有依赖项，包括 pytest
                        bat "pipenv install --dev"
                    }
                }
            }
        }
        stage('Testing') {
            steps {
                dir("${env.WORK_PATH}") {
                    script {
                        if (params.TEST_ENVIRONMENT == 'test_unit') {
                            bat 'pipenv run pytest tests\\test_unit --testmon'
                        } else if (params.TEST_ENVIRONMENT == 'test_amd_desktop') {
                            bat 'pipenv run pytest tests\\test_system --testmon'
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            emailext body: 'Test results are available at: $BUILD_URL', subject: 'Test Results', to: 'everpalm@yahoo.com.tw'
            bat "pipenv run python -m pytest --cache-clear"
        }
        success {
            echo 'todo - 1'
        }
        failure {
            echo 'todo - 2'
        }
    }
}
