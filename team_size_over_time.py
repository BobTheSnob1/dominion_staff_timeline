import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
from io import StringIO
from datetime import datetime


def plot_team_size_over_time():
    # URL of the published Google Sheets document
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQodbH1DyWrvBdsGa_egy98PDxeLoMMu5yw8Bzb2tGUy2i3kE17e0NReWK1d75V9-eHGeiVjUa468dZ/pub?gid=945876828&single=true&output=csv'  # noqa: E501

    print(f'Downloading data from {url}...')

    # Fetch the CSV data
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    response.raise_for_status()

    # Read the CSV data into a DataFrame
    data = StringIO(response.text)
    df = pd.read_csv(data, index_col=0)
    df.index = pd.to_datetime(df.index)

    # Filter data to current date
    current_date = datetime.now()
    filtered_data = df[df.index <= current_date]

    # Ensuring no future dates are included
    filtered_data = filtered_data.loc[:current_date]

    # Count occurrences of each role per day
    role_counts_per_day = {
        'Admin': filtered_data.apply(
            lambda x: x.str.contains('Admin', na=False).sum(), axis=1
            ),
        'Moderator': filtered_data.apply(
            lambda x: x.str.contains('Moderator', na=False).sum(), axis=1
            ),
        'Curator': filtered_data.apply(
            lambda x: x.str.contains('Curator', na=False).sum(), axis=1
            ),
        'Helper': filtered_data.apply(
            lambda x: x.str.contains('Helper', na=False).sum(), axis=1
            )
    }

    # Plotting
    plt.figure(figsize=(15, 8))
    plt.stackplot(filtered_data.index,
                  role_counts_per_day['Admin'],
                  role_counts_per_day['Moderator'],
                  role_counts_per_day['Curator'],
                  role_counts_per_day['Helper'],
                  colors=['red', 'blue', 'purple', 'teal'])
    plt.plot(filtered_data.index, sum(role_counts_per_day.values()),
             color='black', linewidth=2)
    plt.title('Team Size Over Time by Role')
    plt.xlabel('Date')
    plt.ylabel('Number of Members')
    plt.grid(axis='x')
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=90)
    plt.xlim(filtered_data.index.min(), filtered_data.index.max())
    plt.show()


if __name__ == "__main__":
    plot_team_size_over_time()
