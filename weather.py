import requests
import openai  # optional (for AI description)

# --- CONFIG ---
API_KEY = "YOUR_OPENWEATHER_API_KEY"  # replace this
CITY = input("Enter city name: ")

# Optional: Set your OpenAI API key if using AI description
openai.api_key = "YOUR_OPENAI_API_KEY"  # optional

# --- WEATHER DETECTION FUNCTION ---
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != 200:
        print("City not found ❌")
        return None

    weather = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"].capitalize(),
    }
    return weather


# --- AI DESCRIPTION (Optional) ---
def ai_describe_weather(weather):
    prompt = (
        f"The temperature in {weather['city']} is {weather['temperature']}°C "
        f"with {weather['condition']} and humidity of {weather['humidity']}%. "
        "Give a short friendly description like a weather report."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4-turbo"
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"].strip()


# --- MAIN EXECUTION ---
weather = get_weather(CITY)
if weather:
    print("\n🌤️  WEATHER DATA")
    print(f"City: {weather['city']}")
    print(f"Temperature: {weather['temperature']}°C")
    print(f"Condition: {weather['condition']}")
    print(f"Humidity: {weather['humidity']}%\n")

    # Optional AI summary
    if openai.api_key != "YOUR_OPENAI_API_KEY":
        summary = ai_describe_weather(weather)
        print("🧠 AI Summary:", summary)
