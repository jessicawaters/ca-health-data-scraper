import requests
import pandas as pd
import time
import matplotlib.pyplot as plt

url = "https://data.ca.gov/api/3/action/package_search"

all_data = []
start = 0
rows = 100

# ----------------------------
# LIMIT CONTROL (NEW)
# ----------------------------
TARGET = 1000

while True:
    params = {
        "q": "",
        "rows": rows,
        "start": start
    }

    response = requests.get(url, params=params)

    # safety check (NEW)
    if response.status_code != 200:
        print("Request failed:", response.status_code)
        break

    data = response.json()

    results = data.get("result", {}).get("results", [])

    if not results:
        break

    all_data.extend(results)

    print(f"Collected so far: {len(all_data)}")

    start += rows

    # ----------------------------
    # STOP AT ~1000 (NEW)
    # ----------------------------
    if len(all_data) >= TARGET:
        break

    time.sleep(0.2)  # polite delay


print("\nTotal datasets collected:", len(all_data))


# ----------------------------
# CLEAN DATA
# ----------------------------
clean_data = []

for d in all_data:
    clean_data.append({
        "title": d.get("title"),
        "organization": d.get("organization", {}).get("title") if d.get("organization") else None,
        "created": d.get("metadata_created"),
        "updated": d.get("metadata_modified"),
        "num_resources": len(d.get("resources", [])),
        "notes": d.get("notes")  # NEW (helps later analysis)
    })

df = pd.DataFrame(clean_data)


# ----------------------------
# DATE PROCESSING
# ----------------------------
df["created"] = pd.to_datetime(df["created"], errors="coerce")
df["year"] = df["created"].dt.year


# ----------------------------
# SAVE
# ----------------------------
df.to_csv("health_datasets_full.csv", index=False)


# ----------------------------
# ANALYSIS
# ----------------------------
print("\nYEAR DISTRIBUTION:")
print(df["year"].value_counts().sort_index())


print("\nTOP ORGANIZATIONS:")
print(df["organization"].value_counts().head(10))


print("\nRESOURCE DISTRIBUTION:")
print(df["num_resources"].describe())


# ----------------------------
# GRAPH 1: YEAR TREND
# ----------------------------
year_counts = df["year"].value_counts().sort_index()

plt.figure()
year_counts.plot(kind="bar")
plt.title("Health Datasets by Year")
plt.xlabel("Year")
plt.ylabel("Count")
plt.tight_layout()
plt.show()


# ----------------------------
# GRAPH 2: TOP ORGANIZATIONS
# ----------------------------
org_counts = df["organization"].value_counts().head(10)

plt.figure()
org_counts.plot(kind="bar")
plt.title("Top Organizations Publishing Health Datasets")
plt.xlabel("Organization")
plt.xticks(fontsize=5)
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# ----------------------------
# GRAPH 3: RESOURCE DISTRIBUTION
# ----------------------------

plt.figure()
plt.hist(df["num_resources"], bins=30)
plt.title("Distribution of Number of Resources per Dataset")
plt.xlabel("Number of Resources")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# ----------------------------
# GRAPH 4: AVERAGE RESOURCES PER YEAR
# ----------------------------

avg_resources_by_year = df.groupby("year")["num_resources"].mean()

plt.figure()
avg_resources_by_year.plot(kind="line", marker="o")
plt.title("Average Number of Resources per Dataset Over Time")
plt.xlabel("Year")
plt.ylabel("Average Number of Resources")
plt.tight_layout()
plt.show()