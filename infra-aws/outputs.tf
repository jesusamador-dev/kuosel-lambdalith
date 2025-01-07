output "s3_bucket_name" {
  value = aws_s3_bucket.lambda_bucket.bucket
}

output "lambda_function_name" {
  value = can(data.aws_lambda_function.existing_lambda.function_name)
    ? data.aws_lambda_function.existing_lambda.function_name
    : aws_lambda_function.kuosel_lambda.function_name
}

output "lambda_function_arn" {
  value = can(data.aws_lambda_function.existing_lambda.arn)
    ? data.aws_lambda_function.existing_lambda.arn
    : aws_lambda_function.kuosel_lambda.arn
}
