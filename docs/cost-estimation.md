# JanSahay AI - Cost Estimation (AWS ap-south-1 Mumbai)

## Monthly Cost Breakdown

### Tier 1: Development / MVP (10K users)

| Service | Spec | Monthly Cost |
|---------|------|-------------|
| ECS Fargate (Backend) | 2 tasks × 0.5 vCPU × 1GB | $29 |
| ECS Fargate (Frontend) | 1 task × 0.25 vCPU × 0.5GB | $7 |
| RDS Aurora PostgreSQL | db.t3.medium (Single AZ) | $58 |
| ElastiCache Redis | cache.t3.micro | $13 |
| ALB | 1 ALB + 10 LCU-hours | $22 |
| CloudFront | 50 GB transfer | $5 |
| ECR | 5 GB images | $0.50 |
| Route 53 | 1 hosted zone | $0.50 |
| S3 | 10 GB storage | $0.25 |
| **Total** | | **~$135/month** |

### Tier 2: Production (100K users)

| Service | Spec | Monthly Cost |
|---------|------|-------------|
| ECS Fargate (Backend) | 4 tasks × 1 vCPU × 2GB | $180 |
| ECS Fargate (Frontend) | 2 tasks × 0.5 vCPU × 1GB | $29 |
| RDS Aurora PostgreSQL | db.r6g.large (Multi-AZ) | $292 |
| ElastiCache Redis | cache.r6g.large (cluster) | $146 |
| ALB | 1 ALB + 50 LCU-hours | $45 |
| CloudFront + WAF | 500 GB transfer | $48 |
| Google Cloud Speech | 50K API calls | $60 |
| Twilio WhatsApp | 10K messages | $50 |
| CloudWatch + Logs | Standard | $25 |
| **Total** | | **~$875/month** |

### Tier 3: Bharat Scale (10M+ users)

| Service | Spec | Monthly Cost |
|---------|------|-------------|
| ECS Fargate (Backend) | 20 tasks × 2 vCPU × 4GB (auto-scale) | $1,800 |
| ECS Fargate (Frontend) | 5 tasks × 1 vCPU × 2GB | $180 |
| RDS Aurora PostgreSQL | db.r6g.2xlarge (Multi-AZ + read replicas) | $1,170 |
| ElastiCache Redis | cache.r6g.xlarge (cluster, 3 nodes) | $880 |
| ALB + WAF | 2 ALBs + 500 LCU-hours | $350 |
| CloudFront | 5 TB transfer | $425 |
| Google Cloud Speech | 500K API calls | $600 |
| Twilio WhatsApp | 500K messages | $2,500 |
| S3 + Backup | 500 GB | $12 |
| CloudWatch | Enhanced | $75 |
| **Total** | | **~$7,992/month** |

## Pay-as-you-go Advantages
- **ECS Fargate**: Pay per second of compute used
- **Aurora Serverless v2**: Auto-scales to 0 in off-hours
- **CloudFront**: Only pay for data transferred
- **No upfront costs**: All services are on-demand

## Cost Optimization Strategies
1. **Use Fargate Spot** for non-critical tasks (70% savings)
2. **Reserved Instances** for RDS (40% savings over 1 year)
3. **S3 Intelligent-Tiering** for infrequent assets
4. **Scheduled scaling** to reduce tasks during night hours
5. **Redis TTL** to minimize cache memory usage
