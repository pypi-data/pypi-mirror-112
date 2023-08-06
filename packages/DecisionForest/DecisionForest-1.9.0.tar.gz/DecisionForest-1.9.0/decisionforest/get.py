import http.client
import pandas as pd
from .config import Config


def get(dataset, **kwargs):
    """
    Return DataFrame of requested DecisionForest dataset.
    Args:
        dataset (str): Dataset codes are available on DecisionForest.com, example: dataset='SMD'
        ** date (str): Date, example: date='2018-12-28'
        ** start, end (str): Date filters, example: start='2018-12-28', end='2018-12-30'
        ** symbol (str): Symbol codes are available on DecisionForest.com on the product page , example: symbol='AAPL'
    """

    conn = http.client.HTTPSConnection(Config.DOMAIN)
    u = f"/api/{dataset}/?key={Config.KEY}"

    for key, value in kwargs.items():
        u = f'{u}&{key}={value}'

    conn.request("GET", u)
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = eval(data)

    if dataset == 'DFCF':
        d = {}
        for i in range(len(data)):
            d[i] = {}
            d[i]['date'] = data[i]['date']
            d[i]['symbol'] = data[i]['symbol']
            d[i]['intrinsic_value_per_share'] = float(
                data[i]['intrinsic_value_per_share'])

        df = pd.DataFrame.from_dict(d, orient='index')
        df = df.sort_values(by=['date'])
        df.reset_index(drop=True, inplace=True)

    elif dataset == 'DFIV':
        d = {}
        for i in range(len(data)):
            d[i] = {}
            d[i]['date'] = data[i]['date']
            d[i]['symbol'] = data[i]['symbol']
            d[i]['intrinsic_value_per_share'] = float(
                data[i]['intrinsic_value_per_share'])

        df = pd.DataFrame.from_dict(d, orient='index')
        df = df.sort_values(by=['date'])
        df.reset_index(drop=True, inplace=True)

    elif dataset == 'STAT':
        d = {}
        for i in range(len(data)):
            d[i] = {}
            d[i]['date'] = data[i]['date']
            d[i]['symbol'] = data[i]['symbol']
            d[i]['adf_stat'] = float(data[i]['adf_stat'])
            d[i]['adf_pvalue'] = float(data[i]['adf_pvalue'])
            d[i]['adf_cv'] = float(data[i]['adf_cv'])
            d[i]['adf_corr'] = float(data[i]['adf_corr'])
            d[i]['h'] = float(data[i]['h'])
            d[i]['c'] = float(data[i]['c'])
            d[i]['var_stat'] = float(data[i]['var_stat'])
            d[i]['var_pvalue'] = float(data[i]['var_pvalue'])
            d[i]['var_corr'] = float(data[i]['var_corr'])
            d[i]['coef'] = float(data[i]['coef'])
            d[i]['half'] = float(data[i]['half'])       

        df = pd.DataFrame.from_dict(d, orient='index')
        df = df.sort_values(by=['date'])
        df.reset_index(drop=True, inplace=True)

    else:
        df = pd.DataFrame()

    return df
