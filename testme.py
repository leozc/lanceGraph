import lancedb
import pandas as pd
import datasource
from lancedb.embeddings import with_embeddings
import duckdb

import datasource
db = lancedb.connect(".lancedb")
tbname = "addresstx"
tbl = None
if tbname in db.table_names():
    print ("table exists")
    tbl = db.open_table(tbname)
    print(tbl.schema)
    addresstx = tbl.to_lance()
    x = duckdb.sql("SELECT * FROM addresstx USING SAMPLE 10").to_df()

    # for x in df.to_dict(orient='records'):
    #     print (x)
else:
    print ("creating table")
    
    df = pd.DataFrame(datasource.generateRandomAddressPairs(3,100))
    
    print ("Dataframe created")
    # can I do better? need to generate an embedding for {from:str , to:str}
    data = with_embeddings(func = datasource.map_address_to_float, column="from", wrap_api=False, data = df)
    data = with_embeddings(func = datasource.map_address_to_float, column="to", wrap_api=False, data = data)

    tbl = db.create_table(tbname, data = data)
