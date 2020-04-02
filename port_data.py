import csv

import psycopg2

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres port=5555")
cur = conn.cursor()
csv_file = 'traininglog.csv'
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row.
    cur.execute("SET datestyle = dmy")
    for row in reader:
        cur.execute("INSERT INTO workouts_training VALUES ({0}, '{1}', '{2}', '{3}', {4}, {5}, {6}, '{7}')".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        conn.commit()
f.close()
with open('characteristics.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    cur.execute("SET datestyle = dmy")
    for row in reader:
        cur.execute("INSERT INTO workouts_characteristics VALUES ({0}, '{1}', {2}, '{3}', {4}, {5}, {6}, {7}, {8})".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        conn.commit()
f.close()
