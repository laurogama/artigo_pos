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
                                      'humidity', 'luminance', 'gas'],
                             parse_dates=True)


# parse_dates={"timestamp": "YYYY-MM-DD HH:MM:SS.SSS"}

def visualize_data(df):
    # printing  univariate distribution
    # df = df[['id', 'timestamp', 'temperature', 'humidity', 'sender']]
    print df.dtypes
    print df.head()
    print df.describe()
    plot_graphics(df)


def plot_graphics(df):
    # df.sort(columns='timestamp')
    df.plot(x='timestamp', y='temperature')
    df.plot(x='timestamp', y='humidity')
    df.plot(x='timestamp', y='luminance')
    df.plot(x='timestamp', y='gas')
    plt.show()


if __name__ == '__main__':
    engine = create_engine(SQL_ENGINE)
    dataframe = load_data()
    visualize_data(dataframe)
