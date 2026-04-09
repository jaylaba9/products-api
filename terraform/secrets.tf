resource "random_password" "db_pass" {
  length = 16
  special = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_secretsmanager_secret" "db_secret" {
  name = "db-pass-secret"
}

resource "aws_secretsmanager_secret_version" "db_secret_version" {
  secret_id = aws_secretsmanager_secret.db_secret.id
  secret_string = random_password.db_pass.result
}