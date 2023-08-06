import pandas as pd
import numpy as np
import getpass
from functools import reduce

# set the sf account name
sf_account = 'ra45066.eu-west-1'
from toolkit_w.snowflake.snowflakeq import Snowflakeq

SQ = Snowflakeq()


# pwd = getpass.getpass("passsword:")

class Crp:
    """

     CHURN USECASE MODULE

    """

    def getTrainingframe(self, df: pd.DataFrame, dateFlag_sep, date_flag_min):
        """
        Params:
            df                -> Dataframe
            dateFlag_sep      -> Timestamp separator
            date_flag_min     -> Min date for training frame
        ---------------------
        Output:

        """
        #     dateFlag_sep = np.max(df['order_date']) - pd.DateOffset(months=timeFlag)
        #     date_flag_min = dateFlag_sep - pd.DateOffset(months=train_window)

        df = df[(df.order_date < dateFlag_sep) & (df.order_date >= date_flag_min)]

        return df

    def getTargetframe(self, df: pd.DataFrame, dateFlag_sep, lag: int):
        """
        Params:
            df           -> dataframe
            dateFlag_sep ->
            lag          ->
        --------------------
        Output:


        """
        #     dateFlag_sep = np.max(df['order_date']) - pd.DateOffset(months=timeFlag)
        date_max = dateFlag_sep + pd.DateOffset(days=lag)
        df = df[(df.order_date >= dateFlag_sep) & (df.order_date < date_max)]

        return df

    def getTargetValues(self, train_data: pd.DataFrame, target_data: pd.DataFrame):

        """
        Params:
            train_data  -> Dataframe of the training frame
            target_data -> Dataframe on which we base the target value
        --------------------
        Output:

        """

        target = []
        customers_id = train_data['customerid'].unique()
        for c_id in customers_id:
            if c_id in target_data['customerid'].unique():
                value = 1
            else:
                value = 0
            target.append([c_id, value])

        target = pd.DataFrame(target, columns=['customerid', 'is_returned'])

        # Output

        return target

    def getRecency(self, matrix: pd.DataFrame, dateFlag):
        """
        Params:

            matrix ->      data matrix
            dateFlag    -> The date flag separator
        ---------------------
        Output:- entire modified dataframe with the recency feature

        """

        matrix['Recency'] = matrix.apply(lambda x: dateFlag - pd.to_datetime(x.order_date), axis=1).dt.days

        # Output
        return matrix

    def getLastOrderparams(self, matrix: pd.DataFrame, train_df: pd.DataFrame, dateFlag_sep, date_flag_min,
                           customer_name, sq_pass):
        """
        Params:
            matrix      ->
            train_df    ->
        --------------------
        Output:
            output = matrix with last order value
        """

        # Type modification for query execution
        dateFlag_sep = str(dateFlag_sep.date())
        date_flag_min = str(date_flag_min.date())

        # Map the relevant values according to the primary key
        target = train_df[train_df.customerid.map(matrix['createdat']) == train_df.createdat][['customerid',
                                                                                               'totalprice',
                                                                                               'totaldiscounts',
                                                                                               'totalweight']]
        matrix = matrix.reset_index()

        # Get the order item data
        item_order = SQ.get_data_from_sf("V_ORDERS_ITEMS_VIEW", customer_name, sq_pass, dateFlag_sep, date_flag_min)

        item_order.columns = item_order.columns.str.lower()

        rel_ord = item_order[item_order.customer_id.isin(matrix['customerid'].unique())].sort_values(by='order_id')

        rel_ord = rel_ord[~(rel_ord.product_type == '')]

        dum_df = pd.get_dummies(rel_ord, columns=["product_type"], prefix=["Type_is"])

        filter_col = [col for col in dum_df if col.startswith('Type_is')]

        dum_df = dum_df.groupby('order_id')[filter_col].sum().reset_index()

        dum_df = pd.merge(rel_ord[['order_id', 'created_at', 'customer_id']], dum_df, on='order_id').drop_duplicates()

        dum_df = dum_df.rename(columns={'customer_id': 'customerid', 'created_at': 'createdat'})

        df = dum_df[dum_df.set_index(['customerid', 'createdat']).index.isin(
            matrix.set_index(['customerid', 'createdat']).index)].drop_duplicates()

        matrix = pd.merge(df, matrix, on=['customerid', 'createdat'])

        output = pd.merge(matrix, target, on='customerid', how='left')

        output = output.rename(columns={'totalprice': 'LastOrderValue', 'totaldiscounts': 'LastOrderDiscount',
                                        'totalweight': 'LastOrderWeight'})

        # Output
        return output

    def getTotalSpentLMonth(self, train_df, dateFlag_sep, df_matrix, lastTimeflagParam):
        """
        Params:
            lastTimeflagParam - > int

        -----------------
        Output:

        """

        total_spent_last_month_sep = dateFlag_sep - pd.DateOffset(days=lastTimeflagParam)

        last_month_df = train_df[
            (train_df.order_date >= total_spent_last_month_sep - pd.DateOffset(days=lastTimeflagParam)) & (
                    train_df.order_date <= total_spent_last_month_sep)]

        last_month_spent = last_month_df.groupby('customerid').agg({'totalprice':
                                                                        'sum'}).reset_index().rename(
            columns={'totalprice': 'LatestTotalSPent'})

        df_matrix = df_matrix.reset_index()

        df_matrix = pd.merge(df_matrix, last_month_spent, on='customerid', how='left')

        df_matrix = df_matrix.fillna(0)

        # df_matrix = df_matrix.rename(columns = {'totalprice':'Last_Month_Total_Spent'})

        return df_matrix

    def getFeaturesMatrix(self, train_df, df, timeFlag, items_dataset, customer_name, train_window, sq_pass,
                          lastTimeflagParam):
        """
        Params:
            train_df -> train timeframe dataframe
            org_df   -> original dataframe with the all the needed data
            timeFlag -> date separator (between the traget period and the train period)
        ----------------
        Output: Features Matrix of the chosen timeframe
        """

        # Get customer ids
        customers = train_df['customerid'].unique()
        # Get the date which acts as reference point for future calculations
        dateFlag_sep = np.max(df['order_date']) - pd.DateOffset(days=timeFlag)
        # The date which is the min date for the feature matrix
        date_flag_min = dateFlag_sep - pd.DateOffset(days=train_window)
        # Create a grouping aggregator
        grp = train_df.groupby('customerid')

        grp_dict = {'createdat': 'max', 'id': 'count', 'totalprice': 'sum'}

        df_matrix = grp.agg(grp_dict).rename(columns={'id': 'num_orders', 'totalprice': 'TotalSpent'})
        # Create only date column
        df_matrix['order_date'] = df_matrix['createdat'].dt.date

        # Recency Feature
        df_matrix = self.getRecency(df_matrix, dateFlag_sep)
        # Different Last orders parameters feature ( Discount value, weight )
        df_matrix = self.getLastOrderparams(df_matrix, train_df, dateFlag_sep, date_flag_min, customer_name, sq_pass)
        df_matrix = self.getTotalSpentLMonth(train_df, dateFlag_sep, df_matrix, lastTimeflagParam)

        # Turn the separators into strings for the snowflake query
        dateFlag_sep = str(dateFlag_sep)
        date_flag_min = str(date_flag_min)
        orders_param = SQ.get_data_from_sf('V_DIFFDAYSBETWEENPURCHASESAGG', customer_name, sq_pass, dateFlag_sep,
                                           date_flag_min)

        orders_param.columns = orders_param.columns.str.lower()

        output = pd.merge(df_matrix, orders_param, how='left', on='customerid')
        output = output.fillna(999)

        return output

    def getMergedDF(self, data_list, key):
        """
        Params:
            data_list -> list that contains all dataframes
            key - string, the mutual key for the merge.
        ---------------
        Output: Merged dataset


        """
        output = reduce(lambda left, right: pd.merge(left, right, on=[key],
                                                     how='outer'), data_list)

        return output

    def prepareDF(self, df, dateFlag_sep, date_flag_min, lag, items_dataset, customer_name, train_window, sq_pass,
                  lastTimeflagParam):
        """
        Params:
            original_dataset ->
            timeFlag         ->
            train_window     ->
        -------------------------------
        Output:

        """

        # Get the first matrices
        train_data = self.getTrainingframe(df, dateFlag_sep, date_flag_min)

        # For the target values calculations first -> get the relevant dataframe with the relevant timeframe
        target_frame = self.getTargetframe(df, dateFlag_sep, lag)

        # Calculate the target value
        target_value = self.getTargetValues(train_data, target_frame)

        # Calculate features
        df = self.getFeaturesMatrix(train_data, df, lag, items_dataset, customer_name, train_window, sq_pass,
                                    lastTimeflagParam)

        # Merge feature sets
        # data = self.getMergedDF(df,'customerid')
        # Merge with target value

        finalDF = pd.merge(df, target_value, on='customerid')

        # finalDf = finalDF.rename(columns = {'num_orders':'Num_orders','totalprice':'Total_spent'})

        output = finalDF

        return output

    def buildDF(self, lag, train_window, customer_name, sq_pass, items_dataset, lastTimeflagParam, max_date, min_date):
        """
        Params:
            original_dataset  - > the original raw data
            lag               - > size ( in months) of the targetValue window
            train_window      - > size of the feature matrix
            lastTimeflagParam - > size of the timeframe for latest params
        Output: Constructed dataframe

        """

        original_dataset = SQ.get_data_from_sf('v_get_clean_data', customer_name, sq_pass, max_date, min_date)
        original_dataset.columns = original_dataset.columns.str.lower()
        original_dataset['createdat'] = pd.to_datetime(original_dataset['createdat'])
        original_dataset['order_date'] = original_dataset['createdat'].dt.date
        original_dataset['order_date'] = pd.to_datetime(original_dataset['order_date'])

        # Lower limit date
        min_date = np.min(original_dataset['order_date']) + pd.DateOffset(days=train_window)
        #         print('Min date for training timeframe:',min_date)
        output = []
        # Upper limit date
        date_max = np.max(original_dataset['order_date'])
        # Initial relative timeFlag
        dateFlag_sep = date_max - pd.DateOffset(days=lag)
        # Initial timeframe min date
        date_flag_min = dateFlag_sep - pd.DateOffset(days=train_window)
        print(dateFlag_sep, date_flag_min)

        # First, perform initial cleaning and save a log file of action

        # Construct dataframe according to that timeframe
        output.append(
            self.prepareDF(original_dataset, dateFlag_sep, date_flag_min, lag, items_dataset, customer_name,
                           train_window, sq_pass,
                           lastTimeflagParam))
        #         print(dateFlag_sep,date_flag_min)
        # Repeat the procedure until the bottom limit of the trainFrame reaches the minimum date possible according to the original dataset.
        while date_flag_min >= min_date:
            dateFlag_sep = dateFlag_sep - pd.DateOffset(days=lag)
            date_flag_min = dateFlag_sep - pd.DateOffset(days=train_window)
            print(dateFlag_sep, date_flag_min)
            output.append(
                self.prepareDF(original_dataset, dateFlag_sep, date_flag_min, lag, items_dataset, customer_name,
                               train_window, sq_pass, lastTimeflagParam))

        output_final = pd.concat(output)

        output_final = output_final.drop(['index', 'order_id', 'createdat', 'min_days_between_purchases',
                                          'max_days_between_purchases', 'std_days_between_purchases'], axis=1)

        return output_final