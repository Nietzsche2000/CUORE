import uproot
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import awkward as ak

def uproot_df(path):
    # OPEN THE ROOT FILE AT THE SPECIFIED PATH
    file = uproot.open(path)
    # ACCESS THE FIRST TREE IN THE FILE BASED ON THE FIRST KEY
    tree = file[file.keys()[0]]
    # LOAD THE DATA INTO A PANDAS DATAFRAME
    df = tree.arrays(library="pd")
    # GET A LIST OF COLUMN NAMES IN THE DATAFRAME
    column_names = df.columns.tolist()
    # PRINT(COLUMN_NAMES) - COMMENTED OUT FOR NOW
    return df

if __name__ == "__main__":
    # DEFINE THE BASE PATH FOR THE ROOT FILES
    base_path = "./Waveforms_Ds3613_Bkg_Ch{:04d}.root"
    # INITIALIZE AN EMPTY LIST TO STORE DATAFRAMES
    dfs = []
    # LOOP THROUGH FILE INDICES FROM 1 TO 52
    for i in range(1, 53):
        file_path = base_path.format(i)
        # PRINT THE CURRENT FILE INDEX
        print(i)
        # APPEND EACH DATAFRAME TO THE LIST AFTER READING
        dfs.append(uproot_df(base_path.format(i)))

    # PRINT STATUS OF COMBINING DATAFRAMES
    print("COMBINING")
    # CONCATENATE ALL DATAFRAMES INTO A SINGLE DATAFRAME
    combined_df = pd.concat(dfs, ignore_index=True)
    # PRINT STATUS OF MERGING DATAFRAMES
    print("MERGING")
    # PERFORM A SELF-JOIN ON COMBINED_DF WHERE 'EVENTID' MATCHES 'MULTI_EVENTID'
    merged_df = pd.merge(combined_df, combined_df, left_on='EventID', right_on='Multi_EventID')
    # PRINT STATUS OF GROUPING DATA
    print("GROUPING")
    # GROUP BY 'EVENTID' FROM THE LEFT DATAFRAME AND COLLECT 'MULTI_CHANNELID' FROM THE RIGHT DATAFRAME
    result = merged_df.groupby('EventID_x')['Multi_ChannelID_y'].apply(list).to_dict()

    # PRINT THE FINAL RESULT OF THE GROUPING
    print(result)
