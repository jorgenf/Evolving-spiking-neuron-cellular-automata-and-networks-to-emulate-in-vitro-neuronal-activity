from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# where to find data
pickle_name = Path("plots/pickles/20210816")

# where to save plots
savepath = Path("plots/figures/fitness_vs_generations")

# esthetics
sns.set_context("paper")
width = 7.16
aspect_ratio = 1.9

# set color theme
model_palette = {
    "CA" : "#509A29", # green
    "Network" : "#2A74BC" # blue
    }

savepath.mkdir(parents=True, exist_ok=True)
df = pd.read_pickle(Path(f"{pickle_name}/individual_data.pkl"))

# df = pd.melt(
#     df, 
#     id_vars=["Generation", "Rank", "Culture", "DIV", "Number of generations", "Model type", "Population size"],
#     var_name="Fitness type",
#     value_vars=["Temporal", "Spatial", "Overall"],
#     value_name="Fitness"
#     )

total_n_plots = len(df["Culture"].unique()) * len(df["DIV"].unique()) * 2
n_plots = 0
for culture in df["Culture"].unique():
    for div in df["DIV"].loc[df["Culture"] == culture].unique():

        n_gens=df["Number of generations"].loc[
            (df["DIV"] == div) &
            (df["Culture"] == culture)
            ].unique()[0]

        n_inds=df["Population size"].loc[
            (df["DIV"] == div) &
            (df["Culture"] == culture)
            ].unique()[0]
        
        for rank in [10, n_inds]:
            n_plots += 1
            print(" " * 40, end="\r")
            print(f"Creating plot {n_plots}/{total_n_plots} ({culture} {div})", end="\r")
            ax = sns.relplot(
                data=df.loc[
                    (df["Rank"] <= rank) &
                    (df["DIV"] == div) &
                    (df["Culture"] == culture)
                    ],
                # data=df,
                x="Generation",
                y="Fitness",
                # style="Reference culture",
                # hue="Fitness type",
                hue="Model type",
                # style="Fitness type",
                kind="line",
                height=(width/aspect_ratio),
                aspect=aspect_ratio,
                palette=model_palette,
            )

            ax.set(
                title=f"{culture} {div} DIV  top {rank}",
                # title=f"Top {rank} phenotypes",
                yticks=(0, 0.5, 1),
                xticks=(0, n_gens-1)
                # xticks=range(0, n_gens, n_gens//5)
                )
            
            ax.savefig(Path(f"{savepath}/{culture}-{div}_top-{rank}"))
            plt.close()

print("\nDone")