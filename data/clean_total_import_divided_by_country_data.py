import pandas as pd


def clean_import_data(input_file, fixed_file="TradeData_fixed.csv", output_file=None):
    """
    清理进口数据文件，计算各国进口权重并导出结果
    """
    
    with open(input_file, 'r', encoding='latin1') as fin, \
        open(fixed_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            line = line.rstrip('\r\n')
            if line.endswith(','):
                line = line[:-1]
            fout.write(line + '\n')
    
    try:
        df = pd.read_csv(
            fixed_file,
            encoding='utf-8-sig',
            engine='python'
        )
    except UnicodeDecodeError:
        df = pd.read_csv(
            fixed_file,
            encoding='latin1',
            engine='python'
        )
    
    if all(col in df.columns for col in ['partnerCode', 'partnerISO', 'cifvalue']):
        df = df[['partnerCode', 'partnerISO', 'cifvalue']]
        df.dropna(inplace=True)
        
        df['cifvalue'] = pd.to_numeric(df['cifvalue'], errors='coerce')
        
        world_row = df[df['partnerISO'] == 'W00']
        if world_row.empty:
            raise ValueError("未找到 partnerISO = 'W00' 的 World 行！")
        us_total_import = world_row['cifvalue'].iloc[0]
        
        
        country_rows = df[(df['partnerISO'] != 'W00') & (df['partnerCode'] != 0)].copy()
        country_rows = country_rows.dropna(subset=['cifvalue'])
        
        country_weights = {}
        for _, row in country_rows.iterrows():
            iso = row['partnerISO']
            weight = row['cifvalue'] / us_total_import
            country_weights[iso] = weight
        
        sorted_weights = sorted(country_weights.items(), key=lambda x: -x[1])
        
        weight_data = []
        for iso, w in sorted_weights:
            country_row = country_rows[country_rows['partnerISO'] == iso]
            partner_code = country_row['partnerCode'].iloc[0] if not country_row.empty else 'N/A'
            cif_value = country_row['cifvalue'].iloc[0] if not country_row.empty else 0
            
            weight_data.append({
                'partnerCode': partner_code,
                'partnerISO': iso,
                'weight': w
            })
        
        weight_df = pd.DataFrame(weight_data)
        
        if output_file:
            weight_df.to_csv(output_file, index=False, encoding='utf-8')
        
        return weight_df
    else:
        missing_cols = [col for col in ['partnerCode', 'partnerISO', 'cifvalue'] if col not in df.columns]
        raise ValueError(f"输入文件缺少必要的列: {', '.join(missing_cols)}")


if __name__ == "__main__":
    input_file = "./dataset/country/2025.csv"
    output_file = "./dataset/output_country/2025.csv"
    
    weight_df = clean_import_data(input_file, output_file=output_file)