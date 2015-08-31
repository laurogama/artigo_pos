import pandas as pd
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pylab as plt
from sqlalchemy import create_engine


__author__ = 'laurogama'

SQL_ENGINE = 'sqlite:////home/laurogama/pos-uea/artigo final/artigo_pos/environ_wsn/broker/test.db'


def load_data():
    query = "SELECT * from message"
    return pd.read_sql_table("message", engine,
                             columns=['id', 'timestamp', 'temperature',
                                      'humidity', 'sender'],
                             parse_dates={
                                 "timestamp": "YYYY-MM-DD HH:MM:SS.SSS"})


# parse_dates={"timestamp": "YYYY-MM-DD HH:MM:SS.SSS"}

def visualize_data(df):
    # printing  univariate distribution
    # df = df[['id', 'timestamp', 'temperature', 'humidity', 'sender']]
    print df.dtypes
    print df.head()
    # print df.tail()
    # sns.distplot(df['temperature'])
    # sns.pairplot(data=df, vars=['temperature', 'humidity'])
    # sns.plt.show()
    df.plot(columns=['humidity','temperature'], x='timestamp')
    plt.show()
    df.plot(x='timestamp', y='humidity')
    plt.show()

if __name__ == '__main__':
    engine = create_engine(SQL_ENGINE)
    dataframe = load_data()
    visualize_data(dataframe)
