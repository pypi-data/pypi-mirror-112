from datetime import date, datetime, timedelta
from os import listdir, path, getcwd
from pickle import load

from causalimpact import CausalImpact
import numpy as np
import pandas as pd
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from sklearn.neighbors import NearestNeighbors

import .constants as c


def get_comp_titles(input_isbn,start_date,nn_period,num_neighbours,snowflake_df):
    """
    This function returns a given number of most similarly-selling ISBNs to the ISBN passed in.
    
    Keyword args:
    - input_isbn: the ISBN input by the user that is receiving some promotional activity to evaluate. eBook or print.
    - start_date: the date this promotional activity began
    - nn_period: the sales period to assess to find the most similarly-selling ISBNs
    - num_neighbours: the number of ISBNs to return
    - snowflake_df: the dataframe from Snowflake containing all PRH sales, already opened and unpickled    
    """
    
    def clean_vectorise_df(snowflake_df,start_date,nn_period):
        """
        This function slices the Snowflake dataframe, normalises each ISBN's sales as per a normal distribution,
        and vectorises those sales.
        
        Keyword args:
        - snowflake_df: the dataframe from Snowflake containing all PRH sales, already opened and unpickled 
        - start_date: the date this promotional activity began
        - nn_period: the number of data before start_date to find the most similarly-selling ISBNs
        """        
        def get_min_date(start_date,nn_period):
            return start_date-timedelta(days=nn_period)
        
        def slice_snowflake_data(snowflake_df,min_date,start_date):
            return snowflake_df[(snowflake_df['date']>=min_date) &
                                (snowflake_df['date']<start_date)]
                    
        def clean_snowflake_data(snowflake_df):
            pt = pd.pivot_table(snowflake_df,
                                values='units',
                                index=['isbn'],
                                columns='date',
                                aggfunc=np.sum)
            return pd.DataFrame(pt.to_records())

        def fill_missing_data(snowflake_df,min_date,start_date):        
            date_range = pd.date_range(min_date,start_date,freq='D')
            column_list = [d.strftime("%Y-%m-%d") for d in date_range]
            column_list.append('isbn')       
            return snowflake_df.loc[:, snowflake_df.columns.isin(column_list)]

        def remove_zero_sales(snowflake_df):
            snowflake_df = snowflake_df.replace(np.nan,0)
            return snowflake_df.loc[~(df==0).all(axis=1)]

        def get_vec(row):
            #turns the row into a np array
            vec = row.values[1:]
            #transforms the array into a normal distribution
            vec = TimeSeriesScalerMeanVariance().fit_transform(vec.reshape(1, -1))
            return np.concatenate(vec).ravel()
        
        min_date = get_min_date(start_date,nn_period) 
        
        snowflake_df = slice_df(snowflake_df,min_date,start_date)
        snowflake_df = clean_snowflake_data(snowflake_df)
        snowflake_df = fill_missing_data(snowflake_df,min_date,start_date)
        snowflake_df = remove_zero_sales(snowflake_df)    
        snowflake_df['vec'] = snowflake_df.apply(get_vec, axis=1)
        
        return snowflake_df[['isbn','vec']]
    

    def get_k_neighbours(input_isbn,vectorised_df,num_neighbours):
        """
        This function takes the vectorised dataframe, turns it into a nearest neighbours class 'knn', 
        then uses kneighbors to return the n nearest neighbours to the passed ISBN - i.e. the most similarly-selling books.
        
        Keyword args:
        - input_isbn: the ISBN input by the user that is receiving some promotional activity to evaluate. eBook or print.
        - vectorised_df: the dataframe containing ISBNs and a vector of sales 
        - num_neighbours: the number of ISBNs to return
        """        
        
        def get_knn(vectorised_df):
            vector_arrays = vectorised_df['vec'].to_numpy().tolist()
            return NearestNeighbors().fit(vector_arrays)        

        def get_vector(vectorised_df,input_isbn):
            return vectorised_df.loc[vectorised_df['isbn']==input_isbn,'vec'].iloc[0].reshape(1, -1)

        def flatten_neighbour_list(nb_indexes):
            nb_list = nb_indexes.tolist()
            return [item for sublist in nb_list for item in sublist]        

        def id_to_isbn(nb_indexes,vectorised_df):
            return [vectorised_df.iloc[i,0] for i in nb_indexes]

        knn = get_knn(vectorised_df)
        vector = get_vector(vectorised_df,input_isbn)
        nb_indexes = knn.kneighbors(vector,num_neighbours,return_distance=False)
        nb_indexes = flatten_neighbour_list(nb_indexes)
        return id_to_isbn(nb_indexes,vectorised_df)

    vectorised_df = clean_vectorise_df(snowflake_df,start_date,nn_period)
    return get_k_neighbours(input_isbn,vectorised_df,num_neighbours)


