provider "aws" {
  region = "us-east-2"
}

# Bucket S3 para almacenar el ZIP de la Lambda
resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "kuosel-lambda-bucket-${random_id.bucket_id.hex}"
}

resource "random_id" "bucket_id" {
  byte_length = 8
}

resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.lambda_bucket.id
  key    = "deployment-package.zip"
  source = "../deployment-package.zip" # Ruta local del ZIP
}

# Data source para buscar el rol existente
data "aws_iam_role" "existing_role" {
  name = "kuosel-lambda-execution-role"
}

# Crear el rol si no existe
resource "aws_iam_role" "lambda_execution_role" {
  count = can(data.aws_iam_role.existing_role.name) ? 0 : 1

  name = "kuosel-lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Adjuntar política AWSLambdaBasicExecutionRole
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = coalesce(try(data.aws_iam_role.existing_role.name, null), try(aws_iam_role.lambda_execution_role[0].name, null))
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Adjuntar política AmazonCognitoPowerUser
resource "aws_iam_role_policy_attachment" "cognito_power_user" {
  role       = coalesce(try(data.aws_iam_role.existing_role.name, null), try(aws_iam_role.lambda_execution_role[0].name, null))
  policy_arn = "arn:aws:iam::aws:policy/AmazonCognitoPowerUser"
}

# Data source para buscar la Lambda existente
data "aws_lambda_function" "existing_lambda" {
  function_name = "kuosel-lambdalith"
}

# Unificar creación y actualización de Lambda
resource "aws_lambda_function" "kuosel_lambda" {
  function_name = "kuosel-lambdalith"
  handler       = "main.handler"
  runtime       = "python3.11"
  s3_bucket     = aws_s3_bucket.lambda_bucket.id
  s3_key        = aws_s3_object.lambda_zip.key

  role = coalesce(
    try(data.aws_iam_role.existing_role.arn, null),
    try(aws_iam_role.lambda_execution_role[0].arn, null)
  )

  memory_size = 128
  timeout     = 30

  environment {
    variables = {
      COGNITO_USER_POOL_ID = var.COGNITO_USER_POOL_ID
      COGNITO_CLIENT_ID    = var.COGNITO_CLIENT_ID
      COGNITO_DOMAIN       = var.COGNITO_DOMAIN
      DB_USER              = var.DB_USER
      DB_PASSWORD          = var.DB_PASSWORD
      DB_HOST              = var.DB_HOST
      DB_PORT              = var.DB_PORT
      DB_NAME              = var.DB_NAME
      PYTHONPATH           = "/var/task/dependencies:/var/task"
    }
  }

  lifecycle {
    # Permitir actualizaciones sin recrear la Lambda
    create_before_destroy = false
    ignore_changes = [role]
  }
}
