import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def time_frame_plot_etfs(df_etfs, eu_stock_symbols, suptitle):
    time_frames = ['year_month', 'month'] 
    titles = ['Year/month', 'Month']
    nticks = {'year_month': 15}
    step = 1
    # Plot F.T. European ETF opening prices
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=[15,6])
    fig.suptitle(t='European F.T. ETFs\' opening prices', fontsize=12)
    for ax_index, time_frame in enumerate(time_frames):
        # df open mean
        df_om = df_etfs[df_etfs['stock_symbol'].isin(eu_stock_symbols)].copy(deep=True)
        # Add year/month column only if needed to improve performance
        if time_frame == 'year_month':
            df_om['year_month'] = df_om['year'].astype('string') + '-' + df_om['month'].astype('string')
        df_om = df_om.groupby(
                by=[time_frame, 'stock_symbol'], as_index=False
            )['open'].mean().rename(columns={'open':'open_mean'})
        
        plot_op = sns.lineplot(data=df_om, x=df_om[time_frame], y=df_om['open_mean'],
                                hue=df_om['stock_symbol'], legend='auto', ax=axes[ax_index]
                              )
        xtick_labels = plot_op.get_xticklabels()
        displayed_xtick_labels = []
        if len(xtick_labels) > 15:
            step = int(np.floor(len(xtick_labels) / nticks[time_frame]))
        for index in range(0, len(xtick_labels)-1, step):
            displayed_xtick_labels.append(xtick_labels[index])
        
        plot_op.set( # Note that the .set method is possible since sns.lineplot() 
                     # returns a matplotlib.axes.Axes
                title= titles[ax_index],
                xlabel=time_frame, ylabel='Avg open price'
            )
        if time_frame == 'year_month':
             plot_op.set_xticks(ticks=range(0, len(xtick_labels), step), labels=displayed_xtick_labels, rotation=70)