import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

folders = ['C', 'C++', 'Java', 'Python']
metrics = ['CountLineCode', 'MaxCyclomatic', 'MaxNesting', 'SumCyclomatic']

for folder in folders:
    df = pd.read_csv('C:/Users/AVAKSon/Desktop/about time/backup 4 final/' + folder + '/csv/' + folder + '_edited.csv')
    filtered_df = df[df['Kind'].isin(['File', 'Module File'])]
    for metric in metrics:
        metric_data = filtered_df[metric]
        mean_val = np.mean(metric_data)
        median_val = np.median(metric_data)
        std_dev = np.std(metric_data)
        min_val = np.min(metric_data)
        max_val = np.max(metric_data)
        print(folder + ' statistic:\n')
        print(metric + ':\n')
        print("Mean: ", mean_val)
        print("Median: ", median_val)
        print("Standard Deviation: ", std_dev)
        print("Minimum: ", min_val)
        print("Maximum: ", max_val)


        # Shapiro-Wilk Test
        shap_stat, shap_p = stats.shapiro(metric_data)
        print("\nShapiro-Wilk Statistic: ", shap_stat)
        print("Shapiro-Wilk P-value: ", shap_p)
        # Kolmogorov-Smirnov Test
        ks_stat, ks_p = stats.kstest(metric_data,'norm')
        print("Kolmogorov-Smirnov Statistic: ", ks_stat)
        print("Kolmogorov-Smirnov P-value: ", ks_p)
        print('----------------------------------------------------')

        filtered_df = df[df['Kind'].isin(['File', 'Module File'])]

        filtered_df = filtered_df.reset_index()
        plt.figure(figsize=(12,9))
        file_data = filtered_df[filtered_df['Kind'] == 'File']
        module_file_data = filtered_df[filtered_df['Kind'] == 'Module File']
        plt.plot(file_data.index + 1, file_data[metric], label='File', color = 'blue')
        plt.plot(module_file_data.index + 1, module_file_data[metric], label='Module File', color = 'blue')
        plt.xlabel(folder, fontsize=35)
        plt.ylabel(metric, fontsize=35)
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.show()