# -*- coding: utf-8 -*-
"""
@author: chengmarc
@github: https://github.com/chengmarc

"""
import os, sys, time, datetime, json, configparser, getpass, threading

try:
    import tkinter
    import pandas
    from requests import Request, Session
    from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
    print("SYSTEM: Core modules imported.")
    print("")

except ImportError as e:
    print(f"SYSTEM: The module '{e.name}' is not found, please install it using either pip or conda.")
    getpass.getpass("SYSTEM: Press Enter to quit in a few seconds...")
    sys.exit()


# %% Function overview
"""
The graph below is an overview of the call structure of the functions.
│
├───map_info()                      # convert a json object to a dataframe row
├───map_headers()                   # convert a json object to a dataframe header
├───coin_info()                     # convert a json object to a dataframe row
├───coin_headers()                  # convert a json object to a dataframe header
│
├───config_create()                 # detect config and create one if not exist
├───config_read_api()               # read from section [API Key] in config
├───config_read_check()             # read from section [Checks] in config
├───config_read_path()              # read from section [Paths] in config
├───config_save()                   # save to config
│
└───get_datetime()                  # get current datetime
"""


# %% Functions for converting json object


def map_info(coin: dict) -> list:
    """
    Given a json dictionary represent the mapping for a specific coin,
    This function will convert it to a list, which represents a row in a dataframe.
    """
    info = list(coin.values())[:-1]

    if list(coin.values())[-1] != None:
        platform = [list(coin.values())[-1]['name']]
    else:
        platform = []

    return info + platform


def map_headers(coin: dict) -> list:
    """
    Given a json dictionary represent the mapping for a specific coin,
    This function will convert it to a list, which represents the headers in a dataframe.
    """
    headers = list(coin.keys())
    headers.remove('platform')
    headers.append('platform')

    return headers


def coin_info(coin: dict) -> list:
    """
    Given a json dictionary represent the information for a specific coin,
    This function will convert it to a list, which represents a row in a dataframe.
    """
    info = []
    for key in coin.keys():
        if key != 'platform' and key != 'quote':
            info.append(coin[key])

    if coin['platform'] != None:
        platform = [coin['platform']['name']]
    else:
        platform = ['None']

    quote = list(coin['quote']['USD'].values())

    return info + platform + quote


def coin_headers(coin: dict) -> list:
    """
    Given a json dictionary represent the information for a specific coin,
    This function will convert it to a list, which represents the headers in a dataframe.
    """
    headers = list(coin.keys())
    headers.remove('quote')
    headers.remove('platform')
    headers.append('platform')
    headers.extend(coin['quote']['USD'].keys())

    return headers


# %% Functions for output path and output time


def config_create() -> None:
    """
    This function detects if the config file exist.
    If not, it will create the config file with default save locations.
    """
    config_file = r"C:\Users\Public\cmcs_config.ini"
    if not os.path.exists(config_file):
        content = ("[API Key]\n"
                   "api_key=Put your CoinMarketCap API key here\n"
                   "[Checks]\n"
                   "mapping=Not Accepted\n"
                   "listing=Accepted\n"
                   "category=Accepted\n"
                   "[Paths]\n"
                   r"output_path_mapping=C:\Users\Public\Documents" + "\n"
                   r"output_path_listing=C:\Users\Public\Documents" + "\n"
                   r"output_path_category=C:\Users\Public\Documents" + "\n")
        with open(config_file, "w") as f:
            f.write(content)
            f.close()


def config_read_api() -> str:
    """
    This function will return the api key recorded in the config file.

    Return:         a string that represents the api key
    """
    config_file = r"C:\Users\Public\cmcs_config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)
    config_api = config.get("API Key", 'api_key')
    return config_api


def config_read_check(selection: str) -> str:
    """
    Given a selection, this function will return the corresponding path.

    Return:         a string that represents either checked or not checked
    """
    config_file = r"C:\Users\Public\cmcs_config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)
    config_check = config.get("Checks", selection)
    return config_check


def config_read_path(selection: str) -> (str, bool):
    """
    Given a selection, this function will return the corresponding path.

    Return:         a tuple of str and boolean
                    the string represents the path
                    the boolean represents the validity of the path
    """
    config_file = r"C:\Users\Public\cmcs_config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)
    config_path = config.get("Paths", selection)

    if os.path.isdir(config_path):
        return config_path, True
    else:
        return config_path, False


def config_save(check1, check2, check3,
                path1, path2, path3, api_key) -> None:
    """
    Given three strings, this function will save the strings to the config file.
    """
    config_file = r"C:\Users\Public\cmcs_config.ini"
    content = ("[API Key]\n"
               f"api_key={api_key}\n"
               "[Checks]\n"
               f"mapping={check1}\n"
               f"listing={check2}\n"
               f"category={check3}\n"
               "[Paths]\n"
               f"output_path_mapping={path1}\n"
               f"output_path_listing={path2}\n"
               f"output_path_category={path3}\n")
    with open(config_file, "w") as f:
        f.write(content)
        f.close()


def get_datetime() -> str:
    """
    This function returns a string that represents the current datetime.

    Return:         a string of the format: %Y-%m-%d_%H-%M-%S
    """
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted_datetime


# %% Functions for user notice


def notice_start(name: str) -> None:
    length = len(name) + 6*2
    print("")
    print(length*"#")
    print(f"##### {name} #####")
    print(length*"#")
    print("")


def notice_request_received(name: str) -> None:
    print(f'Request recieved for {name}')


def notice_df_extracted() -> None:
    print('Dataframe extracted')


def notice_all_df_extracted() -> None:
    print('Dataframe extracted for all categories')


def notice_save_success() -> None:
    print("Successfully loaded output config.")
    print("Data has been saved to the desired location.")
    print("")


def notice_timeout() -> None:
    print("")
    print("Request timeout, please try again")
    sys.exit()

