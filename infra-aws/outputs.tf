output "s3_bucket_name" {
  value = aws_s3_bucket.lambda_bucket.bucket
}


output "lambda_function_name" {
  value = var.lambda_already_exists ? data.aws_lambda_function.existing_lambda[0].function_name : aws_lambda_function.kuosel_lambda[0].function_name
}

output "lambda_function_arn" {
  value = var.lambda_already_exists ? data.aws_lambda_function.existing_lambda[0].arn : aws_lambda_function.kuosel_lambda[0].arn
}
