import logging;
from sqlalchemy import create_engine; # TO use this package, install package in CMD by using 'pip install sqlalchemy'
import os;
import pandas as pd;
from fn_log_print import fn_log_print;
import boto3;


# Create Reports Folder if Not Exists
# ---------------------------------------------------
if not os.path.exists ("reports"):
 os.makedirs("reports")
 fn_log_print("info","Output reports folder created");
else:
 fn_log_print("info","reports Folder Already Exists");



# Logging Configuration
# ---------------------------------------------------
logging.basicConfig (
    filemode= 'w',
    filename= "D:\\Python_DE\\DE_Projects\\P2-SalesReportGenerator\\logs\\logs.log",
    level= logging.INFO,
    format = '%(asctime)s  %(message)s'
)




# PostgreSQL Connection
# ---------------------------------------------------

DB_USER = "postgres"
DB_PASSWORD = "8489"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"

engine = create_engine(
    f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}' 
                       )
try:  # Checking the DB Connection  is Successfull or Not
 with engine.connect() as conn:
  fn_log_print("info","PostgreSQL Database Connected Successfully");
except Exception as e:
   fn_log_print("ERROR",f"PostgreSQL Database Connection Failed: {e}");

try:
 fn_log_print("info",f"Reading Sales Data from postgresql");

 query = """ select order_date,customer_name,order_amount from orders ; """
 df = pd.read_sql(query, engine)
 #print(df)
 
# ---------------------------------------------------
#               Daily Sales
# ---------------------------------------------------

 
 daily_sales = (df.groupby("order_date")["order_amount"]
              .sum()
              .reset_index()
              .sort_values("order_date"))

 fn_log_print("info",f"DAILY SALES : \n{daily_sales}\n")
  
 # ---------------------------------------------------
 #               Monthly Sales
 # ---------------------------------------------------
 
 df["sale_date"] = pd.to_datetime((df["order_date"]))
 df["month"] = df["sale_date"].dt.to_period('M')
 
 monthly_sales = (df.groupby("month")["order_amount"]
                  .sum()
                  .reset_index()
                  .sort_values("month"))
 fn_log_print("info",f"MONTHLY SALES : \n{monthly_sales}\n")

 # ---------------------------------------------------
 #               Customer Wise Sales
 # ---------------------------------------------------
 customer_sales = (df.groupby("customer_name")["order_amount"]
                         .sum()
                         .reset_index()
                         .sort_values("order_amount",ascending=False))
 fn_log_print("info",f"CUSTOMER SALES : \n{customer_sales}\n")

 # ---------------------------------------------------
 #               Generating Reports to Appropriate Folder
 # ---------------------------------------------------

 if(os.path.exists("reports//daily_sales.csv")): # TO remove the already existing file
  os.remove("reports//daily_sales.csv")
 daily_sales.to_csv("reports//daily_sales.csv");
 fn_log_print("info",f"Daily Sales Report Generated Successfully");


 if(os.path.exists("reports//monthly_sales.csv")): # TO remove the already existing file
  os.remove("reports//monthly_sales.csv")
 monthly_sales.to_csv("reports//monthly_sales.csv")
 fn_log_print("info",f"Monthly Sales Report Generated Successfully");

 if(os.path.exists("reports//customer_sales.csv")): # TO remove the already existing file
  os.remove("reports//customer_sales.csv")
 customer_sales.to_csv("reports//customer_sales.csv")
 fn_log_print("info",f"Customer Sales Report Generated Successfully");

 # ---------------------------------------------------
 #               Connecting S3 to upload files
 # ---------------------------------------------------
# Access key - AKIAY4JAFL5LIS7QSY2J
# Secret access key - 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


 s3 = boto3.client(
        "s3",
        aws_access_key_id="AKIAY4JAFL5LIS7QSY2J",
        aws_secret_access_key="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",
        region_name="ap-south-2"
    )

 s3.upload_file(
        "reports/customer_sales.csv",
        "bepositivebucket",
        "daily_sales.csv"
    )

 print("✅ File uploaded successfully to S3")


except Exception as e:
  fn_log_print("info",f"Error : {e}");

finally:

    print("Pipeline Finished")

