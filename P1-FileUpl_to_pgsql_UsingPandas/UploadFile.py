import pandas as pd;
import logging;
import psycopg2;



logging.basicConfig (
    filename = "D:\\Python_DE\\DE_Projects\\logging_log.log",
    filemode = 'w',
    level = logging.DEBUG,
    format = '%(message)s %(asctime)s %(levelname)s'
)
inputfile = 'D:\\Python_DE\\DE_Projects\\Employee.csv';
outputfile = 'D:\\Python_DE\\DE_Projects\\output.csv'

try:
    
# To Install psycopg2, Run in Powershell
# 1.  pip install psycopg2-binary
# 2.  python.exe -m pip install --upgrade pip

                                #Postgre SQL Connection
    connection = psycopg2 .connect(
        host = "localhost",
        port = "5432",
        database  = "postgres",
        user="postgres",
        password="8489"
    )

    print("Connected to PostgreSQL Database Successfully") ;  
    logging.debug("Connected to PostgreSQL Database Successfully")


                                 # Reading the CSV File
    df = pd.read_csv(inputfile);
    #print(df)
    logging.debug("CSV read Successfully") ; print('CSV Read Successfully')

                               # Removing Duplicates
    df = df.drop_duplicates()
    logging.info("Duplicates Removed")
    #print(df)

    #Removing Null Values
    df = df.dropna()
    #print(df)
    logging.debug("Null Values Removed") ; print('Null Values Removed Successfully')


    #Generate the Cleaned Data:
    df.to_csv(outputfile , index=True) #If Index is True, It will generated Number for each rows
    logging.info('CSV Report Generated')

                                    #Cur Object
    cur = connection.cursor()
    for index, row in df.iterrows():
        #print(row /n);
        cur.execute(""" Insert into employee_stg values (%s, %s, %s, %s, %s) """,
                 (  row['id'],
                    row['first_name'],
                    row['last_name'],
                    row['email'],
                    row['DateOfJoining']
                    ))
        connection.commit();
        print("Data Loaded Successfully");



except Exception as a:
   logging.error(str(e))

finally:
    logging.info('All Process Finished')
    print("All Process Completed")
