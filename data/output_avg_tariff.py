import pandas as pd
import pycountry


def build_iso3_to_iso2():
    """
    构建ISO3到ISO2的国家代码映射
    
    返回:
    dict: ISO3代码到ISO2代码的映射字典
    """
    mapping = {}
    for country in pycountry.countries:
        if hasattr(country, 'alpha_3') and hasattr(country, 'alpha_2'):
            mapping[country.alpha_3] = country.alpha_2
    mapping.update({
        'S19': 'S19',
        'W00': 'W00',
        'Z00': 'Z00',
        'VNM': 'VN',
        'KOR': 'KR',
        'RUS': 'RU',
        'TWN': 'TW',
        'HKG': 'HK',
        'MAC': 'MO',
    })
    return mapping


def compute_weighted_tariff(row, iso2_in_tariff, iso2_to_weight):
    """
    计算单行的加权平均关税
    """
    total = 0.0
    for iso2 in iso2_in_tariff:
        tariff = row.get(f"{iso2}_ad_val", 0.0)
        if pd.isna(tariff):
            tariff = 0.0
        weight = iso2_to_weight.get(iso2, 0.0)  # 若无对应权重，视为0
        total += tariff * weight
    return total


def compute_weighted_average_tariff(weights_df=None, tariff_df=None, weights_file=None, tariff_file=None, output_file=None):
    """
    计算加权平均关税并保存结果
    """
    if weights_df is None or tariff_df is None:
        if weights_file is None or tariff_file is None:
            raise ValueError("Either weights_df and tariff_df must be provided, or weights_file and tariff_file must be specified.")
        weights_df = pd.read_csv(weights_file)
        tariff_df = pd.read_csv(tariff_file)

    iso3_to_iso2 = build_iso3_to_iso2()
    weights_df['iso2'] = weights_df['partnerISO'].map(iso3_to_iso2).fillna(weights_df['partnerISO'])
    iso2_to_weight = dict(zip(weights_df['iso2'], weights_df['weight']))
    ad_val_cols = [col for col in tariff_df.columns if col.endswith('_ad_val')]
    iso2_in_tariff = [col.replace('_ad_val', '') for col in ad_val_cols]
    tariff_df['weighted_avg_tariff'] = tariff_df.apply(
        lambda row: compute_weighted_tariff(row, iso2_in_tariff, iso2_to_weight), 
        axis=1
    )
    sel=['hts8','weighted_avg_tariff']
    output_df = tariff_df[sel].copy()
    output_df.sort_values(by='hts8',inplace=True)
    if output_file:
        output_df.to_csv(output_file, index=False, float_format="%.8f")   
    return output_df


if __name__ == "__main__":
    weights_file = "../dataset/output_country/country_import_weights.csv"
    tariff_file = "hts_rates_by_country_pandas.csv" 
    output_file = "../dataset/total_output/hts8_weighted_average_tariff.csv"
    result_df = compute_weighted_average_tariff(None, None, weights_file, tariff_file, output_file)