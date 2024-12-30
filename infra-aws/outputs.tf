output "s3_bucket_name" {
  value = aws_s3_bucket.lambda_bucket.bucket
}


# Outputs para obtener información útil
output "lambda_function_name" {
  value = coalesce(
    data.aws_lambda_function.existing_lambda[0].function_name,
    aws_lambda_function.kuosel_lambda[0].function_name
  )
}

output "lambda_function_arn" {
  value = coalesce(
    data.aws_lambda_function.existing_lambda[0].arn,
    aws_lambda_function.kuosel_lambda[0].arn
  )
}