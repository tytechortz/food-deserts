import pandas as pd
import numpy as np
import geopandas as gpd

groceries = pd.read_csv('/Users/jamesswank/Downloads/Grocery_S_ExportTable1.csv')


block_geo_data = gpd.read_file('/Users/jamesswank/Python_Projects/CensusBlocks/assets/blocks4.json')


svi_data = pd.read_csv("/Users/jamesswank/Python_Projects/Food_Deserts/Colorado_SVI_2020.csv")
svi_data = svi_data[svi_data['COUNTY'] == 'Arapahoe']
svi_data['FIPS'] = svi_data['FIPS'].astype(str)

svi_data['TRACTCE20'] = svi_data['FIPS'].str[-6:]
svi_data = svi_data[['TRACTCE20', 'E_TOTPOP', 'E_POV150']]
svi_data['pct_pov'] = svi_data['E_POV150'] / svi_data['E_TOTPOP'] 



def get_grocery_stores():
    df = groceries
    # print(df['Store'])


    return df

def get_block_data():
    block_df1 = pd.read_csv('/Users/jamesswank/Python_Projects/CensusBlocks/Data/BlockPop.csv')
   
    geo_arap = block_geo_data
    
    geo_arap['GEOID'] = geo_arap['GEOID'].astype(int)
    
    block_df1['Total'] = block_df1['Total'].str.replace(',', '').astype(int)
   
    df1 = block_geo_data.merge(block_df1, on="GEOID")
    
    df2 = pd.merge(df1, svi_data, on="TRACTCE20")
   

    return df2

