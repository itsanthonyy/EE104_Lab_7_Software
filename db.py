import psycopg2

import environ
env = environ.Env()
environ.Env.read_env()

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    user='postgres',
    password=env('DBPASS'),
    database=env('DATABASE')
)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the tasks table if it doesn't exist
# Create the tasks table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id SERIAL PRIMARY KEY,
             first_name TEXT,
             middle_name TEXT,
             last_name TEXT,
             phone_number TEXT,
             email TEXT,
             first_vaccination_date DATE,
             second_vaccination_date DATE)''')


# Insert sample tasks into the tasks table
# Insert sample tasks into the tasks table
cursor.execute("INSERT INTO tasks (first_name, middle_name, last_name, phone_number, email, first_vaccination_date, second_vaccination_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
               ('John', 'Doe', None, '1234567890', 'john@example.com', '2023-04-01', '2023-04-29'))
cursor.execute("INSERT INTO tasks (first_name, middle_name, last_name, phone_number, email, first_vaccination_date, second_vaccination_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
               ('Max', None, 'Doe', '0987654321', 'jane@example.com', '2023-04-05', '2023-05-03'))
cursor.execute("INSERT INTO tasks (first_name, middle_name, last_name, phone_number, email, first_vaccination_date, second_vaccination_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
               ('Chris', 'M', 'Smith', '1112223333', 'alice@example.com', '2023-04-10', '2023-05-08'))
cursor.execute("INSERT INTO tasks (first_name, middle_name, last_name, phone_number, email, first_vaccination_date, second_vaccination_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
               ('Bob', 'A', 'Johnson', '4445556666', 'bob@example.com', '2023-04-15', '2023-05-10'))
cursor.execute("INSERT INTO tasks (first_name, middle_name, last_name, phone_number, email, first_vaccination_date, second_vaccination_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
               ('Eve', None, 'Brown', '7778889999', 'eve@example.com', '2023-04-20', '2023-05-15'))


# Commit the changes and close the connection
conn.commit()
conn.close()