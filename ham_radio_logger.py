import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import requests
import pytz
from timezonefinder import TimezoneFinder

class HamRadioLoggerApp:
    def __init__(self, root):
        """Initialize the GUI components of the Ham Radio Contact Logger App"""
        self.root = root
        self.root.title("Ham Radio Contact Logger")

        # Labels and Entry Fields for User Inputs
        # Callsign input
        self.callsign_label = tk.Label(root, text="Callsign:")
        self.callsign_label.grid(row=0, column=0, padx=10, pady=5)
        self.callsign_entry = tk.Entry(root)
        self.callsign_entry.grid(row=0, column=1, padx=10, pady=5)
        self.callsign_entry.bind('<KeyRelease>', self.update_country_by_callsign)

        # Frequency input
        self.frequency_label = tk.Label(root, text="Frequency (MHz):")
        self.frequency_label.grid(row=1, column=0, padx=10, pady=5)
        self.frequency_entry = tk.Entry(root)
        self.frequency_entry.grid(row=1, column=1, padx=10, pady=5)

        # Mode input
        self.mode_label = tk.Label(root, text="Mode:")
        self.mode_label.grid(row=2, column=0, padx=10, pady=5)
        self.mode_entry = tk.Entry(root)
        self.mode_entry.grid(row=2, column=1, padx=10, pady=5)

        # Signal Report input
        self.report_label = tk.Label(root, text="Signal Report:")
        self.report_label.grid(row=3, column=0, padx=10, pady=5)
        self.report_entry = tk.Entry(root)
        self.report_entry.grid(row=3, column=1, padx=10, pady=5)

        # Country input
        self.country_label = tk.Label(root, text="Country:")
        self.country_label.grid(row=4, column=0, padx=10, pady=5)
        self.country_entry = tk.Entry(root)
        self.country_entry.grid(row=4, column=1, padx=10, pady=5)
        self.country_entry.bind('<KeyRelease>', self.update_location_info)

        # Town input
        self.town_label = tk.Label(root, text="Town:")
        self.town_label.grid(row=5, column=0, padx=10, pady=5)
        self.town_entry = tk.Entry(root)
        self.town_entry.grid(row=5, column=1, padx=10, pady=5)
        self.town_entry.bind('<KeyRelease>', self.update_location_info)

        # Display fields for derived data
        self.grid_square_label = tk.Label(root, text="Grid Square:")
        self.grid_square_label.grid(row=6, column=0, padx=10, pady=5)
        self.grid_square_value = tk.Label(root, text="N/A")
        self.grid_square_value.grid(row=6, column=1, padx=10, pady=5)

        self.coords_label = tk.Label(root, text="GPS Coordinates:")
        self.coords_label.grid(row=7, column=0, padx=10, pady=5)
        self.coords_value = tk.Label(root, text="N/A")
        self.coords_value.grid(row=7, column=1, padx=10, pady=5)

        self.local_time_label = tk.Label(root, text="Local Time:")
        self.local_time_label.grid(row=8, column=0, padx=10, pady=5)
        self.local_time_value = tk.Label(root, text="N/A")
        self.local_time_value.grid(row=8, column=1, padx=10, pady=5)

        self.weather_label = tk.Label(root, text="Weather:")
        self.weather_label.grid(row=9, column=0, padx=10, pady=5)
        self.weather_value = tk.Label(root, text="N/A")
        self.weather_value.grid(row=9, column=1, padx=10, pady=5)

        # Log and View Buttons
        self.log_button = tk.Button(root, text="Log Contact", command=self.log_contact)
        self.log_button.grid(row=10, column=0, columnspan=2, pady=10)

        self.view_button = tk.Button(root, text="View Log", command=self.view_log)
        self.view_button.grid(row=11, column=0, columnspan=2, pady=5)

    def update_country_by_callsign(self, event=None):
        """Update country based on the callsign input"""
        callsign = self.callsign_entry.get()
        if callsign:
            country = self.get_country_by_callsign(callsign)
            if country:
                self.country_entry.delete(0, tk.END)
                self.country_entry.insert(0, country)
                self.update_location_info()

    def update_location_info(self, event=None):
        """Update location information based on the country and town input"""
        country = self.country_entry.get()
        town = self.town_entry.get()
        if country and town:
            self.get_grid_square(country, town)

    def get_country_by_callsign(self, callsign):
        """Fetch country data for a given callsign using an API"""
        try:
            response = requests.get(f'https://api.hamqth.com/callbook/?callsign={callsign}')
            if response.status_code == 200:
                data = response.json()
                return data.get('country', 'N/A')
            else:
                return 'N/A'
        except requests.RequestException:
            return 'N/A'

    def get_grid_square(self, country, town):
        """Retrieve latitude, longitude, and grid square information for the given location"""
        try:
            api_key = "YOUR_API_KEY"  # Insert your actual OpenCage API key here
            location = f"{town}, {country}"
            response = requests.get(
                f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={api_key}"
            )
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    lat = data['results'][0]['geometry']['lat']
                    lon = data['results'][0]['geometry']['lng']
                    grid_square = self.lat_lon_to_grid_square(lat, lon)
                    self.display_grid_square_and_coords(lat, lon, grid_square)
                    self.get_local_time_and_weather(lat, lon)
                    return grid_square
                else:
                    messagebox.showerror("Lookup Error", "No results found for the given location.")
                    return 'N/A'
            else:
                messagebox.showerror("API Error", f"Failed to retrieve data: {response.status_code} {response.reason}")
                return 'N/A'
        except requests.RequestException as e:
            messagebox.showerror("Request Exception", f"An error occurred: {e}")
            return 'N/A'

    def lat_lon_to_grid_square(self, lat, lon):
        """Convert latitude and longitude to Maidenhead Grid Square"""
        upper_lat = lat + 90
        upper_lon = lon + 180

        A = int(upper_lon / 20)
        B = int(upper_lat / 10)
        C = int((upper_lon - A * 20) / 2)
        D = int((upper_lat - B * 10) / 1)

        E = int((upper_lon - A * 20 - C * 2) * 12)
        F = int((upper_lat - B * 10 - D * 1) * 24)

        return f"{chr(A + 65)}{chr(B + 65)}{C}{D}{chr(E + 65)}{chr(F + 65)}"

    def display_grid_square_and_coords(self, lat, lon, grid_square):
        """Display the calculated grid square and coordinates on the GUI"""
        self.grid_square_value.config(text=grid_square)
        self.coords_value.config(text=f"Lat: {lat}, Lon: {lon}")

    def get_local_time_and_weather(self, lat, lon):
        """Fetch and display the local time and weather based on coordinates"""
        try:
            # Get local time using timezone information
            tf = TimezoneFinder()
            timezone_str = tf.timezone_at(lat=lat, lng=lon)
            if timezone_str:
                tz = pytz.timezone(timezone_str)
                local_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
                self.local_time_value.config(text=local_time)
            else:
                self.local_time_value.config(text="N/A")

            # Get weather using OpenWeatherMap API
            weather_api_key = "YOUR_API_KEY"  # Insert your actual OpenWeatherMap API key here
            weather_response = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"
            )
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                weather_description = weather_data['weather'][0]['description']
                temperature = weather_data['main']['temp']
                weather_info = f"{weather_description.capitalize()}, {temperature} °C"
                self.weather_value.config(text=weather_info)
            else:
                self.weather_value.config(text="N/A (No Data)")
        except requests.RequestException as e:
            self.local_time_value.config(text="N/A")
            self.weather_value.config(text="N/A")
            messagebox.showerror("Request Exception", f"An error occurred while fetching local time or weather: {e}")

    def log_contact(self):
        """Log contact data to CSV and clear the input fields"""
        # Get data from the entry fields
        callsign = self.callsign_entry.get()
        frequency = self.frequency_entry.get()
        mode = self.mode_entry.get()
        report = self.report_entry.get()
        country = self.country_entry.get()
        town = self.town_entry.get()
        grid_square = self.grid_square_value.cget('text')
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        local_time = self.local_time_value.cget("text")
        weather = self.weather_value.cget("text")

        # Validate input
        if not callsign or not frequency or not mode or not report or not country or not town:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        # Write data to CSV file
        with open("ham_radio_contacts.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([callsign, frequency, mode, report, country, town, grid_square, date_time, local_time, weather])

        # Clear entry fields after logging
        self.callsign_entry.delete(0, tk.END)
        self.frequency_entry.delete(0, tk.END)
        self.mode_entry.delete(0, tk.END)
        self.report_entry.delete(0, tk.END)
        self.country_entry.delete(0, tk.END)
        self.town_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", "Contact logged successfully!")

    def view_log(self):
        """Display the log of contacts in a new window"""
        try:
            with open("ham_radio_contacts.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                log_entries = ""
                for row in reader:
                    if len(row) >= 10:
                        log_entries += (
                            f"Callsign: {row[0]}, "
                            f"Frequency: {row[1]} MHz, "
                            f"Mode: {row[2]}, "
                            f"Report: {row[3]}, "
                            f"Country: {row[4]}, "
                            f"Town: {row[5]}, "
                            f"Grid Square: {row[6]}, "
                            f"Date/Time: {row[7]}, "
                            f"Local Time: {row[8]}, "
                            f"Weather: {row[9]}\n"
                        )
                    else:
                        log_entries += "Incomplete log entry: missing fields.\n"

            # Create a new window to display the log entries
            if log_entries:
                log_window = tk.Toplevel(self.root)
                log_window.title("Logged Contacts")
                log_text = tk.Text(log_window, wrap='word')
                log_text.insert(tk.END, log_entries)
                log_text.config(state='disabled')
                log_text.pack(expand=True, fill='both', padx=10, pady=10)
            else:
                messagebox.showinfo("Log", "No contacts logged yet.")
        except FileNotFoundError:
            messagebox.showinfo("Log", "No contacts logged yet.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HamRadioLoggerApp(root)
    root.mainloop()
