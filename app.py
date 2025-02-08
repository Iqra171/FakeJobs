import pandas as pd
from fuzzywuzzy import fuzz

# Load dataset
df = pd.read_csv("jobs.csv") 
df = df.apply(lambda col: col.astype(str).str.lower()) 

def normalize_location(location):
    """Formats locations consistently for better matching."""
    if location:
        parts = [p.strip() for p in location.split(",")]  
        return ", ".join(parts)
    return None

def find_best_match(job_title, location=None, company=None):
    """
    Finds the best match in the dataset using fuzzy string matching.
    Ensures minimum similarity before accepting a match.
    """
    best_match = None
    best_score = 0
    min_required_score = 80  # Ensure at least 80% match before considering a job

    for _, row in df.iterrows():
        row_title = str(row["title"]) if pd.notna(row["title"]) else ""
        row_location = normalize_location(str(row["location"])) if pd.notna(row["location"]) else ""
        row_company = str(row["company_profile"]) if pd.notna(row["company_profile"]) else ""

        title_score = fuzz.partial_ratio(job_title, row_title)
        location_score = fuzz.partial_ratio(location, row_location) if location else 0
        company_score = fuzz.partial_ratio(company, row_company) if company else 0

        # Weighted score
        total_score = (title_score + location_score + company_score) / (
            3 if location and company else 2 if location or company else 1
        )

        if total_score > best_score and title_score >= min_required_score:
            best_match = row
            best_score = total_score

    # If best score is below 80, return None to indicate no match
    return (best_match, round(best_score, 2)) if best_match and best_score >= min_required_score else (None, 0)

def check_fraudulent_job(user_input):
    """
    Extracts job details from user input and checks if the job is fraudulent.
    """
    parts = user_input.lower().split(" at ")
    job_title = parts[0].strip() if len(parts) > 0 else None
    location = normalize_location(parts[1].strip()) if len(parts) > 1 else None

    match, score = find_best_match(job_title, location)

    if match is not None:
        fraud_status = "Legit ✅" if match["fraudulent"] == "0" else "❌ Fraudulent"
        print(f"\n✅ Best match found: {match['title']} in {match['location']}")
        print(f"🔍 Fraud status: {fraud_status} (Match Score: {score}%)")
    else:
        print("\n❌ No matching job found in the dataset.")

# User input
user_input = input("Enter job details (e.g., 'Marketing Manager at XYZ Company in US, AL, ALEXANDER CITY'): ")
check_fraudulent_job(user_input)
