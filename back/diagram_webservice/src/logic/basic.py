from utils.aliases import DATASETS, OUT_DIR
import pandas as pd
import matplotlib.pyplot as plt



def prepare_sdg():
    df = pd.read_csv(DATASETS.get("sdg"))
    
    # The file of this file is weird, in the way, that it comes with two headers.
    # Where in the first row is the second header.
    # See file for 1st header
    
    header = df.iloc[0]
    df = df[1:]
    df.columns = header
    return df
    

# prototype
def basic_sdg():
    df = prepare_sdg()
    df = df[df["WHO region"] == "Global"]
    df.drop(columns=["WHO region"],inplace=True)
    df = df.T
    
    header = df.iloc[0]
    df = df[1:]
    df.columns = header
    
    plt.bar(df['Male'], df['Female'])
    plt.savefig(f"{OUT_DIR}/male_female.png")