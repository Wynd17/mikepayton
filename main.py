import pandas as pd
import numpy as np

# ---------------------- DATA HANDLING ----------------------
def load_data(filename):
    """Load student data from CSV file"""
    try:
        df = pd.read_csv(filename)
        print("✅ Data loaded successfully!")
        return df
    except FileNotFoundError:
        print("⚠️ File not found. Creating a new one...")
        cols = ["name", "quiz1", "quiz2", "quiz3", "quiz4", "quiz5", "project", "exam"]
        return pd.DataFrame(columns=cols)

def save_data(df, filename="grades.csv"):
    """Save student data to CSV file"""
    df.to_csv(filename, index=False)
    print(f"💾 Data saved to {filename}")

# ---------------------- CRUD OPERATIONS ----------------------
def insert_student(df):
    """Add a new student record"""
    name = input("Enter student name: ")
    quizzes = [float(input(f"Enter Quiz {i+1} score: ")) for i in range(5)]
    project = float(input("Enter Project score: "))
    exam = float(input("Enter Exam score: "))

    data = {"name": name, "quiz1": quizzes[0], "quiz2": quizzes[1], "quiz3": quizzes[2],
            "quiz4": quizzes[3], "quiz5": quizzes[4], "project": project, "exam": exam}
    
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    print("✅ Student added successfully!")
    return df

def delete_student(df):
    """Delete a student record by name"""
    name = input("Enter student name to delete: ")
    if name in df["name"].values:
        df = df[df["name"] != name]
        print(f"🗑️ {name} removed successfully!")
    else:
        print("⚠️ Student not found.")
    return df

def sort_data(df):
    """Sort data by chosen column"""
    print("\nSort by: name | weighted | percentile | improvement")
    column = input("Enter column to sort by: ").lower()
    if column in df.columns:
        df = df.sort_values(by=column, ascending=False).reset_index(drop=True)
        print(f"✅ Sorted by {column}")
    else:
        print("⚠️ Invalid column.")
    return df

# ---------------------- CALCULATIONS ----------------------
def compute_weighted(df):
    """Compute weighted average grade"""
    try:
        weights = {
            "quiz1": 0.1, "quiz2": 0.1, "quiz3": 0.1, "quiz4": 0.1, "quiz5": 0.1,
            "project": 0.3, "exam": 0.2
        }

        for col in weights.keys():
            if col not in df.columns:
                raise KeyError(f"Missing column: {col}")

        df["weighted"] = sum(df[col] * weights[col] for col in weights)
        print("✅ Weighted grades computed!")
    except Exception as e:
        print(f"⚠️ Error: {e}")
    return df

def compute_statistics(df):
    """Compute percentile, outliers, and improvement"""
    if "weighted" not in df.columns:
        print("⚠️ Compute weighted grades first.")
        return df

    df["percentile"] = df["weighted"].rank(pct=True) * 100

    mean = df["weighted"].mean()
    std = df["weighted"].std(ddof=0)

    df["outlier"] = np.abs(df["weighted"] - mean) > (2 * std)
    df["improvement"] = (df["weighted"] - mean).round(2)

    print("📊 Statistics computed: percentile, outlier, improvement.")
    return df

# ---------------------- MAIN MENU ----------------------
def main():
    filename = "grades.csv"
    df = load_data(filename)

    while True:
        print("\n------ GRADE ANALYZER MENU ------")
        print("1. View Data")
        print("2. Insert Student")
        print("3. Delete Student")
        print("4. Sort Data")
        print("5. Compute Weighted Grades")
        print("6. Compute Statistics (percentile, outlier, improvement)")
        print("7. Save & Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print(df if not df.empty else "⚠️ No data available.")
        elif choice == "2":
            df = insert_student(df)
        elif choice == "3":
            df = delete_student(df)
        elif choice == "4":
            df = sort_data(df)
        elif choice == "5":
            df = compute_weighted(df)
        elif choice == "6":
            df = compute_statistics(df)
        elif choice == "7":
            save_data(df)
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
