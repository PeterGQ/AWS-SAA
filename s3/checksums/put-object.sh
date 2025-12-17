#!usr/bin/env bash

CHECKSUM_SHA1=$(openssl dgst -sha256 -binary myfile.txt | base64)

aws s3api put-object \
       --bucket="joe-schmoe-checksums-examples" \
       --key="myfilesha1.txt" \
       --body="myfile.txt" \
       --checksum-algorithm="SHA1" \
       --checksum-sha1="$CHECKSUM_SHA1" \
       --metadata ChecksumSHA1="$CHECKSUM_SHA1"