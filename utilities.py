import pandas as pd
import numpy as np
import geopandas as gpd

groceries = pd.read_csv('/Users/jamesswank/Downloads/Grocery_S_ExportTable1.csv')


block_geo_data = gpd.read_file('/Users/jamesswank/Python_Projects/CensusBlocks/assets/blocks4.json')
# print(block_geo_data.dtypes)
# print(block_geo_data['GEOID'])
# print(block_geo_data['TRACTCE20'])
# print(block_geo_data['GEOID'])
# print(block_geo_data.columns)
# geo_arap = block_geo_data[block_geo_data['COUNTYFP20'] == "005"]
# block_geo_data['GEOID'] = block_geo_data['GEOID'].astype(int)

svi_data = pd.read_csv("/Users/jamesswank/Python_Projects/Food_Deserts/Colorado_SVI_2020.csv")
svi_data = svi_data[svi_data['COUNTY'] == 'Arapahoe']
svi_data['FIPS'] = svi_data['FIPS'].astype(str)
# print(svi_data['FIPS'])
svi_data['TRACTCE20'] = svi_data['FIPS'].str[-6:]
svi_data = svi_data[['TRACTCE20', 'E_TOTPOP', 'E_POV150']]
svi_data['pct_pov'] = svi_data['E_POV150'] / svi_data['E_TOTPOP'] 
# print(svi_data['FIPS'])
# print(svi_data)

# print(block_geo_data)


def get_grocery_stores():
    df = groceries
    # print(df['Store'])


    return df

def get_block_data():
    block_df1 = pd.read_csv('/Users/jamesswank/Python_Projects/CensusBlocks/Data/BlockPop.csv')
    # print(block_df1.columns)

    # print(block_df1['GEOID'])
    # geo_data = gpd.read_file('Census_Blocks_2020_SHAPE_WGS/Census_Blocks_2020_WGS.shp')
    # print(geo_data.columns)
    # geo_arap = geo_data[geo_data['COUNTYFP20'] == "005"]
    geo_arap = block_geo_data
    # print(geo_arap.columns)
    # print(block_geo_data.columns)
    # geo_arap['GEOID'] = geo_arap['GEOID'].apply(lambda x: x[9:])
    # df1['Total'] = df1['Total'].str.replace(',', '').astype(int)
    # geo_arap['GEOID'] = geo_arap['GEOID'].str.replace(',', '').astype(int)
    geo_arap['GEOID'] = geo_arap['GEOID'].astype(int)
    # print(block_geo_data)
    # print(block_df1.dtypes)
    block_df1['Total'] = block_df1['Total'].str.replace(',', '').astype(int)
    # block_df1['Total'] = block_df1['Total'].astype(int)
    # print(block_df1.columns)
    df1 = block_geo_data.merge(block_df1, on="GEOID")
    # df = block_geo_data.merge(block_df1, on="GEOID")
    # print(df)
    # df2 = pd.merge(block_geo_data, svi_data, on="TRACTCE20")
    df2 = pd.merge(df1, svi_data, on="TRACTCE20")
    # print(df2.columns)

    return df2

