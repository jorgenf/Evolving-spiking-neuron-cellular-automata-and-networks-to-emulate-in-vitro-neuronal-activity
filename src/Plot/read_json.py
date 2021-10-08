import json
from pathlib import Path
import re
import shutil

import pandas as pd

# recognize the density of the reference culture
def find_culture(filename):
    culture_types = {
        "Dense" : ["2-1-10.spk.txt", "2-1-31.spk.txt"],
        "Small" : ["6-2-10.spk.txt", "6-2-13.spk.txt", "6-2-17.spk.txt", "6-2-24.spk.txt", "6-2-28.spk.txt", "6-2-31.spk.txt", "6-2-34.spk.txt", "6-2-6.spk.txt"],
        "Small & sparse" : ["8-1-10.spk.txt", "8-1-13.spk.txt", "8-1-17.spk.txt", "8-1-20.spk.txt", "8-1-24.spk.txt", "8-1-28.spk.txt", "8-1-31.spk.txt", "8-1-34.spk.txt", "8-1-6.spk.txt"],
        "Sparse" :	["6-1-10.spk.txt", "6-1-31.spk.txt"],
        "Ultra sparse" : ["8-1-10 ultrasparse.spk.txt", "8-1-31 ultrasparse.spk.txt"],
    }

    for key in culture_types:
        if filename in culture_types[key]:
            return key
        else:
            continue
    
    print(f"Error: \"{filename}\" not found")
    return None


