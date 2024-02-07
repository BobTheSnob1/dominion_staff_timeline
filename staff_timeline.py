import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import requests
from io import StringIO
from tqdm import tqdm


def plot_staff_timeline():
    # URL of the published Google Sheets document (replace with your URL)
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQodbH1DyWrvBdsGa_egy98PDxeLoMMu5yw8Bzb2tGUy2i3kE17e0NReWK1d75V9-eHGeiVjUa468dZ/pub?gid=945876828&single=true&output=csv'  # noqa: E501

    print(f'Downloading data from {url}...')

    # Fetch the CSV data
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Read the CSV data into a DataFrame
    data = StringIO(response.text)
    # specify column 0 as the index, otherwise pd will add its own
    df = pd.read_csv(data, index_col=0)

    # Convert index to datetime and limit the timeline to the current date
    df.index = pd.to_datetime(df.index)
    current_date = datetime.now()
    df = df[df.index <= current_date]

    # Visualization
    fig, ax = plt.subplots(figsize=(15, 10))  # Adjust size as needed

    # Colors for roles, including 'Not staff'
    colors = {
        'Helper': 'teal',
        'Curator': 'purple',
        'Moderator': 'blue',
        'Admin': 'red',
        'Retired/Removed': 'none',
        '': 'none'
    }

    for i in range(len(df.columns)):
        if i % 2 == 0:
            ax.axhspan(i - 0.5, i + 0.5, facecolor='lightgray', alpha=0.5)

    role_times = input('Would you like to add numbers for time spent in each role? [y/n]: ')  # noqa: E501
    while role_times not in ['y', 'n']:
        role_times = input("Please enter either 'y' or 'n': ")
    role_times = True if role_times == 'y' else False

    # Plotting each staff member's timeline
    for index, staff_member in tqdm(
            enumerate(df.columns),
            total=len(df.columns),
            desc="Processing:"
            ):

        current_role = None
        start_date = None
        new_staff = True

        for date in df.index:
            role = df.at[date, staff_member]

            if pd.isna(role):
                role = ''  # Assign a default role for NaN values

            if role != current_role:
                if (start_date and
                        current_role and
                        colors[current_role] != 'none'):

                    # Calculate the duration in days
                    duration = (date - start_date).days

                    # Plot the period of the previous role
                    bar = ax.barh(
                        staff_member,
                        duration, left=start_date,
                        color=colors[current_role]
                    )

                    # Check if this staff member is new
                    if new_staff and start_date > datetime(2019, 8, 25):
                        # Add the staff member's name as a label
                        ax.text(
                            start_date, staff_member,
                            staff_member + ' ', va='center', ha='right',
                            fontsize=4, color='black'
                        )
                        new_staff = False

                    if role == 'Retired/Removed':
                        new_staff = True

                    if role_times:
                        # Annotate the duration next to the bar
                        ax.text(
                            start_date + (date - start_date) / 2,
                            staff_member,
                            str(duration),
                            va='center', ha='center',
                            fontsize=4, color='black'
                        )

                current_role = role
                start_date = date

        # Ensure the last role period is plotted and annotated
        if start_date and current_role and colors[current_role] != 'none':
            duration = (df.index[-1] - start_date).days
            ax.barh(
                staff_member,
                duration, left=start_date,
                color=colors[current_role]
            )
            if role_times:
                ax.text(
                    start_date + (df.index[-1] - start_date) / 2,
                    staff_member,
                    str(duration),
                    va='center', ha='center',
                    fontsize=4, color='black'
                )

    print(' =================================================\n',
          '   Processing complete!\n',
          '================================================='
          )
    # Setting labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Staff Members')
    ax.set_title('Staff Timeline')

    # Adjust y-axis label size
    ax.tick_params(axis='y', labelsize='4')

    ax.yaxis.grid(False)  # Horizontal gridlines
    ax.xaxis.grid(True)  # Vertical gridlines

    plt.xticks(rotation=45)
    plt.tight_layout()

    final_path = input('What should the file name be?\nFile name: ')
    final_dpi = int(input(
        'What should the dpi be? (Resolution is dpi*15 x dpi*10)\ndpi: '
    ))

    while True:
        try:
            plt.savefig(final_path, dpi=final_dpi)
            print(f"Timeline saved to '{final_path}'")
            break
        except TypeError or ValueError:
            print('This is not a valid number. Must be an integer.')
            final_dpi = int(input(
                'What should the dpi be? (Resolution is dpi*15 x dpi*10)' +
                '\ndpi: '
            ))

    plt.show()


if __name__ == "__main__":
    plot_staff_timeline()
