# Fireplace Analysis
# Script: 001_import_data.py
# Author: Becca Kuss
# Date 2021-02-18

# A - Read in Log Data ===========================================================

# Read in the fireplace log data
log_data = pd.read_csv('fireplace_data/fireplace_usage.csv',
                       header=0,
                       names=["date", "fire_start", "fire_end", "note"])

# Replace NaNs in the end time with 23:55
log_data['fire_end'] = log_data['fire_end'].replace(np.nan, "23:55")

# Split the start and end columns into hour and minute
log_data[['fire_start_hour', 'fire_start_min']] = log_data.fire_start.str.split(":", expand=True)
log_data[['fire_end_hour', 'fire_end_min']] = log_data.fire_end.str.split(":", expand=True)

# Convert data types
log_data['date'] = pd.to_datetime(log_data['date'])
log_data['fire_start_hour'] = pd.to_numeric(log_data['fire_start_hour'])
log_data['fire_start_min'] = pd.to_numeric(log_data['fire_start_min'])
log_data['fire_end_hour'] = pd.to_numeric(log_data['fire_end_hour'])
log_data['fire_end_min'] = pd.to_numeric(log_data['fire_end_min'])

# Remove unnecessary columns
log_data = log_data.drop(columns=['fire_start', 'fire_end', 'note'])

# A - Read in Ecobee Data ===========================================================

# Read in the hourly ecobee thermostat data
ecobee_files = glob.glob('ecobee_data' + "/*.csv")
ecobee_data_list = []
for filename in ecobee_files:
    df = pd.read_csv(filename, header=None, index_col=False, skiprows=6,
                     names=["date", "time", "system_setting", "system_mode", "calendar_event", "program_mode",
                            "cool_sp_f", "heat_sp_f", "temp_f", "humidity", "outdoor_temp_f", "wind_speed_km_h",
                            "heat_stg1_sec", "fan_sec", "dm_offset", "tstat_temp", "tstat_hum", "laundry_f",
                            "laundry2", "office_f", "office2"])
    ecobee_data_list.append(df)

ecobee_data = pd.concat(ecobee_data_list, axis=0, ignore_index=True)

# Split the start and end columns into hour and minute
ecobee_data[['hour', 'min', 'sec']] = ecobee_data.time.str.split(":", expand=True)

# Convert data types
ecobee_data['date'] = pd.to_datetime(ecobee_data['date'])
ecobee_data['hour'] = pd.to_numeric(ecobee_data['hour'])
ecobee_data['min'] = pd.to_numeric(ecobee_data['min'])
ecobee_data['sec'] = pd.to_numeric(ecobee_data['sec'])

# Select columns we need
ecobee_data = ecobee_data[['date', 'hour', 'min', 'sec', 'heat_stg1_sec', 'outdoor_temp_f']]



