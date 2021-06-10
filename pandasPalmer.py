import pandas as pd
import numpy as np
import os.path as path
from urllib.parse import urlparse
from urllib.request import request

def CreateDataFrame(file_name, idx=None, remove_nulls=True):
    file_name = file_name.strip()
    state = []

    rslt = urlparse(file_name)
    is_url = all([rslt.scheme, rslt.netloc, rslt.path])
    is_url_valid = False
    if is_url:
        state.append('url detected')
        with request.urlopen(file_name) as resp:
            is_url_valid = (resp.staus == 200)
        if not is_url_valid:
            state.append('invalid url')

    if path.exists(file_name) or is_url:
        # Import File based on file extension
        if (file_name[-4:].upper() == '.CSV'):
            df = pd.read_csv(file_name,index_col=idx,parse_dates=True,infer_datetime_format=True)
            state.append("csv")
        
        elif (file_name[-4:].upper() == '.XLS') or (file_name[-5:].upper() == '.XLSX'):
            df = pd.read_excel(file_name, index_col=idx, parse_dates=True, infer_datetime_format=True)
            state.append("xls")
        
        elif (file_name[-5:].upper() == '.JSON'):
            df = pd.read_json(file_name)
            state.append('json')

        state.append('imported')

        if idx is not None:
            if type(idx) == list or type(idx) == str:
                if set(idx).issubset(set(df)):
                    df.set_index(keys=idx,inplace=True)
                    state.append('indexed')
                else:
                    print(f"There was a problem with the index the columns don't exist {idx}")

        if remove_nulls:
            df.dropna(inplace=True)
    else:
        print(f'Had problems locating the data [{file_name}]')

    print(state)

    return 

if __name__ == "__main__":
    # execute only if run as a script
    main()
