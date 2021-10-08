from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



# where to read data
pickle_name = Path("plots/pickles/20210816")
df = pd.read_pickle(Path(f"{pickle_name}/summary.pkl"))

print(df)
print(df.groupby(["model"])["reference file"].value_counts())
# print(df.groupby(["model", "culture"])["div"].value_counts())

print("\nDone")