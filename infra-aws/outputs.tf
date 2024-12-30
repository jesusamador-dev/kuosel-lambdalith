output "s3_bucket_name" {
  value = aws_s3_bucket.lambda_bucket.bucket
}


output "lambda_function_name" {
  value = coalesce(
    try(data.aws_lambda_function.existing_lambda[0].function_name, null),
    try(aws_lambda_function.kuosel_lambda[0].function_name, null)
  )
}

output "lambda_function_arn" {
  value = coalesce(
    try(data.aws_lambda_function.existing_lambda[0].arn, null),
    try(aws_lambda_function.kuosel_lambda[0].arn, null)
  )
}
