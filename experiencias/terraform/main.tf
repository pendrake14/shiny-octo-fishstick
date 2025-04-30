terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "experiencias-terraform-state"
    key    = "terraform.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Configuration
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "experiencias-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = {
    Environment = var.environment
    Project     = "experiencias"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "experiencias" {
  name = "experiencias-cluster"
}

# ECS Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = "experiencias-app"
  network_mode            = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                     = 256
  memory                  = 512

  container_definitions = jsonencode([
    {
      name      = "web"
      image     = "${aws_ecr_repository.experiencias.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
      environment = [
        {
          name  = "DJANGO_SETTINGS_MODULE"
          value = "config.settings.prod"
        }
      ]
      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = aws_secretsmanager_secret_version.db_url.arn
        }
      ]
    }
  ])
}

# ECR Repository
resource "aws_ecr_repository" "experiencias" {
  name = "experiencias"
}

# RDS Instance
module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "experiencias-db"

  engine            = "postgres"
  engine_version    = "15"
  instance_class    = "db.t3.micro"
  allocated_storage = 20

  db_name  = "experiencias"
  username = "postgres"
  port     = "5432"

  vpc_security_group_ids = [module.vpc.default_security_group_id]
  subnet_ids             = module.vpc.private_subnets

  family = "postgres15"
  major_engine_version = "15"

  tags = {
    Environment = var.environment
    Project     = "experiencias"
  }
}

# Secrets Manager for Database URL
resource "aws_secretsmanager_secret" "db_url" {
  name = "experiencias-db-url"
}

resource "aws_secretsmanager_secret_version" "db_url" {
  secret_id = aws_secretsmanager_secret.db_url.id
  secret_string = jsonencode({
    DATABASE_URL = "postgres://${module.db.db_instance_username}:${module.db.db_instance_password}@${module.db.db_instance_endpoint}/${module.db.db_instance_name}"
  })
} 