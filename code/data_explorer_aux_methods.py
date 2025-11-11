import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def time_frame_plot_etfs(df_etfs, stock_symbols, suptitle_part):
    time_frames = ['year_month', 'month'] 
    titles = ['Year/month', 'Month']
    nticks = {'year_month': 15}
    step = 1
    # Plot F.T. European ETF opening prices
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=[15,6])
    fig.suptitle(t=f'{suptitle_part} F.T. ETFs\' opening prices', fontsize=12)
    for ax_index, time_frame in enumerate(time_frames):
        # df open mean
        df_om = df_etfs[df_etfs['stock_symbol'].isin(stock_symbols)].copy(deep=True)      
        df_om = df_om.groupby(
                by=[time_frame, 'stock_symbol'], as_index=False
            )['open'].mean().rename(columns={'open':'open_mean'})#
        
        
        # Since there is not yeaar-month representation while keeping
        # the datetime (timestamp(?)) type, use strftime to get xtick_label 
        if time_frame == 'year_month':
            x_s = df_om[time_frame].dt.strftime('%Y-%m')
        else:
            x_s = df_om[time_frame]
        plot_op = sns.lineplot(data=df_om, x=x_s, y=df_om['open_mean'],
                               hue=df_om['stock_symbol'], 
                               hue_order=df_om['stock_symbol'].copy().drop_duplicates().sort_values(),
                               legend='auto', ax=axes[ax_index]
                              )
        
        xtick_labels = plot_op.get_xticklabels() #unique x labels
        displayed_xtick_labels = []
        if len(xtick_labels) > 15:
            step = int(np.floor(len(xtick_labels) / nticks[time_frame]))
        for index in range(0, len(xtick_labels)-1, step):
            displayed_xtick_labels.append(xtick_labels[index])
        
        plot_op.set( # Note that the .set method is possible since sns.lineplot() 
                     # returns a matplotlib.axes.Axes
                title=titles[ax_index],
                xlabel=time_frame, ylabel='Avg open price'
            )
        if time_frame == 'year_month':
            plot_op.set_xticks(ticks=range(0, len(xtick_labels), step), labels=displayed_xtick_labels, rotation=70)