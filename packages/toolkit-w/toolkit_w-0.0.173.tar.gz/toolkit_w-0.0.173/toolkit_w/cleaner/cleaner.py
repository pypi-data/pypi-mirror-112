import pandas as pd
import numpy as np
import json


class Cleaner:
    """ Module that helps to clean and arrange raw data"""

    def getCleanData(self, df: pd.DataFrame):
        """
        Params:
            df-> Dataframe
        -----------------------
        Output:
            Clean dataframe after filtering
            log_file - Description of actions taken
        """
        log_file = []
        # Clean cancelled orders
        df['cancelledat'] = df['cancelledat'].fillna('Valid')
        df_1 = df[(df.cancelledat == 'Valid')]
        # Record canceled orders
        canceled_orders_num = (len(df) - len(df_1))

        # Clean free orders
        free = df[(df.totaldiscounts == df.totalorderitemsprice) | (df.totalprice == 0)]
        free_orders_num = len(free)

        df_2 = df_1[~(df_1.id.isin(free['id'].values))]
        print(len(df_1), len(df_2))
        # Missing customer data

        missing_customers = len(df_1[(df_1['customerid'].isnull())])

        df_3 = df_2[~(df_2['customerid'].isnull())]
        print(len(df_2), len(df_3))
        log_file.append([canceled_orders_num, free_orders_num, missing_customers])

        # log file for documentation
        log_file = pd.DataFrame(log_file, columns=['Number_of_canceled_Orders', 'Number_of_free_orders',
                                                   'Number_of_missing_customers_info'])
        return df_3, log_file

    def getshippingprice(self, df):
        """

        """
        df['shipping_price'] = df['shippingaggregate'].apply(lambda x: Cleaner().getshippingpricevalue(x))

        return df

    def getshippingpricevalue(self, x):
        if len(x) > 1:
            try:
                value = json.loads(x)
            except:
                shipping_price = 'error'
            try:
                shipping_price = value[0]['discounted_price']
                shipping_price = pd.to_numeric(shipping_price)
            except:
                shipping_price = 'error'
        else:
            shipping_price = 0

        return shipping_price
