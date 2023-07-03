import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define your API key and series ID
api_key = 'dcfc236e067e45e8a956b45342b80203'
series_id = 'FINSAL'

# Calculate the start date 3 years ago
start_date = datetime.now() - timedelta(days=3*365)
start_date_str = start_date.strftime('%Y-%m-%d')

# Construct the API request URL
url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_date_str}'

# Send the API request and get the response
response = requests.get(url)

# Parse the response JSON
data = response.json()

# Check if the response contains an error
if 'error_code' in data:
    print(f"API Error: {data['error_message']}")
else:
    # Extract dates and values from the response
    dates = [entry['date'] for entry in data['observations']]
    values = [float(entry['value']) for entry in data['observations']]

    # Calculate the percentage change from one period ago
    percent_changes = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

    # Apply the transformation formula (((1+a)/100)^4))-1
    transformed_changes = [(1 + change / 100) ** 4 - 1 for change in percent_changes]

    # Create a bar chart
    plt.bar(dates[1:], transformed_changes)
    plt.xlabel('Date')
    plt.ylabel('Nominal Final Demand CAGR')
    plt.title('Nominal Final Demand CAGR')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



