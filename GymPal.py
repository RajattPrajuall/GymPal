pip install pyTelegramBotAPI
# Create a .env file in Colab
with open('.env', 'w') as f:
    f.write('BOT_TOKEN=')

!pip install python-dotenv # install python-dotenv which contains the required load_dotenv function
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv('.env')

# Access the variable
bot_token = os.getenv('BOT_TOKEN')
print(f'Bot token: {bot_token}')

import os
import telebot
from telebot import types
import json

# Initialize the bot
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# A dictionary to store user data
user_data = {}

# States for user input
STATE_WEIGHT = 1
STATE_HEIGHT = 2
STATE_GENDER = 3

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    """Welcome the user and ask for weight."""
    chat_id = message.chat.id
    user_data[chat_id] = {}  # Initialize user data
    bot.send_message(chat_id, "Welcome to *GymPal*! Let's record your details.\n\nPlease enter your *weight* in kilograms (e.g., 70):", parse_mode="Markdown")

# Handle weight input
@bot.message_handler(func=lambda message: message.chat.id in user_data and "weight" not in user_data[message.chat.id])
def handle_weight(message):
    """Save the user's weight and ask for height."""
    chat_id = message.chat.id
    try:
        weight = float(message.text)
        user_data[chat_id]["weight"] = weight
        bot.send_message(chat_id, "Great! Now enter your *height* in centimeters (e.g., 170):", parse_mode="Markdown")
    except ValueError:
        bot.send_message(chat_id, "Please enter a valid number for your weight.")

# Handle height input
@bot.message_handler(func=lambda message: message.chat.id in user_data and "height" not in user_data[message.chat.id])
def handle_height(message):
    """Save the user's height and ask for gender."""
    chat_id = message.chat.id
    try:
        height = float(message.text)
        user_data[chat_id]["height"] = height

        # Provide gender options using InlineKeyboardMarkup
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Male", callback_data="Male"))
        markup.add(types.InlineKeyboardButton("Female", callback_data="Female"))
        markup.add(types.InlineKeyboardButton("Other", callback_data="Other"))
        bot.send_message(chat_id, "Finally, select your *gender*:", reply_markup=markup, parse_mode="Markdown")
    except ValueError:
        bot.send_message(chat_id, "Please enter a valid number for your height.")

