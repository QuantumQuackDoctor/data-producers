
pipeline {
    agent any
    parameters{
        string(name: 'KeyName', defaultValue: $(base64 -w0 userdata.sh))
        string(name: 'Environment', defaultValue: params.Environment ?: 'dev')
    }
    stages{
        stage("Deploy Base Infrastructure"){
            steps {
                sh "aws cloudformation deploy --stack-name Data-${params.Environment} --region ${AWS_REGION} --template-file data-producer-cf.template --parameter-overrides Environment=${params.Environment} UserData=$(base64 -w0 userdata.sh) KeyName=${KeyName} --no-fail-on-empty-changeset --capabilities CAPABILITY_NAMED_IAM"
            }
        }
    }
}