import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_team_size_over_time(file_path):
    # Load the data
    data = pd.read_csv(file_path)

    # Filter data to current date
    current_date = pd.to_datetime("now")
    filtered_data = data[data.iloc[:, 0] <= current_date]

    # Count occurrences of each role per day
    role_counts_per_day = {
        'Admin': filtered_data.iloc[:, 1:].apply(
            lambda x: x.str.contains('Admin', na=False).sum(), axis=1
            ),
        'Moderator': filtered_data.iloc[:, 1:].apply(
            lambda x: x.str.contains('Moderator', na=False).sum(), axis=1
            ),
        'Curator': filtered_data.iloc[:, 1:].apply(
            lambda x: x.str.contains('Curator', na=False).sum(), axis=1
            ),
        'Helper': filtered_data.iloc[:, 1:].apply(
            lambda x: x.str.contains('Helper', na=False).sum(), axis=1
            )
    }

    # Plotting
    plt.figure(figsize=(15, 8))
    plt.stackplot(filtered_data.iloc[:, 0],
                  role_counts_per_day['Admin'],
                  role_counts_per_day['Moderator'],
                  role_counts_per_day['Curator'],
                  role_counts_per_day['Helper'],
                  colors=['red', 'blue', 'purple', 'teal'])
    plt.plot(filtered_data.iloc[:, 0], sum(
        role_counts_per_day.values()),
        color='black',
        linewidth=2)
    plt.title('Team Size Over Time by Role')
    plt.xlabel('Date')
    plt.ylabel('Number of Members')
    plt.grid(axis='x')
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.show()

# Example usage
# plot_team_size_over_time('path_to_your_csv_file.csv')
