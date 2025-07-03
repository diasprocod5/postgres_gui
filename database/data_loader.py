from database import Database
class DataLoader:
    def __init__(self):
        self.db = Database()
        self.users = [] # users without related account | client_id, full_name, phone
        self.accounts = [] # | account_id, full_name, phone
        self.tariffs = [] # | tariff_id, tariff_name, tariff_type

    def load_all(self):
        self.load_users()
        self.load_accounts()
        self.load_tariffs()

    def load_users(self):
        self.users = self.db.execute_query('SELECT * FROM get_users_without_account()')[0]

    def load_accounts(self):
        self.accounts = self.db.execute_query('SELECT * FROM get_accounts()')[0]

    def load_tariffs(self):
        self.tariffs = self.db.execute_query('SELECT * FROM get_tariffs()')[0]



if __name__=='__main__':
    db = Database()
    db.connect('postgres',79230)
    dl = DataLoader()
    dl.load_all()
    print(dl.tariffs)
    print(dl.accounts)
    print(dl.users)