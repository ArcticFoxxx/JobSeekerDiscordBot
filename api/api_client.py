import requests
import os
def get_job_listings(keywords, location, salary, results_to_take):
    '''
    This function gets job requests from www.reed.com

    parm: location, keywords, results to take, salary etc. TODO

    output: Json
    '''

    # Defining a params dict for the parameters to be sent to the API
    API_ENDPOINT = 'https://www.reed.co.uk/api/1.0/search'
    API_KEY = os.environ.get("API_KEY")


    params = {
        'keywords': keywords,
        'location': location,
        'minimumSalary': salary,
        'resultsToTake': results_to_take
    }

    # Sending a GET request and saving the response as a response object
    response = requests.get(url=API_ENDPOINT, params=params, auth=(API_KEY, ''))

    # Handle the response
    if response.status_code == 200:
        # Request succeeded, process the response
        data = response.json()
        return data
    else:
        # Request failed, handle the error
        print(f'Request failed with status code: {response.status_code}')
        return None