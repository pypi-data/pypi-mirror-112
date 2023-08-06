try: import cPickle as pickle
except: import pickle
from datetime import date, timedelta
import glob
from os import getcwd, path

import pandas as pd
from shucks.snowflake import SnowflakeConfig
import constants as c

SSQL = SnowflakeConfig.load(path.expanduser('~/shucks/sf_config.ini'))

snowflake_format = c.SNOWFLAKE_FORMAT
index_folder = getcwd()

end_date = date.today()-timedelta(days=1)
start_date = end_date-timedelta(days=365)

def get_snowflake_data(start_date,end_date,index_folder,snowflake_format):
    
    def save_snowflake_data(df, index_folder, snowflake_format):
        out_path = path.join(index_folder, snowflake_format)    
        pickle.dump(df, open(out_path, "wb"))
        print(f"Saved data in {index_folder}")
        
    print("Getting Snowflake data...",end=" ")
    
    query = f"""
        SELECT v.DATE as "date",
               v.ISBN as "isbn",
               SUM(v.ORDERED_UNITS) as "units",
               t.producttype as "format"               
        FROM   prh_global_uk_sandbox.PUBLIC.gdh_edw_pos_vw v
        JOIN   prh_global_uk_sandbox.PUBLIC.title t ON t.EAN = v.ISBN
        WHERE  DATE >= '{start_date}'
        AND    DATE <= '{end_date}'
        AND    cust_level_name = 'Amazon' 
        AND    iso_country_code = 'GB' 
        AND    summary_level = 'D' 
        AND    currency_symbol = 'GBP'
        GROUP BY v.DATE, v.ISBN, t.producttype
        ORDER BY v.DATE, v.ISBN"""
    
    with SSQL.connect() as conn:
        df = pd.read_sql(query, conn)      
    
    print(f"Got data for {start_date}-{end_date}.")
    
    save_snowflake_data(df, index_folder, snowflake_format)


get_snowflake_data(start_date,end_date,index_folder,snowflake_format)