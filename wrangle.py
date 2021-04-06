#basic imports
import pandas as pd
import numpy as np
import env

import sklearn.preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def nulls_by_col(df):
    '''
    This function takes in a dataframe of observations and attributes and returns a dataframe where each row is an attribute name, 
    the first column is the number of rows with missing values for that attribute, and the second column is percent of total rows 
    that have missing values for that attribute. 
    '''
    
    num_missing = df.isnull().sum()
    rows = df.shape[0]
    pct_missing = num_missing / rows
    cols_missing = pd.DataFrame({'number_missing_rows': num_missing, 'percent_rows_missing': pct_missing})
    return cols_missing

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



def cols_missing(df):
    '''
    This function takes in a dataframe and returns a dataframe with 3 columns: the number of columns missing, 
    percent of columns missing, and number of rows with n columns missing. 
    '''
    
    df2 = pd.DataFrame(df.isnull().sum(axis =1), columns = ['num_cols_missing']).reset_index()\
    .groupby('num_cols_missing').count().reset_index().\
    rename(columns = {'index': 'num_rows' })
    df2['pct_cols_missing'] = df2.num_cols_missing/df.shape[1]
    return df2




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def handle_missing_values(df, prop_required_column = .5, prop_required_row = .70):
    '''
    This function takes in: a dataframe, the proportion (0-1) of rows (for each column) with non-missing values required to keep 
    the column, and the proportion (0-1) of columns/variables with non-missing values required to keep each row.  
    
    It returns the dataframe with the columns and rows dropped as indicated. 
    '''
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Final wrangle_zillow Function:

