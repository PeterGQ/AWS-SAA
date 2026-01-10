import boto3

def get_all_cognito_users(user_pool_id, region):
    # Initialize the Cognito Identity Provider client
    client = boto3.client('cognito-idp', region_name=region)
    
    users_list = []
    next_token = None
    
    print(f"{'Username':<30} | {'Email':<30}")
    print("-" * 65)

    try:
        while True:
            # Prepare arguments for list_users
            list_args = {'UserPoolId': user_pool_id}
            if next_token:
                list_args['PaginationToken'] = next_token

            # Call Cognito API
            response = client.list_users(**list_args) 
            
            for user in response.get('Users', []):
                username = user.get('Username')
                email = "N/A"
                
                # Search for the email attribute in the Attributes list
                for attribute in user.get('Attributes', []):
                    if attribute['Name'] == 'email':
                        email = attribute['Value']
                        break
                
                print(f"{username:<30} | {email:<30}")
                users_list.append({'Username': username, 'Email': email})

            # Check if there are more users to fetch
            next_token = response.get('PaginationToken')
            if not next_token:
                break

    except Exception as e:
        print(f"Error fetching users: {e}")

    return users_list

# --- Configuration ---
USER_POOL_ID = 'us-east-1_qbnhBDjBY'
REGION = 'us-east-1'

if __name__ == "__main__":
    get_all_cognito_users(USER_POOL_ID, REGION)