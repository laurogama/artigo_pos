__author__ = 'laurogama'
EXCHANGES = [{"name": 'logs', "type": 'fanout'}]
DATABASE_FILE = 'test.db'
SQLITE_TEST_DB = 'sqlite:///{}'.format(DATABASE_FILE)

MESSAGE_FIELDS = ['timestamp', 'id', 'humidity', 'ilumination', 'temperature',
                  'noise', 'carbon_monoxide']