def wrangle_zillow():
    
    '''
    This function reads in the csv from the acquire.py which acquires the Zillow data from Codeup's database on the MySQL server.  
    
    It then prepares the data by removing columns and rows that are missing more than 50% of the 
    data, restricts the dataframe to include only single unit properties, with at least one
    bedroom and bathroom and at least 500 square feet, adds a column to indicate county (based on 
    fips), drops any unnecessary columns, adjusts for outliers in taxvaluedollarcnt and
    calculatedfinishedsquarefeet, fills missing values in buildinglotsize and buildingquality with 
    median values, and renames columns to user-friendly titles.
    '''
    df = pd.read_csv('zillow_db.csv', index_col=0)
    
    #change fips to int
    df.fips = df.fips.astype(int)
    
    # Restrict df to only properties that meet single unit use criteria
    single_use = [261, 262, 263, 264, 266, 268, 273, 276, 279]
    df = df[df.propertylandusetypeid.isin(single_use)]
    
    # Restrict df to only those properties with at least 1 bath & bed and 500 sqft area
    df = df[(df.bedroomcnt > 0) & (df.bathroomcnt > 0) & ((df.unitcnt<=1)|df.unitcnt.isnull())\
            & (df.calculatedfinishedsquarefeet>=500)]

    # Handle missing values i.e. drop columns and rows based on a threshold
    df = handle_missing_values(df)
    
    # Add column for counties
    df['county'] = np.where(df.fips == 6037, 'Los_Angeles',
                           np.where(df.fips == 6059, 'Orange', 
                                   'Ventura'))    
    # drop columns not needed
    df = df.drop(columns = ['id','calculatedbathnbr', 'finishedsquarefeet12', 'fullbathcnt', 'heatingorsystemtypeid'
       ,'propertycountylandusecode', 'propertylandusetypeid','propertyzoningdesc', 
        'censustractandblock', 'rawcensustractandblock',  'propertylandusedesc'])

    # replace nulls in unitcnt with 1
    df.unitcnt.fillna(1, inplace = True)
    
    # assume that since this is Southern CA, null means 'None' for heating system
    df.heatingorsystemdesc.fillna('None', inplace = True)
    
    # replace nulls with median values for select columns
    df.lotsizesquarefeet.fillna(7313, inplace = True)
    df.buildingqualitytypeid.fillna(6.0, inplace = True)

    # Columns to look for outliers
    df = df[df.taxvaluedollarcnt < 5_000_000]
    df[df.calculatedfinishedsquarefeet < 8000]
    
    # Just to be sure we caught all nulls, drop them here
    df = df.dropna()
   
    #recalculate yearbuilt to age of home:
    df.yearbuilt = 2017 - df.yearbuilt 
    #rename columns:
    df.rename(columns={'taxvaluedollarcounty':'tax_value', 'bedroomcnt':'bedrooms', 'bathroomcnt':'bathrooms', 'calculatedfinishedsquarefeet':
                      'square_feet', 'lotsizesquarefeet':'lot_size', 'buildingqualitytypeid':'buildingquality', 'yearbuilt':'age', 'taxvaluedollarcnt': 'tax_value', 'landtaxvaluedollarcnt': 'land_tax_value', 'unitcnt': 'unit_count', 'heatingorsystemdesc': 'heating_system', 'structuretaxvaluedollarcnt': 'structure_tax_value'}, inplace=True)
    
    df['age_bin'] = pd.cut(df.age, 
                           bins = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140],
                           labels = ["0-5","5-10","10-20","20-30", "30-40", "40-50", "50-60", "60-70", "70-80", 
                                     "80-90", "90-100", "100-110", "110-120", "120-130", "130-140"])

    # create taxrate variable
    df['taxrate'] = df.taxamount/df.tax_value*100

    # create acres variable
    df['acres'] = df.lot_size/43560

    # bin acres
    df['acres_bin'] = pd.cut(df.acres, bins = [0, .10, .15, .25, .5, 1, 5, 10, 20, 50, 200], 
                       labels = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9])

    # bin tax value
    df['tax_value_bin'] = pd.cut(df.tax_value, bins = [0, 80000, 150000, 225000, 300000, 350000, 450000, 550000, 650000, 900000, 5000000], labels = ["< $80,000","$150,000", "$225,000", "$300,000", "$350,000", "$450,000", '$550,000', "$650,000", "$900,000", "$5,000,000"])
    
    #bin land_tax_value
    df['land_tax_value_bin'] = pd.cut(df.land_tax_value, bins = [0, 50000, 100000, 150000, 200000, 250000,350000, 450000, 650000, 800000, 1000000], labels = ["< $50,000","$100,000", "$150,000", "$200,000", "$250,000", "$350,000", '$450,000', "$650,000", "$800,000", "$1,000,000"])
    
    # square feet bin
    df['sqft_bin'] = pd.cut(df.square_feet, 
                            bins = [0, 800, 1000, 1250, 1500, 2000, 2500, 3000, 4000, 7000, 12000],
                            labels = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9]
                       )

    # dollar per square foot-structure
    df['structure_dollar_per_sqft'] = df.structure_tax_value/df.square_feet


    df['structure_dollar_sqft_bin'] = pd.cut(df.structure_dollar_per_sqft, 
                                             bins = [0, 25, 50, 75, 100, 150, 200, 300, 500, 1000, 1500],
                                             labels = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9]
                                            )


    # dollar per square foot-land
    df['land_dollar_per_sqft'] = df.land_tax_value/df.lot_size

    df['lot_dollar_sqft_bin'] = pd.cut(df.land_dollar_per_sqft, bins = [0, 1, 5, 20, 50, 100, 250, 500, 1000, 1500, 2000],
                                       labels = ['0', '1', '5-19', '20-49', '50-99', '100-249', '250-499', '500-999', '1000-1499', '1500-2000']
                                      )


    # update datatypes of binned values to be float
    df = df.astype({'sqft_bin': 'float64', 'acres_bin': 'float64', 
                    'structure_dollar_sqft_bin': 'float64'})


    # ratio of bathrooms to bedrooms
    df['bath_bed_ratio'] = df.bathrooms/df.bedrooms

    # 12447 is the ID for city of LA. 
    # I confirmed through sampling and plotting, as well as looking up a few addresses.
    df['cola'] = df['regionidcity'].apply(lambda x: 1 if x == 12447.0 else 0)
  
    
    return df [((df.bathrooms <= 7) & (df.bedrooms <= 7) &
               (df.bathrooms >= 1) & 
               (df.bedrooms >= 1) & 
               (df.acres <= 20) &
               (df.square_feet <= 9000) & 
               (df.taxrate <= 10)
              )]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def remove_outliers():
    '''
    remove outliers in bed, bath, square feet, acres & tax rate
    '''
    df= wrangle_zillow()
    return df[((df.bathrooms <= 7) & (df.bedrooms <= 7) &
               (df.bathrooms >= 1) & 
               (df.bedrooms >= 1) & 
               (df.acres <= 20) &
               (df.square_feet <= 9000) & 
               (df.taxrate <= 10)
              )]


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def tidy_wrangle():
    '''This function takes in the wrangled zillow dataframe, drops unneeded columns and prepares it for splitting then scaling.'''
    df= wrangle_zillow()
    df= df.drop(columns=['parcelid', 'bathrooms', 'bedrooms', 'buildingquality', 'county','square_feet', 'lot_size', 'regionidcity','regionidcounty', 'regionidzip', 'roomcnt', 'unit_count', 'assessmentyear', 'transactiondate', 'heating_system', 'age_bin', 'taxrate',  'acres_bin', 'sqft_bin', 'structure_dollar_sqft_bin', 'lot_dollar_sqft_bin', 'bath_bed_ratio','tax_value_bin', 'land_tax_value_bin'])
    return df


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def data_split(df, stratify_by='logerror'):
    '''
    this function takes in a dataframe and splits it into 3 samples, 
    a test, which is 20% of the entire dataframe, 
    a validate, which is 24% of the entire dataframe,
    and a train, which is 56% of the entire dataframe. 
    It then splits each of the 3 samples into a dataframe with independent variables
    and a series with the dependent, or target variable. 
    The function returns 3 dataframes and 3 series:
    X_train (df) & y_train (series), X_validate & y_validate, X_test & y_test. 
    '''

    # split df into test (20%) and train_validate (80%)
    train_validate, test = train_test_split(df, test_size=.2, random_state=123)

    # split train_validate off into train (70% of 80% = 56%) and validate (30% of 80% = 24%)
    train, validate = train_test_split(train_validate, test_size=.3, random_state=123)
    # split train into X (dataframe, drop target) & y (series, keep target only)
    X_train = train.drop(columns=['logerror'])
    y_train = train['logerror']
    
    # split validate into X (dataframe, drop target) & y (series, keep target only)
    X_validate = validate.drop(columns=['logerror'])
    y_validate = validate['logerror']
    
    # split test into X (dataframe, drop target) & y (series, keep target only)
    X_test = test.drop(columns=['logerror'])
    y_test = test['logerror']
    
    return X_train, y_train, X_validate, y_validate, X_test, y_test

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
