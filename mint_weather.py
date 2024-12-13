from io import BytesIO
import os
import requests
import customtkinter
from tkinter import messagebox
from PIL import Image
import datetime


# Currently displays the time for sunrise and sunset 
# of any location relative to your current timezone
def epoch_to_date_time(epoch):
    date_time = datetime.datetime.fromtimestamp(epoch)
    return date_time.strftime("%H:%M")


def get_weather_data():
    city_name = city_entry.get()
    # Use your openweathermap api key here
    api_key = os.environ.get('open_weather_map_api_key')
    open_weather_map_base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = f'{open_weather_map_base_url}q={city_name}&appid={api_key}&units=metric'

    response = requests.get(complete_url)
    return response.json()


def display_weather_data():
    weather_data = get_weather_data()

    # Show loading state
    weather_label.configure(text="Loading...")
    icon_label.configure(image='')

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

        weather_label.configure(text=f'Temperature: {temperature:.0f}°C '
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
    # with open("icon.png", "wb") as f:
    #     f.write(icon_data.content)
    icon_image = customtkinter.CTkImage(dark_image=Image.open(BytesIO(icon_data.content)), 
                                        size=(100, 100))
    icon_label.configure(image=icon_image)
    # icon_label.image = icon_image

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')

root = customtkinter.CTk()
root.geometry('1000x700')
root.title('Mint Weather')

# City entry frame
city_entry_frame = customtkinter.CTkFrame(master=root, )
city_entry_frame.pack(pady=20, padx=60, fill ='both', expand=True)

# City entry text box
city_entry = customtkinter.CTkEntry(master=city_entry_frame, placeholder_text='Los Angeles', 
                                    font=("Courier", 14))
city_entry.pack(pady=12, padx=10)

# Get weather button
get_weather_button = customtkinter.CTkButton(master=city_entry_frame, text="Get Weather", 
                               font=("Courier", 12), command=display_weather_data)
get_weather_button.pack(pady=12, padx=10)

# Weather label frame
weather_frame = customtkinter.CTkFrame(master=root, )
weather_frame.pack(pady=20, padx=60, fill ='both', expand=True)
weather_label = customtkinter.CTkLabel(master=weather_frame, 
                                       text='', 
                                       font=("Courier", 14))
weather_label.pack(pady=12, padx=10)

# Weather icon frame
icon_frame = customtkinter.CTkFrame(master=weather_frame)
icon_label = customtkinter.CTkLabel(master=icon_frame, image='', text='')
icon_label.pack(pady=12, padx=10)
icon_frame.pack(pady=20, padx=60, expand=True)

root.mainloop()