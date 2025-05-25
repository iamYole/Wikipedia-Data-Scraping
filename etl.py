import logging
import os
import requests
import csv
import json
import pandas as pd
from bs4 import BeautifulSoup
import psycopg2
from sqlalchemy import create_engine
from dotenv import find_dotenv, load_dotenv

#loading the environment variables
dot_env_file = find_dotenv()
load_dotenv(dot_env_file)

#setting the log parameters

dir_path = os.path.dirname(os.path.realpath(__file__))
logs_dir = os.path.join(dir_path, 'logs')
# Create the directory if it doesn't exist
os.makedirs(logs_dir, exist_ok=True)
# Define the full path to the log file inside the 'logs' directory
log_file_path = os.path.join(logs_dir, 'logs.log')


# Define and create 'data' folder
dir_path = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(dir_path, 'data')
os.makedirs(data_dir, exist_ok=True)

# Full path to the file inside 'data' folder
data_file_path = os.path.join(data_dir, 'universities.csv')
cleaned_file_path = os.path.join(data_dir, 'cleaned_universities.csv')


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_file_path)
formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Initiating the ETL Job............")
logger.info("====================================================================")

def extract_data(row):
    row_list = row.find_all('td')
    row_item = list(map(lambda x: x.text.strip(), row_list))
    link = row_list[1].find_all('a')[1]['href'].lstrip('/')
    row_item[-1] = f"https://en.wikipedia.org/"+ link if link else ''
    return row_item

