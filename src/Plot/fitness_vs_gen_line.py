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
font_size = 7
width = 7.16 / 2
aspect_ratio = 1.9

# set color theme
model_palette = {
    "CA" : "#509A29", # green
    "Network" : "#2A74BC" # blue
    }

savepath.mkdir(parents=True, exist_ok=True)
df = pd.read_pickle(Path(f"{pickle_name}/individual_data.pkl"))
df["Generation"] = df["Generation"].astype(int)

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
                legend=False
            )

            # ax.set_xlabel("Generation", fontsize=font_size)
            # ax.set_ylabel("Fitness", fontsize=font_size)
            # ax.tick_params(labelsize=font_size)

            ax.set(
                title=f"{culture} {div} DIV  top {rank}",
                yticks=(0, 0.5, 1),
                xticks=(0, n_gens-1),
                )

            # ax.get_legend().remove()
            
            ax.savefig(Path(f"{savepath}/{culture}-{div}_top-{rank}"), dpi=300)
            plt.close()            

print(df)

n_gens=df["Number of generations"].min()

n_inds=df["Population size"].min()

for rank in [10, n_inds]:
    n_plots += 1
    print(" " * 40, end="\r")
    print(f"Creating plot {n_plots}/{total_n_plots}", end="\r")
    ax = sns.relplot(
        data=df.loc[
            (df["Rank"] <= rank) &
            (df["Generation"] <= n_gens)
            # (df["Model type"] == "Network")# &
            # (df["Culture"] == culture)
            ],
        # data=df,
        x="Generation",
        y="Fitness",
        style="Culture",
        hue="Model type",
        # hue="DIV",
        kind="line",
        height=(width/aspect_ratio),
        aspect=aspect_ratio,
        palette=model_palette,
        # palette="Greens_d",
        # legend=False
    )

    ax.set(
        title=f"All cultures and DIV top {rank}",
        yticks=(0, 0.5, 1),
        xticks=(0, n_gens),
        )
    
    ax.savefig(Path(f"{savepath}/all_cultures_and_div_top-{rank}"), dpi=300)
    plt.close()

print("\nDone")