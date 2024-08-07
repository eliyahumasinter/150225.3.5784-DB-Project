import psycopg2
from config import load_config
from reg_num import random_registration_num
import re


def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        conn = psycopg2.connect(**config)
        print('Connected to the PostgreSQL server.')
        cur = conn.cursor()

        sql = '''ALTER TABLE airplane
                 ADD COLUMN aircraft_rn character varying;'''
        cur.execute(sql)
        conn.commit()

        sql = '''SELECT count(*) FROM airplane;'''
        cur.execute(sql)
        count = cur.fetchall()[0][0]
        print(str(count))

        for sn in range(count-1):
            sql = f"UPDATE airplane SET aircraft_rn = '{random_registration_num()}' WHERE serialnumber = {sn};"
            cur.execute(sql)
            conn.commit()

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    config = load_config()
    connect(config)
