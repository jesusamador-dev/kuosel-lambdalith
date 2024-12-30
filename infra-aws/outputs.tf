output "lambda_function_name" {
  value = aws_lambda_function.kuosel_lambda.function_name
}

output "lambda_function_arn" {
  value = aws_lambda_function.kuosel_lambda.arn
}

output "s3_bucket_name" {
  value = aws_s3_bucket.lambda_bucket.bucket
}
