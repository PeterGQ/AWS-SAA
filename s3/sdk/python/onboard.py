import boto3
import argparse
from botocore.exceptions import ClientError

# --- CONFIGURATION ---
cognito = boto3.client('cognito-idp')
USER_POOL_ID = 'us-east-1_fG0wseHvG'  # Update this!
# ---------------------

def onboard_user(email, role_group):
    try:
        # 1. CHECK IF USER EXISTS
        existing = cognito.list_users(
            UserPoolId=USER_POOL_ID,
            Filter=f'email = "{email}"',
            Limit=1
        )

        if existing['Users']:
            print(f"Skipping: User {email} already exists.")
            return

        # 2. CREATE THE USER
        print(f"Creating account for {email}...")
        cognito.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=email,
            UserAttributes=[
                {'Name': 'email', 'Value': email}, 
                {'Name': 'email_verified', 'Value': 'True'}
            ]
        )

        # 3. ASSIGN TO COGNITO GROUP
        cognito.admin_add_user_to_group(
            UserPoolId=USER_POOL_ID,
            Username=email,
            GroupName=role_group
        )
        print(f"✅ Success: {email} added to {role_group}.")

    except ClientError as e:
        print(f"❌ Error: {e.response['Error']['Message']}")

if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Onboard a user to AWS Cognito.")
    
    # Define the arguments
    parser.add_argument("email", help="The email address of the user to create.")
    parser.add_argument("group", help="The Cognito group to add the user to.")

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Run the function using the arguments
    onboard_user(args.email, args.group)