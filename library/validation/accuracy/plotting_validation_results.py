import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

import sys
from pathlib import Path
sys.path.insert(0,str(Path(os.path.abspath('.')).parent.parent))
import library.validation.accuracy.metric as metric







def ave_nmbe_hour(reference_data_hourly, model_data_hourly, total = False):
    nmbe_mean_by_hour = {}
    average_nmbe_mean_by_hour = {}
    totmean_hour = {}


    for column in reference_data_hourly.columns:
        nmbe_mean_by_hour[column] = {}
        totmean_hour[column] = np.abs(reference_data_hourly[column].mean())

        for hour in range(24):
            actual_hourly = reference_data_hourly[reference_data_hourly.index.hour == hour][column]
            predicted_hourly = model_data_hourly[model_data_hourly.index.hour == hour][column]

            if not actual_hourly.empty and not predicted_hourly.empty:
                if total == True:
                    nmbe_value = metric.nmbe(predicted_hourly, actual_hourly, norm = totmean_hour[column])
                else:    
                    nmbe_value = metric.nmbe(predicted_hourly, actual_hourly)
                nmbe_mean_by_hour[column][hour] = nmbe_value


        for hour in range(24):
            nmbe_values_at_hour = [nmbe_mean_by_hour[column][hour] for column in nmbe_mean_by_hour if hour in nmbe_mean_by_hour[column]]

            if nmbe_values_at_hour:
                average_nmbe_mean_by_hour[hour] = np.mean(nmbe_values_at_hour)
        
        
    return nmbe_mean_by_hour, average_nmbe_mean_by_hour  



def ave_nmbe_month(reference_data_monthly, model_data_monthly, total = False):
    nmbe_mean_by_month = {}
    average_nmbe_mean_by_month = {}
    totmean_month = {}

    for column in reference_data_monthly.columns:
        nmbe_mean_by_month[column] = {}
        totmean_month[column] = np.abs(reference_data_monthly[column].mean())

        for month in range(1,13):
            actual_monthly = reference_data_monthly[reference_data_monthly.index.month == month][column]
            predicted_monthly = model_data_monthly[model_data_monthly.index.month == month][column]

            if not actual_monthly.empty and not predicted_monthly.empty:
                if total == True:
                    nmbe_value = metric.nmbe(predicted_monthly, actual_monthly, norm = totmean_month[column])
                else:    
                    nmbe_value = metric.nmbe(predicted_monthly, actual_monthly)
                nmbe_mean_by_month[column][month] = nmbe_value

    for month in range(1,13):
        nmbe_values_at_month = [nmbe_mean_by_month[column][month] for column in nmbe_mean_by_month if month in nmbe_mean_by_month[column]]

        if nmbe_values_at_month:
            average_nmbe_mean_by_month[month] = np.mean(nmbe_values_at_month)

    return nmbe_mean_by_month, average_nmbe_mean_by_month
                    
        
def ave_nrmse_hour(reference_data_hourly, model_data_hourly, total = False):
    nrmse_mean_by_hour = {}
    average_nrmse_mean_by_hour = {}
    totmean_hour = {}


    for column in reference_data_hourly.columns:
        nrmse_mean_by_hour[column] = {}
        totmean_hour[column] = np.abs(reference_data_hourly[column].mean())

        for hour in range(24):
            actual_hourly = reference_data_hourly[reference_data_hourly.index.hour == hour][column]
            predicted_hourly = model_data_hourly[model_data_hourly.index.hour == hour][column]

            if not actual_hourly.empty and not predicted_hourly.empty:
                if total == True:
                    nrmse_value = metric.nrmse(predicted_hourly, actual_hourly, norm = totmean_hour[column])
                else:    
                    nrmse_value = metric.nrmse(predicted_hourly, actual_hourly)
                nrmse_mean_by_hour[column][hour] = nrmse_value


        for hour in range(24):
            nrmse_values_at_hour = [nrmse_mean_by_hour[column][hour] for column in nrmse_mean_by_hour if hour in nrmse_mean_by_hour[column]]

            if nrmse_values_at_hour:
                average_nrmse_mean_by_hour[hour] = np.mean(nrmse_values_at_hour)
        
        
    return nrmse_mean_by_hour, average_nrmse_mean_by_hour  


