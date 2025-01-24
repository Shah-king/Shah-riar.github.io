import requests
from requests.exceptions import RequestException
def start_session():
    url = "https://hackdiversity.xyz/api/start-session"
    load = {
        "firstName": "Shahriar",
        "lastName": "Ferdous"
    }

    try:
        response = requests.post(url, json=load, timeout=10)  # Sending a POST request to the API with the provided payload and a timeout of 10 seconds
        if response.status_code == 200:  # Check if the response status code is 200 (successful request)
            session_id = response.json().get("session_id") # If successful, extract the session_id from the response JSON
            print("Session started successfully. Session ID:", session_id)
            return session_id # Return the session_id for further use
        else:
            print("Failed to start session. Status code:", response.status_code) # If the request was not successful, print the status code for debugging
    except requests.exceptions.Timeout:
        print("Request timed out.") # Catch the Timeout error in case the request takes too long to respond
    except Exception as e: # Catch any other exceptions that may occur during the request process
        print(f"Error occurred: {e}")
# Start session and retrieve the session ID
session_id = start_session()

'''Fetch data from API with retry logic for better error case handling'''
def fetch_data_retries(url, headers, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10) # Send a GET request to the URL with headers and a timeout of 10 seconds
            if response.status_code == 200:
                return response.json() # If successful, return the response data in JSON format
            else:
                print(f"Attempt {attempt + 1} failed with status code: {response.status_code}") # If not successful, print the attempt number and status code
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed with error: {e}") # Handle any exceptions during the request (e.g., timeout, connection errors)
    
    raise Exception("Failed to fetch data after multiple attempts")

def get_route(session_id):
    url = "https://hackdiversity.xyz/api/navigation/routes"
    headers = {
        "Authorization": f"Bearer {session_id}"  
    }
    response = requests.get(url, headers=headers) # Send GET request to fetch routes
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch routes: {response.status_code}")

routes = get_route(session_id)

def filter_routes(routes):
    '''Filter only accessible routes from the data.'''
    accessible_routes = []
    for route in routes:
        if route.get('is_accessible'): # Loop through the routes and add those with 'is_accessible' set to True
            accessible_routes.append(route)
    return accessible_routes

def sort_by_distance(routes):
    '''Sort routes using bubble sort.'''
    k = len(routes)
    for i in range(k):
        for j in range(0, k - i - 1):
            if routes[j]['distance'] > routes[j + 1]['distance']:
                routes[j], routes[j + 1] = routes[j + 1], routes[j] #iterating through the routes and swapping them based on distance
    return routes

accessible_routes = filter_routes(routes) # Filtering accessible routes from the retrieved data
sorted_routes = sort_by_distance(accessible_routes) # Sorting the filtered routes by distance

def test_algorithm(session_id):
    # Retrieve sample data
    test_url = "https://hackdiversity.xyz/api/test/mockRoutes"
    headers = {
        "Authorization": f"Bearer {session_id}"  # Correct Authorization format
    }
    test_routes = requests.get(test_url, headers=headers).json()  # Fetch test routes data

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
    response = requests.post(url, json=sorted_routes, headers=headers) # Submit the sorted final routes

    if response.status_code in [200, 201]:
        print("Final routes submitted successfully.") # Check if the response status code is 200 or 201 (success)
        print("Response:", response.json())
    else:
        raise Exception(f"Failed to submit final routes: {response.status_code}") # Raise an exception if submission fails

submit_final_routes(session_id, sorted_routes)

def check_status(session_id):
    url = "https://hackdiversity.xyz/api/navigation/status"
    headers = {
        "Authorization": f"Bearer {session_id}" 
    }
    response = requests.get(url, headers=headers) # Send a GET request to check the status of the session

    if response.status_code == 200:
        print("Status:", response.json()) 
    else:
        raise Exception(f"Failed to check status: {response.status_code}") # Raise an exception if status check fails

check_status(session_id)
