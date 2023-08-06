#import necessary libraries

import numpy as np
import pandas as pd
import csv
from datetime import datetime, timedelta, time
import datetime as dt
from statsmodels.tsa.stattools import acf
from statsmodels.graphics.tsaplots import plot_acf
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import matplotlib.dates as md
import os


#Set seaborn as default plotting style
sns.set(style="ticks") 
pd.plotting.register_matplotlib_converters()


def set_my_path(pyname, folder ): 
    if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(pyname),folder))) == False:
        os.makedirs(os.path.abspath(os.path.join(os.path.dirname(pyname),folder)))
    
    return os.path.abspath(os.path.join(os.path.dirname(pyname),folder))


# Find path of the required file. Output: root path
def find_my_file(filename):
    for root, dirs, files in os.walk("C:\Spider_project"):
        for name in files:
            if name == filename:
                your_file = os.path.abspath(os.path.join(root, name))
    return your_file

# Calculate days number of the experiment recording
def calculate_days(df):
    days = df.groupby('Date')
    days_number=len(days)
    return days_number

# Download original recording and delete incomplete days. 
def download_complete_days(csv_file):
    day = 24*60
    # download data and add DateTime index
    df=pd.read_csv(csv_file)
    df.index=pd.to_datetime(df.Date+' '+df.Time, dayfirst=True)
    df.index.name = 'DateTime'
    days = df.groupby('Date')
    day_length=days.size() 
    days_number=len(days) 
    
    # remove incomplete days
    for n in range(0, days_number):
        if day_length[n]!= day:
            df=df[df.Date!=day_length.index[n]]
    df = df.drop(columns = 'Unnamed: 0')
    return df

# Separate LD and DD conditions of the original recording.
def split_LD_DD(data):
    # find mean of light values for each date
    mylights=data.groupby('Date')['lights'].mean()
    # if mean != 0, then it's LD, else DD. Write indexes of LD and DD days
    ld_days = mylights.index[mylights!=0]
    dd_days = mylights.index[mylights==0]
    # find indexes of LD and DD days in the  original dataframe. Create new dataframes based on mathced indexes
    df_LD = data[data['Date'].isin(ld_days)]
    df_DD = data[data['Date'].isin(dd_days)]
    return (df_LD, df_DD)

# Create dataframe to store results of ACF function.
# Input: LD/DD/original dataframe, number of lags (36 for this analysis). Output: dataframe with ACF
def make_df_acf(df,m_lag):
    # create list of columns with spider's IDs
    spiders = df.columns[3:]
    # create  1 minute time step as an index
    time = np.arange(0, m_lag*60+1)/60.
    # create autocorrelation dataframe
    acf_df = pd.DataFrame(columns = spiders, index= time)
    for s in spiders:
        acf_df[s]= acf(df[s], nlags=m_lag*60, fft=True)
    return(acf_df)

#Create an frp dataframe and save it to csv
def frp_dataframe(df_DD_acf, spider_list):
    frp_df = pd.DataFrame(columns = ['FRP', 'corr'], index= spider_list)
    for i in range(0,len(spider_list)):
        frp_df.loc[spider_list[i]] = find_peak(df_DD_acf, spider_list[i])
        frp_df.to_csv('frp.csv')
    return frp_df

# Find peak, or FRP value, using ACF. 
# Input:  autocorrelation dataframe, list of spiders. Output: FRP in hours and correlation value.
def find_peak(df,spider):
    # set minimum value for FRP (15h) and cut off dataframe
    switch = 15
    df_new = df.truncate(before=switch)
    # find max value. peak will contain index 
    peak = df_new[spider].values.argmax()
    # xpeak is time in hours (if input was produced by make_df_acf function)
    xpeak = df_new.index[peak]
    # ypeak is value of autocorrelation (-//-)
    ypeak = df_new[spider].iloc[peak]
    return xpeak, ypeak

# Find threshold of activity onset. 
# Input: original dataframe, 1-day dataframe, list of spiders, required coefficient (0.2 for all species for this analysis). Output: threshold value
def find_threshold(data, data_2, spider, coef): 
    # find mean activity for all days
    mean_full_activity = data[spider].mean()
    # find mean activity for one day
    mean_day_activity = data_2[spider].mean()
    # find std for all days and one day
    full_std = data[spider].std()
    day_std = data_2[spider].std()
    # find higher mean value. Add std multiplied by a required coefficient.
    if mean_full_activity>= mean_day_activity:
        threshold  = mean_full_activity  + coef*full_std
    else:
        threshold = mean_day_activity+ coef*day_std  
    return threshold