def ave_nrmse_month(reference_data_monthly, model_data_monthly, total = False):
    nrmse_mean_by_month = {}
    average_nrmse_mean_by_month = {}
    totmean_month = {}

    for column in reference_data_monthly.columns:
        nrmse_mean_by_month[column] = {}
        totmean_month[column] = np.abs(reference_data_monthly[column].mean())

        for month in range(1,13):
            actual_monthly = reference_data_monthly[reference_data_monthly.index.month == month][column]
            predicted_monthly = model_data_monthly[model_data_monthly.index.month == month][column]

            if not actual_monthly.empty and not predicted_monthly.empty:
                if total == True:
                    nrmse_value = metric.nrmse(predicted_monthly, actual_monthly, norm = totmean_month[column])
                else:    
                    nrmse_value = metric.nrmse(predicted_monthly, actual_monthly)
                nrmse_mean_by_month[column][month] = nrmse_value

    for month in range(1,13):
        nrmse_values_at_month = [nrmse_mean_by_month[column][month] for column in nrmse_mean_by_month if month in nrmse_mean_by_month[column]]

        if nrmse_values_at_month:
            average_nrmse_mean_by_month[month] = np.mean(nrmse_values_at_month)

    return nrmse_mean_by_month, average_nrmse_mean_by_month


            
def time_line_plot(mean, average_mean, validation_metric, time_granularity, plots_path, lim, total = False):
    plt.figure(figsize=(18,6))

    for column, values in mean.items():
        time = list(values.keys())
        metric = list(values.values())
    
        plt.plot(time, metric, label=column)

    plt.plot(list(average_mean.keys()), list(average_mean.values()), label='Average', linestyle='--', color='black')

    plt.axhline(y=0, color='red', linestyle='--', label='Zero Line')

    plt.xlabel(f'{time_granularity}', fontsize = 14)
    plt.ylabel(f'{validation_metric}', fontsize = 14)
    if total == True:
        plt.title(f'{validation_metric} (total mean) by {time_granularity} Averaged Across All Sites', fontsize = 26)

    else:
        plt.title(f'{validation_metric} (specific mean) by {time_granularity} Averaged Across All Sites', fontsize = 26)
        

    plt.tick_params(axis='x', labelsize = 20)
    plt.tick_params(axis='y', labelsize = 16)

    plt.ylim(lim)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    if total == True:
        plt.savefig(os.path.join(plots_path, 'time', f'{time_granularity}ly_{validation_metric}_tot.png'), dpi=300)

    else:
        plt.savefig(os.path.join(plots_path, 'time', f'{time_granularity}ly_{validation_metric}_spe.png'), dpi=300)

    plt.show()
    
    

def time_box_plot(mean, validation_metric, time_granularity, plots_path, lim, total=False):
    fig, ax = plt.subplots(figsize=(16, 8))

    months = sorted(mean[list(mean.keys())[0]].keys()) 
    data = [[mean[site][month] for site in mean] for month in months]

    boxprops = dict(facecolor='#99E4F5', color='#3D4CD7')
    plt.boxplot(data, positions=np.array(range(1, len(months)+1)), widths=0.4, patch_artist=True, boxprops=boxprops)
    
    ax.set_xlabel(f'{time_granularity}')
    ax.set_ylabel(f'{validation_metric}')

    if total:
        ax.set_title(f'Boxplot for {validation_metric} (total mean) by {time_granularity}')
    else:
        ax.set_title(f'Boxplot for {validation_metric} (specific mean) by {time_granularity}')

    plt.ylim(lim)
    
    ax.set_xticks(range(1, len(months)+1))
    ax.set_xticklabels(months)
    
    filename = f'boxplot_{time_granularity}_{"tot" if total else "spe"}.png'
    plt.savefig(os.path.join(plots_path, 'time', filename), dpi=300)

    plt.show()

    
    
