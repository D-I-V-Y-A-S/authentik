import requests
import os 
from dotenv import load_dotenv

load_dotenv() 

API_TOKEN = os.getenv("API_TOKEN")
BASE_URL = os.getenv("BASE_URL")
JIRA_URL= os.getenv("JIRA_URL")
Jira_api_token= os.getenv("Jira_api_token")
Suspend_user= os.getenv("Suspend_user")

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

headers_1={
      "Authorization": f"Bearer {Jira_api_token}",
      "Content-Type": "application/json"  
}


def deactivate_user(account_id):
    response=requests.post(f"{Suspend_user}/{account_id}/suspend",headers=headers_1)
    if response.status_code==204:
        return "Done"

def compare_user(username_to_search):
# def compare_user():
    # username_to_search = "Demo"
    response = requests.get(
        f"{BASE_URL}/api/v3/core/users/?username={username_to_search}",
        headers=headers
    )
    if response.status_code == 200:
        users = response.json()
        # print(users)
        if users["results"]:  
            #fetch user data from authentik
            user = users["results"][0]  
            is_active=user['is_active']
            email=user['email']
            #fetch from atlassian using email
            response= requests.get(f"{Suspend_user}",headers=headers_1)
            res_json=response.json()
            user_data = next((user for user in res_json['data'] if user['email'] == email), None)
            if user_data:
                account_status = user_data['status']
                print(account_status)
                account_id = user_data['accountId']
                print(f"Account ID: {account_id}, Account Status: {account_status}")
            else:
                print("User not found")
            print(f"Account status of {email}: {account_status} == {is_active}")   
            #compare account_status between authentik and atlassian
            if (account_status == "active" and is_active):
                print("all good!")
            elif (account_status == "suspended" and not is_active):
                print("all good!")
            elif (account_status == "active" and not is_active):
                print("Need to deactivate user in jira")
                print(deactivate_user(account_id))
            else:
                print("rest")
    else:
            print("Error:", response.status_code, response.text)
# compare_user()