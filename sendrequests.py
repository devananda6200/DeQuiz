import requests

def generate_quiz(domain, interest):
    url = 'http://127.0.0.1:5000/generate_quiz'
    payload = {
        'domain': domain,
        'interest': interest
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raises an error for 4xx and 5xx responses
        print("Response from the server:")
        print(response.json())
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
        if e.response is not None:
            print(f"Response content: {e.response.content}")  # Print the full response content
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def submit_quiz(answers):
    url = 'http://127.0.0.1:5000/submit_quiz'
    payload = {
        'answers': answers
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raises an error for 4xx and 5xx responses
        print("Response from the server:")
        print(response.json())
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
        if e.response is not None:
            print(f"Response content: {e.response.content}")  # Print the full response content
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    domain = "Science"  # Change this to the appropriate domain
    interest = "Physics"  # Change this to the appropriate interest
    generate_quiz(domain, interest)

    # Example answers submission
    answers = ['A', 'C', 'B', 'D', 'A']  # Replace with actual user answers
    submit_quiz(answers)