def categorical_box(merged_df, complexity_name, metric_name, plots_path, x_order=None, x_ticklabels=None, colors=['#56DBB8']):  
    plt.figure(figsize=(12, 6))
    sns.boxplot(x=complexity_name, y=metric_name, data=merged_df, order=x_order, palette=colors)
    
    if x_ticklabels:
        plt.xticks(range(len(x_ticklabels)), x_ticklabels)
        
    plt.title(f'{metric_name} grouped by {complexity_name}', fontsize = 20)
    plt.xlabel(complexity_name, fontsize = 20)
    plt.ylabel(metric_name, fontsize = 20)
    plt.xticks(rotation=45)
    plt.tick_params(axis='x', labelsize = 20)
    plt.tick_params(axis='y', labelsize = 20)    
    
    plt.grid(True)
    
    plt.savefig(os.path.join(plots_path, 'climate', f'{complexity_name}_{metric_name}.png'), dpi=300)
    
    plt.show()

    
    
def categorical_month_box(merged_df, complexity_name, validation, nmbe_mean_by_month):
    unique_classifications = merged_df[complexity_name].unique()
    unique_sites_df = pd.DataFrame({complexity_name: unique_classifications})
    
    
    sites_by_complexity = {}
    for classification in unique_classifications:
        sites_by_complexity[classification] = merged_df[merged_df[complexity_name] == classification]



    data_nmbe_by_complexity = {} 
    for classification, sites_df in sites_by_complexity.items():
        if isinstance(classification, float) and np.isnan(classification):
            print(f"Skipping NaN {complexity_name}")
            continue
    
        site_indices = sites_df.index
    
        nmbe_values = validation.loc[site_indices, 'nmbe']
        nrmse_daily_values = validation.loc[site_indices, 'nrmse_daily']
    
        keys_month = site_indices.intersection(nmbe_mean_by_month.keys())

        if not keys_month.empty: 
            average_nmbe_mean_by_month = {index: sum(nmbe_mean_by_month[key][index] for key in keys_month) / len(keys_month) for index in nmbe_mean_by_month[next(iter(keys_month))].keys()}
        
            data_nmbe = pd.DataFrame({f'Month_{i}': [nmbe_mean_by_month[key][i] for key in keys_month] for i in range(1, 13)})
        
            data_nmbe_by_complexity[classification] = data_nmbe
        else:
            print(f"No common keys found for {complexity_name} {classification}")

 

    boxplot_data = []
    climates = []
    for classification, data_nmbe in data_nmbe_by_complexity.items():
        nmbe_values = [data_nmbe[f'Month_{i}'] for i in range(1, 13)]
        boxplot_data.append(nmbe_values)
        climates.append(classification)
    
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    df = pd.DataFrame(boxplot_data, columns=months)

    custom_colors = ['#003327', '#089E7B', '#56DBB8', '#AFF8E2', '#C8F480', '#DCFFA3', '#EBFFD2']

    plt.figure(figsize=(20, 6))

    for i, classification in enumerate(climates):
        plt.boxplot(df.values[i], positions=[x + i * 0.13 for x in range(len(df.columns))], widths=0.11, patch_artist=True, boxprops=dict(facecolor=custom_colors[i]))
    
    plt.xticks(range(len(df.columns)), df.columns)
    plt.xlabel('Month')
    plt.ylabel('Value')
    plt.title('Boxplot for Different Climate Classifications')

    legend_elements = [Patch(facecolor=color, edgecolor='black', label=label) for color, label in zip(custom_colors, climates)]
    plt.legend(handles=legend_elements)

    plt.grid(True)
    plt.show()
