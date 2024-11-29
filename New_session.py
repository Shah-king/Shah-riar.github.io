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
            print("Failed to start session. Status code:", response.status_code)
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except Exception as e:
        print(f"Error occurred: {e}")

# Start session and retrieve the session ID
session_id = start_session()

def get_route(session_id):
    url = "https://hackdiversity.xyz/api/navigation/routes"
    headers = {
        "Authorization": f"Bearer {session_id}"  # Correct Authorization format
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch routes: {response.status_code}")

routes = get_route(session_id)

def filter_routes(routes):
    '''Filter only accessible routes from the data.'''
    accessible_routes = []
    for route in routes:
        if route.get('is_accessible'):
            accessible_routes.append(route)
    return accessible_routes

def sort_by_distance(routes):
    '''Sort routes using bubble sort.'''
    k = len(routes)
    for i in range(k):
        for j in range(0, k - i - 1):
            if routes[j]['distance'] > routes[j + 1]['distance']:
                routes[j], routes[j + 1] = routes[j + 1], routes[j]
    return routes

accessible_routes = filter_routes(routes)
sorted_routes = sort_by_distance(accessible_routes)

def test_algorithm(session_id):
    # Retrieve sample data
    test_url = "https://hackdiversity.xyz/api/test/mockRoutes"
    headers = {
        "Authorization": f"Bearer {session_id}"  # Correct Authorization format
    }
    test_routes = requests.get(test_url, headers=headers).json()

    # Filter and sort
    accessible_test_routes = filter_routes(test_routes)
    sorted_test_routes = sort_by_distance(accessible_test_routes)

    # Submit test results
    submit_url = "https://hackdiversity.xyz/api/test/submit-sorted-routes"
    response = requests.post(submit_url, json=sorted_test_routes, headers=headers)

    if response.status_code == 200:
        print("Test data submitted successfully.")
        print("Response:", response.json())
    else:
        raise Exception(f"Failed to submit test data: {response.status_code}")

test_algorithm(session_id)

def submit_final_routes(session_id, sorted_routes):
    url = "https://hackdiversity.xyz/api/navigation/sorted_routes"
    headers = {
        "Authorization": f"Bearer {session_id}"  
    }
    response = requests.post(url, json=sorted_routes, headers=headers)

    if response.status_code in [200, 201]:
        print("Final routes submitted successfully.")
        print("Response:", response.json())
    else:
        raise Exception(f"Failed to submit final routes: {response.status_code}")

submit_final_routes(session_id, sorted_routes)

def check_status(session_id):
    url = "https://hackdiversity.xyz/api/navigation/status"
    headers = {
        "Authorization": f"Bearer {session_id}" 
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Status:", response.json())
    else:
        raise Exception(f"Failed to check status: {response.status_code}")

check_status(session_id)
