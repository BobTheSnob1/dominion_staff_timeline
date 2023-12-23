import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import requests
from io import StringIO

# URL of the published Google Sheets document (replace with your URL)
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQodbH1DyWrvBdsGa_egy98PDxeLoMMu5yw8Bzb2tGUy2i3kE17e0NReWK1d75V9-eHGeiVjUa468dZ/pub?gid=945876828&single=true&output=csv'  # noqa: E501

print(f"Downloading data from {url}...")

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

# Fill the data with roles, including "Not staff" periods
for index, staff_member in enumerate(df.columns):
    if (index + 1) % 10 == 0:
        print(f"Pre-processing {staff_member}, ",
              f"which is {index+1}/{len(df.columns)}")

    current_role = "Not staff"
    for date in df.index:
        role = df.at[date, staff_member]
        if pd.isna(role) or role == '':
            df.at[date, staff_member] = current_role
        else:
            current_role = role
            if role == 'Retired/Removed':
                current_role = "Not staff"

print(" ================================\n",
      "   Pre-processing complete...\n",
      "================================"
      )

# Visualization
fig, ax = plt.subplots(figsize=(15, 10))  # Adjust size as needed

# Colors for roles, including "Not staff"
colors = {
    'Helper': 'teal',
    'Curator': 'purple',
    'Moderator': 'blue',
    'Admin': 'red',
    'Retired/Removed': 'none',
    'Not staff': 'none'
}

for i in range(len(df.columns)):
    if i % 2 == 0:
        ax.axhspan(i - 0.5, i + 0.5, facecolor='lightgray', alpha=0.5)

# Plotting each staff member's timeline
for index, staff_member in enumerate(df.columns):
    if (index + 1) % 10 == 0:
        print(f"Processing {staff_member}, ",
              f"which is {index+1}/{len(df.columns)}")

    current_role = None
    start_date = None

    for date in df.index:
        role = df.at[date, staff_member]

        if role != current_role:
            if start_date and current_role:
                # Plot the period of the previous role
                ax.barh(
                    staff_member,
                    date - start_date, left=start_date,
                    color=colors[current_role]
                )
            current_role = role
            start_date = date

    # Ensure the last role period is plotted
    if start_date and current_role:
        ax.barh(
            staff_member,
            df.index[-1] - start_date,
            left=start_date, color=colors[current_role]
        )

print(" =================================================\n",
      "   Creating timeline, this may take a while...\n",
      "================================================="
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

# Save as a high-resolution image
final_path = input("What should the file name be?\nFile name: ")
plt.savefig(final_path, dpi=1000)  # Adjust filename as needed

print(f"Timeline saved to '{final_path}'")

plt.show()
