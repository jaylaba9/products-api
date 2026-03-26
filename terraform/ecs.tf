resource "aws_ecs_cluster" "main" {
  name = "products-api-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# create role
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "products-api-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

# assign policy to the created role
resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_ecs_task_definition" "app" {
  family                   = "products-api-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "products-api"
      image     = "475987770087.dkr.ecr.eu-central-1.amazonaws.com/products-api:v1"
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
    }
  ])
}

resource "aws_security_group" "ecs_tasks" {
  name = "products-api-sg-task"
  description = "Allow inbound access from ALB only"
  vpc_id = module.vpc.vpc_id

  ingress {
    protocol = "tcp"
    from_port = 8000
    to_port = 8000
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol = "-1"
    from_port = 0
    to_port = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_service" "main" {
  name = "products-api-service"
  cluster = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count = 1
  launch_type = "FARGATE"

  network_configuration {
    security_groups = [aws_security_group.ecs_tasks.id]
    subnets = module.vpc.private_subnets
    assign_public_ip = false
  }
}