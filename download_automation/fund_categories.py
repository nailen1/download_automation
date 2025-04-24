from financial_dataset_preprocessor import *
import pandas as pd

FUND_CATEGORIES = ['-', '운용펀드', '일반', '클래스펀드']

def get_df_category():
    data = get_mapping_fund_class()
    df_category = pd.DataFrame(data=[{'fund_code': k, 'class': v} for k, v in data.items()])
    return df_category

def get_dfs_category_of_funds():
    df_category = get_df_category()
    dfs = dict(tuple(df_category.groupby('class')))
    return dfs

def get_df_by_category(category):
    dfs = get_dfs_category_of_funds()
    if category in dfs.keys():
        df = dfs[category]
    else:
        raise ValueError(f"Category '{category}' not found in the available categories.")
    return df

def get_fund_codes_mothers():
    df = get_df_by_category('운용펀드')
    fund_codes = df['fund_code'].tolist()
    return fund_codes

def get_fund_codes_classes():
    df = get_df_by_category('클래스펀드')
    fund_codes = df['fund_code'].tolist()
    return fund_codes

def get_fund_codes_general():
    df = get_df_by_category('일반')
    fund_codes = df['fund_code'].tolist()
    return fund_codes

def get_fund_codes_nonclassified():
    df = get_df_by_category('-')
    fund_codes = df['fund_code'].tolist()
    return fund_codes
