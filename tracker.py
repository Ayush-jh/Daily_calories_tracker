import datetime as dt
import json
import os
from typing import List, Dict

DATA_FILE = "calorie_data.json"

# ---------- Data Loading / Saving ----------
def load_data() -> Dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"daily_goal": 2000, "days": {}}

def save_data(data: Dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_today() -> str:
    return dt.date.today().isoformat()

def get_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def get_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")

def print_header(title: str):
    print("\n" + "=" * 50)
    print(f"{title:^50}")
    print("=" * 50)

# ---------- Core Functions ----------
def add_meal(data: Dict):
    today = get_today()
    if today not in data["days"]:
        data["days"][today] = []

    print("\nCategories: Breakfast | Lunch | Dinner | Snack | Other")
    category = input("Category: ").strip().title() or "Other"
    name = input("Meal name: ").strip()
    calories = get_float("Calories: ")

    meal = {
        "name": name,
        "calories": calories,
        "category": category,
        "time": dt.datetime.now().strftime("%H:%M")
    }
    data["days"][today].append(meal)
    save_data(data)
    print(f"✓ Added: {name} ({calories} kcal)")

def view_today(data: Dict):
    today = get_today()
    meals = data["days"].get(today, [])
    goal = data["daily_goal"]

    print_header(f"Today's Meals ({today})")

    if not meals:
        print("No meals recorded today.")
        return

    total = 0
    print(f"{'Time':<8} {'Category':<12} {'Meal':<25} {'Calories':>10}")
    print("-" * 60)
    for m in meals:
        print(f"{m['time']:<8} {m['category']:<12} {m['name']:<25} {m['calories']:>10.1f}")
        total += m["calories"]

    print("-" * 60)
    print(f"{'TOTAL':<46} {total:>10.1f}")
    remaining = goal - total
    status = "UNDER" if remaining >= 0 else "OVER"
    print(f"\nDaily Goal : {goal:.0f} kcal")
    print(f"Remaining  : {remaining:.1f} kcal  ({status})")

def set_goal(data: Dict):
    new_goal = get_float("Enter new daily calorie goal: ")
    data["daily_goal"] = new_goal
    save_data(data)
    print(f"✓ Daily goal updated to {new_goal:.0f} kcal")

def view_history(data: Dict):
    print_header("History (Last 7 Days)")
    days = sorted(data["days"].keys(), reverse=True)[:7]

    if not days:
        print("No history yet.")
        return

    print(f"{'Date':<12} {'Meals':>6} {'Total kcal':>12} {'vs Goal':>12}")
    print("-" * 45)
    for day in days:
        meals = data["days"][day]
        total = sum(m["calories"] for m in meals)
        diff = total - data["daily_goal"]
        sign = "+" if diff > 0 else ""
        print(f"{day:<12} {len(meals):>6} {total:>12.1f} {sign}{diff:>10.1f}")

def search_meals(data: Dict):
    keyword = input("Search meal name (partial match): ").strip().lower()
    found = []
    for day, meals in data["days"].items():
        for m in meals:
            if keyword in m["name"].lower():
                found.append((day, m))

    if not found:
        print("No matching meals found.")
        return

    print(f"\nFound {len(found)} matching meal(s):")
    print(f"{'Date':<12} {'Time':<8} {'Meal':<25} {'Calories':>10}")
    print("-" * 60)
    for day, m in found:
        print(f"{day:<12} {m['time']:<8} {m['name']:<25} {m['calories']:>10.1f}")

def delete_meal(data: Dict):
    today = get_today()
    meals = data["days"].get(today, [])
    if not meals:
        print("No meals today to delete.")
        return

    print("\nToday's meals:")
    for i, m in enumerate(meals, 1):
        print(f"{i}. {m['name']} ({m['calories']} kcal)")

    idx = get_int("Enter number to delete (0 to cancel): ")
    if 1 <= idx <= len(meals):
        removed = meals.pop(idx - 1)
        save_data(data)
        print(f"✓ Deleted: {removed['name']}")
    else:
        print("Cancelled.")

def export_report(data: Dict):
    today = get_today()
    meals = data["days"].get(today, [])
    total = sum(m["calories"] for m in meals)
    goal = data["daily_goal"]

    filename = f"calorie_report_{today}.txt"
    with open(filename, "w") as f:
        f.write("=" * 50 + "\n")
        f.write(f"CALORIE TRACKER REPORT - {today}\n")
        f.write(f"Generated: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"{'Time':<8} {'Category':<12} {'Meal':<25} {'Calories':>10}\n")
        f.write("-" * 60 + "\n")
        for m in meals:
            f.write(f"{m['time']:<8} {m['category']:<12} {m['name']:<25} {m['calories']:>10.1f}\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'TOTAL':<46} {total:>10.1f}\n")
        f.write(f"\nDaily Goal : {goal:.0f} kcal\n")
        f.write(f"Remaining  : {goal - total:.1f} kcal\n")

    print(f"✓ Report saved as {filename}")

def weekly_summary(data: Dict):
    print_header("Weekly Summary")
    days = sorted(data["days"].keys(), reverse=True)[:7]
    if not days:
        print("Not enough data.")
        return

    totals = []
    for day in days:
        total = sum(m["calories"] for m in data["days"][day])
        totals.append(total)
        print(f"{day}: {total:.0f} kcal")

    avg = sum(totals) / len(totals)
    print(f"\nAverage over last {len(days)} days: {avg:.1f} kcal")
    print(f"Daily Goal: {data['daily_goal']:.0f} kcal")

# ---------- Main Menu ----------
def main():
    data = load_data()

    while True:
        print_header("ADVANCED CALORIE TRACKER")
        print("1. Add Meal")
        print("2. View Today's Meals & Progress")
        print("3. Set Daily Calorie Goal")
        print("4. View History (Last 7 Days)")
        print("5. Search Meals")
        print("6. Delete Meal (Today)")
        print("7. Weekly Summary")
        print("8. Export Today's Report")
        print("9. Exit")
        print("-" * 50)

        choice = input("Choose option (1-9): ").strip()

        if choice == "1":
            add_meal(data)
        elif choice == "2":
            view_today(data)
        elif choice == "3":
            set_goal(data)
        elif choice == "4":
            view_history(data)
        elif choice == "5":
            search_meals(data)
        elif choice == "6":
            delete_meal(data)
        elif choice == "7":
            weekly_summary(data)
        elif choice == "8":
            export_report(data)
        elif choice == "9":
            print("\nStay healthy! Data saved. Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
