#import os
#os.environ["ORACLE_HOME"] ='/usr/lib/oracle/11.2/client64/lib/'
import cx_Oracle
import pandas as pd
con=cx_Oracle.connect("mana0809","mana0809","MAFILUAT")
query ="select * from TBL_FAQS"
data=pd.read_sql(query,con=con)
print(data)
