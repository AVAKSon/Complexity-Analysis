import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


languages = ['C', 'C++', 'Java', 'Python']
directories = ['C:/Users/AVAKSon/Desktop/about time/C', 'C:/Users/AVAKSon/Desktop/about time/C++', 'C:/Users/AVAKSon/Desktop/about time/Java', 'C:/Users/AVAKSon/Desktop/about time/Python']
results = {}
for lang, dir in zip(languages, directories):
    file_paths = glob.glob(os.path.join(dir, '*'))
    token_counts = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tokens = content.split()
            token_counts.append(len(tokens))

    stats_dict = {
            'mean': np.mean(token_counts),
            'median': np.median(token_counts),
            'std_dev': np.std(token_counts),
            'min': np.min(token_counts),
            'max': np.max(token_counts)
        }

    results[lang] = (token_counts, stats)
    ks_statistic, ks_pvalue=stats.kstest(rvs=token_counts,cdf='norm')

    sw_statistic, sw_pvalue=stats.shapiro(x=token_counts)
    stats_dict['Kolmogorov-Smirnov'] = (ks_statistic, ks_pvalue)
    stats_dict['Shapiro-Wilk'] = (sw_statistic, sw_pvalue)

    results[lang] = (token_counts,stats_dict)

fig, axs = plt.subplots(len(languages), figsize=(12,8))

for ax,(lang,data) in zip(axs.flat,results.items()):
    print(f"{lang} Stats: {data[1]}")
    ax.plot(data[0])
    ax.set(xlabel='Algorithm Index', ylabel='Token Count',
           title=f'Token count per Algorithm ({lang})')
plt.tight_layout()
plt.show()