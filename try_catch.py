import requests
import os 
from dotenv import load_dotenv

load_dotenv() 

API_TOKEN = os.getenv("API_TOKEN")
BASE_URL = os.getenv("BASE_URL")
JIRA_URL_FOOCORP= os.getenv("JIRA_URL_FOOCORP")
JIRA_API_TOKEN= os.getenv("JIRA_API_TOKEN")
JIRA_URL_BARTECH=os.getenv("JIRA_URL_BARTECH")

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

headers_1={
      "Authorization": f"Bearer {JIRA_API_TOKEN}",
      "Content-Type": "application/json"  
}

def deactivate_user_bartech(account_id):
    try:
        response = requests.post(f"{JIRA_URL_BARTECH}/{account_id}/suspend", headers=headers_1)
        if response.status_code == 204:
            return "Done"
        else:
            print(f"Failed to deactivate user {account_id}: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Error deactivating user {account_id} in Bartech: {e}")
    return None


def deactivate_user_foocorp(account_id):
    try:
        response = requests.post(f"{JIRA_URL_FOOCORP}/{account_id}/suspend", headers=headers_1)
        if response.status_code == 204:
            return "Done"
        else:
            print(f"Failed to deactivate user {account_id}: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Error deactivating user {account_id} in Foocorp: {e}")
    return None


def compare_user(username_to_search):
    print("Jira controller started")
    try:
        # --- Authentik ---
        response = requests.get(
            f"{BASE_URL}/api/v3/core/users/?name={username_to_search}",
            headers=headers
        )
        response.raise_for_status() 
        users = response.json()
        print(users)

        if users.get("results"):
            user = users["results"][0]
            is_active = user.get("is_active", False)
            email = user.get("email", "")
            domain = email.rsplit("@", 1)[1] if "@" in email else ""
            print(domain)

            # --- Jira-Bartech ---
            if domain == "bartech.click":
                try:
                    response = requests.get(f"{JIRA_URL_BARTECH}", headers=headers_1)
                    response.raise_for_status()
                    res_json = response.json()

                    user_data = next((u for u in res_json.get('data', []) if u.get('email') == email), None)
                    if user_data:
                        account_status = user_data.get('status')
                        account_id = user_data.get('accountId')
                        print(f"Account ID: {account_id}, Account Status: {account_status}")
                        
                        print(f"Account status of {email}: {account_status} == {is_active}")
                        if account_status == "active" and is_active:
                            print("all good!")
                        elif account_status == "suspended" and not is_active:
                            print("all good!")
                        elif account_status == "active" and not is_active:
                            print("Need to deactivate user in Jira")
                            print(deactivate_user_bartech(account_id))
                        else:
                            print("rest")
                    else:
                        print("User not found in Bartech Jira")
                except Exception as e:
                    print(f"Error checking Bartech Jira: {e}")

            # --- Jira-Foocorp ---
            elif domain == "foocorp.click":
                try:
                    response = requests.get(f"{JIRA_URL_FOOCORP}", headers=headers_1)
                    response.raise_for_status()
                    res_json = response.json()

                    user_data = next((u for u in res_json.get('data', []) if u.get('email') == email), None)
                    if user_data:
                        account_status = user_data.get('status')
                        account_id = user_data.get('accountId')
                        print(f"Account ID: {account_id}, Account Status: {account_status}")
                        
                        print(f"Account status of {email}: {account_status} == {is_active}")
                        if account_status == "active" and is_active:
                            print("all good!")
                        elif account_status == "suspended" and not is_active:
                            print("all good!")
                        elif account_status == "active" and not is_active:
                            print("Need to deactivate user in Jira")
                            print(deactivate_user_foocorp(account_id))
                        else:
                            print("rest")
                    else:
                        print("User not found in Foocorp Jira")
                except Exception as e:
                    print(f"Error checking Foocorp Jira: {e}")

            else:
                print("Domain not matched!")

        else:
            print("No users found in authentik")

    except requests.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    print("Jira controller ended")


# Example run
compare_user(username_to_search="Test User 29")
