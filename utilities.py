import pandas as pd
import numpy as np
import geopandas as gpd

groceries = pd.read_csv('/Users/jamesswank/Downloads/Grocery_S_ExportTable1.csv')


block_geo_data = gpd.read_file('/Users/jamesswank/Python_Projects/CensusBlocks/assets/blocks4.json')
# print(block_geo_data)
# print(block_geo_data.columns)
# geo_arap = block_geo_data[block_geo_data['COUNTYFP20'] == "005"]
block_geo_data['GEOID'] = block_geo_data['GEOID'].astype(int)


# print(block_geo_data)


def get_grocery_stores():
    df = groceries



    return df

def get_block_data():
    block_df1 = pd.read_csv('/Users/jamesswank/Python_Projects/CensusBlocks/Data/BlockPop.csv')
    
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
    
    df = block_geo_data.merge(block_df1, on="GEOID")
    # print(df)
    

    return df

