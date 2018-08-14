#!/bin/bash
echo "Deploying to stage development"
./node_modules/.bin/serverless deploy --stage development --verbose
