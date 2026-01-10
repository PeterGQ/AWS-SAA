import boto3
import argparse
from botocore.exceptions import ClientError

# --- CONFIGURATION ---
cognito = boto3.client('cognito-idp')
USER_POOL_ID = 'us-east-1_qbnhBDjBY'  # Update this if necessary
TEMP_PASSWORD = 'Temp1234!' #Note: 
# ---------------------

def onboard_user(email, role_group):
    # Extract the part before the @ symbol to use as the Username
    username = email.split('@')[0]
    
    try:
        # 1. CHECK IF USER ALREADY EXISTS (Check by Email attribute)
        existing = cognito.list_users(
            UserPoolId=USER_POOL_ID,
            Filter=f'email = "{email}"',
            Limit=1
        )

        if existing['Users']:
            print(f"Skipping: A user with email {email} already exists.")
            return

        # 2. CREATE THE USER
        # We use the extracted 'username' for the Username field
        print(f"Creating account for {username} (Email: {email})...")
        cognito.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=username,
            TemporaryPassword=TEMP_PASSWORD,
            UserAttributes=[
                {'Name': 'email', 'Value': email}, 
                {'Name': 'email_verified', 'Value': 'True'}
            ],
            DesiredDeliveryMediums=['EMAIL'] # Sends temporary password via email
        )

        # 3. ASSIGN TO COGNITO GROUP
        # Must use the same 'username' used in step 2
        cognito.admin_add_user_to_group(
            UserPoolId=USER_POOL_ID,
            Username=username,
            GroupName=role_group
        )
        print(f"✅ Success: {username} added to {role_group}.")

    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Onboard a user to AWS Cognito.")
    parser.add_argument("email", help="The email address of the user to create.")
    parser.add_argument("group", help="The Cognito group to add the user to.")

    args = parser.parse_args()
    onboard_user(args.email, args.group)