# Find activity onset in the evening dark condition.
# Input: number of positive counts, difference, threshold, 1-day dataframe, cutoff-dataframe, switch_time, list of spider's IDs.
# Output: time of activity onset and number of crossing at that time.
def find_onset(pos_count, difference, threshold, data_2, data_3,switch_time, spider):
    #if spider is idle during dark period -> no onset - make nan
    #if mean_switch_activity <= 2.0:
     #   onset = np.nan
       # time_minutes = np.nan
       # #return for time a timestamp, so plotting will be w/o errors. It doesn't mean that spider have time of onset.
       # time_of_onset =  data_2.index[0]
    # if there is no positive counts, we deal with noise or unactive spider, set onset to NaN . 
    if pos_count == 0:
        onset = np.nan
        time_minutes = np.nan
        time_of_onset = data_2.index[0]
    # else activity is a value above our threshold ( Notice that actually activity should be above double threshold). 
    else:
        # difference = x - threshold,
        # difference>=t -> x>= 2*threshold
        activity = data_3[spider][(difference >= threshold)]
        # onset is the first value of activity list
        onset = activity[0] 
        time_of_onset = activity.index[0]
        # return time in minutes from turning lights off to spider being active
        time_minutes = (time_of_onset - switch_time).total_seconds()/60.
    return onset, time_of_onset, time_minutes
    
# create empty lists
def empty_lists():
    onset_l = []    
    time_of_onset_l = []
    time_minutes_l = []
    return [onset_l, time_of_onset_l, time_minutes_l]
# find a timestamp, when lights turn off

def find_switch_time(df, spider):
    time = df[spider].index[df.lights == 1][-1]
    # false 'onset' during switch time can be detected. to avoid it, take 1 min step from the switch.
    switch_time = time + dt.timedelta(minutes = 1)
    return switch_time

# fill empty lists
def completed_lists(onset_list, onset, time_of_onset_list, time_of_onset, time_minutes_list, time_minutes):
    onset_list.append(onset)
    time_of_onset_list.append(time_of_onset)
    time_minutes_list.append(time_minutes) 
    return onset_list, time_of_onset_list, time_minutes_list

# create a dataframe with recording after lights are off, find activity after switch
def find_switch_activity(df, switch_time, spider):
    # create dataframe which will store only values after one minute of lights being off
    df_onset = df.truncate(before=switch_time)
    # find mean spider's activity after switch_time # don't need in update?
    mean_switch_activity = df_onset[spider].mean()
    return df_onset, mean_switch_activity

# write onsets for each spider
def write_onset(dataframe, spider):
    days_number=calculate_days(dataframe)
    day = 24*60
    # create empty lists to store  all necessary values
    onset_list, time_of_onset_list, time_minutes_list = empty_lists()
    #loop through all days
    for i in range(0, days_number):         
        # create 1-day dataframe 
        new_f = pd.DataFrame(dataframe.iloc[i*day:day+i*day])
        # find switch time. 
        switch_time = find_switch_time(new_f, spider)  
        # keep only part of dataframe of evening dark condition, find mean activity during this period
        df_onset, mean_switch_activity = find_switch_activity(new_f, switch_time, spider)
        # find the threshold
        threshold = find_threshold(dataframe,new_f, spider, 0.2)
        #calculate difference between the threshold and spider's activity
        difference = df_onset.apply(lambda x: x[spider]-threshold, axis=1)
        #calculate how much positive difference values are there
        pos_count = len(list(filter(lambda x: (x >= 0), difference)))
        # find onsets and times (timestamp and time in minutes between turnong lights off and activity onset)
        onset, time_of_onset, time_minutes = find_onset(pos_count, difference, threshold, new_f, df_onset, switch_time, spider)
        # write lists of all values which we will use in the future
        onset_list, time_of_onset_list, time_minutes_list = completed_lists(onset_list, onset, time_of_onset_list, time_of_onset, time_minutes_list, time_minutes)
    return onset_list, time_of_onset_list, time_minutes_list

#create onset dataframe
def onset_dataframe(LD_dataframe, spider_list):
    onset_df = pd.DataFrame(columns = spider_list,  index = LD_dataframe.Date.unique())
    for i in range(0,len(spider_list)):
        onset, time, t = write_onset(LD_dataframe, spider_list[i])
        onset_df[spider_list[i]] = t
        onset_df.to_csv('onset.csv')
    return onset_df


