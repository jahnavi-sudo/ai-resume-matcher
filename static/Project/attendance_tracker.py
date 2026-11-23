import json
import os

DATA_FILE = "subjects.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def calculate_status(attended, total, target=75.0):
    if total == 0:
        return 0.0, "No classes held yet."
    percentage = (attended / total) * 100
    if percentage >= target:
        # Calculate how many classes can be safely missed
        bunkable = int((attended * 100 / target) - total)
        return percentage, f"Safe! You can miss {bunkable} next class(es)."
    else:
        # Calculate consecutive classes needed to reach target
        needed = 0
        temp_att, temp_tot = attended, total
        while (temp_att / temp_tot) * 100 < target:
            temp_att += 1
            temp_tot += 1
            needed += 1
        return percentage, f"Warning! Attend the next {needed} class(es) straight."

def main():
    subjects = load_data()
    while True:
        print("\n--- B.Tech Attendance & Target Tracker ---")
        print("1. Add / Update Subject")
        print("2. View Attendance Report")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            name = input("Enter Subject Name (e.g., Engineering Maths): ").strip()
            try:
                attended = int(input("Classes Attended: "))
                total = int(input("Total Classes Held: "))
                if attended > total or attended < 0 or total < 0:
                    print("Invalid numbers! Attended cannot exceed total classes.")
                    continue
                subjects[name] = {"attended": attended, "total": total}
                save_data(subjects)
                print(f"Saved {name}!")
            except ValueError:
                print("Please enter valid whole numbers.")

        elif choice == "2":
            if not subjects:
                print("No subjects added yet.")
                continue
            print("\n--- Attendance Summary (Target: 75%) ---")
            for name, info in subjects.items():
                pct, advice = calculate_status(info["attended"], info["total"])
                print(f"{name}: {info['attended']}/{info['total']} ({pct:.2f}%) -> {advice}")

        elif choice == "3":
            print("Goodbye! Keep coding.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
