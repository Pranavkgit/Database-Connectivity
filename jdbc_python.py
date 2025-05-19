#import pandas and database connector libraries
import pandas as pd
import mysql.connector

# Connecting a database(configuration details) 
database_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'pranav353',
    'database': 'assgn'
}

# setting up the database and cursor connections  
conn = mysql.connector.connect(**database_config)
cursor = conn.cursor()

# List of all the .csv filename w.r.t to table names created.
filenames = {
    "Country.csv": "Country",
    "League.csv": "League",
    "Team.csv": "Team",
    "Player.csv": "Player",
    "Match_cleaned.csv": "Match",
    "Player_Attributes.csv": "Player_Attributes",
    "Team_Attributes.csv": "Team_Attributes"
}

# Insert the data into the tables first, one after the other. 
for filename, table_name in filenames.items():
    #using pandas library read out the .csv file
    data_frame = pd.read_csv(filename)

    # Replace all the values that are unnecassary with NULL_STRING or 0 or empty ''
    for i in data_frame.columns:
        if data_frame[i].dtype == 'object':
            data_frame[i].fillna('NULL_STRING', inplace=True)
        elif data_frame[i].dtype in ['int64', 'float64']:
            data_frame[i].fillna(0, inplace=True)
        else:
            data_frame[i].fillna('', inplace=True)

    # .drop_duplicates is a method which directly drops out all the duplicates.
    data_frame.drop_duplicates(inplace=True)

    for i, j in data_frame.iterrows():
        # extract the rowdata into a tuple first
        row_tuple = tuple(j)
        delimeter_value = ', '.join(['%s'] * len(j)) #join all the values with length of the row using a delimeter ','
        #creating a insert query
        Insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in data_frame.columns])}) VALUES ({delimeter_value})"

        # execute the statement row by row
        try:
            cursor.execute(Insert_query, row_tuple)
        except mysql.connector.Error as err:
            continue

    # after each table commit the data
    conn.commit()
    print("Data is inserted.")

# Loading the match_cleaned.csv file seperately as the file is too large
match_data = pd.read_csv("Match.csv") 

# Do the same steps as above
for column in match_data.columns:
    if match_data[column].dtype == 'object':
        match_data[column].fillna('NULL_STRING', inplace=True)
    elif match_data[column].dtype in ['int64', 'float64']:
        match_data[column].fillna(0, inplace=True)
    else:
        match_data[column].fillna('', inplace=True)

for i, j in match_data.iterrows():
    # Convert row to tuple
    row_tuple = tuple(j)
    Match_delimeter = ', '.join(['%s'] * len(j))
    Match_query = f"INSERT INTO `Match` ({', '.join([f'`{col}`' for col in match_data.columns])}) VALUES ({Match_delimeter})"

    # Execute the SQL statement with row values
    try:
        cursor.execute(Match_query, row_tuple)
    except mysql.connector.Error as err:
       continue

# After all the insertion is done commit it.
conn.commit()
#checking the Match_cleaned.csv file wheather it's inserted or not.
print("Data from Match.csv inserted into Match table successfully.")

# closing out the cursor and the connection
cursor.close()
conn.close()
