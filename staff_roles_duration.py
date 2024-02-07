import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO


def plot_staff_roles_duration():
    # URL of the published Google Sheets document
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQodbH1DyWrvBdsGa_egy98PDxeLoMMu5yw8Bzb2tGUy2i3kE17e0NReWK1d75V9-eHGeiVjUa468dZ/pub?gid=945876828&single=true&output=csv'  # noqa: E501

    print(f'Downloading data from {url}...')

    # Fetch the CSV data
    response = requests.get(url)
    response.raise_for_status()

    # Read the CSV data into a DataFrame
    data = StringIO(response.text)
    df = pd.read_csv(data, index_col=0)
    df.index = pd.to_datetime(df.index)

    # Count occurrences of each role per staff member
    staff_roles_counts = {}
    for column in df.columns:
        staff_data = df[column].dropna()
        if not staff_data.empty:
            roles = staff_data.value_counts()
            staff_roles_counts[column] = roles

    # Convert to DataFrame and fill NaN
    staff_roles_df = pd.DataFrame.from_dict(staff_roles_counts, orient='index')
    staff_roles_df.fillna(0, inplace=True)

    # Color mappings
    role_colors = {
        'Admin': 'red',
        'Moderator': 'blue',
        'Curator': 'purple',
        'Helper': 'teal'
        }

    # Plotting
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    roles = ['Admin', 'Moderator', 'Curator', 'Helper']

    for i, role in enumerate(roles):
        ax = axes[i // 2, i % 2]
        ax.hist(staff_roles_df[role], bins=20, color=role_colors[role])
        ax.set_title(f'{role} Tenure')
        ax.set_xlabel('Days in Role')
        ax.set_ylabel('Number of Staff Members')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_staff_roles_duration()
