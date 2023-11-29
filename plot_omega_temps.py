import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.signal import find_peaks
from datetime import datetime
import numpy as np
date_format = '%m/%d/%Y %H:%M'

# Read the CSV file
csv_file = 'temps_oct31-nov6.csv'  
df = pd.read_csv(csv_file, encoding = 'utf8', delimiter=',')
print(f"{df}")
df_dict = df.to_dict(orient='dict')
print(f"df: {list(df_dict.keys())}")
print(df[' Date and Time (UTC)'])
window_length = 101
polyorder = 8
df['Smoothed Signal'] = savgol_filter(df[' RTD 1 (°C)'], window_length, polyorder)

peaks, _ = find_peaks(df['Smoothed Signal'])
valleys, _=find_peaks(-df['Smoothed Signal'])
diff_0 = np.concatenate((peaks, valleys))
diff_0 = sorted(diff_0)

# Extract the relevant columns
date_time = pd.to_datetime(df[' Date and Time (UTC)'], format=date_format)
print(f"date_time: {date_time}")
rtd1_temperature = df[' RTD 1 (°C)']
print(f"rtd1_temperature: {rtd1_temperature}")
rtd2_temperature = df[' RTD 2 (°C)']
print(f"rtd2_temperature: {rtd2_temperature}")
rtd1_temperature_smooth = df['Smoothed Signal']
print(f"rtd1_temperature: {rtd1_temperature_smooth}")



# Create a figure and axis for the plot
plt.figure(figsize=(10, 6))
plt.plot(date_time, rtd1_temperature, label='RTD 1 (°C)')
plt.plot(date_time, rtd2_temperature, label='RTD 2 (°C)')
#plt.plot(date_time, rtd1_temperature_smooth, label='RTD 1 smooth (°C)')
#plt.plot(date_time[peaks], df['Smoothed Signal'][peaks], 'ro', label='Local Maxima')
#plt.plot(date_time[valleys], df['Smoothed Signal'][valleys], 'bo', label='Local Minima')
print(date_time[peaks])

# Set plot labels and legend
plt.xlabel('Date and Time (UTC)')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Data from CSV')
plt.legend()

# Show the plot
plt.grid()
plt.tight_layout()


L_periods= []
L_periods.append(0)
L_pp= []
L_pp.append(0)
list_peaks= list(date_time[peaks])
list_val_diff0 = list(rtd1_temperature[diff_0])
list_dt_diff0 = list(date_time[diff_0])
for i in list_peaks:
    ind = list_peaks.index(i)
    if ind > 0:
        datetime2 = i
        datetime1 = list_peaks[ind-1]
        time_difference = float((datetime2 - datetime1).total_seconds())/60
        print(f"Difference between time {datetime1} (position {ind-1}) and {datetime2} (position {ind}) is: {time_difference} minutes")
        L_periods.append(time_difference)

for j in list_val_diff0:
    ind = list_val_diff0.index(j)
    if ind > 0:
        temp2 = j
        temp1 = list_val_diff0[ind-1]
        time2 = list_dt_diff0[ind]
        time1 = list_dt_diff0[ind -1]
        temp_difference = np.abs(temp2 - temp1)
        print(f"Temperature difference between time {temp1} (position {ind-1}) and {temp2} (position {ind}) is: {round(temp_difference,2)} °")
        L_pp.append(temp_difference)


plt.figure()
plt.plot(date_time[peaks], L_periods, label='Period')
plt.xlabel('Date and Time (UTC)')
plt.ylabel('Period (minutes)')
plt.title('Period through time')
print(f"Mean period with Kp~20: {np.round(np.mean(L_periods[5:43]),1)}")
print(f"Mean period with Kp~10: {np.round(np.mean(L_periods[43:48]),1)}")
print(f"Mean period with Kp~40: {np.round(np.mean(L_periods[48:68]),1)}")
print(f"Mean period with Kp~100: {np.round(np.mean(L_periods[68:759]),1)}")
plt.figure()
plt.plot(date_time[diff_0], L_pp, label='Peak to Peak')
plt.xlabel('Date and Time (UTC)')
plt.ylabel('Temperature (°C)')
plt.title('Peak to Peak value through time')
plt.show()

