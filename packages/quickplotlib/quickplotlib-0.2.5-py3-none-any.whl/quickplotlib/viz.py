#!/usr/bin/env python
# coding: utf-8

# In[ ]:

"""
Version:
--------
- quickplot v0.2.4
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

def bar(table, key_column, value_column, title= None, x_label= None, y_label= None, frame_dimensions= (12, 9), error_column= None, show_mean= True, annotate= True, process_data_type= True, **kwargs):

    df = table.copy()
    
    if process_data_type:
        df[value_column] = df[value_column].astype(float)
        
        if error_column is not None:
            df[error_column] = df[error_column].astype(float)
            
    x = df[key_column]
    y = df[value_column]
    
    fig = plt.figure(figsize= frame_dimensions)
    ax = plt.gca()
    
    ax.tick_params(axis= 'x', which= 'both', bottom= False, top= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.tick_params(axis= 'y', which= 'both', left= False, right= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False);
    ax.spines['bottom'].set_visible(False);ax.spines['left'].set_visible(False)

    plt.title(title, fontsize= 18, alpha= 0.8, pad= 15)
    plt.xlabel(x_label, fontsize= 16, alpha= 0.8)
    plt.ylabel(y_label, fontsize= 16, alpha= 0.8)
    
    keys = df[key_column].nunique()
    width = ax.get_ylim()[1] / keys
    
    if error_column is not None:
        yerr = df[error_column]
        bars = plt.bar(x, y, yerr= yerr, ecolor= '0.4', capsize= width / 7.5 * 100, color= '#f28e2b', **kwargs)
    
    if error_column is None:
        bars = plt.bar(x, y, color= '#f28e2b', **kwargs)
    
    if show_mean:
        mean = y.mean()
        line = plt.axhline(mean, color= '0.4', dashes= [len(x), len(x) / 2])

    if annotate:
        ymax = ax.get_ylim()[np.argmax(np.abs(ax.get_ylim()))]
        for bar in ax.patches:
            yval = bar.get_height()
            xval = bar.get_width()
            if yval > 0:
                plt.text(bar.get_x() + (xval / 4), yval + (np.abs(ymax) * 0.025), str(round(yval, 2)), va= 'center', ha= 'center'
                         , color= '0.2', size= 12, fontweight= 'normal', rotation= 'horizontal')
            if yval <= 0:
                plt.text(bar.get_x() + (xval / 4), yval - (np.abs(ymax) * 0.025), str(round(yval, 2)), va= 'center', ha= 'center'
                         , color= '0.2', size= 12, fontweight= 'normal', rotation= 'horizontal')

        if show_mean:
            if mean <= (ax.patches[-1].get_height() + ax.patches[-1].get_height() * (np.abs(ymax) * 0.025)):
                placement = np.argmin([bar.get_height() for bar in ax.patches])
                plt.text(ax.patches[placement].get_x() + ax.patches[placement].get_width() / 2, mean + ymax * 0.025, str(round(mean, 2))+' (mean)'
                         , va= 'center', ha= 'center', color='0.2', size= 12, fontweight= 'normal')
            else:
                placement = -1
                plt.text(ax.patches[placement].get_x() + ax.patches[placement].get_width() / 2, mean + ymax * 0.025, str(round(mean, 2))+' (mean)'
                         , va= 'center', ha= 'center', color='0.2', size= 12, fontweight= 'normal')

    plt.tight_layout()
    plt.show()
    
def segmented_bar(table, segment_column, key_column, value_column, title= None, x_label= None, y_label= None, frame_dimensions= (12, 9), error_column= None, show_mean= True, annotate= True, process_data_type= True, **kwargs):
    
    df = table.copy()
    
    if process_data_type:
        df[value_column] = df[value_column].astype(float)
        
        if error_column is not None:
            df[error_column] = df[error_column].astype(float)
                
    groups = df[segment_column].nunique()
    keys = df[key_column].nunique()
        
    fig = plt.figure(figsize= frame_dimensions)
    ax = plt.gca()
    
    ax.tick_params(axis= 'x', which= 'both', bottom= False, top= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.tick_params(axis= 'y', which= 'both', left= False, right= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False);
    ax.spines['bottom'].set_visible(False);ax.spines['left'].set_visible(False)

    plt.title(title, fontsize= 18, alpha= 0.8, pad= 15)
    plt.xlabel(x_label, fontsize= 16, alpha= 0.8)
    plt.ylabel(y_label, fontsize= 16, alpha= 0.8)
    
    if error_column is not None:
        std_err = df.pivot_table(index= key_column, columns= segment_column, values= error_column)
        df = df.pivot_table(index= key_column, columns= segment_column, values= value_column)
        
        ind = np.arange(keys)    # the x locations for the groups
        width = ax.get_ylim()[1] / keys   # the width of the bars

        for group in np.arange(groups):
            ax.bar(ind + (width * group), df[df.columns[group]], width
                   , ecolor= '0.4', capsize= width / 10 * 100, yerr= std_err[std_err.columns[group]], **kwargs)
    
    if error_column is None:
        df = df.pivot_table(index= key_column, columns= segment_column, values= value_column)
        
        ind = np.arange(keys)    # the x locations for the groups
        width = ax.get_ylim()[1] / keys   # the width of the bars

        for group in np.arange(groups):
            ax.bar(ind + (width * group), df[df.columns[group]], width, **kwargs)
            
    ax.set_xticks(ind + width / groups)
    ax.set_xticklabels(df.index)

    legend = ax.legend([group for group in df.columns], fontsize= 12, frameon= False)
    
    for text in legend.get_texts():
        text.set_color('0.2')
    
    if show_mean:
        mean = df.mean().mean()
        line = plt.axhline(mean, color= '0.4', dashes= [width * 7.5, width * 5])

    if annotate:
        ymax = ax.get_ylim()[np.argmax(np.abs(ax.get_ylim()))]
        for bar in ax.patches:
            yval = bar.get_height()
            xval = bar.get_width()
            if yval > 0:
                plt.text(bar.get_x() + (xval * 0.05), yval + (np.abs(ymax) * 0.025), str(round(yval, 2)), va= 'center', ha= 'left'
                         , color= '0.2', size= 12, fontweight= 'normal', rotation= 'horizontal')
            if yval <= 0:
                plt.text(bar.get_x() + (xval * 0.05), yval - (np.abs(ymax) * 0.025), str(round(yval, 2)), va= 'center', ha= 'left'
                         , color= '0.2', size= 12, fontweight= 'normal', rotation= 'horizontal')

        if show_mean:
            if mean <= (ax.patches[-1].get_height() + ax.patches[-1].get_height() * (np.abs(ymax) * 0.025)):
                placement = np.argmin([bar.get_height() for bar in ax.patches])
                plt.text(ax.patches[placement].get_x() + ax.patches[placement].get_width() / 2, mean + ymax * 0.025, str(round(mean, 2))+' (mean)'
                         , va= 'center', ha= 'center', color='0.2', size= 12, fontweight= 'normal')
            else:
                placement = -1
                plt.text(ax.patches[placement].get_x() + ax.patches[placement].get_width() / 2, mean + ymax * 0.025, str(round(mean, 2))+' (mean)'
                         , va= 'center', ha= 'center', color='0.2', size= 12, fontweight= 'normal')

    plt.tight_layout()
    plt.show()
    
def plot_distribution(table, value_column, segment_column= None, title= None, x_label= None, y_label= None, frame_dimensions= (12, 9), kde= False, bins= None, process_data_type= True, log10_transform= False, **kwargs):
    
    df = table.copy()
    
    if process_data_type:
        for column in [column for column in df.columns if column != segment_column]:
            try:
                df[column] = df[column].astype(float)
            except:
                pass
    
    if log10_transform:
        for column in df[[column for column in df.columns if column != segment_column]].columns:
            if 0 in df[column].values:
                df[column] = np.log10(df[column] + 1) 
                if (float('inf') in df[column].values) | (float('-inf') in df[column].values):
                    return 'Error. You may be applying a log10 transformation on an incompatible distribution. Transformation resulted in infinity.'
            else:
                df[column] = np.log10(df[column])
    
    if segment_column is None:
        if bins is None:
            sns.distplot(df[value_column], kde= kde, **kwargs)
        else: 
            sns.distplot(df[value_column], kde= kde, bins= bins, **kwargs)
            
        fig = plt.gcf() 
        ax = plt.gca()
        fig.set_size_inches(frame_dimensions[0], frame_dimensions[1])
            
    if segment_column is not None:
        if bins is None:
            for segment in sorted(df[segment_column].unique()):
                sns.distplot(df[df[segment_column] == segment][value_column], kde= kde, label= segment, **kwargs)
        else: 
            for segment in sorted(df[segment_column].unique()):
                sns.distplot(df[df[segment_column] == segment][value_column], kde= kde, label= segment, bins= bins, **kwargs)
    
        fig = plt.gcf() 
        ax = plt.gca()
        fig.set_size_inches(frame_dimensions[0], frame_dimensions[1])

        legend = ax.legend(fontsize= 12, frameon= False)
        for text in legend.get_texts():
            text.set_color('0.2')
            
    plt.title(title, fontsize= 18, alpha= 0.8, pad= 15)
    plt.xlabel(x_label, fontsize= 16, alpha= 0.8)
    plt.ylabel(y_label, fontsize= 16, alpha= 0.8)
    
    ax.tick_params(axis= 'x', which= 'both', bottom= False, top= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.tick_params(axis= 'y', which= 'both', left= False, right= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False);
    ax.spines['bottom'].set_visible(False);ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.show()
    
def plot_distribution_summary(table, value_column, segment_column= None, title= None, x_label= None, y_label= None, frame_dimensions= 'auto', horizontal= True, violin= False, process_data_type= True, log10_transform= False, **kwargs):
    
    df = table.copy()
    
    if process_data_type:
        for column in [column for column in df.columns if column != segment_column]:
            try:
                df[column] = df[column].astype(float)
            except:
                pass
    
    if log10_transform:
        for column in df[[column for column in df.columns if column != segment_column]].columns:
            if 0 in df[column].values:
                df[column] = np.log10(df[column] + 1) 
                if (float('inf') in df[column].values) | (float('-inf') in df[column].values):
                    return 'Error. You may be applying a log10 transformation on an incompatible distribution. Transformation resulted in infinity.'
            else:
                df[column] = np.log10(df[column])
                
    if horizontal == True:
        orient= 'h'
    if horizontal == False:
        orient= 'v'
    
    if violin:
        if horizontal:
            sns.violinplot(x= value_column, y= segment_column, data= df, orient= orient, **kwargs)
            if frame_dimensions == 'auto':
                fig = plt.gcf() 
                ax = plt.gca()
                
                if segment_column is not None:
                    fig.set_size_inches(12, 2 * df[segment_column].nunique()) 
                else:
                    fig.set_size_inches(12, 2) 

        else:
            sns.violinplot(x= segment_column, y= value_column, data= df, orient= orient, **kwargs)
            if frame_dimensions == 'auto':
                fig = plt.gcf() 
                ax = plt.gca()
                
                if segment_column is not None:
                    fig.set_size_inches(2 * df[segment_column].nunique(), 12) 
                else:
                    fig.set_size_inches(2, 12) 
    else: 
        if horizontal:
            sns.boxplot(x= value_column, y= segment_column, data= df, orient= orient, **kwargs)
            if frame_dimensions == 'auto':
                fig = plt.gcf() 
                ax = plt.gca()
                
                if segment_column is not None:
                    fig.set_size_inches(12, 1.25 * df[segment_column].nunique()) 
                else:
                    fig.set_size_inches(12, 1.25) 

        else:
            sns.boxplot(x= segment_column, y= value_column, data= df, orient= orient, **kwargs)
            if frame_dimensions == 'auto':
                fig = plt.gcf() 
                ax = plt.gca()
                
                if segment_column is not None:
                    fig.set_size_inches(1.25 * df[segment_column].nunique(), 12) 
                else:
                    fig.set_size_inches(1.25, 12) 
                    
    if frame_dimensions != 'auto':
        fig = plt.gcf() 
        ax = plt.gca()
        fig.set_size_inches(frame_dimensions[0], frame_dimensions[1])
            
    plt.title(title, fontsize= 18, alpha= 0.8, pad= 15)
    plt.xlabel(x_label, fontsize= 16, alpha= 0.8)
    plt.ylabel(y_label, fontsize= 16, alpha= 0.8)
    
    ax.tick_params(axis= 'x', which= 'both', bottom= False, top= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.tick_params(axis= 'y', which= 'both', left= False, right= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False);
    ax.spines['bottom'].set_visible(False);ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.show()
    
def scatter(table, x_column, y_column, segment_column= None, title= None, x_label= None, y_label= None, frame_dimensions= (12, 9), process_data_type= True, log10_transform= False, **kwargs):

    df = table.copy()
    
    if process_data_type:
        for column in [column for column in df.columns if column != segment_column]:
            try:
                df[column] = df[column].astype(float)
            except:
                pass
    
    if log10_transform:
        for column in df[[column for column in df.columns if column != segment_column]].columns:
            if 0 in df[column].values:
                df[column] = np.log10(df[column] + 1) 
                if (float('inf') in df[column].values) | (float('-inf') in df[column].values):
                    return 'Error. You may be applying a log10 transformation on an incompatible distribution. Transformation resulted in infinity.'
            else:
                df[column] = np.log10(df[column])
    
    if segment_column is not None:
        sns.scatterplot(x= df[x_column], y= df[y_column], hue= df[segment_column]
                        , linewidth= 0, alpha= 0.75, **kwargs
                       )
    else:
        sns.scatterplot(x= df[x_column], y= df[y_column]
                        , linewidth= 0, alpha= 0.75, **kwargs
                       )
        
    fig = plt.gcf() 
    ax = plt.gca()
    fig.set_size_inches(frame_dimensions[0], frame_dimensions[1])
    
    plt.title(title, fontsize= 18, alpha= 0.8, pad= 15)
    plt.xlabel(x_label, fontsize= 16, alpha= 0.8)
    plt.ylabel(y_label, fontsize= 16, alpha= 0.8)
    
    if segment_column is not None:
        legend = ax.legend(fontsize= 12, frameon= False)
        for text in legend.get_texts():
            text.set_color('0.2')
    
    ax.tick_params(axis= 'x', which= 'both', bottom= False, top= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.tick_params(axis= 'y', which= 'both', left= False, right= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False);
    ax.spines['bottom'].set_visible(False);ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.show()
    
def pairplot(table, segment_column= None, title= None, frame_dimensions= (12, 10), hist= False, process_data_type= True, log10_transform= False, **kwargs):
   
    df = table.copy()

    if process_data_type:
        for column in [column for column in df.columns if column != segment_column]:
            try:
                df[column] = df[column].astype(float)
            except:
                pass
    
    if log10_transform:
        for column in df[[column for column in df.columns if column != segment_column]].columns:
            if 0 in df[column].values:
                df[column] = np.log10(df[column] + 1) 
                if (float('inf') in df[column].values) | (float('-inf') in df[column].values):
                    return 'Error. You may be applying a log10 transformation on an incompatible distribution.'
            else:
                df[column] = np.log10(df[column])

    if segment_column is not None: 
        if hist:
            g = sns.pairplot(df, hue= segment_column, diag_kind= 'hist'
                                 , plot_kws= {'linewidth': 0, 'alpha': 0.5}
                                 , diag_kws= {'alpha': 0.5}
                                 , **kwargs
                                )
        else:
            g = sns.pairplot(df, hue= segment_column, diag_kind= 'auto'
                                 , plot_kws= {'linewidth': 0, 'alpha': 0.5}
                                 , **kwargs
                                )
    else: 
        g = sns.pairplot(df, hue= segment_column, diag_kind= 'auto'
                             , plot_kws= {'linewidth': 0}
                             , **kwargs
                            )

    fig = plt.gcf() 
    ax = plt.gca()
    fig.set_size_inches(frame_dimensions[0], frame_dimensions[1])
    
    g._legend.remove()
    plt.legend(bbox_to_anchor=(1.05, 1), loc= 2, borderaxespad= 0.1, title= segment_column, frameon= False)
            
    plt.suptitle(title, fontsize= 18, alpha= 0.8, y= 1.1)
    
    ax.tick_params(axis= 'x', which= 'both', bottom= False, top= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.tick_params(axis= 'y', which= 'both', left= False, right= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False);
    ax.spines['bottom'].set_visible(False);ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.show()
    
def correlation_heatmap(table, title= None, frame_dimensions= (12, 9), annotate= True, color_map= 'Diverging', color_blind= False, segment_column= None, segment= None, process_data_type= True, correction_margin= False, log10_transform= False, **kwargs):
    
    df = table.copy()
    
    if (segment_column is not None) & (segment is not None):
        df = df[df[segment_column] == segment]
    
    if process_data_type:
        for column in [column for column in df.columns if column != segment_column]:
            try:
                df[column] = df[column].astype(float)
            except:
                pass
    
    if log10_transform:
        for column in df[[column for column in df.columns if column != segment_column]].columns:
            if 0 in df[column].values:
                df[column] = np.log10(df[column] + 1) 
                if (float('inf') in df[column].values) | (float('-inf') in df[column].values):
                    return 'Error. You may be applying a log10 transformation on an incompatible distribution. Transformation resulted in infinity.'
            else:
                df[column] = np.log10(df[column])
    
    if color_map == 'Diverging':
        if color_blind:
            sns.heatmap(df.corr(), cmap= 'viridis', vmin= -1, vmax= 1, annot= annotate, **kwargs)
        else:
            sns.heatmap(df.corr(), cmap= 'RdBu_r', vmin= -1, vmax= 1, annot= annotate, **kwargs)
    else:
        sns.heatmap(df.corr(), cmap= color_map, vmin= -1, vmax= 1, annot= annotate, **kwargs)

    fig = plt.gcf() 
    ax = plt.gca()
    fig.set_size_inches(frame_dimensions[0], frame_dimensions[1])

    if correction_margin:     
        adjustment = 0.5
        bottom, top = ax.get_ylim()
        ax.set_ylim(bottom + adjustment, top - adjustment)
    
    plt.title(title, fontsize= 18, alpha= 0.8, pad= 15)
    
    ax.tick_params(axis= 'x', which= 'both', bottom= False, top= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.tick_params(axis= 'y', which= 'both', left= False, right= False, color= '0.2'
                   , labelcolor= '0.2', grid_alpha= 0.8, labelsize = 12)
    ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False);
    ax.spines['bottom'].set_visible(False);ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.show()

