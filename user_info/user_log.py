import yaml
import mysql.connector
from datetime import date

# Load connection configuration from yaml doc
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
cursor = cnx.cursor()

# Ready txt file for output
log_file = open(f'user_grants_log_({date.today().strftime("%Y_%m_%d")}).txt', "w")
userlist = []

# Query for all users that have access to selected db
query = ('SELECT user FROM mysql.user')
cursor.execute(query)
# For each user found, make another query retrieving their access privileges
for row in cursor.fetchall():
    # Periods in the username will interrupt the query. Add " around the username
    # For each user, show privileges granted
    query = (f'SHOW GRANTS FOR "{row[0]}"@localhost')
    cursor.execute(query)
    for sub_row in cursor.fetchall():
        print(row[0], ": ", sub_row)
    # Ensure newline is added between each line
    userlist.append(f'{row[0]}: {sub_row}\n')

# Close/clean SQL operations
cursor.close()
cnx.close()

# Write to txt file
log_file.writelines(userlist)
log_file.close()
