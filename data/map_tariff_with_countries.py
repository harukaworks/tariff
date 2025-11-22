import pandas as pd


GSP_BENEFICIARY_COUNTRIES = {
    'AF', 'AL', 'AO', 'AM', 'AZ', 'BD', 'BY', 'BJ', 'BT', 'BO',
    'BA', 'BW', 'BF', 'BI', 'CV', 'KH', 'CM', 'CF', 'TD', 'KM',
    'CD', 'CG', 'CI', 'DJ', 'DM', 'EC', 'EG', 'SV', 'GQ', 'ER',
    'ET', 'FJ', 'GA', 'GM', 'GE', 'GH', 'GD', 'GT', 'GN', 'GW',
    'GY', 'HT', 'HN', 'IN', 'ID', 'JO', 'KZ', 'KE', 'KI', 'KG',
    'LA', 'LB', 'LS', 'LR', 'LY', 'MG', 'MW', 'MY', 'MV', 'ML',
    'MH', 'MR', 'MU', 'MX', 'FM', 'MN', 'ME', 'MA', 'MZ', 'MM',
    'NA', 'NP', 'NI', 'NE', 'NG', 'MK', 'PW', 'PA', 'PG', 'PY',
    'PE', 'PH', 'RW', 'WS', 'SN', 'RS', 'SL', 'SB', 'SO', 'ZA',
    'SS', 'LK', 'LC', 'VC', 'SD', 'SR', 'SZ', 'TJ', 'TZ', 'TH',
    'TL', 'TG', 'TO', 'TT', 'TN', 'TM', 'UG', 'UA', 'UZ', 'VU',
    'VE', 'VN', 'ZM', 'ZW'
}

GSP_LDC_COUNTRIES = {
    'AF', 'AO', 'BD', 'BF', 'BI', 'BT', 'CD', 'CF', 'CG', 'CI',
    'DJ', 'ER', 'ET', 'GA', 'GM', 'GN', 'GW', 'HT', 'KM', 'KG',
    'LA', 'LR', 'LS', 'MG', 'MH', 'ML', 'MM', 'MR', 'MW', 'MZ',
    'NE', 'NG', 'RW', 'SB', 'SL', 'SO', 'SS', 'ST', 'TD', 'TG',
    'TJ', 'TL', 'UG', 'VU', 'YE', 'ZM', 'ZW'
} & GSP_BENEFICIARY_COUNTRIES

FTA_COUNTRY_MAP = {
    'nafta_canada_ind': ['CA'],
    'nafta_mexico_ind': ['MX'],
    'apta_indicator': ['CA'],
    'israel_fta_indicator': ['IL'],
    'jordan_indicator': ['JO'],
    'singapore_indicator': ['SG'],
    'chile_indicator': ['CL'],
    'morocco_indicator': ['MA'],
    'australia_indicator': ['AU'],
    'bahrain_indicator': ['BH'],
    'dr_cafta_indicator': ['CR', 'DO', 'GT', 'HN', 'NI', 'SV'],
    'oman_indicator': ['OM'],
    'peru_indicator': ['PE'],
    'korea_indicator': ['KR'],
    'colombia_indicator': ['CO'],
    'panama_indicator': ['PA'],
}

ALL_FTA_COUNTRIES = set(c for countries in FTA_COUNTRY_MAP.values() for c in countries)


COMMON_NON_PREFERENTIAL = {'CN', 'RU', 'TW', 'BR', 'SA', 'AE', 'TR', 'ZA', 'CH', 'NO', 'PL', 'RO', 'HU', 'TH'}

ALL_COUNTRIES = sorted(
    GSP_BENEFICIARY_COUNTRIES |
    ALL_FTA_COUNTRIES |
    {'CU', 'KP'} |
    COMMON_NON_PREFERENTIAL
)


