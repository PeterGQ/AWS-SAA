terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "6.26.0"
    }
  }
}

provider "aws" {
  #f
}

resource "aws_s3_bucket" "default" {
  # Configuration options
  region = "us-east-2"
}

resource "aws_s3_object" "object" {
    bucket = aws_s3_bucket.default.id
    key    = "example.txt"
    source = "example.txt"
    region = "us-east-2"

    etag = filemd5("example.txt")
}