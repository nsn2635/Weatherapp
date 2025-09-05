import tkinter as tk
import requests

# Replace with your OpenWeatherMap API key
API_KEY = "bd9f282577cab296177bfc5eea8a2970"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"


def get_weather():
    city = city_entry.get()
    if not city:
        result_label.config(text="Please enter a city name")
        return

    url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != "404":
            main = data["main"]
            temp = main["temp"]
            feels_like = main["feels_like"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            weather_desc = data["weather"][0]["description"].capitalize()

            result = (
                f"City: {city.capitalize()}\n"
                f"Temperature: {temp}°C\n"
                f"Feels Like: {feels_like}°C\n"
                f"Pressure: {pressure} hPa\n"
                f"Humidity: {humidity}%\n"
                f"Condition: {weather_desc}"
            )
        else:
            result = "City not found!"
    except Exception as e:
        result = f"Error: {e}"

    result_label.config(text=result)


# Tkinter window setup
root = tk.Tk()
root.title("Weather App")
root.geometry("300x250")

city_entry = tk.Entry(root, width=20, font=("Arial", 14))
city_entry.pack(pady=10)

search_btn = tk.Button(root, text="Get Weather", command=get_weather)
search_btn.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=10)

root.mainloop()