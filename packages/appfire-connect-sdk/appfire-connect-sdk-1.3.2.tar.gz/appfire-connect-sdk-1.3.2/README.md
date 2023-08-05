
# Appfire connect app SDK  
  
## What does it do?  
Creates a Atlassian Connect app template and provides a toolkit for deploying to AWS environment  
  
## Command Line Arguments  
```  
--verbose, -v : "verbose"  
--region, -r : "AWS region", default="us-east-1"  
--profile, -p : "AWS profile as the default environment", default="default"  
--env, -e : "personal, dev, test, stage or prod", default="personal"  
--stack, -s : "CDK stack to deploy", default="app", "core" or "app"
--stage, -stage : "dev, test, stage or prod", default="dev"
--app-suffix, -as : "green" or nothing (not passing the argument)
```  
###### Note: see personal.env.yml or env.yml for personal or DTS/Prod environments respectively.  
  
## Run via Python  
```  
create-appfire-app -v  
```  
  
## Bootstrap app  
#### bootstraps CDK toolkit   
```  
appfire bootstrap   
``` 

## Deploy core stack  
```  
appfire deploy -s core 
```

## Deploy biz service stack  
```  
appfire deploy -s biz-service 
```

## Deploy app service stack  
```  
appfire deploy -s app-service 
```

## Deploy module service stack  
```  
appfire deploy -s module-service 
```

## Deploy app  
```  
appfire deploy 
```

## List stacks  
```  
appfire list (or appfire ls)  
```  
 
## Diff stack  
```
appfire diff   
```
## Destroy app stack  
```
appfire destroy 
```

## Run the app
#### The app will run locally on port 9000 using the AWS_PROFILE as set from personal.env.yaml ['environment']['personal']['profile']
```
appfire run 
```