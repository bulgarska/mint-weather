import requests
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime


def epoch_to_date_time(epoch):
    date_time = datetime.datetime.fromtimestamp(epoch)
    return date_time.strftime("%H:%M")


def get_weather_data():
    city_name = city_entry.get()
    # Use your openweathermap api key here
    api_key = 'Insert_API_key'
    open_weather_map_base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = f'{open_weather_map_base_url}q={city_name}&appid={api_key}&units=metric'

    response = requests.get(complete_url)
    return response.json()


def display_weather_data():
    weather_data = get_weather_data()

    # Show loading state
    weather_label.config(text="Loading...")
    icon_label.config(image='')

    if weather_data['cod'] == 200:
        main_data = weather_data['main']
        temperature = main_data['temp']
        sunrise_time = weather_data['sys']['sunrise']
        sunset_time = weather_data['sys']['sunset']
        weather_description = weather_data['weather'][0]['description']
        temperature_feels_like = main_data['feels_like']
        humidity = main_data['humidity']
        temp_min = main_data['temp_min']
        temp_max = main_data['temp_max']
        wind_speed = weather_data['wind']['speed']
        visibility = weather_data['visibility']

        weather_label.config(text=f'Temperature: {temperature:.0f}°C '
                                  f'\nSunrise: {epoch_to_date_time(sunrise_time)} '
                                  f'\nSunset: {epoch_to_date_time(sunset_time)} '
                                  f'\nDescription: {weather_description} '
                                  f'\nFeels Like: {temperature_feels_like:.0f}°C '
                                  f'\nHumidity: {humidity}% '
                                  f'\nMin Temperature: {temp_min:.0f}°C '
                                  f'\nMax Temperature: {temp_max:.0f}°C \nWind Speed: {wind_speed} m/s '
                                  f'\nVisibility: {(visibility/1000):.0f} km ')
    else:
        messagebox.showerror("Error", weather_data["message"])

    # Update icon
    icon_name = weather_data['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{icon_name}@2x.png"
    icon_data = requests.get(icon_url)
    with open("icon.png", "wb") as f:
        f.write(icon_data.content)
    icon_image = ImageTk.PhotoImage(Image.open("icon.png"))
    icon_label.config(image=icon_image)
    icon_label.image = icon_image


root = tk.Tk()
root.geometry('800x600')
root.title('Mint Weather')
root.config(bg='#ffc0cb')

# City entry frame
city_entry_frame = tk.Frame(root, bg='#cbffc0', bd=5)
city_entry_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

# City entry text box
city_entry = tk.Entry(city_entry_frame, bg='#ffc0cb', font=("Courier", 14))
city_entry.place(relwidth=0.65, relheight=1)
city_entry.insert(0, "Los Angeles")

# Get weather button
get_weather_button = tk.Button(city_entry_frame, bg='#ffc0cb', text="Get Weather", font=("Courier", 12),
                               command=display_weather_data)
get_weather_button.place(relx=0.7, relwidth=0.3, relheight=1)

# Weather label frame
weather_frame = tk.Frame(root, bg='#cbffc0', bd=10)
weather_frame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.5, anchor='n')
weather_label = tk.Label(weather_frame, bg='#ffc0cb', font=("Courier", 14), justify='left', bd=5, anchor='w')
weather_label.place(relwidth=1, relheight=1)

# Weather icon frame
icon_frame = tk.Frame(weather_frame, bg='#cbffc0')
icon_label = tk.Label(icon_frame, bg='#ffc0cb')
icon_label.place(relx=0.5, rely=0.5, anchor='center')
icon_frame.place(relx=0.8, rely=0.3, relwidth=0.2, relheight=0.4, anchor='n')

root.mainloop()