#!/bin/bash
echo "Deploying to stage production"
./node_modules/.bin/serverless deploy --stage production --region ap-northeast-1 --verbose
