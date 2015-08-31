import sqlite3

import pandas as pd

from settings import DATABASE_FILE

__author__ = 'laurogama'


def load_data():
    con = sqlite3.connect(DATABASE_FILE)
    query = "SELECT * from message"
    return pd.read_sql_query(query, con)


def visualize_data(df):
    print df.head()
    print df.tail()
    pass


if __name__ == '__main__':
    # db_session = create_db_session()
    dataframe = load_data()
    visualize_data(dataframe)
