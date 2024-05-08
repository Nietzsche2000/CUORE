import uproot
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import awkward as ak


def uproot_df(path):
    file = uproot.open(path)
    tree = file[file.keys()[0]]
    df = tree.arrays(library="pd")
    column_names = df.columns.tolist()
    # print(column_names)
    return df

if __name__ == "__main__":
    base_path = "./Waveforms_Ds3613_Bkg_Ch{:04d}.root"
    dfs = []
    for i in range(1, 53):
        file_path = base_path.format(i)
        print(i)
        dfs.append(uproot_df(base_path.format(i)))

    print("COMBINING")
    combined_df = pd.concat(dfs, ignore_index=True)
    print("MERGING")
    # Perform a self-join on combined_df where 'EventID' matches 'Multi_EventID'
    merged_df = pd.merge(combined_df, combined_df, left_on='EventID', right_on='Multi_EventID')
    print("GROUPING")
    # Group by 'EventID' from the left DataFrame and collect 'Multi_ChannelID' from the right DataFrame
    result = merged_df.groupby('EventID_x')['Multi_ChannelID_y'].apply(list).to_dict()

    # Print the result
    print(result)
    