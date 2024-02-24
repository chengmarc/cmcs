# -*- coding: utf-8 -*-
"""
@author: chengmarc
@github: https://github.com/chengmarc

"""
from cmcs_libraries import os, time, json
from cmcs_libraries import pandas as pd
from cmcs_libraries import map_info, map_headers, coin_info, coin_headers, get_datetime
from cmcs_libraries import ConnectionError, Timeout, TooManyRedirects
from cmcs_libraries import notice_start, notice_request_received, notice_timeout
from cmcs_libraries import notice_df_extracted, notice_all_df_extracted, notice_save_success


# %% Mapping API


def main1(session, path):
    notice_start('Extract ID Mapping')

    """API Request"""
    try:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
        parameters = {}
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        mapping = data['data']
        notice_request_received('/v1/cryptocurrency/map')

    except (ConnectionError, Timeout, TooManyRedirects):
        notice_timeout()


    """Extract dataframe"""
    df = []
    for coin in mapping:
        df.append(map_info(coin))
    df = pd.DataFrame(df)

    df.columns = map_headers(coin)
    notice_df_extracted()


    """Save dataframe"""
    output_path = path
    output_name = f"Mapping {get_datetime()}.csv"
    df.to_csv(os.path.join(output_path, output_name))
    notice_save_success()


# %% Listing API


def main2(session, path):
    notice_start('Extract All Listings')


    """API Request"""
    try:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        listing = []
        for i in [0, 1]:
            parameters = {'start': 1+i*5000, 'limit': 5000}
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            listing.extend(data['data'])
        notice_request_received('/v1/cryptocurrency/listings/latest')

    except (ConnectionError, Timeout, TooManyRedirects):
        notice_timeout()


    """Extract dataframe"""
    df = []
    for coin in listing:
        df.append(coin_info(coin))
    df = pd.DataFrame(df)

    df.columns = coin_headers(coin)
    notice_df_extracted()


    """Save dataframe"""
    output_path = path
    output_name = f"All Crypto {get_datetime()}.csv"
    df.to_csv(os.path.join(output_path, output_name))
    notice_save_success()


# %% Category API


def main3(session, path):
    notice_start('Extract All Categories')


    """API Request"""
    try:
        # get categories
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/categories'
        parameters = {}
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        categories = data['data']
        notice_request_received('/v1/cryptocurrency/categories')

        # create a category-data map
        data_map = []
        for category in categories:
            name = category['name']
            if 'Ecosystem' not in name and 'Portfolio' not in name:
                time.sleep(2.100)
                url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/category'
                parameters = {'id': category['id'], 'limit': 1000}
                response = session.get(url, params=parameters)
                data = json.loads(response.text)
                data_map.append((name, data))
                notice_request_received(name)

    except (ConnectionError, Timeout, TooManyRedirects):
        notice_timeout()


    """Extract dataframe"""
    dataframes = []
    for name, data in data_map:
        if 'coins' in data['data'].keys():
            listing = data['data']['coins']

            df = []
            for coin in listing:
                df.append(coin_info(coin))
            df = pd.DataFrame(df)    

            df.columns = coin_headers(coin)
            dataframes.append((name.replace("/", ""), df))
    notice_all_df_extracted()


    """Save dataframe"""   
    for name, df in dataframes:
        output_path = path
        output_name = f"{name} {get_datetime()}.csv"
        df.to_csv(os.path.join(output_path, output_name))
    notice_save_success()

