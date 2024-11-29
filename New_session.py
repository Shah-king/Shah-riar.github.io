import requests

def start_session():
    url = "https://hackdiversity.xyz/api/start-session"
    payload = {
        "firstName": "Shahriar",
        "lastName": "Ferdous"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)  # Added timeout
        if response.status_code == 200:
            session_id = response.json().get("session_id")
            print("Session started successfully. Session ID:", session_id)
            return session_id
        else:
            print("Failed to start session.")
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except Exception as e:
        print(f"Error occurred: {e}")

# Run the function
session_id = start_session()

def get_route(session_id):
    url = "https://hackdiversity.xyz/api/navigation/routes"
    headers = {
        "Authorization":"Bearer{8730afc7-7923-488a-ab92-417c52cba6c2}"
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch routes: {response.status_code}")
routes = get_route(session_id)





