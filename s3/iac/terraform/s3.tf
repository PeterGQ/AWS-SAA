
resource "aws_s3_bucket" "my-s3-bucket" {
  region = "us-east-2"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}