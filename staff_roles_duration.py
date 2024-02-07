import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
from io import StringIO


def fetch_data(url):
    print(f'Downloading data from {url}...')
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("The request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

    data = StringIO(response.text)
    return pd.read_csv(data, index_col=0)


def calculate_role_durations(df):
    df.index = pd.to_datetime(df.index)
    current_date = pd.to_datetime("now")
    filtered_data = df[df.index <= current_date]

    staff_roles = {}
    for column in filtered_data.columns:
        staff_data = filtered_data[column].dropna()
        if not staff_data.empty:
            roles = staff_data.value_counts()
            staff_roles[column] = roles

    staff_roles_df = pd.DataFrame.from_dict(
        staff_roles,
        orient='index'
        ).fillna(0)

    # Calculate total tenure for each staff member and sort
    staff_roles_df['Total'] = staff_roles_df.sum(axis=1)
    staff_roles_df.sort_values('Total', ascending=False, inplace=True)
    staff_roles_df.drop('Total', axis=1, inplace=True)

    return staff_roles_df


def make_plot(staff_roles_df):
    fig, ax = plt.subplots(figsize=(20, 10))

    role_colors = {
        'Admin': 'red',
        'Moderator': 'blue',
        'Curator': 'purple',
        'Helper': 'teal'
        }
    bottom = np.zeros(len(staff_roles_df))

    for role, color in role_colors.items():
        if role in staff_roles_df.columns:
            ax.bar(
                staff_roles_df.index,
                staff_roles_df[role],
                bottom=bottom,
                color=color,
                label=role
            )
            bottom += staff_roles_df[role]

    ax.set_title('Duration in Staff Roles for Each Staff Member')
    ax.set_xlabel('Staff Member')
    ax.set_ylabel('Days in Role')
    ax.set_xticks(staff_roles_df.index)
    ax.set_xticklabels(staff_roles_df.index, rotation=90, fontsize=8)

    # Removing the vertical tick lines
    for tick in ax.get_xticklines():
        tick.set_visible(False)

    ax.grid(axis='x')
    plt.show()


def plot_staff_roles_duration():
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQodbH1DyWrvBdsGa_egy98PDxeLoMMu5yw8Bzb2tGUy2i3kE17e0NReWK1d75V9-eHGeiVjUa468dZ/pub?gid=945876828&single=true&output=csv'  # noqa: E501
    df = fetch_data(url)
    if df is not None:
        staff_roles_df = calculate_role_durations(df)
        make_plot(staff_roles_df)

    final_path = input("What should the file name be?\nFile name: ")
    final_dpi = int(
        input("What should the dpi be? (Resolution is dpi*15 x dpi*10)\ndpi: ")
    )

    while True:
        try:
            plt.savefig(final_path, dpi=final_dpi)
            print(f"Timeline saved to '{final_path}'")
            break
        except (TypeError, ValueError):
            print("This is not a valid number. Must be an integer.")
            final_dpi = int(
                input(
                    "What should the dpi be? (Resolution is dpi*15 x dpi*10)"
                    + "\ndpi: "
                )
            )


def main():
    plot_staff_roles_duration()


if __name__ == "__main__":
    main()
