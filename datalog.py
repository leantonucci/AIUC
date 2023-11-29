import serial
import matplotlib.pyplot as plt
import time
from datetime import datetime

def send_and_receive(serial_port, message):
    ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
    ser.write(message.encode())
    response = ser.readline().decode().strip()
    ser.close()
    return response

def main():
    serial_port = 'COM5'  # Change this to the appropriate port on your system
    message_to_send = '3A.Value?\n'  # Change this to the message you want to send

    # Initialize lists to store data for plotting
    timestamps = []
    temps = []

    try:
        while True:
            # Send and receive data
            response = send_and_receive(serial_port, message_to_send)
            print(f"Message to PTC10 sent: {message_to_send}")
            print(f"Response: {response}")

            try:
                # Convert the received string to float
                temp = float(response)
                print(f"Temp to plot: {temp}")

                # Append temps to the lists
                timestamps.append(datetime.now())
                temps.append(temp)

                # Plot the updated data
                plt.plot(timestamps, temps)
                plt.title('Received Temps')
                plt.xlabel('Datetime')
                plt.ylabel('Temperature')
                plt.xticks(rotation=45, ha='right')
                plt.pause(0.1)  # Pause to update the plot

                # Wait for 5 seconds before the next iteration
                time.sleep(5)

            except ValueError:
                print("Received data is not a valid float.")

    except KeyboardInterrupt:
        print("Plotting stopped by the user.")

if __name__ == "__main__":
    main()