FTA_RATE_FIELDS = {
    'nafta_mexico_ind': ('mexico_ad_val_rate', 'mexico_specific_rate'),
    'jordan_indicator': ('jordan_ad_val_rate', 'jordan_specific_rate'),
    'singapore_indicator': ('singapore_ad_val_rate', 'singapore_specific_rate'),
    'chile_indicator': ('chile_ad_val_rate', 'chile_specific_rate'),
    'morocco_indicator': ('morocco_ad_val_rate', 'morocco_specific_rate'),
    'australia_indicator': ('australia_ad_val_rate', 'australia_specific_rate'),
    'bahrain_indicator': ('bahrain_ad_val_rate', 'bahrain_specific_rate'),
    'dr_cafta_indicator': ('dr_cafta_ad_val_rate', 'dr_cafta_specific_rate'),
    'oman_indicator': ('oman_ad_val_rate', 'oman_specific_rate'),
    'peru_indicator': ('peru_ad_val_rate', 'peru_specific_rate'),
    'korea_indicator': ('korea_ad_val_rate', 'korea_specific_rate'),
    'colombia_indicator': ('colombia_ad_val_rate', 'colombia_specific_rate'),
    'panama_indicator': ('panama_ad_val_rate', 'panama_specific_rate'),
}

def parse_excluded(excluded_str):
    if pd.isna(excluded_str) or excluded_str == '':
        return set()
    parts = str(excluded_str).replace(';', ',').replace(' ', ',').split(',')
    codes = {code.strip().upper() for code in parts if len(code.strip()) == 2}
    return codes

def get_gsp_countries(gsp_ind, gsp_excl):
    if pd.isna(gsp_ind) or gsp_ind == '':
        return set()
    gsp_ind = str(gsp_ind).strip()
    if gsp_ind == 'A':
        return GSP_BENEFICIARY_COUNTRIES
    elif gsp_ind == 'A+':
        return GSP_LDC_COUNTRIES
    elif gsp_ind == 'A*':
        excluded = parse_excluded(gsp_excl)
        return GSP_BENEFICIARY_COUNTRIES - excluded
    else:
        return set()

def process_row(row):
    hts8 = row['hts8']
    if pd.isna(hts8):
        return None
    mfn_ad = float(row.get('mfn_ad_val_rate', 0) or 0)
    mfn_spec = float(row.get('mfn_specific_rate', 0) or 0)
    result = {}
    for country in ALL_COUNTRIES:
        result[f"{country}_ad_val"] = mfn_ad
        result[f"{country}_specific"] = mfn_spec
    col2_ad = float(row.get('col2_ad_val_rate', 0) or 0)
    col2_spec = float(row.get('col2_specific_rate', 0) or 0)
    if col2_ad > 0 or col2_spec > 0:
        result['CU_ad_val'] = col2_ad
        result['CU_specific'] = col2_spec
        result['KP_ad_val'] = col2_ad
        result['KP_specific'] = col2_spec
    for ind_field, countries in FTA_COUNTRY_MAP.items():
        if row.get(ind_field) and str(row[ind_field]).strip() not in ('', '0', 'False', 'N', 'No'):
            ad_f, spec_f = FTA_RATE_FIELDS.get(ind_field, (None, None))
            ad_val = float(row.get(ad_f, 0) or 0) if ad_f else 0.0
            spec_val = float(row.get(spec_f, 0) or 0) if spec_f else 0.0
            for c in countries:
                if c in ALL_COUNTRIES:
                    result[f"{c}_ad_val"] = ad_val
                    result[f"{c}_specific"] = spec_val
    gsp_ind = row.get('gsp_indicator')
    gsp_excl = row.get('gsp_ctry_excluded')
    gsp_countries = get_gsp_countries(gsp_ind, gsp_excl)
    for c in gsp_countries:
        if c in ALL_COUNTRIES:
            result[f"{c}_ad_val"] = 0.0
            result[f"{c}_specific"] = 0.0
    result['hts8'] = hts8
    return result

def mapping(df=None, input_file=None, output_file=None):
    if df is None:
        df = pd.read_csv(input_file, dtype=str, na_filter=False)
    records = []
    for _, row in df.iterrows():
        out_row = process_row(row)
        if out_row is not None:
            records.append(out_row)
    output_df = pd.DataFrame(records)
    cols = ['hts8'] + [col for col in output_df.columns if col != 'hts8']
    output_df = output_df[cols]
    if output_file:
        output_df.to_csv(output_file, index=False, float_format='%.6f')
    return output_df

if __name__ == "__main__":
    input_csv = "dataset/tariff/tariff_database_2015.csv"
    output_csv = "hts_rates_by_country_pandas.csv"
    mapping(None, input_csv, output_csv)