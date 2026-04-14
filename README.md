# ca-health-data-scraper
Python scraper analyzing California health-related datasets using the CA Open Data API

## California Health Data Scraper (CA Open Data API)

Project Overview:

This project collects health-related datasets from the California Open Data Portal using their public API. The goal is to explore how health-related data is distributed across time, organizations, and dataset complexity.

A key limitation encountered during this project was the cost with AI inference tools (Hugging Face and external model providers). Several initial approaches using hosted AI models failed due to rate limits, insufficient quotas, or paid access requirements. Because of this, the project was redesigned to rely entirely on free and publicly accessible API data collection and local Python analysis. (Sorry about this!)

## Data Source:

Data was collected from the California Open Data API: https://data.ca.gov/api/3/action/package_search

The dataset was retrieved using API requests and pagination to gather 1000 records.

## Methods
- requests to access the CA Open Data API
- Pagination (start, rows) to collect multiple pages of results
- Looping until reaching approximately 1000 datasets
- Data cleaning using pandas
- Feature extraction:
  - dataset title
  - organization
  - creation date
  - last update date
  - number of resources
  - notes field for additional context

To ensure responsible data collection, a short delay (time.sleep) was included between requests to avoid overwhelming the server.

## Analysis and Visualizations

The following analyses and visualizations were performed:

1. Dataset Trends Over Time
A bar chart showing how dataset creation varies by year.

2. Top Organizations
A bar chart identifying which agencies publish the most health-related datasets.

3. Resource Distribution
A histogram showing how many resources datasets typically contain.

4. Average Resources Over Time
A line chart showing how dataset complexity changes across years.

## Key Findings

The analysis revealed several important patterns:

- A small number of California agencies account for the majority of health-related datasets, with departments such as Health Care Services and Public Health being the most active publishers. Surprisingly, the Fish adn Wildlife department had high amounts of datasets. A good reminder not all health data is about humans. 
- Dataset publication has increased significantly in recent years, especially from 2023 through 2026, suggesting rapid growth in data availability.
- Dataset complexity varies widely, with some datasets containing only a few resources while others contain over 200. This indicates inconsistent structuring across agencies.
- Newer datasets tend to include more structured and multi-resource formats, which suggests improvements in data reporting practices over time.

## Scraper Performance Evaluation

The performance of the web scraper was evaluated using the following criteria:

- **Completeness of data collection:** The scraper successfully collected approximately 1000 datasets using API pagination, ensuring coverage across multiple pages of results.
- **Stability of execution:** The script ran continuously without crashing by handling API responses and checking for valid results at each request.
- **Efficiency:** Pagination with controlled batch sizes (100 records per request) ensured efficient and manageable data retrieval.
- **Responsiveness to API limits:** A delay (`time.sleep`) was included between requests to prevent overwhelming the CA Open Data API and to ensure responsible scraping behavior.
- **Data quality checks:** The scraper verified response status codes and ensured that extracted fields (title, organization, dates, and resources) were consistently structured before storing them.

Overall, the scraper was considered successful because it reliably collected a large, structured dataset (≈1000 records) suitable for analysis without errors or data corruption.

## Limitations

Several limitations affected this project:

- Cost barriers and API restrictions prevented the use of hosted AI inference models, which is why the project had to go in a different direction. 
- The dataset is dependent on what is available in the California Open Data Portal at the time of access.
- Keyword-based or broad querying may include datasets that are only loosely related to health.
- API pagination and metadata availability limit the completeness of the dataset.

## Conclusion

This project demonstrates how public APIs can be used to collect, clean, and analyze real-world datasets using Python. Despite limitations caused by external AI model access restrictions, the final implementation successfully provides meaningful insight into how California health-related datasets are distributed, how they evolve over time, and how dataset complexity varies across agencies.
