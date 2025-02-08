import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load dataset
df = pd.read_csv("jobs.csv")

# Convert fraudulent column to categorical for better visualization
df["fraudulent"] = df["fraudulent"].map({0: "Legit", 1: "Fraudulent"})

# 1. Distribution of Fraudulent vs. Legitimate Jobs
plt.figure(figsize=(6,4))
sns.countplot(data=df, x="fraudulent", palette="coolwarm")
plt.title("Distribution of Fraudulent vs. Legitimate Jobs")
plt.xlabel("Job Type")
plt.ylabel("Count")
plt.show()

# 2. Word Cloud for Fraudulent Job Postings
fraud_jobs = " ".join(df[df["fraudulent"] == "Fraudulent"]["description"].dropna())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(fraud_jobs)

plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Common Words in Fraudulent Job Descriptions")
plt.show()

# 3. Salary Range Analysis (Checking Missing Values)
df["has_salary"] = df["salary_range"].notnull()
plt.figure(figsize=(6,4))
sns.countplot(data=df, x="has_salary", hue="fraudulent", palette="viridis")
plt.title("Salary Range Availability in Job Postings")
plt.xlabel("Salary Mentioned")
plt.ylabel("Count")
plt.xticks(ticks=[0,1], labels=["Missing", "Available"])
plt.show()

# 4. Industries Most Affected by Fraudulent Jobs
top_industries = df[df["fraudulent"] == "Fraudulent"]["industry"].value_counts().head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=top_industries.values, y=top_industries.index, palette="magma")
plt.title("Industries with the Most Fraudulent Job Postings")
plt.xlabel("Count")
plt.ylabel("Industry")
plt.show()
