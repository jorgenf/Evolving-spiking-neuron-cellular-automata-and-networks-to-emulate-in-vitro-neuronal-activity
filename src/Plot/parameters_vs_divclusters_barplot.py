from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


rank = 10 # plot top x individuals

# where to read data
pickle_name = Path("plots/pickles/20210816")

# where to save plots
savepath = Path("plots/figures/parameter_vs_divclusters")

# plot esthetics
sns.set_context("paper")
font_size = 7
width = 7.16 / 2
aspect_ratio = 1.9
culture_order = ["Small & sparse", "Sparse", "Small", "Dense"] # "Ultra sparse" left out

# do stuff
df = pd.read_pickle(Path(f"{pickle_name}/param_data.pkl"))
savepath.mkdir(parents=True, exist_ok=True)
df["Generation"] = df["Generation"].astype(int)

# for normalizing genes to parameter values
gene_functions = {
        "Firing threshold" : lambda x : (x * 5) + 0.1,
        "Random fire probability" : lambda x : x * 0.15,
        "Refractory period" : lambda x : round(x * 10),
        "Inhibition percentage" : lambda x : x * 0.5,
        "Leak constant" : lambda x : x * 0.2,
        "Integration constant" : lambda x : x * 0.5,
    }

def normalize_gene(row):
    for key in gene_functions:
        if row["Model parameter"] == key: 
            return gene_functions[key](row["Gene value"])
    
    if row["Model parameter"] == "Density constant" and row["Model type"] == "CA":
        return round(row["Gene value"] * 5) + 1
    elif row["Model parameter"] == "Density constant" and row["Model type"] == "Network":
        return round(row["Gene value"] * 4) + 0.1
    else:
        print(f"Error: '{key}' not found")
        return None

# pick only top individuals from each experiment
filtered_df = pd.DataFrame()
for parameter_name in df["Model parameter"].unique():
    filtered_df = filtered_df.append(df.loc[df["Model parameter"] == parameter_name].sort_values("Fitness", ascending=False).groupby("Experiment ID").head(rank))
df = filtered_df

# translate gene to parameter value
df["Parameter value"] = df.apply(normalize_gene, axis=1)

# finished manipulating dataframe, print results
print(df)

# plot parameters vs div
total_n_plots = len(df["Model parameter"].unique()) * len(df["Model type"].unique())
n_plots = 0

def parameter_limits(model_parameter):
    if model_parameter == "Density constant":
        return (0, 6)
    else:
        return (gene_functions[model_parameter](0), gene_functions[model_parameter](1))

for model_parameter in df["Model parameter"].unique():

    param_min, param_max = parameter_limits(model_parameter)
    for model_type in df["Model type"].unique():
    
        if model_type == "CA":
            color_theme = "Greens_d"
        else:
            color_theme = "Blues_d"

        div_order = df["DIV"].loc[
                    (df["Model parameter"] == model_parameter) &
                    (df["Model type"] == model_type)
                    ].unique()
        div_order.sort()

        # plutting function
        ax = sns.barplot(
            data=df.loc[
                (df["Model parameter"] == model_parameter) &
                (df["Model type"] == model_type)
                ],
            order=culture_order,
            x="Culture",
            y="Parameter value",
            hue="DIV",
            hue_order=div_order,
            ci="sd",
            palette=color_theme,
        )

        # text and font size
        ax.axes.set_title(f"{model_parameter} {model_type} top {rank}", fontsize=font_size)
        ax.set_xlabel("Culture", fontsize=font_size)
        ax.set_ylabel(f"{model_parameter}", fontsize=font_size)
        ax.tick_params(labelsize=font_size)

        ax.set(
            # title=,
            yticks=(param_min, param_max),
            )

        # remove legende
        ax.get_legend().remove()
        
        # save results
        fig = ax.get_figure()
        fig.set_size_inches(width, width/aspect_ratio)
        fig.savefig(Path(f"{savepath}/{model_parameter}_{model_type}_top-{rank}"), dpi=300)
        plt.close()

print("\nDone")

