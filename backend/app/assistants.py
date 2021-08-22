from typing import List
from pandas import read_parquet
from math import exp

def pqt_to_list( pqt_filepath : str ) -> List:
    pqt = read_parquet(pqt_filepath , engine="pyarrow")
    tmp_dict = pqt.to_dict()
    columns = list(tmp_dict.keys()) 
    max_id = len(tmp_dict[columns[0]])
    return [ 
                { 
                    col : tmp_dict[col][id] \
                        if isinstance(tmp_dict[col][id] , int)  \
                        else str(tmp_dict[col][id])\
                        for col in columns 
                } \
                    for id in range( max_id )
            ]

def sigmoid(x):
    return 1 / (1 + exp(-x))

def hyp_tan(x):
    return ( exp(2*x) - 1 ) / ( exp( 2*x) + 1 ) 