def extract(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    table = soup.find('table', attrs={'class':'wikitable'})
    trs = table.find_all('tr')

    columns = []
    for item in trs[0].find_all('th'):
        columns.append(item.text.strip())

    headers = list(map(lambda x: x.text.strip(), trs[0].find_all('th')))
    headers[6] = "Delivery_Method"
    headers[-1] = "Link"
    
    rows = trs[1:]
    data = list(map(extract_data, rows))

    logger.info(f"extracted {len(data)} rows from the url....")
    logger.info("====================================================================")

    return headers, data


def saving_to_csv(headers, data):
    with open(data_file_path, 'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(data)

        logger.info(f"the data has been saved to: {data_file_path}")
        logger.info("====================================================================")

def data_cleaning_transformation(file_path,year):
    df = pd.read_csv(file_path, encoding="utf-8")

    logger.info("Loading data for cleaning and transformation............")
    logger.info("====================================================================")

    df["Founded"] = df["Founded"].str.extract(r"(\d{4})").astype(int)
    df["Enrollment"] = df["Enrollment"].str.replace(r"[^\d]", "", regex=True).astype(int).values
    df[["location_city", "location_country"]] = df["Location"].str.extract(r"^(.*?),?\s*([^,]+)$")
    df["location_city"] = df["location_city"].replace('', pd.NA).fillna('Not Available')
    df["updated_year"] = year

    df.to_csv(cleaned_file_path, sep=",", header=True)
    logger.info(f" Saved the cleaned data to: {cleaned_file_path}")
    logger.info("====================================================================")

def connect_to_postgres():
    conn = psycopg2.connect(
        host=os.getenv("host"),
        port=os.getenv("port"),
        password=os.getenv("password"),
        user=os.getenv("user"),
        database=os.getenv("database")
    )
    logger.info("Database connection established....")
    logger.info("====================================================================")
    return conn
    
    


def loading_data_to_database(file_path):
    df = pd.read_csv(file_path, index_col=0)
    conn = connect_to_postgres()
    engine = create_engine("postgresql+psycopg2://", creator=lambda:conn)

    create_qry_file = open("sql_scripts/postgres_create_table.sql")
    create_gry = create_qry_file.read()

    try:
        cursor = conn.cursor()
        cursor.execute(create_gry)
        conn.commit()
        cursor.close()
        logger.info("Tables creation query executed sucessufully !!!")
    except Exception as e:
        conn.rollback()  # Roll back on error
        cursor.close()
        logger.error("Error executing query:", e)
        logger.info("====================================================================")

    #loading the cleaned data to the database
    logger.info("loading the cleaned data to the database")
    logger.info("====================================================================")

    data = df.itertuples(index=None, name=None)
    merge_qry_file = open("sql_scripts/postgres_upsert.sql")
    merge_qry = merge_qry_file.read()

    try:
        cursor = conn.cursor()
        cursor.executemany(merge_qry, data)
        conn.commit()
        cursor.close()
        logger.info(f" Table loaded sucessufully !!!")
        logger.info("====================================================================")
    except Exception as e:
        conn.rollback()
        cursor.close()
        logger.error("Error executing query:", e)
        logger.info("====================================================================")

    #loading dimUniversities
    logger.info("loading dimUniversity")
    logger.info("====================================================================")

    dim_uni_qry = """
            select DISTINCT(u.university_name) as university_name,u.founded,u.uni_link
            from universities u ;
            """
    df_universities = pd.read_sql(dim_uni_qry, con=engine)
    uni_data = df_universities.itertuples(index=None, name=None)
    merge_dimUni_file = open("sql_scripts/upsert_dim_universities.sql")
    merge_dimUni = merge_dimUni_file.read()

    try:
        cursor = conn.cursor()
        cursor.executemany(merge_dimUni, uni_data)
        conn.commit()
        cursor.close()
        logger.info(f"dimUniversity loaded sucessufully !!!")
        logger.info("====================================================================")
    except Exception as e:
        conn.rollback()
        cursor.close()
        logger.error("Error executing query:", e)
        logger.info("====================================================================")

    #loading dimLocations
    logger.info("loading dimLocations")
    logger.info("====================================================================")
    dim_location_qry = """ 
                    select distinct u.location_city, u.location_country, u.continent
                    from universities u 
                    """

    df_locations = pd.read_sql(dim_location_qry, con=engine)
    location_data = df_locations.itertuples(index=None, name=None)
    merge_dimloc_file = open("sql_scripts/upsert_dim_locations.sql")
    merge_dimloc = merge_dimloc_file.read()

    try:
        cursor = conn.cursor()
        cursor.executemany(merge_dimloc, location_data)
        conn.commit()
        cursor.close()
        logger.info("dimLoaction loaded sucessufully !!!")
        logger.info("====================================================================")
    except Exception as e:
        conn.rollback()
        cursor.close()
        logger.error("Error executing query:", e)
        logger.info("====================================================================")

    #loading dimAffilations
    logger.info("loading dimAffilations")
    logger.info("====================================================================")
    dim_affilations_qry = """ 
                    SELECT distinct affiliation from universities;
                    """

    df_affilations = pd.read_sql(dim_affilations_qry, con=engine)
    affilations_data = df_affilations.itertuples(index=None, name=None)
    merge_dimaff_file = open("sql_scripts/upsert_dim_afflilations.sql")
    merge_dimaff = merge_dimaff_file.read()

    try:
        cursor = conn.cursor()
        cursor.executemany(merge_dimaff, affilations_data)
        conn.commit()
        cursor.close()
        logger.info("dimAffilations loaded sucessufully !!!")
        logger.info("====================================================================")
    except Exception as e:
        conn.rollback()
        cursor.close()
        logger.error("Error executing query:", e)
        logger.info("====================================================================")

    #loading dimDeliveryMethods
    logger.info("loading dimDeliveryMethods")
    logger.info("====================================================================")

    dim_delivery_method_qry = """ 
                    SELECT distinct delivery_method from universities;
                    """

    df_delivery_method_qry = pd.read_sql(dim_delivery_method_qry, con=engine)
    #converts the datafram to a tuple
    delivery_method_data = df_delivery_method_qry.itertuples(index=None, name=None)
    merge_dimdilvery_file = open("sql_scripts/upsert_dim_deliveryMethod.sql")
    merge_delivery_methods = merge_dimdilvery_file.read()

    try:
        cursor = conn.cursor()
        cursor.executemany(merge_delivery_methods, delivery_method_data)
        conn.commit()
        cursor.close()
        logger.info("dimDeliveryMethods loaded sucessufully !!!")
        logger.info("====================================================================")
    except Exception as e:
        conn.rollback()
        cursor.close()
        logger.error("Error executing query:", e)
        logger.info("====================================================================")

     #loading dimDeliveryMethods
    logger.info("loading the fact table")
    logger.info("====================================================================")
    qry = """
        select r.university_rank, r.enrollment, du.university_id, l.location_id,dm.delivery_method_id,a.affiliation_id, r.updated_year
        from universities r
            left join dimuniversities du on r. university_name = du.university_name 
            left join dimAffilations a on r.affiliation = a.affiliation
            left join dimDeliveryMethods dm on r.delivery_method = dm.delivery_method
            left join dimlocations l on (r.location_city , r.location_country, r.continent) = (l.location_city,l.location_country, l.continent)
        """

    df_fact_ranking = pd.read_sql(qry, con=engine)  
    fact_data = df_fact_ranking.itertuples(index=None, name=None)

    insert_qry = """ 
                INSERT INTO factrankings 
                    (university_rank,enrollment,university_id,location_id,delivery_method_id,affiliation_id,updated_year)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

    try:
        cursor = conn.cursor()
        cursor.executemany(insert_qry, fact_data)
        conn.commit()
        cursor.close()
        logger.info("factRankings loaded sucessufully !!!")
        logger.info("====================================================================")
    except Exception as e:
        conn.rollback()
        cursor.close()
        logger.error("Error executing query:", e)
        logger.info("====================================================================")

def main():
    url = 'https://en.wikipedia.org/wiki/List_of_largest_universities_and_university_networks_by_enrollment'
    headers, data = extract(url)
    saving_to_csv(headers, data)
    data_cleaning_transformation(data_file_path,"2025")
    loading_data_to_database(cleaned_file_path)

if __name__ == "__main__":
    main()
