from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
import geocoder


root=Tk()
root.title("Weather")
root.geometry("900x500+300+200")
root.resizable(0,0)


def getWeather():
    try:
        city = textfield.get()
        if not city:
            messagebox.showerror("Weather App", "Please enter a city.")
            return

        # Use timezonefinder to get timezone from coordinates
        tf = TimezoneFinder()
        g = geocoder.arcgis(city)

        if not g.ok or not g.latlng:
            messagebox.showerror("Weather App", "Could not find location. Invalid city name.")
            return

        lat, lon = g.latlng
        result = tf.timezone_at(lng=lon, lat=lat)

        if not result:
            messagebox.showerror("Weather App", "Could not find a valid timezone for the city.")
            return

        # Time
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text=f"Current Weather in {city.title()}")  # Added city name for clarity

        # Weather API
        api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=db0723e8411d5428346e29aecde840bc&units=metric"

        json_data = requests.get(api).json()
        if json_data.get('cod') != 200:
            messagebox.showerror("Weather App", "Error fetching weather data.")
            return

        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = json_data['main']['temp']
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        # Update labels
        t.config(text=f"{int(temp)}°C")
        c.config(text=f"{condition} | FEELS LIKE {int(json_data['main']['feels_like'])}°C")
        w.config(text=f"{wind} m/s")
        h.config(text=f"{humidity}%")
        d.config(text=description)
        p.config(text=f"{pressure} hPa")

    except Exception as e:
        messagebox.showerror("Weather App", f"An error occurred: {e}")


search_image = tk.PhotoImage(file="Copy of search.png")
myimage = tk.Label(root, image=search_image)
myimage.place(x=20,y=20)

textfield=tk.Entry(root, justify="center", width=17,font=("poppins",25,"bold"),bg="#404040",border=0,fg="white")
textfield.place(x=50,y=40)
textfield.focus()

Search_icon= tk.PhotoImage(file="Copy of search_icon.png")
myimage_icon = Button(image=Search_icon,borderwidth=0,cursor="hand2",bg="#404040",command=getWeather)
myimage_icon.place(x=400,y=34)

#logo
Logo_image = tk.PhotoImage(file="Copy of logo.png")
logo= tk.Label(image=Logo_image)
logo.place(x=150,y=100)

#bottom box
Frame_image= tk.PhotoImage(file="Copy of box.png")
frame_myimage= tk.Label(image=Frame_image)
frame_myimage.pack(side="bottom",padx=5,pady=5)

#time
name=Label(root,font=("arial",20,"bold"))
name.place(x=30,y=100)
clock=Label(root,font=("Helvetica",20))
clock.place(x=30,y=130)

#label
label1=Label(root, text="WIND", font=("Helvetica",20,"bold"),fg="white",bg="#1ab5ef")
label1.place(x=120,y=400)

label2=Label(root, text="HUMIDITY", font=("Helvetica",20,"bold"),fg="white",bg="#1ab5ef")
label2.place(x=250,y=400)

label1=Label(root, text="DESCRIPTION", font=("Helvetica",20,"bold"),fg="white",bg="#1ab5ef")
label1.place(x=430,y=400)

label1=Label(root, text="PRESSURE", font=("Helvetica",20,"bold"),fg="white",bg="#1ab5ef")
label1.place(x=650,y=400)

t=Label(font=("arial",70,"bold"),fg="#ee666d")
t.place(x=400,y=150)
c=Label(font=("arial",15,"bold"))
c.place(x=400,y=250)

w=Label(text="...",font=("arial",15,"bold"))
w.place(x=120,y=430)
h=Label(text="...",font=("arial",15,"bold"))
h.place(x=280,y=430)
d=Label(text="...",font=("arial",15,"bold"))
d.place(x=450,y=430)
p=Label(text="...",font=("arial",15,"bold"))
p.place(x=670,y=430)


root.mainloop()