output "s3_bucket_name" {
  value = aws_s3_bucket.lambda_bucket.bucket
}


output "lambda_function_name" {
  value = try(aws_lambda_function.kuosel_lambda.function_name, null)
}

output "lambda_function_arn" {
  value = try(aws_lambda_function.kuosel_lambda.arn, null)
}

