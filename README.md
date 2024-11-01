# Ham-Radio-Contact-Logger
A GUI application for logging ham radio contacts, displaying country information, Maidenhead grid square, local time, GPS coordinates, and weather conditions based on user input. The app uses the OpenCage and OpenWeatherMap APIs to fetch location and weather data.

Features

    Log ham radio contacts with details like callsign, frequency, mode, report, country, town, and weather.
    Automatically fetches and displays location-specific data such as:
        - Maidenhead Grid Square
        - Local GPS Coordinates
        - Local Time
        - Weather information
    
	Save and view logs in a CSV format.

Prerequisites

    - Python 3.x
    
	Required Python libraries:
		- tkinter for GUI
        - requests for making API requests
        - pytz and timezonefinder for handling timezone information
    
	API Keys:
        - OpenCage Geocoding API Key
        - OpenWeatherMap API Key

Installation

    Clone or download this repository:
	git clone https://github.com/yourusername/ham-radio-contact-logger.git
	
	cd ham-radio-contact-logger

	Install the required Python packages: Use the following command to install the required libraries if they are not already installed.

	pip install requests pytz timezonefinder
	
	Set up API keys:

    Sign up for an OpenCage API Key and get your API key. - https://opencagedata.com/
    Sign up for an OpenWeatherMap API Key and get your API key. - https://openweathermap.org/

Insert API Keys in Code:

    Open the Python file (ham_radio_logger.py or similar).
    Find the following lines and replace "YOUR_API_KEY" with your actual API keys:

Usage

    1. Run the Application: Start the application by running:
	
	python ham_radio_logger.py

    2. Logging a Contact:
        Enter the following details in the respective fields:
			- Callsign
            - Frequency (MHz)
            - Mode
            - Signal Report
            - Country
            - Town
        
	The app will automatically fetch location-specific information based on country and town, including:
            - Grid Square
            - GPS Coordinates
            - Local Time
            - Weather
			
    Click Log Contact to save the contact in ham_radio_contacts.csv.

    3. Viewing Logged Contacts:
        Click View Log to open a new window displaying all saved contact entries.

File Structure

    - ham_radio_logger.py: Main application code.
    - ham_radio_contacts.csv: Stores all logged contacts in CSV format (created on first log entry).

Error Handling

If the application encounters issues, such as missing API keys, connection issues, or failed API responses, it will display an appropriate error message.
License

This project is licensed under the MIT License. Feel free to use, modify, and distribute this software.
