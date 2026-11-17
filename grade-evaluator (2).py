import csv
import sys
import os

PASS_MARK = 50
FORMATIVE = "Formative"
SUMMATIVE = "Summative"


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)

            # An empty file has no header row at all
            if reader.fieldnames is None:
                print(f"Error: '{filename}' is empty. Add the grades and try again.")
                sys.exit(1)

            header = [h.strip().lower() for h in reader.fieldnames]
            score_column = "score" if "score" in header else "grade"
            for needed in ("assignment", "group", score_column, "weight"):
                if needed not in header:
                    print(f"Error: column '{needed}' is missing. Header found: {header}")
                    sys.exit(1)

            for line_number, row in enumerate(reader, start=2):
                # Normalise the column names so spaces/capitals do not matter
                clean = {k.strip().lower(): (v or "").strip() for k, v in row.items() if k}
                try:
                    assignments.append({
                        "name": clean["assignment"],
                        "group": clean["group"].capitalize(),
                        "score": float(clean[score_column]),
                        "weight": float(clean["weight"]),
                    })
                except ValueError:
                    print(f"Error on line {line_number}: score and weight must be numbers (e.g. 85 or 12.5).")
                    sys.exit(1)
    except PermissionError:
        print(f"Error: no permission to read '{filename}'.")
        sys.exit(1)
    except csv.Error as e:
        print(f"Error: could not read '{filename}' as a CSV file ({e}).")
        sys.exit(1)

    if len(assignments) == 0:
        print(f"Error: '{filename}' has a header but no grade rows.")
        sys.exit(1)

    return assignments


def validate_grades(assignments):
    """Every score must be between 0 and 100."""
    errors = []
    for a in assignments:
        if a["score"] < 0 or a["score"] > 100:
            errors.append(f"Invalid score {a['score']:g} for '{a['name']}' (must be 0-100).")
    return errors


def total_weight(assignments, group=None):
    total = 0
    for a in assignments:
        if group is None or a["group"] == group:
            total += a["weight"]
    return total


def validate_weights(assignments):
    """Total = 100, Summative = 40, Formative = 60."""
    errors = []
    if total_weight(assignments) != 100:
        errors.append(f"Total weight is {total_weight(assignments):g}, it must be exactly 100.")
    if total_weight(assignments, SUMMATIVE) != 40:
        errors.append(f"Summative weight is {total_weight(assignments, SUMMATIVE):g}, it must be exactly 40.")
    if total_weight(assignments, FORMATIVE) != 60:
        errors.append(f"Formative weight is {total_weight(assignments, FORMATIVE):g}, it must be exactly 60.")
    return errors


def weighted_total(assignments, group=None):
    """Points earned out of the weight, e.g. score 80 on weight 10 gives 8."""
    earned = 0
    for a in assignments:
        if group is None or a["group"] == group:
            earned += a["score"] * a["weight"] / 100
    return earned


def category_percentage(assignments, group):
    """Score as a percentage of the category's own weight."""
    weight = total_weight(assignments, group)
    if weight == 0:
        return 0
    return weighted_total(assignments, group) / weight * 100


def calculate_gpa(total_grade):
    return (total_grade / 100) * 5.0


def has_passed(formative_pct, summative_pct):
    return formative_pct >= PASS_MARK and summative_pct >= PASS_MARK


def find_resubmissions(assignments):
    """Failed formatives that share the highest weight (all ties included)."""
    failed = [a for a in assignments if a["group"] == FORMATIVE and a["score"] < PASS_MARK]
    if len(failed) == 0:
        return []
    highest = failed[0]["weight"]
    for a in failed:
        if a["weight"] > highest:
            highest = a["weight"]
    return [a for a in failed if a["weight"] == highest]


def main():
    assignments = load_csv_data()

    errors = validate_grades(assignments) + validate_weights(assignments)
    if errors:
        print("\nValidation failed:")
        for e in errors:
            print(" -", e)
        sys.exit(1)

    total = weighted_total(assignments)
    formative_pct = category_percentage(assignments, FORMATIVE)
    summative_pct = category_percentage(assignments, SUMMATIVE)
    gpa = calculate_gpa(total)
    status = "PASSED" if has_passed(formative_pct, summative_pct) else "FAILED"

    print("\n===== TRANSCRIPT =====")
    for a in assignments:
        print(f"{a['name']:<25} {a['group']:<10} score: {a['score']:>5.1f}  weight: {a['weight']:>4.1f}")
    print("----------------------")
    print(f"Total grade:      {total:.2f} / 100")
    print(f"Formative:        {formative_pct:.2f}%")
    print(f"Summative:        {summative_pct:.2f}%")
    print(f"GPA:              {gpa:.2f} / 5.0")
    print(f"Final status:     {status}")

    resubmit = find_resubmissions(assignments)
    if resubmit:
        print("\nEligible for resubmission:")
        for a in resubmit:
            print(f" - {a['name']} (weight {a['weight']:g}, score {a['score']:g})")
    else:
        print("\nNo formative assignments to resubmit.")


if __name__ == "__main__":
    main()