# Prepare dataframe for linear regression model
def df_for_model(onset_dataframe, frp_dataframe, spider_list):
    df_for_model = pd.DataFrame(columns = ["Onset"], index = spider_list)
    # write onset column
    df_for_model.Onset = onset_dataframe[spider_list].mean()
    # create and write frp column
    df_for_model['FRP'] = frp_dataframe.FRP
    # save csv file
    df_for_model.to_csv('Onset(FRP).csv')
    return df_for_model

# Find linear regreassion to analyze if there is any correlation between time of activity onset and FRP.
# Input: df_for_model dataframe. Output: all required parameters
def lin_reg(dataframe):
    
    # prepare 2D array for linear regression model
    y = dataframe.Onset.values.reshape((-1,1)) #will return a np.array with values for the dates
    x = dataframe.FRP.values.reshape((-1,1))
    
    # create a linear regression object 
    model = LinearRegression()  
    # train model. We use same data for training and for prediction
    model.fit(x, y)
    y_pred = model.predict(x)
    
    # calculate the coefficient of determination of the prediction. 1 - perfect fit.
    r_sq = model.score(x, y)
    r, p_value = pearsonr(dataframe.FRP, dataframe.Onset)
    b0 = model.intercept_
    b1 =  model.coef_
    return(y_pred, r_sq, b0, b1, r, p_value)

# Create Raster plots with 24h spider's activity.
# Input: dataframe with original recordings of full fays, list of spider's IDs and jpeg filename. 
def plot_Raster(data, spider, filename):
    # get rid of warning
    plt.rcParams.update({'figure.max_open_warning': 0})
    days_number = calculate_days(data)
    fig, axes = plt.subplots(days_number, figsize=(13,16))
    day = 24*60
    # loop through all days
    for i in range(0, days_number):
        # create new dataframe which will contain information about one day
        new_f=pd.DataFrame(data.iloc[i*day:day+i*day])
        # plot this data (so plotting is day-by-day)
        sns.lineplot(x = new_f.index, y =  new_f[spider], color="b", ax=axes[i])
        # check values of lights and make a decision if it's LD or DD
        day_lights = new_f.lights.unique()
        if day_lights.mean()>0:            #it's LD
            # first gray bar
            axes[i].axvspan(new_f.index[0], new_f.index[new_f.lights == 1][0], alpha = 0.5, color = 'gray')
            # second gray bar                   
            axes[i].axvspan(new_f.index[new_f.lights == 1][-1], new_f.index[-1], alpha = 0.5, color = 'gray')
        else:                           #it's DD
            axes[i].axvspan(new_f.index[0],new_f.index[-1],alpha = 0.5, color = 'gray')
        
        # change ticks size, set labels and ax-limits, adjust subplots
        axes[i].tick_params(axis='both', which='major', labelsize=10)
        plt.subplots_adjust(hspace=.25)
        axes[i].set_ylabel(new_f.Date[i], fontsize=8)
        axes[i].set_xlabel('')
        axes[i].set_xlim(new_f.index[0],new_f.index[-1])
        # delete labels of x-axes except the last x-axis
        for ax in axes.flat:
            ax.label_outer()
    # make Date format in hours:minutes
    axes[i].xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    plt.savefig(filename)
# Make raster plots on the left panel and ACF plots on the right. 
# Input: LD/DD dataframe for raster plots, dataframe with applied rolled avarage (e.g 1 h), list of spider's IDs, jpeg filename
def plot_ACF_raster(raster_data, roll_data, spider, filename):
    # get rid of warning
    plt.rcParams.update({'figure.max_open_warning': 0})
    day = 24*60
    days_number=calculate_days(raster_data)
    # in this function two subplots tools are combined. grid will be used for the right panel
    grid = plt.GridSpec(days_number, 2)
    fig = plt.figure(figsize=(15,10))
    # first plot left panel
    # loop through the days
    for i in range(0, days_number):
        # for index we set 2i+1 so we will skip even indexes.
        axes = fig.add_subplot(days_number,2,2*i+1)
        new_f=pd.DataFrame(raster_data.iloc[i*day:day+i*day])
        sns.lineplot(x= new_f.index, y = new_f[spider], color="b", ax = axes)
        # check values of lights and make a decision if it is DD or LD
        
        day_lights = new_f.lights.unique()
        if day_lights.mean()>0:            #it's LD
            # first gray bar
            axes.axvspan(new_f.index[0], new_f.index[new_f.lights == 1][0], alpha = 0.5, color = 'gray')
            # second gray bar                   
            axes.axvspan(new_f.index[new_f.lights == 1][-1], new_f.index[-1], alpha = 0.5, color = 'gray')
        else:                           #it's DD
            axes.axvspan(new_f.index[0],new_f.index[-1],alpha = 0.5, color = 'gray')
        
        # change ticks size
        axes.tick_params(axis='both', which='major', labelsize=10)
        # make Date format in hours:minutes
        axes.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
        plt.subplots_adjust(hspace=.1)
        axes.set_ylabel(new_f.Date[i], fontsize=9)
        axes.set_xlabel('')
        axes.set_xlim(new_f.index[0],new_f.index[-1])
    for axes in plt.gcf().axes:
        try:
            axes.label_outer()
        except:
            pass
    # make Date format in hours:minute
    axes.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    # use grid to plot right panel
    ax2 = fig.add_subplot(grid[:, 1])
    # set my lag and plot acf. lag is 36, make sure to keep it consistent in all functions
    m_lag = 36
    plot_acf(roll_data[spider], ax=ax2, lags = m_lag*60, fft=True, title = None)
    df = make_df_acf(roll_data, m_lag)
    x_val, y_val =  find_peak(df, spider)
    # setting ticks
    ax2.tick_params(axis='both', which='major', labelsize=10)
    ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/60))
    ax2.xaxis.set_major_formatter(ticks)
    # x_val is in minutes, and ticks set for hours. Multiple to convert x_val                                 
    ax2.plot(x_val*60, y_val, marker='o', markersize = 10, color = 'r')
    
    plt.savefig(filename)
