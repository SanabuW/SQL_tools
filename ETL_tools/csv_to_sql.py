import yaml
import mysql.connector
import csv

# Load connection configuration from yaml doc and create connection dictionary
db = yaml.safe_load(open('db.yaml'))
config = {
    'user': db['user'],
    'password': db['pwrd'],
    'host': db['host'],
    'database': db['db'],
    'auth_plugin': 'mysql_native_password'
}

# Set up connection
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered = True)

# Query for and print the initial table to console
query = ('SELECT * FROM colleges')
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

# Open reader to access data to input
with open("japan_uni_list.csv", "r") as reader_obj:
    uni_csv = csv.reader(reader_obj, delimiter=',')
    # The main loading query.
    # For each row/university in the reader, send the name and city value into the INSERT query. Then execute query
    for uni_row in uni_csv:
        query = (f'INSERT INTO `colleges` VALUES(NULL, "{uni_row[1]}", NULL, "{uni_row[2]}", NULL, "Japan")')
        cursor.execute(query)
        cnx.commit()

# Query for and print the changed table to confirm results
query = ('SELECT * FROM colleges')
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

# Close/clean SQL operations
cursor.close()
cnx.close()
