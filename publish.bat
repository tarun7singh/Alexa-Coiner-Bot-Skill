del index.zip 
cd lambda
7z a -r ..\index.zip *
cd .. 
aws lambda update-function-code --function-name coiner --zip-file fileb://index.zip