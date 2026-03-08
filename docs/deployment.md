# JanSahay AI - AWS Deployment Guide

## Architecture on AWS

```
                    ┌─────────────┐
                    │  Route 53   │  (DNS)
                    │ jansahay.ai │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │ CloudFront  │  (CDN)
                    │   + WAF     │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │    ALB      │  (Application Load Balancer)
                    │ (HTTPS/TLS) │
                    └───┬─────┬───┘
                        │     │
               ┌────────┘     └────────┐
               │                       │
        ┌──────┴──────┐        ┌───────┴──────┐
        │ ECS Fargate │        │ ECS Fargate  │
        │  Backend ×4 │        │ Frontend ×2  │
        │  (FastAPI)  │        │   (React)    │
        └──────┬──────┘        └──────────────┘
               │
        ┌──────┴──────────────────┐
        │                         │
  ┌─────┴─────┐          ┌───────┴──────┐
  │ RDS Aurora │          │ ElastiCache  │
  │ PostgreSQL │          │   Redis      │
  │ Multi-AZ   │          │   Cluster    │
  └────────────┘          └──────────────┘
```

## Step-by-Step Deployment

### 1. Prerequisites
```bash
aws configure  # Set up AWS CLI with ap-south-1 (Mumbai)
aws ecr create-repository --repository-name jansahay-backend
aws ecr create-repository --repository-name jansahay-frontend
```

### 2. Build & Push Docker Images
```bash
# Login to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com

# Build & push backend
docker build -t jansahay-backend ./backend
docker tag jansahay-backend:latest <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/jansahay-backend:latest
docker push <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/jansahay-backend:latest

# Build & push frontend
docker build -t jansahay-frontend ./frontend
docker tag jansahay-frontend:latest <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/jansahay-frontend:latest
docker push <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/jansahay-frontend:latest
```

### 3. Create Infrastructure
```bash
# VPC with public/private subnets
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# RDS Aurora PostgreSQL (Multi-AZ)
aws rds create-db-cluster \
  --db-cluster-identifier jansahay-db \
  --engine aurora-postgresql \
  --master-username jansahay \
  --master-user-password <SECURE_PASSWORD> \
  --region ap-south-1

# ElastiCache Redis
aws elasticache create-cache-cluster \
  --cache-cluster-id jansahay-redis \
  --engine redis \
  --cache-node-type cache.t3.micro \
  --num-cache-nodes 1

# ECS Cluster
aws ecs create-cluster --cluster-name jansahay-cluster
```

### 4. Create ECS Task Definition & Service
```bash
# Register task definition (see task-definition.json)
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service with ALB
aws ecs create-service \
  --cluster jansahay-cluster \
  --service-name jansahay-service \
  --task-definition jansahay-task \
  --desired-count 4 \
  --launch-type FARGATE \
  --load-balancers targetGroupArn=<TG_ARN>,containerName=backend,containerPort=8000
```

### 5. Configure Auto-Scaling
```bash
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/jansahay-cluster/jansahay-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 20

aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/jansahay-cluster/jansahay-service \
  --policy-name cpu-scaling \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration \
    "TargetValue=70.0,PredefinedMetricSpecification={PredefinedMetricType=ECSServiceAverageCPUUtilization}"
```

### 6. Configure CloudFront + SSL
```bash
# Request ACM certificate
aws acm request-certificate --domain-name jansahay.ai --validation-method DNS

# Create CloudFront distribution
aws cloudfront create-distribution --origin-domain-name <ALB_DNS>
```

### 7. Configure Route 53
```bash
aws route53 change-resource-record-sets \
  --hosted-zone-id <ZONE_ID> \
  --change-batch '{"Changes":[{"Action":"UPSERT","ResourceRecordSet":{"Name":"jansahay.ai","Type":"A","AliasTarget":{"HostedZoneId":"<CF_ZONE>","DNSName":"<CF_DOMAIN>","EvaluateTargetHealth":false}}}]}'
```

## Environment Variables for ECS
Set these in AWS Systems Manager Parameter Store:
- `DATABASE_URL` — RDS Aurora connection string
- `REDIS_URL` — ElastiCache endpoint
- `JWT_SECRET_KEY` — Generated with `openssl rand -hex 32`
- `GOOGLE_CLOUD_PROJECT_ID` — GCP project for Speech API
- `TWILIO_ACCOUNT_SID` — For WhatsApp bot
