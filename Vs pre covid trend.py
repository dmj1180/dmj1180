import requests
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from scipy.stats import linregress

# Define your API key and series ID
api_key = 'dcfc236e067e45e8a956b45342b80203'
series_id = 'FINSAL'

# Construct the API request URL
url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json'

# Send the API request and get the response
response = requests.get(url)

# Parse the response JSON
data = response.json()

# Check if the response contains an error
if 'error_code' in data:
    print(f"API Error: {data['error_message']}")
else:
    # Extract dates and values from the response, handling missing or invalid values
    dates = []
    values = []
    for entry in data['observations']:
        if 'value' in entry and entry['value'] != '.':
            dates.append(entry['date'])
            values.append(float(entry['value']))

    # Convert dates to datetime objects
    dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

    # Filter data starting from year 2010
    start_year = datetime(2010, 1, 1)
    filtered_dates = [date for date in dates if date >= start_year]
    filtered_values = [value for date, value in zip(dates, values) if date >= start_year]

    # Plot the line chart
    plt.plot(filtered_dates, filtered_values, label='FINSAL')

    # Add trendline for the period starting from 2010
    start_date = datetime(2010, 1, 1)
    end_date = filtered_dates[-1]  # Use the last date in the filtered data as the end date
    x = np.array([(date - start_date).days for date in filtered_dates])
    y = np.array(filtered_values)
    slope, intercept, _, _, _ = linregress(x, y)

    extrapolated_dates = [start_date + timedelta(days=day) for day in range((end_date - start_date).days + 1)]
    extrapolated_x = np.array([(date - start_date).days for date in extrapolated_dates])
    extrapolated_y = slope * extrapolated_x + intercept
    plt.plot(extrapolated_dates, extrapolated_y, linestyle='--', color='red', label='Trendline')

    # Set plot labels and title
    plt.xlabel('Year')
    plt.ylabel('FINSAL')
    plt.title('FINSAL Trendline')

    # Add legend
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()


