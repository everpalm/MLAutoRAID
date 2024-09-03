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
        // Add parameters for test suite selection with default value 'all'
        choice(
            choices: [
                'all',
                'unit',
                'system'
            ],
            description: 'Select the test suite to run',
            name: 'MY_SUITE'
        )
    }
    environment {
        MY_PRIVATE_TOKEN = credentials('gitlab-private-token')
        WORK_PATH = 'C:\\Users\\STE\\Projects\\MLAutoRAID\\workspace\\MLAutoRAID'
    }
    stages {
        stage('Setup') {
            steps {
                dir("${env.WORK_PATH}") {
                    script {
                        // Install all dependencies, including pytest
                        bat "pipenv install --dev"
                    }
                }
            }
        }
        stage('Testing') {
            steps {
                dir("${env.WORK_PATH}") {
                    script {
                        // Determine which tests to run based on the MY_SUITE parameter
                        if (params.MY_SUITE == 'unit') {
                            bat 'pipenv run pytest tests\\test_unit --testmon'
                        } else if (params.MY_SUITE == 'system') {
                            bat 'pipenv run pytest tests\\test_system --testmon'
                        } else if (params.MY_SUITE == 'all') {
                            bat 'pipenv run pytest tests --testmon'
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            // Send email notification and clear pytest cache
            emailext body: 'Test results are available at: $BUILD_URL', subject: 'Test Results', to: 'everpalm@yahoo.com.tw'
            bat "pipenv run python -m pytest --cache-clear"
        }
        success {
            echo 'Test completed successfully.'
        }
        failure {
            echo 'Test failed.'
        }
    }
}
