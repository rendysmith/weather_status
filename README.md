Weather SDK

This is a simple Python SDK (Software Development Kit) designed to retrieve weather information using the OpenWeatherAPI. The SDK allows users to fetch current weather data for a given city and also provides the option to periodically update weather information for multiple cities. It utilizes SQLite for storing weather data of the requested cities.
Features

    City-based Weather Information: The SDK accepts a city name and returns information about the current weather in that city.
    Data Caching: It stores weather data of requested cities locally, allowing quick access to recent weather information. Data is considered valid if it's less than 10 minutes old.
    Support for Multiple Cities: The SDK can handle weather data for multiple cities simultaneously, up to a maximum of 10 cities.
    Two Operating Modes:
        On-demand Mode: Updates weather information only when requested by the client.
        Polling Mode: Periodically updates weather information for all stored locations to ensure instant response to client requests.
    Exception Handling: The SDK throws exceptions with descriptive messages in case of any failures, such as API key errors or network issues.
    Modular Testing: Unit tests are available for SDK methods, utilizing mock requests for network operations.

Installation and Setup

    Clone the repository or download the code files.
    Ensure you have Python installed on your system (version 3.6 or above recommended).
    Install the required dependencies using pip:

    pip install requests

    Obtain an API key from OpenWeatherAPI. You can sign up for an account and get the key from OpenWeatherAPI website.
    Create a SQLite database named weather.db in the same directory as the code file.
    Run the create_table() function to create the necessary table structure in the database.

Usage

    Import the SDK module into your Python script:

    python

from weather_sdk import get_weather

Initialize the SDK with your OpenWeatherAPI key:

python

API_KEY = "your_api_key_here"

Choose the mode of operation:

    On-demand Mode: Fetch weather information for a specific city:

    python

city_name = "Tokyo"  # Replace with the desired city name
weather_data = get_weather(API_KEY, city_name)
print(weather_data)

Polling Mode: Update weather information for all stored cities:

python

        mode = 2
        weather_data = get_weather(API_KEY, mode=mode)
        print(weather_data)

    Handle the returned weather data as needed for your application.

Testing

The SDK includes unit tests to ensure the correctness of its functionality. To run the tests, execute the test script included in the repository:

python test_weather_sdk.py

Ensure that the SDK functions correctly under different scenarios, including successful API calls, error responses, and data caching.
Contributions

Contributions to this SDK are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on GitHub.
License

This project is licensed under the MIT License. See the LICENSE file for more details.
Author

This SDK is maintained by [Your Name]. For inquiries or support, please contact ritmorica@gmail.com.
