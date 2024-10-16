import requests
import streamlit as st
import openai




def run():
# Function to get weather data from OpenWeatherMap API
    def get_current_weather(location, API_key):
        if "," in location:
            location = location.split(",")[0].strip()

        urlbase = "https://api.openweathermap.org/data/2.5/"
        urlweather = f"weather?q={location}&appid={API_key}"
        url = urlbase + urlweather

        response = requests.get(url)
        data = response.json()

        # Handle cases where location is invalid
        if response.status_code != 200:
            return f"Could not retrieve weather for {location}. Please check the location name."

        # Extract temperatures & Convert Kelvin to Celsius
        temp = data['main']['temp'] - 273.15
        feels_like = data['main']['feels_like'] - 273.15
        temp_min = data['main']['temp_min'] - 273.15
        temp_max = data['main']['temp_max'] - 273.15
        humidity = data['main']['humidity']
        weather_desc = data['weather'][0]['description']

        return {
            "location": location,
            "temperature": round(temp, 2),
            "feels_like": round(feels_like, 2),
            "temp_min": round(temp_min, 2),
            "temp_max": round(temp_max, 2),
            "humidity": round(humidity, 2),
            "description": weather_desc.capitalize()
        }

    # Function to generate a suggestion using OpenAI's ChatCompletion
    def generate_suggestion(weather_info, openai_api_key):
        openai.api_key = openai_api_key

        prompt = (
            f"The current weather in {weather_info['location']} is as follows: "
            f"Temperature: {weather_info['temperature']}°C, "
            f"Feels like: {weather_info['feels_like']}°C, "
            f"Min Temp: {weather_info['temp_min']}°C, Max Temp: {weather_info['temp_max']}°C, "
            f"Humidity: {weather_info['humidity']}%, "
            f"Description: {weather_info['description']}. "
            f"Based on this weather, suggest an appropriate activity or recommendation for the day."
        )

        # Use ChatCompletion instead of Completion for chat-based models
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return response['choices'][0]['message']['content'].strip()

    # Streamlit app
    if __name__ == "__main__":
        # Title of the app
        st.title("Where What to Wear Weather?")
        
        # Get the API keys from Streamlit secrets
        weather_api_key = st.secrets["WEATHER_API_KEY"]
        openai_api_key = st.secrets["OPEN_API_KEY"]
        
        # Input from the user for the location
        location = st.text_input("Enter the location:", "Syracuse, NY")
        
        if location:
            # Get the weather information
            weather_info = get_current_weather(location, weather_api_key)

            # Check if the response is a dictionary (valid data) or an error message
            if isinstance(weather_info, dict):
                st.write(f"**Weather in {weather_info['location']}:**")
                st.write(f"Temperature: {weather_info['temperature']}°C")
                st.write(f"Feels like: {weather_info['feels_like']}°C")
                st.write(f"Min Temp: {weather_info['temp_min']}°C, Max Temp: {weather_info['temp_max']}°C")
                st.write(f"Humidity: {weather_info['humidity']}%")
                st.write(f"Description: {weather_info['description']}")
                
                # Get the suggestion from OpenAI using the chat model
                suggestion = generate_suggestion(weather_info, openai_api_key)
                st.write("**Suggestion based on the current weather:**")
                st.write(suggestion)
            else:
                st.error(weather_info)  # Show the error message if the location is invalid
