import datetime as dt

'''
NAME = AYUSH KUMAR JHA
DATE = 06/10/2025
PROJECTS = CALORIE TRACKER CONSOLE APLLICATION
'''

print("----------------------------- Calorie Tracker -----------------------------")


# STORE MEAL AND CALORIE ENTER BY THE USER
Meals = []
Calories = []

# USER ASKED HOW MANY MEAL TO ENTER
user_meal = int(input("How many meal you want to enter: "))

meal_loop = 0

# USING WHILE LOOP TO ENTER FOOD AND CALORIE AMOUNT
while meal_loop < user_meal:
    mealName = input("Enter your Meal Name: ")
    calorieName = int(input("Enter Your Calorie Amount: "))
    Meals.append(mealName)
    Calories.append(calorieName)
    meal_loop +=1


# CALCULATE TOTAL CALORIES AND AVERAGE AVERAGE OF CALORIES
total_calorie = 0
for t_calo in Calories:
    total_calorie += t_calo
avg_calorie = (total_calorie/len(Calories))

# USER ASK DAILY CALORIES LIMIT
user_daily_limit = float(input("Enter Your daily calorie limit: "))

# CHECK TOTAL DAILY CALORIE LIMIT
Daily_calories_limit = total_calorie - user_daily_limit

# CHECK WHEN CALORIE LIMIT IS EXCEED 
if total_calorie > user_daily_limit:
    print(f"Your calorie limit is exceed {Daily_calories_limit}")
else:
    print(f"Good Work You are Healthy and your calories is {-Daily_calories_limit}")



print(f"{'Meal Name':<15}\t{'Calories':<10}")
print("-" * 30)
for i in range(len(Meals)):
    print(f"{Meals[i]:<15}\t{Calories[i]:<10.2f}")
print(f"{'Total:':<15}\t{total_calorie:<10.2f}")
print(f"{'Average:':<15}\t{avg_calorie:<10.2f}")


# FILE SAVING 
timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
user_file_save = input("You want save a file: ").lower()
if user_file_save == "y":
    with open("calroies.txt","w")as ca:
        ca.write(f"Timestamp {timestamp}")
        for i in range(len(Meals)):
            ca.write(f"\n{Meals[i]:<15}{Calories[i]:<10.2f}")
        ca.write(f"Average Calories Meal: {avg_calorie:.2f}\n")
        ca.write(f"Calorie Daily Limited: {user_daily_limit}\n")
        ca.write(f"Total Calories{total_calorie}")