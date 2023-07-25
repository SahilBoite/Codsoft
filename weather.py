import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import emoji
from datetime import datetime
from dateutil import tz

API_KEY = "401d57814b6ad22f7261954e9ca12c02"
API_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data():
    district = district_var.get()
    if not district:
        messagebox.showwarning("Warning", "Please select a district.")
        return

    params = {
        "appid": API_KEY,
        "q": f"{district},IN",
        "units": "metric"
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        display_weather_data(data)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch weather data: {e}")

def display_weather_data(data):
    # Clear previous data
    for row in weather_tree.get_children():
        weather_tree.delete(row)

    table_data = [
        ("Location", f"{district_var.get()}, India"),
        ("Temperature", f"{data['main']['temp']:.1f} °C"),
        ("Humidity", f"{data['main']['humidity']}%"),
        ("Wind Speed", f"{data['wind']['speed']} m/s"),
        ("Weather Description", f"{get_weather_emoji(data['weather'][0]['description'])} {data['weather'][0]['description'].capitalize()}"),
    ]

    # Convert sunrise and sunset times to human-readable format
    utc_zone = tz.gettz("UTC")
    local_zone = tz.tzlocal()
    sunrise_time = datetime.fromtimestamp(data["sys"]["sunrise"], tz=utc_zone).astimezone(local_zone).strftime("%H:%M:%S")
    sunset_time = datetime.fromtimestamp(data["sys"]["sunset"], tz=utc_zone).astimezone(local_zone).strftime("%H:%M:%S")
    table_data.append(("Sunrise", sunrise_time))
    table_data.append(("Sunset", sunset_time))

    visibility = data.get("visibility", "N/A")
    if visibility != "N/A":
        visibility = f"{visibility / 1000:.1f} km"  # Convert visibility to kilometers
    table_data.append(("Visibility", visibility))

    atmospheric_pressure = data["main"]["pressure"]
    table_data.append(("Atmospheric Pressure", f"{atmospheric_pressure} hPa"))

    # Insert data into the table
    for row_data in table_data:
        weather_tree.insert("", tk.END, values=row_data)

    # Resize the window to fit the content
    app.update_idletasks()
    app.geometry("")

def get_weather_emoji(weather_description):
    # Define mapping of weather conditions to emojis
    emoji_mapping = {
        "Clear sky": "☀️",
        "Few clouds": "🌤️",
        "Scattered clouds": "⛅️",
        "Broken clouds": "🌤️",
        "Shower rain": "🌦️",
        "Rain": "🌧️",
        "Thunderstorm": "⛈️",
        "Snow": "🌨️",
        "Mist": "🌪️",
    }

    # Return the corresponding emoji or a default one if not found
    return emoji_mapping.get(weather_description, "❓")

# Create the main application window
app = tk.Tk()
app.title("Weather Forecast App")

# Indian districts list as an option list
indian_districts = [
    "Select District",
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Chennai",
    # Add more Indian districts here
]

district_var = tk.StringVar(app)
district_var.set(indian_districts[0])  # Default value is "Select District"

district_option_menu = ttk.OptionMenu(app, district_var, *indian_districts)
district_option_menu.pack(pady=10)

get_weather_button = ttk.Button(app, text="Get Weather", command=get_weather_data)
get_weather_button.pack()

# Create a treeview for the weather data
columns = ["Parameter", "Value"]
weather_tree = ttk.Treeview(app, columns=columns, show="headings")
weather_tree.heading("Parameter", text="Parameter")
weather_tree.heading("Value", text="Value")
weather_tree.pack()

weather_info_label = tk.Label(app, text="", font=("Arial", 12))
weather_info_label.pack(pady=10)

# Start the main event loop
app.mainloop()
