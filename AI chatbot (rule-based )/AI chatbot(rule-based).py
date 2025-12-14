import requests
import random
import html

API_KEY = "fea69228f4be91cd084d34a14a7e112e"


def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code != 200:
            return "I couldn't find weather info for that city."

        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        return f"The weather in {city.title()} is {desc}. Temperature: {temp}°C, Humidity: {humidity}%."

    except Exception:
        return "Something went wrong while fetching the weather."


def get_quiz_question():
    try:
        url = "https://opentdb.com/api.php?amount=10&type=multiple"
        response = requests.get(url)
        data = response.json()

        if data["response_code"] != 0:
            return None

        q = random.choice(data["results"])

        question = html.unescape(q["question"])
        correct = html.unescape(q["correct_answer"])

        options = [html.unescape(opt) for opt in q["incorrect_answers"]]
        options.append(correct)
        random.shuffle(options)

        return question, correct, options

    except Exception:
        return None


def show_menu():
    print("\nKimu: Here’s what I can help you with 👇🏼")
    print("""
• Say 'hello' or 'hi'          → Greeting
• Ask about 'weather'          → Get live weather of any city
• Say 'add' or '+'             → Add two numbers
• Say 'multiply' or '*'        → Multiply two numbers
• Say 'quiz' or 'question'     → Play a quiz question
• Talk about food              → Indian, Italian, or Chinese dishes
• Type 'help' or 'menu'        → Show this list again
• Type 'bye', 'exit', 'quit'   → End the chat
""")


print("Hello, I'm Kimu, your simple rule-based chatbot.")
show_menu()

while True:
    user = input("\nYou: ").lower()

    # exit condition
    if user in ["bye", "exit", "quit"]:
        print("Kimu: Goodbye! Have a great day")
        break

    # help / menu
    elif user in ["help", "menu"]:
        show_menu()

    # weather
    elif "weather" in user:
        city = input("Kimu: Tell me the city name: ")
        print("Kimu:", get_weather(city))

    # quiz
    elif "quiz" in user or "question" in user:
        quiz = get_quiz_question()

        if quiz is None:
            print("Kimu: Couldn't fetch a quiz right now.")
        else:
            question, correct, options = quiz
            print("Kimu: Let's play!")
            print(question)

            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            ans = input("Your answer (number): ")

            if ans.isdigit() and 1 <= int(ans) <= len(options):
                if options[int(ans) - 1] == correct:
                    print("Kimu: Correct! Nicely done 😎")
                else:
                    print(f"Kimu: Wrong. The correct answer was: {correct}")
            else:
                print("Kimu: Please enter a valid number.")

    # math
    elif "add" in user or "+" in user:
        a = float(input("Number 1: "))
        b = float(input("Number 2: "))
        print("Kimu:", a + b)

    elif "multiply" in user or "*" in user:
        a = float(input("Number 1: "))
        b = float(input("Number 2: "))
        print("Kimu:", a * b)

    # greetings
    elif "hello" in user or "hi" in user:
        print("Kimu: Hello there! How can I help you today?")

    # food detection
    elif any(food in user for food in ["samosa", "jalebi", "naan", "daal", "puri"]):
        print("Kimu: Ah, Indian food! You're making me hungry.")

    elif any(food in user for food in ["pasta", "pizza", "risotto", "macaroni"]):
        print("Kimu: Italian dishes are always kids' favorites.")

    elif any(food in user for food in ["dumplings", "fried rice", "pot stickers", "egg role"]):
        print("Kimu: Chinese huh? You seem to love spicy food.")

    else:
        print("Kimu: I’m not sure about that yet. Type 'help' to see what I can do.")
