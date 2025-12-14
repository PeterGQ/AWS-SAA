# Import AWS PowerShell Module
Import-Module AWSPowerShell.NetCore

# Set AWS Region
$region = "us-east-2"

# Prompt for S3 Bucket Name
$bucketName = Read-Host -Prompt 'Enter the S3 bucket name'

# Function to check if the bucket exists
function BucketExists {
    param ($bucketName)
    try {
        Get-S3Bucket -BucketName joe-schmoe43-example-bucket -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Create S3 Bucket if it doesn't exist
if ((BucketExists -bucketName $bucketName)) {
    Write-Host "Bucket $bucketName already exists."
} else {
    New-S3Bucket -BucketName $bucketName #-Region $region
    Write-Host "Bucket $bucketName created."
}

# Create a sample file
$fileName = "sample.txt"
$fileContent = "Hello, S3!"
Set-Content -Path $fileName -Value $fileContent

# Upload the file to the S3 bucket
Write-S3Object -BucketName $bucketName -File $fileName -Key $fileName -Region $region
Write-Host "File $fileName uploaded to bucket $bucketName."

# Clean up local file
Remove-Item -Path $fileName