import pickle
from tabulate import tabulate

# Load the top_300_users_dict from the file
with open('top_300_users_dict.pkl', 'rb') as f:
    top_300_users_dict_loaded = pickle.load(f)

# Convert the dictionary to a list of lists for tabulate
table_data = [
    [username, user_data['activity_count'], ', '.join(user_data['subreddits'])]
    for username, user_data in top_300_users_dict_loaded.items()
]

# Generate the table
table = tabulate(table_data, headers=['Username', 'Activity Count', 'Subreddits'], tablefmt='grid')

# Save the table to a file
with open('top_300_users_table.txt', 'w') as f:
    f.write(table)

