#!/bin/bash
echo "Deploying to stage development"
./node_modules/.bin/serverless deploy --stage development --region ap-northeast-1 --verbose
