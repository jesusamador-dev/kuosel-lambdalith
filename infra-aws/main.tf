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

# Data source para buscar la Lambda existente
data "aws_lambda_function" "existing_lambda" {
  count         = var.lambda_already_exists ? 1 : 0
  function_name = "kuosel-lambdalith"
}

# Rol IAM para Lambda
resource "aws_iam_role" "lambda_execution_role" {
  count = var.lambda_already_exists ? 0 : 1

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

# Adjuntar políticas al rol
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = coalesce(data.aws_iam_role.existing_lambda[0].role, aws_iam_role.lambda_execution_role[0].name)
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Función Lambda
resource "aws_lambda_function" "kuosel_lambda" {
  count       = var.lambda_already_exists ? 0 : 1
  function_name = "kuosel-lambdalith"
  handler       = "main.handler"
  runtime       = "python3.11"
  s3_bucket     = aws_s3_bucket.lambda_bucket.id
  s3_key        = aws_s3_object.lambda_zip.key

  # Usar el rol existente o crear uno nuevo
  role = coalesce(data.aws_lambda_function.existing_lambda[0].role, aws_iam_role.lambda_execution_role[0].arn)

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
}
