E401 = """
    You did not specify your API key in API request.
    Your API key is not activated yet. Within the next couple of hours, it will be activated and ready to use.
    You are using wrong API key in API request. Please, check your right API key in personal account.
    You are using a Free subscription and try requesting data available in other subscriptions . For example, 16 days/daily forecast API, any historical weather data, Weather maps 2.0, etc). 
    Please, check your subscription in your personal account.
"""

E404 = """
    You can get this error when you specified the wrong city name, ZIP-code or city ID. 
    For your reference, this list contains City name, City ID, Geographical coordinates of the city (lon, lat), Zoom, etc.
    You can also get the error 404 if the format of your API request is incorrect. 
    In this case, please review it and check for any mistakes. To see examples of correct API requests, 
    please visit the Documentation of a specific API and read the examples of API calls there.
"""

E429 = """
    If you have a Free plan of Professional subscriptions and make more than 60 API calls per minute 
    (surpassing the limit of your subscription). 
    To avoid this situation, please consider upgrading to a subscription plan that meets your needs or reduce 
    the number of API calls in accordance with the limits.
"""

E500504 ="""
    In case you receive one of the following errors 500, 502, 503 or 504 please contact us for assistance. 
    Please enclose an example of your API request that receives this error into your email to let us analyze it 
    and find a solution for you promptly. 
"""