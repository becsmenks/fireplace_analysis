# Fireplace Analysis
# Script: 002_preprocess_data.py
# Author: Becca Kuss
# Date 2021-02-18

# A - Clean Up Log Data ===========================================================

# For fires that span more than one day, add as two entries
is_spanning = log_data['fire_end_hour'] < log_data['fire_start_hour']

# Create two new rows to replace the single row
new_entry_early = log_data[is_spanning]
new_entry_late = log_data[is_spanning]

# For the early row, set the end hour to midnight
new_entry_early['fire_end_hour'] = np.array([23] * new_entry_early.shape[0])
new_entry_early['fire_end_min'] = np.array([55] * new_entry_early.shape[0])

# For the late row, set the start hour to midnight, and add a day
new_entry_late['fire_start_hour'] = np.array([0] * new_entry_late.shape[0])
new_entry_late['fire_start_min'] = np.array([0] * new_entry_late.shape[0])
new_entry_late['date'] = new_entry_late['date'] + pd.DateOffset(days=1)

# Concatenate the data into the final log data
log_data_list = [log_data[-is_spanning]] + [new_entry_early] + [new_entry_late]
log_data = pd.concat(log_data_list, axis=0, ignore_index=True)

# B - Join Log Data and Ecobee Data ================================================

