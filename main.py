from data.map_tariff_with_countries import mapping 
from data.output_avg_tariff import compute_weighted_average_tariff as comp
from data.clean_total_import_divided_by_country_data import clean_import_data as cc
from data.clean_tariff_data import clean_tariff_data as ct

import pandas as pd

if __name__ == "__main__":
    year=2025
    tariff_file = f"./dataset/tariff/{year}.txt"
    #country_file = f"./dataset/country/{year}.csv"
    output_file = f"./dataset/total_output/{year}.csv"
    df_t = ct(tariff_file,output_file=f'./dataset/output_tariff/{year}.csv')
    df_c = pd.read_csv('./dataset/2025.csv')
    df_m = pd.read_csv(f'./dataset/output_country/{year}.csv')#mapping(df_t,output_file=f'./dataset/output_country/{year}.csv')
    comp(df_c, df_m,output_file=output_file)
