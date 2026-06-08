""" Plots and utility functions for plotting """

import pandas as pd
import scipy.stats as stats
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches


REGIMES = {
    'GFC': ['2007-08-01', '2009-03-31', 'red'],
    'Covid_Crash': ['2020-02-01', '2020-03-31', 'orange'],
    'Post_Covid': ['2020-04-01', '2021-12-31', 'green'],
    '2022_Shock': ['2022-01-01', '2022-12-31', 'purple'],
}


def shade_regimes(ax, regimes=REGIMES):
    """
    Shade crisis/regime periods on any time series axis.
    Call after plotting your main series.
    """
    handles = []
    for label, [start, end, color] in regimes.items():
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end),
                   alpha=0.17, color=color, label=label)
        handles.append(mpatches.Patch(color=color, alpha=0.15+0.2, label=label))
    return handles


def plot_QQ(log_returns: pd.DataFrame):
    columns = log_returns.columns
    fig, ax = plt.subplots(4, 2, figsize=(20,24))
    for i, a in enumerate(ax.flat):
        if i >= len(columns):
            break
        stats.probplot(log_returns[columns[i]], dist='norm', plot=a)
        a.set_title(f"{columns[i]} vs Normal distribution")