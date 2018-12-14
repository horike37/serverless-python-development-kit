#!/bin/bash
echo "Deploying DB to stage production"
cd db
./../node_modules/.bin/serverless deploy --stage production --region ${AWS_DEFAULT_REGION} --alias ${API_VERSION} --verbose
cd ../