def get_sales(input_isbn, start_date, end_date, pre_promo_length, post_promo_length, snowflake_df, comp_titles = None):

    """
    This function slices the snowflake_df to get the passed ISBN's sales during the promo period, pre_promo_length days'
    before and post_promo_length days' after. If comp_titles are passed in (as a list of ISBNs), those titles' sales will
    also be pulled. Otherwise, it checks the passed ISBN's format is checked and that format's overall market sales will 
    be pulled. The dataframes will then be merged and returned (so we have date, title sales, and comp sales.)
    
    Keyword args:
    - input_isbn: the ISBN input by the user that is receiving some promotional activity to evaluate. eBook or print.
    - start_date, end_date: the period in which that promotional activity took place.
    - pre_promo_length: the time period before the promotional activity to get sales for causal_impact to assess.
    - post_promo_length: the time period after the promotional activity to get sales for (due to a halo effect the promo-
    tional activity may still have an effect).
    - snowflake_df: the dataframe from Snowflake containing all PRH sales, already opened and unpickled
    - comp_titles: the list of comp titles' ISBNs: default None.
    
    """
        
    def resample_df(df):        
        df['date'] = pd.to_datetime(df['date'])
        df.set_index(df['date'],inplace=True)
        df = df.resample('D').sum().fillna(0)       
        return pd.DataFrame(df.to_records())

    def get_title_sales(input_isbn, min_date, max_date, snowflake_df):        
        snowflake_df = snowflake_df[(snowflake_df['date']>=min_date) &
                          (snowflake_df['date']<=max_date) &
                          (snowflake_df['isbn']==input_isbn)]        
        return snowflake_df[['date','units']]

    def get_comp_sales(comp_titles, min_date, max_date, snowflake_df):        
        snowflake_df = snowflake_df[(snowflake_df['date']>=min_date) &
                          (snowflake_df['date']<=max_date) &
                          (snowflake_df['isbn'].isin(comp_titles))]
        return snowflake_df.groupby(['date']).agg({'units':'sum'}).reset_index()

    def get_market_sales(input_format, min_date, max_date, snowflake_df):        
        snowflake_df = snowflake_df[(snowflake_df['date']>=min_date) &
                          (snowflake_df['date']<=max_date) &
                          (snowflake_df['format']==input_format)]
        return snowflake_df.groupby(['date']).agg({'units':'sum'}).reset_index()

    def get_input_isbn_format(input_isbn,dfsnowflake_df):        
        return snowflake_df.loc[snowflake_df['isbn']==input_isbn,'format'].values[0]   
    
    min_date = start_date
    max_date = end_date+timedelta(days=post_promo_length)
    
    title_df = get_title_sales(input_isbn, min_date, max_date, snowflake_df)

    if comp_titles: 
        comp_df = get_comp_sales(comp_titles, min_date, max_date, snowflake_df)
    else:
        isbn_format = get_input_isbn_format(input_isbn, snowflake_df)
        comp_df = get_market_sales(isbn_format, min_date, max_date, snowflake_df)
      
    title_df = resample_df(title_df)
    comp_df = resample_df(comp_df)
    
    sales_df = pd.merge(title_df, comp_df, on='date', how='outer')
    sales_df = sales_df.sort_values(by=['date']).reset_index(drop=True)
    sales_df.columns = ["date", "title_sales", "comp_sales"]    
    
    return sales_df


