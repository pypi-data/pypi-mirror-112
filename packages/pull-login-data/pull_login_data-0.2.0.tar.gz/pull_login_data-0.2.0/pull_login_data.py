from time import time
from pandas.core.frame import DataFrame
from pymongo import collection
from pymongo.collection import Collection
import requests
from dataclasses import dataclass
import pandas as pd
import pymongo
import logging
import matplotlib.pyplot as plt
from datetime import date, timedelta

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def remove_cimar_users(user_list):
    clean_user_list = filter(lambda x: 'cimar' not in x['user_email'], user_list)
    return list(clean_user_list)

def format_login_logs(logs, account_id, account_name):
    """Formates the logs DataFrame to remove any proxy logins and 
    only required columns so that the data can be placed into the Database

    Args:
        logs (DataFrame): Original Audit Log DataFrame 

    Returns:
        DataFrame: Formatted audit log DataFrame
    """
    logging.info("Formatting Audit Logs")
    if len(logs) == 0:
        logging.info("User has never logged in")
        return False
    # Filter out and proxy logins then drop proxy column
    logs = logs.loc[(logs.proxy == '') | (logs.proxy.isnull())].copy()
    # Drop unwanted columns
    logs.drop(['detail', 'sid', 'type', 'what', 
               'who', 'action', 'proxy'], axis=1, inplace=True)
    # Add account uuid & name into DF
    logs['account_id'] = account_id
    logs['account_name'] = account_name
    get_date = lambda x: x[:10]
    logs['date'] = logs.when.apply(get_date)
    # Rearrange columns and ensure consistent format of dataframe
    df2=logs.reindex(columns= ['when', 'client_address', 'uuid', 'account_id', 'account_name', 'date'])
    return df2

def add_logs_to_db(logs, collection: Collection):
    """Adds the given DataFrame into the given Mongodb collection

    Args:
        logs (DataFrame): DataFrame data to be added to db
        collection (Collection): Collection to add data into
    """
    logging.info(f"Adding {len(logs)} records to {collection.name}")
    # Function to add to DB
    add_to_db = lambda row: collection.insert_one(row.to_dict())
    # Iterate through DF and add each row to DB
    logs.apply(add_to_db, axis=1)

def get_user_logs(client, user, account_id, account_name, page_rows=10, start_date=None, end_date=None):
    """Get and format the logs of user ready to be populated into the database

    Args:
        client (Client): Client object to inteface with Cimar
        user (dict): Dictionary containing info about user
        account_id (str): UUID of the account
        account_name (str): Name of the account

    Returns:
        DataFrame: Returns a list of the user's logins with columns required for database
    """
    if start_date is None:
        yesterday = date.today() - timedelta(days=1)
        start_date = yesterday.isoformat()

    if end_date is None:
        end_date = date.today().isoformat()

    if isinstance(user, dict):
        user_id = user['user_id']
    else:
        user_id = user

    raw_logs = client.get_user_audit_logs_2(account_id, user_id, only_login = True, start_date=start_date, end_date=end_date, page_rows=page_rows)
    logs: DataFrame = format_login_logs(pd.DataFrame(raw_logs), account_id, account_name)
    return logs  

def filter_account_list_of_inactive_accounts(account_list):
    inactive_list = ['66dace3f-dba6-4add-99cf-c719404256a3', '550c4b0f-0167-4924-8335-a8f060b14836', '4adce4ee-4d4b-4cb6-9a65-e800ba057504',
                     'aa454b2d-70e9-4f0e-97b9-c589bd7a4d3e', '4f19e747-2fb5-4c21-892c-61bb0ad0c632', '65755da3-c488-4582-a1f2-f93f682d936c',
                     '191a165f-e9c5-4393-b9cd-9170e175f980', '93653806-0fe9-4ef4-9402-c304820b1562', '369278a7-f6a9-4dd0-974c-c922c65b3f71', 
                     '035a442d-f005-4ef5-9f7a-e541875d7b73']

    return list(filter(lambda x: x['uuid'] not in inactive_list, account_list))
    