# Handle gender input (button click)
# Handle gender input (button click) - after BMI is calculated
@bot.callback_query_handler(func=lambda call: call.data in ["Male", "Female", "Other"])
def handle_gender(call):
    """Save the user's gender, calculate BMI, and display results."""
    chat_id = call.message.chat.id
    gender = call.data
    user_data[chat_id]["gender"] = gender

    # Calculate BMI
    weight = user_data[chat_id]["weight"]
    height_cm = user_data[chat_id]["height"]
    height_m = height_cm / 100  # Convert height to meters
    bmi = weight / (height_m ** 2)
    bmi = round(bmi, 2)  # Round to two decimal places

    # Classify BMI
    if bmi < 18.5:
        classification = "underweight"
    elif 18.5 <= bmi < 24.9:
        classification = "normal weight"
    elif 25 <= bmi < 29.9:
        classification = "overweight"
    else:
        classification = "obese"

    # Save data to the file
    save_user_data()

    # Show the collected data and BMI
    bot.send_message(
        chat_id,
        f"Thanks for sharing your details:\n\n"
        f"Weight: {weight} kg\n"
        f"Height: {height_cm} cm\n"
        f"Gender: {gender}\n\n"
        f"Your BMI is: *{bmi}* ({classification})\n\n"
        f"Reference:\n"
        f" - Underweight: BMI < 18.5\n"
        f" - Normal weight: 18.5 ≤ BMI < 24.9\n"
        f" - Overweight: 25 ≤ BMI < 29.9\n"
        f" - Obese: BMI ≥ 30\n",
        parse_mode="Markdown"
    )

    # Immediately ask for the workout day after BMI message
    bot.send_message(
        chat_id,
        "What type of workout do you want to do today?\nChoose your workout day:"
    )

    # Create an InlineKeyboardMarkup for workout day selection in rows
    markup = types.InlineKeyboardMarkup(row_width=1)  # Set row width to 1 for each button in a row
    markup.add(
        types.InlineKeyboardButton("Push Day (Chest, Shoulders, Triceps)", callback_data="Push"),
    )
    markup.add(
        types.InlineKeyboardButton("Pull Day (Back, Biceps, Forearms)", callback_data="Pull"),
    )
    markup.add(
        types.InlineKeyboardButton("Legs", callback_data="Legs"),
    )

    # Send the dropdown menu for workout day
    bot.send_message(
        chat_id,
        "Please select a workout day:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data in ["Push", "Pull", "Legs"])
def handle_workout_day_choice(call):
    """Save the selected workout day and display exercises."""
    chat_id = call.message.chat.id
    workout_day = call.data  # Store the workout day selection

    # List exercises for the selected workout day
    if workout_day == "Push":
        exercises = {
            "Chest": [
                "[Push-up](https://www.muscleandstrength.com/exercises/push-up.html)",
                "[Bench Press](https://www.muscleandstrength.com/exercises/barbell-bench-press.html)",
                "[Dumbbell Flys](https://www.muscleandstrength.com/exercises/dumbbell-flys.html)",
                "[Incline Dumbbell Press](https://www.muscleandstrength.com/exercises/incline-dumbbell-bench-press.html)",
                "[Chest Dips](https://www.muscleandstrength.com/exercises/chest-dip.html)"
            ],
            "Shoulders": [
                "[Cable Face Pull](https://www.muscleandstrength.com/exercises/cable-face-pull)",
                "[Lateral Raise](https://www.muscleandstrength.com/exercises/dumbbell-lateral-raise.html)",
                "[Front Raise](https://www.muscleandstrength.com/exercises/dumbbell-front-raise.html)",
                "[Seated Arnold Press](https://www.muscleandstrength.com/exercises/seated-arnold-press.html)",
            ],
            "Triceps": [
                "[Tricep Dips](https://www.muscleandstrength.com/exercises/tricep-dip.html)",
                "[Rope Tricep Pushdowns](https://www.muscleandstrength.com/exercises/rope-tricep-extension.html)",
                "[Skull Crushers](https://www.muscleandstrength.com/exercises/ez-bar-skullcrusher.html)",
                "[Overhead Tricep Extension](https://www.muscleandstrength.com/exercises/two-arm-dumbbell-extension.html)"
            ]
        }
    elif workout_day == "Pull":
        exercises = {
            "Back": [
                "[Pull-up](https://www.muscleandstrength.com/exercises/wide-grip-pull-up.html)",
                "[Lat Pulldown](https://www.muscleandstrength.com/exercises/lat-pull-down.html)",
                "[Deadlift](https://www.muscleandstrength.com/exercises/deadlifts.html)",
                "[Seated Cable Row](https://www.muscleandstrength.com/exercises/seated-row.html)",
                "[T-Bar Row](https://www.muscleandstrength.com/exercises/bent-over-row.html)"
            ],
            "Biceps": [
                "[Bicep Curl](https://www.muscleandstrength.com/exercises/ez-bar-curl.html)",
                "[Hammer Curl](https://www.muscleandstrength.com/exercises/weight-plate-pinches.html)",
                "[Concentration Curl](https://www.muscleandstrength.com/exercises/concentration-cur.html)",
                "[Barbell Curl](https://www.muscleandstrength.com/exercises/standing-barbell-curl.html)",
            ],
            "Forearms": [
                "[Wrist Curls](https://www.muscleandstrength.com/exercises/one-arm-seated-dumbbell-wrist-curl.html)",
                "[Reverse Wrist Curls](https://www.muscleandstrength.com/exercises/reverse-dumbbell-wrist-curl-over-bench.html)",
                "[Farmer's Walk](https://www.muscleandstrength.com/exercises/farmers-walk)",
                "[Hammer Curl](https://www.muscleandstrength.com/exercises/hammer-curl)"
            ]
        }
    else:  # For Legs
        exercises = {
            "Legs": [
                "[Dumbbell Goblet Squat](https://www.muscleandstrength.com/exercises/dumbbell-goblet-squat)",
                "[Lunges](https://www.muscleandstrength.com/exercises/dumbbell-lunge.html)",
                "[Leg Press](https://www.muscleandstrength.com/exercises/45-degree-leg-press.html)",
                "[Deadlifts](https://www.muscleandstrength.com/exercises/stiff-leg-deadlift-aka-romanian-deadlift.html)",
                "[Leg Extensions](https://www.muscleandstrength.com/exercises/leg-extension.html)",
                "[Leg Curl](https://www.muscleandstrength.com/exercises/leg-curl.html)",
                "[Hip Adduction Machine](https://www.muscleandstrength.com/exercises/hip-adduction-machine.html)",
                "[Hip Abduction Machine](https://www.muscleandstrength.com/exercises/hip-abduction-machine.html)"
            ]
        }

    # Format the exercises list for the response
    exercises_list = []
    for muscle_group, exercises_items in exercises.items():
        exercises_list.append(f"{muscle_group}: \n" + "\n".join(exercises_items))

    # Send the exercises for the selected workout day with clickable links
    bot.send_message(
        chat_id,
        f"Here are the exercises for {workout_day}:\n\n" + "\n\n".join(exercises_list),
        parse_mode="Markdown",  # Ensure Markdown is enabled for hyperlink formatting
        disable_web_page_preview=True  # Disable the preview of the link
    )

    # Save the workout day to the user data
    user_data[chat_id]["workout_day"] = workout_day
    save_user_data()



# Save data to a file
def save_user_data():
    with open("GymPal.json", "w") as f:
        json.dump(user_data, f)

# Load data from a file
def load_user_data():
    """Load user data from a JSON file."""
    global user_data
    try:
        with open("GymPal.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = {}
        with open("GymPal.json", "w") as f:
            json.dump(user_data, f)

# Load existing data at the start of the bot
load_user_data()

# Run the bot
print("Bot is running...")
bot.infinity_polling()
