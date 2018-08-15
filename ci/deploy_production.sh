#!/bin/bash
echo "Deploying to stage production"
./node_modules/.bin/serverless deploy --stage production --region ${AWS_DEFAULT_REGION} --verbose