@dataclass
class Client ():
    """Basic Client class to make API calls

    Returns:
        [type]: [description]
    """
    email: str
    password: str
    sid: str = ""
    stack: str = "cloud"

    def __post_init__(self):
        self.sid = self.get_sid() if self.sid == "" else self.sid

    def get_sid(self):
        """Gets a new valid Session ID

        Returns:
            str: A valid Session ID (sid)
        """
        logging.info("Getting Session ID")
        r = requests.post(f"https://{self.stack}.cimar.co.uk/api/v3/session/login", data={"email": self.email, "password": self.password})
        return r.json()['sid']

    def get_account_list(self):
        """Gets the full list of accounts (account/get) that the user has access to

        Returns:
            list: list of accounts with the 'account/get' response
        """
        logging.info("Getting Account List")
        r = requests.get(f"https://{self.stack}.cimar.co.uk/api/v3/account/list", params={"sid": self.sid})
        if r.ok:
            return r.json()['accounts']
        else:
            raise Exception(r.text)

    def get_account(self, uuid: str):
        """Given an account uuid returns the details about an account (account/get)

        Args:
            uuid (str): uuid of the account

        Returns:
            dict: full account details
        """
        logging.info("Getting Account Data")
        r = requests.get(f"https://{self.stack}.cimar.co.uk/api/v3/account/get", params={"sid": self.sid, "uuid": uuid})
        return r.json()

    def get_account_user_list(self, uuid: str):
        """Get all the user's of the account uuid given

        Args:
            uuid (str): uuid of the account

        Returns:
            list: list of dicts about each user in the account
        """
        logging.info(f"Getting account ({uuid}) user list")
        r = requests.get(f"https://{self.stack}.cimar.co.uk/api/v3/account/user/list", params={"sid": self.sid, "uuid": uuid})
        return r.json()['users']

    def get_user_audit_logs(self, account_id: str, user_id: str, only_login = False, page_rows: int = 10):
        """Get the audit logs for a user. Can limit the logs to only be when they've logged into the system

        If you want to return their most recent log simply make the page_rows = 1

        Args:
            account_id (str): uuid of the account to check the users audit logs for
            user_id (str): uuid of the user
            only_login (bool, optional): limit the logs to only LOGIN audits. Defaults to False.
            page_rows (int, default = 10): How many records returned - max is 5000

        Returns:
            list: Up to most recent 1000 logs
        """
        logging.info(f"Getting user audit logs. User: {user_id}, Account: {account_id}")
        params = {
            "sid": self.sid, 
            "user_id": user_id,
            "account_id": account_id, 
            "filter.action.equals": "LOGIN", 
            "page.rows": page_rows
        }
        # Filter to only check login audits
        if only_login:
            params["filter.action.equals"] = "LOGIN"

        try:
            r = requests.get(f"https://{self.stack}.cimar.co.uk/api/v3/audit/user", params=params)
        except Exception as e:
            logging.critical(e)
        return r.json()['events']

    def get_user_audit_logs_2(self, account_id: str, user_id: str, only_login = False, page_rows: int = 10, start_date = None, end_date = None):
        """Get the audit logs for a user. Can limit the logs to only be when they've logged into the system

        If you want to return their most recent log simply make the page_rows = 1

        USES AUDIT/OBJECT rather than AUDIT/USER

        Will skew account reaults slightly

        Args:
            account_id (str): uuid of the account to check the users audit logs for
            user_id (str): uuid of the user
            only_login (bool, optional): limit the logs to only LOGIN audits. Defaults to False.
            page_rows (int, default = 10): How many records returned - max is 5000

        Returns:
            list: Up to most recent 1000 logs
        """
        logging.info(f"Getting user audit logs. User: {user_id}, Account: {account_id}")
        params = {
            "sid": self.sid, 
            "uuid": user_id,
            "page.rows": page_rows
        }
        if start_date is not None and end_date is not None:
            params['filter.when.ge'] = start_date
            params['filter.when.lt'] = end_date

        # Filter to only check login audits
        if only_login:
            params["filter.action.equals"] = "LOGIN"
        
        try:
            r = requests.get(f"https://{self.stack}.cimar.co.uk/api/v3/audit/object", params=params)
        except requests.exceptions.ConnectionError as ce:
            print(ce)
            return []
        
        if r.ok:
            try:
                return r.json()['events']
            except requests.exceptions.ConnectionError as ce:
                print(ce)
                return []
        else:
            try:
                return r.json()['events']
            except requests.exceptions.ConnectionError as ce:
                print(ce)
                return []
            except Exception as e:
                print(e)
                return []

        
    


if __name__ == "__main__":
    # FLOW

    # Create API Client
    # c = Client(api.email, api.password, stack="cloud")

    # Connect to Dev DB

    # client = pymongo.MongoClient(f"mongodb+srv://{db.dev_db_user}:{db.dev_db_password}@loginlogsdatabase.gu8wu.mongodb.net/LoginLogsDatabaseDev?retryWrites=true&w=majority")


    client = pymongo.MongoClient("mongodb+srv://zhooper:h^fC9zws^TtCfeXu@loginlogsdatabase.gu8wu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    # db = client.test

    
    # Will create db & collection if not already created
    db = client.LoginLogsDatabaseDev
    collection = db.LoginLogs

    pml_uuid = "ad6e8e97-fbe4-4df5-9609-8cc56271f203"
    user_id = "46bdd52c-ba3b-4374-814a-7e906daa5a6b"

    result = collection.aggregate([
        {
            '$addFields': {
                'clean_date': {
                    '$dateFromString': {
                        'dateString': '$date'
                    }
                }
            }
        }, 
        {
            '$group': {
                '_id': '$clean_date', 
                'date': {
                    '$first': '$clean_date'
                }, 
                'users': {
                    '$addToSet': '$uuid'
                }, 
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                '_id': -1
            }
        }
    ])

    results_df = pd.DataFrame(result)
    results_df.plot.bar(x="date", y="count")
    plt.savefig("test.png")