# find and read json files, assumes a 2 level folder structure
def read_json(experiment_data_path):
    experiment_number = 0
    experiment_data_path = Path(experiment_data_path)
    # processed_cultures = []

    # path to save temporary dataframes
    temp_data_path_indiv = Path(f"{experiment_data_path}/temp/indiv")
    temp_data_path_param = Path(f"{experiment_data_path}/temp/param")
    temp_data_path_indiv.mkdir(parents=True, exist_ok=True)
    temp_data_path_param.mkdir(parents=True, exist_ok=True)

    data = []

    for folder_level_1 in experiment_data_path.glob("*"):
        experiment_name = folder_level_1.stem
        for folder_level_2 in folder_level_1.glob("*"):
            json_files = Path(folder_level_2).glob("evolution_data.json")
            for filepath in json_files:
                experiment_number += 1
                json_file = Path(filepath).open("r")
                data_unit = json.load(json_file)

            data_unit["experiment_number"] = experiment_number
            data_unit["reference culture"] = find_culture(data_unit["REFERENCE_PHENOTYPE"])
            # processed_cultures.append(data_unit["reference culture"])
            data.append(data_unit)
        
    # unique_cultures = set(processed_cultures)
    # culture_summary = {}
    # for culture in unique_cultures:
    #     culture_summary[culture] = processed_cultures.count(culture)
    
    # print("Processed cultures:")
    # for key in culture_summary:
    #     print(key, ":", culture_summary[key])

    experiment_summary_list_dict = []
    for i_simulation, element in enumerate(data):

        # transform data to a list of dictionaries
        individual_data_list_dict = []
        parameter_data_list_dict = []

        # determine DIV of reference culture
        r = re.search("[0-9]{1,2}-[0-9]{1,2}-[0-9]{1,2}", element["REFERENCE_PHENOTYPE"])
        div = r.group().split("-")[2]

        # prettyprint model type name
        if element["MODEL_TYPE"][0].lower() == "ca":
            model_type = "CA"
        elif element["MODEL_TYPE"][0].lower() == "network":
            model_type = "Network"
        else:
            print(f"Error: Unknown model type \"{individual_data['Model type']}\"")

        simulation_summary = {
                "model" : model_type,
                "culture" : element["reference culture"],
                "reference file" : element["REFERENCE_PHENOTYPE"],
                "div" : div,
                "population" : element["POPULATION_SIZE"],
                "generations" : element["NUM_GENERATIONS"],
            }
        
        experiment_summary_list_dict.append(simulation_summary)

        # create dataframe by writing the json data to a list of dictionaries
        for i_gen in element["generations"]:
            for i, i_ind in enumerate(element["generations"][i_gen]["all"]):
                individual_data = {
                    "Experiment ID" : element["experiment_number"],
                    "Model type" : model_type,
                    # "Dimensions" : element["DIMENSION"],
                    "Population size" : element["POPULATION_SIZE"],
                    "Number of generations" : element["NUM_GENERATIONS"],
                    # "Simulation duration" : element["SIMULATION_DURATION"],
                    # "Time step resolution" : element["TIME_STEP_RESOLUTION"],
                    # "Mutation p" : element["MUTATION_P"],
                    # "Parents p" : element["PARENTS_P"],
                    # "Retained adults p" : element["RETAINED_ADULTS_P"],
                    "Reference phenotype" : element["REFERENCE_PHENOTYPE"],
                    "Culture" : element["reference culture"],
                    "DIV" : div,
                    "Generation" : i_gen,
                    "Rank" : i+1,
                    "Fitness" : i_ind["fitness"],
                    # "Temporal" : i_ind["spike_dist"],
                    # "Spatial" : i_ind["electrode_dist"],
                    # "genotype" : i_ind["genotype"],
                }
                
                # create a different dataframe for plotting parameters
                for j, genome in enumerate(i_ind["genotype"]):
                    parameter_data = {
                        "Experiment ID" : element["experiment_number"],
                        "Population size" : element["POPULATION_SIZE"],
                        "Number of generations" : element["NUM_GENERATIONS"],
                        "Model type" : model_type,
                        "Model parameter" : element["MODEL_TYPE"][2][j],
                        "Culture" : element["reference culture"],
                        "Reference phenotype" : element["REFERENCE_PHENOTYPE"],
                        # "Rank" : i+1,
                        "Fitness" : i_ind["fitness"],
                        "Generation" : i_gen,
                        "Gene value" : genome,
                        "DIV" : div,
                    }

                    parameter_data_list_dict.append(parameter_data)

            # superfluous? reads the old top 5 data. only useful to extract phenotype
            # if "rank 1" in element["generations"][i_gen].keys():
            #     for i, key in enumerate(element["generations"][i_gen]):
            #         if "rank" in key:
            #             # individual_data["genotype"] = element["generations"][i_gen][key]["genotype"],
            #             # individual_data["fitness"] = element["generations"][i_gen][key]["fitness"]
            #             individual_data["rank"] = i+1

                individual_data_list_dict.append(individual_data)
            
        df_indiv = pd.DataFrame(individual_data_list_dict)
        df_param = pd.DataFrame(parameter_data_list_dict)

        df_indiv.to_pickle(Path(f"{temp_data_path_indiv}/{i_simulation}_indiv.pkl"))
        df_param.to_pickle(Path(f"{temp_data_path_param}/{i_simulation}_param.pkl"))

    # for pickle_file in temp_data_path_indiv.glob("*.pkl"):
    individual_data = pd.concat(map(pd.read_pickle, temp_data_path_indiv.glob("*.pkl")))
    parameter_data = pd.concat(map(pd.read_pickle, temp_data_path_param.glob("*.pkl")))

    # clean temp data
    shutil.rmtree(temp_data_path_indiv)
    shutil.rmtree(temp_data_path_param)
    temp_data_path_indiv.parent.rmdir()

    experiment_summary = pd.DataFrame(experiment_summary_list_dict)
    
    return individual_data, parameter_data, experiment_summary

if __name__ == "__main__":

    # path to folder with experiments
    experiment_path = Path("/home/wehak/code/ACIT4610_Semesteroppgave/results_20210816")

    # name of pickle file
    savepath = Path("plots/pickles/20210816")
    savepath.mkdir(parents=True, exist_ok=True)
    individual_data_pickle_name = Path(f"{savepath}/individual_data.pkl")
    parameter_data_pickle_name = Path(f"{savepath}/param_data.pkl")

    # save data as pickle file
    individual_data, parameter_data, experiment_summary = read_json(experiment_path)
    individual_data.to_pickle(individual_data_pickle_name)
    parameter_data.to_pickle(parameter_data_pickle_name)
    experiment_summary.to_pickle(Path(f"{savepath}/summary.pkl"))

    print(individual_data)
    print(parameter_data)
    print(experiment_summary)


    print(f"Data saved to \"{savepath}\"")
