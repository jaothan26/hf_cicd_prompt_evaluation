pipeline {
    agent any
    environment {
        HF_SPACE_URL = "https://huggingface.co/spaces/YourUsername/YourSpaceName"
    }
    stages {
        stage('Setup Environment') {
            steps {
                echo "🚀 Setting up environment..."
                sh "python3 -m venv venv"
                sh "source venv/bin/activate"
                sh "pip install --upgrade pip"
                sh "pip install -r requirements.txt"
            }
        }

        stage('Run Prompt Evaluation') {
            steps {
                echo "📝 Running evaluation..."
                script {
                    def result = sh(script: "python evaluate_prompts.py", returnStatus: true)
                    if (result != 0) {
                        error "❌ Evaluation failed! Stopping deployment."
                    }
                }
            }
        }

        stage('Deploy to Hugging Face Spaces') {
            steps {
                echo "🚀 Deploying to Hugging Face Spaces..."
                sh '''
                git config --global user.email "you@example.com"
                git config --global user.name "Your Name"
                git remote add huggingface ${HF_SPACE_URL}
                git push huggingface main
                '''
            }
        }
    }

    post {
        always {
            echo "📜 Cleaning up temporary files..."
            sh "rm -rf venv"
        }
        failure {
            echo "❌ Deployment failed. Check logs."
        }
        success {
            echo "✅ Deployment successful! 🎉"
        }
    }
}
