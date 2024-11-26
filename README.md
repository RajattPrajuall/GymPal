# GymPal Bot

GymPal Bot is a fitness-focused Telegram bot designed to help users calculate their Body Mass Index (BMI), classify it, and suggest a structured workout plan based on their preferences. This interactive bot provides personalized recommendations and useful links to exercises for different workout days, making it a helpful companion for fitness enthusiasts.

---

## Features
### 🎯 **BMI Calculation**
- Collects user details: weight, height, and gender.
- Calculates BMI and provides a classification:
  - Underweight: BMI < 18.5
  - Normal weight: 18.5 ≤ BMI < 24.9
  - Overweight: 25 ≤ BMI < 29.9
  - Obese: BMI ≥ 30

### 🏋️‍♂️ **Workout Day Selector**
- Users can select their preferred workout day:
  - **Push Day**: Chest, shoulders, triceps.
  - **Pull Day**: Back, biceps, forearms.
  - **Leg Day**: Leg-specific exercises.

### 📖 **Exercise Recommendations**
- Provides a curated list of exercises tailored to the selected workout day.
- Includes clickable links to detailed instructions for each exercise.

### 🛠️ **Data Persistence**
- Saves user data (weight, height, gender, workout preferences) to a JSON file for future sessions.

---

## How It Works
1. **Start the Bot**: Use the `/start` command to initiate the bot.
2. **Enter Weight**: Provide your weight in kilograms.
3. **Enter Height**: Provide your height in centimeters.
4. **Select Gender**: Choose your gender using an interactive button.
5. **View BMI**: The bot calculates and displays your BMI along with classification.
6. **Select Workout Day**: Choose between Push, Pull, or Legs day.
7. **Get Exercises**: Receive a detailed list of exercises with clickable links for instructions.

---

## Technologies Used
- **Programming Language**: Python
- **Libraries**:
  - `pyTelegramBotAPI`: For Telegram bot functionality.
  - `python-dotenv`: To manage environment variables securely.
  - `json`: For storing user data persistently.

---

## Setup Instructions
1. Install the required dependencies:
   ```bash
   pip install pyTelegramBotAPI python-dotenv
   ```
2. Create a `.env` file with your bot token:
   ```
   BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
   ```
3. Run the script:
   ```bash
   python bot.py
   ```
4. Interact with the bot on Telegram!

---

## Future Enhancements
- Add diet recommendations based on BMI.
- Support for multi-language interactions.
- Integration with fitness tracking APIs for progress monitoring.

---

**Get fit and stay motivated with GymPal Bot!** 💪