# Make raster plots w/ activity onsets marked as red crosses
def plot_Raster_onset(dataframe, spider, filename):

    days_number=calculate_days(dataframe)
    fig, axes = plt.subplots(days_number, figsize=(12,13))
    day = 24*60
    # loop through all days
    for i in range(0, days_number):
        # create new dataframe which will contain information about one day
        new_f=pd.DataFrame(dataframe.iloc[i*day:day+i*day])
        sns.lineplot(x = new_f.index, y = new_f[spider], color="b", ax=axes[i])
        # check values of lights and make a decision if it's LD or DD
        day_lights = new_f.lights.unique()
        if day_lights.mean()>0:            #it's LD
            #first gray bar
            axes[i].axvspan(new_f.index[0], new_f.index[new_f.lights == 1][0], alpha = 0.5, color = 'gray')
            #second gray bar                   
            axes[i].axvspan(new_f.index[new_f.lights == 1][-1], new_f.index[-1], alpha = 0.5, color = 'gray')
        else:                           #it's DD
            axes[i].axvspan(new_f.index[0],new_f.index[-1],alpha = 0.5, color = 'gray')
        # change ticks size, set labels and ax-limits, adjust subplots
        axes[i].tick_params(axis='both', which='major', labelsize=10)
        
        plt.subplots_adjust(hspace=.09)
        axes[i].set_ylabel(new_f.Date[i], fontsize=9)
        axes[i].set_xlabel('')
        axes[i].set_xlim(new_f.index[0],new_f.index[-1])
        onset_val, time_val, t_val = write_onset(dataframe, spider)        
        axes[i].plot(time_val, onset_val, linestyle='None', marker='+', markersize = 10, color = 'r')
        # delete labels of x-axes except the last x-axis
        for ax in axes.flat:
            ax.label_outer()
        # make Date format in hours:minutes
    axes[i].xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    plt.savefig(filename)


# Will plot datapoints and linear correlation. 
# Input: dataframe with onset values (mean of onsets) and FRP values. All neccessary coefs from lin_reg function
def plot_regression(dataframe, y_pred, r_sq, b0, b1, r, p_value, title, filename):
    fig = plt.figure(figsize = (6,4))
    sns.scatterplot(dataframe.FRP, dataframe.Onset, color = 'black')
    ax = sns.lineplot(x = dataframe.FRP.values, y = y_pred.reshape(-1),color ='grey', linewidth = 0.4)
    ax.lines[0].set_linestyle("--",)
    ax.set_ylabel('Activity Onset')
    ax.set_xlabel('FRP')
        
    ax = plt.gca()
    xticks = ax.xaxis.get_major_ticks() 
    xticks[0].label1.set_visible(False)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    plt.title(title) #here should be spider's specie name
    ticks = ticker.FuncFormatter(lambda x, pos: '{0:1.1f}'.format(x/60))
    #ax1.yaxis.set_major_formatter(ticks)
    print('𝑅² = ',r_sq)
    print('intercept (b0):', b0)
    print('coef (b1):',b1)
    print('Pearson correlation:', r)
    print('P-value(two-tailed) :', p_value)
    plt.savefig(filename, dpi = 300)