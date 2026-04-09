resource "aws_db_subnet_group" "rds_subnet" {
  name = "products-api-rds-subnet"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_security_group" "rds_sg" {
  name = "products-api-rds-sg"
  description = "Allow inbound access from ECS tasks only"
  vpc_id = module.vpc.vpc_id

  ingress {
    protocol = "tcp"
    from_port = 5432
    to_port = 5432
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  egress {
    protocol = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "rds_db" {
  identifier = "rds-db-instance"
  db_name = "products_db"
  engine = "postgres"
  engine_version = "15"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  username = "dbuser"
  password = aws_secretsmanager_secret_version.db_secret_version.secret_string
  db_subnet_group_name = aws_db_subnet_group.rds_subnet.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot = true
  publicly_accessible = false
}