def get_predicted_sales(input_isbn, sales_df, start_date, end_date):  
    """
    This function returns a df of actual versus predicted sales for the passed ISBN, and a Boolean value for whether there
    was a causal effect of the promotion on sales.
    
    Keyword args:
    - input_isbn: the ISBN input by the user that is receiving some promotional activity to evaluate. eBook or print.
    - sales_df: the dataframe containing the sales of the passed ISBN and either comp titles' sales or the market's sales
    - start_date, end_date: the period in which that promotional activity took place.
    """
        
    def get_indexes(sales_df, start_date, end_date):
        min_index = int(sales_df.index[sales_df['date']==min(sales_df['date'])][0])
        start_index = int(sales_df.index[sales_df['date']==start_date][0])
        
        end_index = int(sales_df.index[sales_df['date']==end_date][0])
        max_index = int(sales_df.index[sales_df['date']==max(sales_df['date'])][0])

        pre_period = [min_index, start_index-1]
        post_period = [start_index, max_index]

        return pre_period, post_period

    def get_causal_impact_df(sales_df, pre_period, post_period):  
        df_pre_causal_impact = sales_df[['title_sales','comp_sales']]
        pre_period, post_period = get_indexes(df,start_date,end_date)

        ci = CausalImpact(df_pre_causal_impact, 
                          pre_period, post_period, 
                          alpha=0.8, prior_level_sd=0.1)

        if ci.inferences.post_cum_effects_lower.iloc[-1]<0:
            causation_check=True
        else: 
            causation_check=False
        return ci.inferences, causation_check

    def clean_causal_impact_df(sales_df,causal_impact_df):

        sales_df = sales_df[['date', 'title_sales']]
        df_actual_predicted = pd.merge(df, 
                                       causal_impact_df, 
                                       left_index=True, 
                                       right_index=True)
        df_actual_predicted = df_actual_predicted[['date','title_sales','preds']]
        df_actual_predicted.columns = ['date','title_sales','predicted_sales']
        df_actual_predicted['predicted_sales'] = round(df_actual_predicted['predicted_sales'],0).astype(int)
        return df_actual_predicted

    #if there were sales of the ISBN before the promo, run the Causal Impact algorithm
    if sales_df.loc[sales_df['date']<start_date,'title_sales'].sum()>0:     
        pre_period, post_period = get_indexes(sales_df,start_date,end_date)
        causal_impact_df, causation_check = get_causal_impact_df(sales_df,pre_period,post_period)
        df_actual_predicted = clean_causal_impact_df(sales_df,causal_impact_df)
    
    #otherwise default to predicted sales being 0, and any uplift being due to the promotional activity
    else:        
        df_actual_predicted = df[['date','title_sales']]
        df_actual_predicted['predicted_sales'] = 0
        causation_check = True
  
    return df_actual_predicted, causation_check


def get_actual_predicted(input_isbn, start_date, end_date, pre_promo_length, post_promo_length, nn_period, num_neighbours, market, snowflake_format):
    """
    This is a "wrapper" function which runs the above functions in order and returns the desired data.
    
    Keyword args:
    - input_isbn: the ISBN input by the user that is receiving some promotional activity to evaluate. eBook or print.
    - sales_df: the dataframe containing the sales of the passed ISBN and either comp titles' sales or the market's sales
    - start_date, end_date: the period in which that promotional activity took place.
    - pre_promo_length: the time period before the promotional activity to get sales for causal_impact to assess.
    - post_promo_length: the time period after the promotional activity to get sales for (due to a halo effect the promo-
    tional activity may still have an effect).
    - nn_period: the sales period to assess to find the most similarly-selling ISBNs
    - num_neighbours:
    - market: whether to use the ISBN's format's overall market instead of comp titles
    - snowflake_format: the format of the snowflake dataframe to use to open and unpickle it
    """    
    
    def open_snowflake_file(snowflake_format):       
        filepath = path.join(getcwd(), snowflake_format)       
        return load(open(filepath, "rb"))    

    snowflake_df = open_snowflake_file(snowflake_format)
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
        
    if market:        
        sales_df = get_sales(input_isbn,start_date,end_date,pre_promo_length,post_promo_length,snowflake_df)

    else:
        comp_titles = get_comp_titles(input_isbn,start_date,nn_period,num_neighbours,snowflake_df)
        sales_df = get_sales(input_isbn,start_date,end_date,pre_promo_length,post_promo_length,snowflake_df,comp_titles)  
              
    df_actual_predicted, causation_check = get_predicted_sales(input_isbn,sales_df,start_date,end_date)
    
    return comp_titles,df_actual_predicted,causation_check


def get_actual_predicted_special(input_isbn, start_date, end_date) -> Tuple[List, pd.DataFrame, bool]:
    return comp_titles, df_actual_predicted, causation_check = evaluate(
        input_isbn,
        start_date,
        end_date,
        c.pre_promo_length, 
        c.post_promo_length, 
        c.nn_period, 
        c.num_neighbours, 
        c.market, 
        c.SNOWFLAKE_FORMAT
    )