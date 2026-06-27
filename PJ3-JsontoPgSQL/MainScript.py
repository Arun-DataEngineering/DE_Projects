
# Importing Packages
# ---------------------------------------------------
import os;
import pandas as pd;
from config.db_config import *;
from sqlalchemy import create_engine;
from fn_log_print import fn_log_print;
import logging;
import json;


# -----------------------------------------
# Create Required Directories
# -----------------------------------------

if not os.path.exists("logs"):
    os.makedirs("logs")
    fn_log_print("info","Pipeline Log Folder Created Successfullly")
else:
    fn_log_print("info","Pipeline Log Folder Already Exists");

# -----------------------------------------
# Logging Configuration
# -----------------------------------------
logging.basicConfig(level=logging.INFO,
                    filemode='w',
                    filename= "D:\\Python_DE\\DE_Projects\\PJ3-JsontoPgSQL\\logs\\pipelinelog.csv" ,
                    format = '%(asctime)s  %(message)s')

try:
    fn_log_print("info", "Data Pipeline Started")


# -----------------------------------------
# Database Connection Checking
# -----------------------------------------

    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    try:
     with engine.connect() as conn:
        fn_log_print("info", "Postgresql Database Connected Successfully")
    except Exception as e:
       fn_log_print("Error", f"Postgresql Database Connection Failed : {e}");

# -----------------------------------------
# Read JSON File
# -----------------------------------------

    json_file = "jsonfile.json";
    with open(json_file, "r") as file:
       json_data = json.load(file);
    
    fn_log_print("info", f"JSon file Read Successfully - {len(json_data)} Records Found")
 
# -----------------------------------------
# Convert JSON To DataFrame
# -----------------------------------------

    df = pd.DataFrame(json_data)
    fn_log_print(  "info","JSON Converted To DataFrame Successfully")
    print(df)

# -----------------------------------------
# Data Validation
# -----------------------------------------
    if df.isnull().sum(). sum():
     fn_log_print(  "Warning","Null Values Found and Removed")
     df.dropna();
    else:
     fn_log_print(  "info","No Null Values Found")

# -----------------------------------------
# Remove Duplicates
# -----------------------------------------
    duplicate_count = df.duplicated().sum();
    if duplicate_count > 0 :
       df.drop_duplicates()
       fn_log_print(  "Warning",f"{duplicate_count} - Duplicate Values Removed")
    else:
       fn_log_print(  "info","No Duplicate Values Found")


    # -----------------------------------------
    # Load Into PostgreSQL
    # -----------------------------------------
    df.to_sql(
       "employee_json",
       engine, 
       if_exists="append",
       index=False
    )
    fn_log_print(  "info","Record Loaded into Postgresql")

    # -----------------------------------------
    # Fetching Total count of Table
    # -----------------------------------------
    count_query = """select count(*) from employee_json"""
    count_result = (pd.read_sql(count_query, engine))
    fn_log_print(  "info",f"{count_result} - Records existed")

    fn_log_print(  "info","Data Validation Completed Successfully")


    

except Exception as e:
    fn_log_print("Error", f"Error has Occoured on : {e}");

finally:

    try:

        engine.dispose()

        fn_log_print( "info", "Database Connection Closed" )

    except:
        pass

    fn_log_print("info","Pipeline Completed")