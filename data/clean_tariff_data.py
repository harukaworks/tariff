import pandas as pd
import re

def clean_tariff_data(input_file, output_file=None, drop_columns=None,sep_sim=','):
    """
    清理关税数据库数据并导出为CSV文件
    """

    if drop_columns is None:
        drop_columns = ['brief_description', 'col1_special_text', 'mfn_text_rate', 'col2_text_rate']
    

    df = pd.read_csv(input_file, sep=sep_sim,engine='python',encoding='latin1')
    
    df.fillna(0, inplace=True)
    
    df = df.replace(to_replace=r'^Free.*$', value=0, regex=True)
    
    df.replace({'9999.999999': 0, 9999.999999: 0}, inplace=True)
    df.replace({'9999.99': 0, 9999.99: 0}, inplace=True)
    
    existing_columns = [col for col in drop_columns if col in df.columns]
    df.drop(columns=existing_columns, inplace=True)
    
    df = df.loc[:, (df != 0).any(axis=0)]
    
    df.columns = df.columns.str.strip()
    
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
    
    if output_file is not None:
        df.to_csv(output_file, index=False)
    
    return df


if __name__ == "__main__":
    input_file = './dataset/tariff/2025.txt'
    output_file = './dataset/output_tariff/2025.csv'
    
    clean_tariff_data(input_file, output_file)