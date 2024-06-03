# ---
from db import getQuery, execQuery, abortQuery
import json
# ---

# This script is used to calculate the related column
# And insert the result into the related column

sql = "SELECT id,summary_vector FROM main2"
rows = getQuery(sql, "")

for row in rows:
    id = row[0]
    vec = row[1]
    text_vec_string = str(vec)
    sql = "SELECT id, class, subclass, title FROM main2 ORDER BY \
    summary_vector <-> '" + text_vec_string + "' LIMIT 6"
    rows2 = getQuery(sql, "")

    # map rows to dict
    rows2 = list(map(lambda x: {'id': x[0], 'class': x[1], 'subclass': x[2], 'title': x[3]}, rows2))

    # insert the ids into related column
    sql = "UPDATE main2 SET related = %s WHERE id=%s"
    execQuery(sql,(str(json.dumps(rows2)),id,))

print("DONE!")
# ---
abortQuery()
# ---
import pandas as pd
import math as Math

df = pd.read_csv('./dataset/class.csv', encoding='ISO-8859-1', sep=",")
df.head()

# loop trough df and print id
for index, row in df.iterrows():
    id = str(Math.floor(row['id']))
    class_name = str(row['class'])
    subclass_name = str(row['subclass'])
    sql = "UPDATE main2 SET class = '" + class_name + "', subclass= '" + subclass_name + "' WHERE id=" + id
    execQuery(sql, "")

print ("DONE !")
# ---

