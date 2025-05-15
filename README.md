# Wikipedia Web Scraper with Data Pipeline

This project demonstrates a complete web scraping and data pipeline solution using Python. It scrapes a Wikipedia article [List of largest universities and university networks by enrollment ](https://en.wikipedia.org/wiki/List_of_largest_universities_and_university_networks_by_enrollment) using BeautifulSoup, cleans and transforms the data, and loads it into a PostgreSQL database running inside a Docker container. The entire process is automated and scheduled using a task scheduler like cron or APScheduler.

🔧 Key Features
🌐 Web Scraping: Extract Wikipedia content (titles, summaries, and full articles) using requests and BeautifulSoup.

🗃️ Database Integration: Store cleaned data in a PostgreSQL database configured via Docker for easy setup and portability.

🧹 Data Cleaning & Transformation: Perform basic text cleaning and transformation to prepare the data for analysis or storage.

⚙️ ETL Pipeline: Efficient loading of scraped data into the database with error handling and logging.

⏱️ Task Scheduling: Automate the scraping and loading process using a task scheduler to run at defined intervals.

📦 Tech Stack
- Python
- BeautifulSoup
- PostgreSQL
- Docker
- APScheduler / cron

### Step 1 - Installing the Virtual Python Enviroment and the required libraries
Launch VS Code and create a new project. From the terminal windown, type `python -m venv venv`.
Ensure the virtual environment is activated by typing `source venv/bin/activate` in the terminal.
![alt text](Images/Img_01.png)

Next, install **requests** and **beautiful soup4** by typing `pip install requests bs4`.

### Step 2 - Write the Python code to scrape with website

**Importing the required packages**

