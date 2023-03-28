import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print(user)
    
    user_display_name = user['name']
    user_email = user['email']
    user_handle = user['preferred_username']
    user_cognito_id = user['sub']
    
    try:
        
        print("try block started")
        sql_query = f"""
        INSERT INTO public.users (
            display_name,
            email, 
            handle, 
            cognito_user_id
            ) 
        VALUES(
            '{user_display_name}',
            '{user_email}', 
            '{user_handle}', 
            '{user_cognito_id}'
            )
        """
        conn = psycopg2.connect(os.getenv("CONNECTION_URL"))
        cur = conn.cursor()
        
        print("SQL-----")
        print(sql_query)
        cur.execute(sql_query)
        conn.commit()
    except Exception as e:
        print("exception")
        print(e)
    return event