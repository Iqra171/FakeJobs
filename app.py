import pandas as pd
from fuzzywuzzy import fuzz
import re

# Load dataset
df = pd.read_csv("jobs.csv")  # Replace with your actual CSV file
df = df.apply(lambda col: col.astype(str).str.lower())  # Convert text columns to lowercase

# Define fraudulent keywords, gibberish patterns, and suspicious words
fraudulent_keywords = ["free money", "earn from home", "no experience needed", "get rich quick"]
suspicious_words = ["urgent", "immediate start", "limited offer", "guaranteed income"]
gibberish_pattern = re.compile(r'\b[a-z]{10,}\b')  # Matches long sequences of lowercase letters

def normalize_location(location):
    """Formats locations consistently for better matching."""
    if location:
        parts = [p.strip() for p in location.split(",")]  # Remove extra spaces
        return ", ".join(parts)  # Reconstruct properly formatted location
    return None

def find_best_match(job_title, location=None):
    """
    Finds the best match in the dataset using fuzzy string matching.
    Handles locations formatted as "US, AL, ALEXANDER CITY".
    """
    best_match = None
    best_score = 0

    for _, row in df.iterrows():
        row_title = str(row["title"]) if pd.notna(row["title"]) else ""
        row_location = normalize_location(str(row["location"])) if pd.notna(row["location"]) else ""

        title_score = fuzz.partial_ratio(job_title, row_title)
        location_score = fuzz.partial_ratio(location, row_location) if location else 0

        # Average scores
        total_score = (title_score + location_score) / (2 if location else 1)

        if total_score > best_score:
            best_match = row
            best_score = total_score

    return best_match, round(best_score, 2)

def check_fraudulent_job(user_input):
    """
    Extracts job details from user input and checks if the job is fraudulent.
    Provides detailed reasons for fraud detection.
    """
    # Extract job title and location, eliminating the company name
    parts = user_input.lower().split(" at ")
    job_title = parts[0].strip() if len(parts) > 0 else None
    location = normalize_location(parts[1].strip()) if len(parts) > 1 else None

    # Find the best match
    match, score = find_best_match(job_title, location)

    if match is not None:
        # Check for fraudulent keywords, gibberish, and suspicious words in the job description
        job_description = str(match["description"]) if pd.notna(match["description"]) else ""
        fraud_reasons = []

        # Check for fraudulent keywords
        for keyword in fraudulent_keywords:
            if keyword in job_description:
                fraud_reasons.append(f"Fraudulent keyword found: '{keyword}'")

        # Check for suspicious words
        for word in suspicious_words:
            if word in job_description:
                fraud_reasons.append(f"Suspicious word found: '{word}'")

        # Check for gibberish
        if gibberish_pattern.search(job_description):
            fraud_reasons.append("Gibberish detected in the job description")

        # If the job is marked as fraudulent in the dataset, add it to the reasons
        if match["fraudulent"] == "1":
            fraud_reasons.append("Marked as fraudulent in the dataset")

        # Determine fraud status
        if fraud_reasons:
            fraud_status = "❌ Fraudulent"
            print(f"\n✅ Best match found: {match['title']} in {match['location']}")
            print(f"🔍 Fraud status: {fraud_status} (Match Score: {score}%)")
            print("Reasons for fraud detection:")
            for reason in fraud_reasons:
                print(f" - {reason}")
        else:
            fraud_status = "Legit ✅"
            print(f"\n✅ Best match found: {match['title']} in {match['location']}")
            print(f"🔍 Fraud status: {fraud_status} (Match Score: {score}%)")
    else:
        print("\n❌ No matching job found in the dataset.")

# User input
user_input = input("Enter job details (e.g., 'Marketing Manager in US, AL, ALEXANDER CITY'): ")
check_fraudulent_job(user_input)
