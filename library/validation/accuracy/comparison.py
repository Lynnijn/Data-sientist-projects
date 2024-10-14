import pandas as pd
import calendar
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import os



## plots for old providers
def daily_ref_mod_interactive(site, site_ref, site_mod):
    
    ref_sum = site_ref.resample('M').sum(min_count=1)
    mod_sum = site_mod.resample('M').sum(min_count=1)

    ref_sum_aligned, mod_sum_aligned = ref_sum.align(mod_sum, fill_value=0)
    
    difference = mod_sum_aligned - ref_sum_aligned
    difference[ref_sum_aligned==0] = float('nan')
    difference[mod_sum_aligned==0] = float('nan')

    fig = px.line(title=f'Reference & Model data for {site}', labels={'value': 'Values', 'index': 'Datetime'}, height=800)

    if not ref_sum_aligned.empty and not mod_sum_aligned.empty:
        fig.add_trace(go.Scatter(x=ref_sum_aligned.index, y=difference.values, name='Difference', mode='lines', connectgaps=False, line=dict(color='#B18AF4')))

    if not ref_sum.empty:
        fig.add_trace(go.Scatter(x=ref_sum.index, y=ref_sum.values, name='Reference', mode='lines', connectgaps=False, line=dict(color='#ECA546')))

    if not mod_sum.empty:
        fig.add_trace(go.Scatter(x=mod_sum.index, y=mod_sum.values, name='Model', mode='lines', connectgaps=False, line=dict(color='#56DBB8')))

    fig.update_xaxes(tickangle=45, rangeslider=dict(visible=True))  
    fig.show()

    
    
def or_daily_ref_mod_interactive(site, site_ref, site_mod):
    
    ref_aligned, mod_aligned = site_ref.align(site_mod, fill_value=0)
    
    difference = mod_aligned - ref_aligned
    difference[ref_aligned==0] = float('nan')
    difference[mod_aligned==0] = float('nan')

    fig = px.line(title=f'Reference & Model data for {site}', labels={'value': 'Values', 'index': 'Datetime'}, height=800)

    if not ref_aligned.empty and not mod_aligned.empty:
        fig.add_trace(go.Scatter(x=ref_aligned.index, y=difference.values, name='Difference', mode='lines', connectgaps=False, line=dict(color='#B18AF4')))

    if not site_ref.empty:
        fig.add_trace(go.Scatter(x=site_ref.index, y=site_ref.values, name='Reference', mode='lines', connectgaps=False, line=dict(color='#ECA546')))

    if not site_mod.empty:
        fig.add_trace(go.Scatter(x=site_mod.index, y=site_mod.values, name='Model', mode='lines', connectgaps=False, line=dict(color='#56DBB8')))

    fig.update_xaxes(tickangle=45, rangeslider=dict(visible=True))  
    fig.show()

    
    
    
def hourly_ref_mod_interactive(site, site_ref, site_mod):
    ref_sum = site_ref.resample('D').sum(min_count=1)
    mod_sum = site_mod.resample('D').sum(min_count=1)

    ref_sum_aligned, mod_sum_aligned = ref_sum.align(mod_sum, fill_value=0)

    difference = mod_sum_aligned - ref_sum_aligned
    difference[ref_sum_aligned==0] = float('nan')
    difference[mod_sum_aligned==0] = float('nan')

    fig = px.line(title=f'Reference & Model data for {site}', labels={'value': 'Values', 'index': 'Datetime'}, height=800)

    if not ref_sum_aligned.empty and not mod_sum_aligned.empty:
        fig.add_trace(go.Scatter(x=ref_sum_aligned.index, y=difference.values, name='Difference', mode='lines', connectgaps=False, line=dict(color='#B18AF4')))
    
    if not ref_sum.empty:
        fig.add_trace(go.Scatter(x=ref_sum.index, y=ref_sum.values, name='Reference', mode='lines', connectgaps=False, line=dict(color='#ECA546')))

    if not mod_sum.empty:
        fig.add_trace(go.Scatter(x=mod_sum.index, y=mod_sum.values, name='Model', mode='lines', connectgaps=False, line=dict(color='#56DBB8')))
    
    fig.update_xaxes(tickangle=45, rangeslider=dict(visible=True))  
    fig.show()

 

 
    
   
    
def shift_check_winter(site, site_ref, site_mod, year):
    plt.figure(figsize=(18, 6))

    if year == 2015:
        date1 = pd.to_datetime('2015-03-29')
        
    elif year == 2016:
        date1 = pd.to_datetime('2016-03-27')
        
    elif year == 2017:
        date1 = pd.to_datetime('2017-03-26')

    elif year == 2018:
        date1 = pd.to_datetime('2018-03-25')
        
    elif year == 2019:
        date1 = pd.to_datetime('2019-03-31')
        
    elif year == 2020:
        date1 = pd.to_datetime('2020-03-29')
        
    elif year == 2021:
        date1 = pd.to_datetime('2021-03-28')
        
    elif year == 2022:
        date1 = pd.to_datetime('2022-03-27')
       
    elif year == 2023:
        date1 = pd.to_datetime('2023-03-26')
        
    elif year == 2024:
        date1 = pd.to_datetime('2024-03-30')
    
    else:
        raise ValueError(f"Year {year} not recognized.")

    start_datetime1 = pd.to_datetime(f'{date1} 00:00:00+00:00')
    end_datetime1 = pd.to_datetime(f'{date1} 23:00:00+00:00')
    datetime_range1 = pd.date_range(start=start_datetime1, end=end_datetime1, freq='H')
 
    plt.plot(site_ref.loc[start_datetime1:end_datetime1].index, site_ref.loc[start_datetime1:end_datetime1], label='Reference', color='#ECA546')
    plt.plot(site_mod.loc[start_datetime1:end_datetime1].index, site_mod.loc[start_datetime1:end_datetime1], label='Model', color='#56DBB8')

    plt.title(f'Reference & Model data for {site} at {date1.strftime("%Y-%m-%d")}')
    plt.xlabel('Datetime')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)

    plt.xticks(datetime_range1, [dt.strftime('%H:%M') for dt in datetime_range1], rotation=45)
    
    plt.show()

    
    
def shift_check_summer(site, site_ref, site_mod, year):
    plt.figure(figsize=(18, 6))
    
    if year == 2015:
        date2 = pd.to_datetime('2015-10-25')
        
    elif year == 2016:
        date2 = pd.to_datetime('2016-10-30')
        
    elif year == 2017:
        date2 = pd.to_datetime('2017-10-29')

    elif year == 2018:
        date2 = pd.to_datetime('2018-10-28')
        
    elif year == 2019:
        date2 = pd.to_datetime('2019-10-27')
        
    elif year == 2020:
        date2 = pd.to_datetime('2020-10-25')
        
    elif year == 2021:
        date2 = pd.to_datetime('2021-10-31')
        
    elif year == 2022:
        date2 = pd.to_datetime('2022-10-30')
        
    elif year == 2023:
        date2 = pd.to_datetime('2023-10-29')
        
    elif year == 2021:
        date2 = pd.to_datetime('2021-10-27')
        
    else:
        raise ValueError(f"Year {year} not recognized.")

    start_datetime2 = pd.to_datetime(f'{date2} 00:00:00+00:00')
    end_datetime2 = pd.to_datetime(f'{date2} 23:00:00+00:00')
    datetime_range2 = pd.date_range(start=start_datetime2, end=end_datetime2, freq='H')

    plt.plot(site_ref.loc[start_datetime2:end_datetime2].index, site_ref.loc[start_datetime2:end_datetime2], label='Reference', color='#ECA546')
    plt.plot(site_mod.loc[start_datetime2:end_datetime2].index, site_mod.loc[start_datetime2:end_datetime2], label='Model', color='#56DBB8')

    plt.title(f'Reference & Model data for {site} at {date2.strftime("%Y-%m-%d")}')
    plt.xlabel('Datetime')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)

    plt.xticks(datetime_range2, [dt.strftime('%H:%M') for dt in datetime_range2], rotation=45)
    
    plt.show()

    
def shift_check(site, site_ref, site_mod, date):
    plt.figure(figsize=(18, 6))

    date = pd.to_datetime(date)
        
    start_datetime = pd.to_datetime(f'{date} 00:00:00+00:00')
    end_datetime = pd.to_datetime(f'{date} 23:00:00+00:00')
    datetime_range = pd.date_range(start=start_datetime, end=end_datetime, freq='H')
 
    plt.plot(site_ref.loc[start_datetime:end_datetime].index, site_ref.loc[start_datetime:end_datetime], label='Reference', color='#ECA546')
    plt.plot(site_mod.loc[start_datetime:end_datetime].index, site_mod.loc[start_datetime:end_datetime], label='Model', color='#56DBB8')

    plt.title(f'Reference & Model data for {site} at {date.strftime("%Y-%m-%d")}')
    plt.xlabel('Datetime')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)

    plt.xticks(datetime_range, [dt.strftime('%H:%M') for dt in datetime_range], rotation=45)
    
    plt.show()

    
def shift_check_daily_winter(site, site_ref, site_mod, year):
    plt.figure(figsize=(18, 6))

    if year == 2015:
        date1 = pd.to_datetime('2015-03-29')
    elif year == 2016:
        date1 = pd.to_datetime('2016-03-27')
    elif year == 2017:
        date1 = pd.to_datetime('2017-03-26')
    elif year == 2018:
        date1 = pd.to_datetime('2018-03-25')
    elif year == 2019:
        date1 = pd.to_datetime('2019-03-31')
    elif year == 2020:
        date1 = pd.to_datetime('2020-03-29')
    elif year == 2021:
        date1 = pd.to_datetime('2021-03-28')
    else:
        raise ValueError(f"Year {year} not recognized.")

    start_datetime1 = date1 - pd.DateOffset(days=3)
    end_datetime1 = date1 + pd.DateOffset(days=3)

    datetime_range1 = pd.date_range(start=start_datetime1, end=end_datetime1, freq='D')

    plt.plot(site_ref.loc[start_datetime1:end_datetime1].index, site_ref.loc[start_datetime1:end_datetime1], label='Reference', color='#ECA546')
    plt.plot(site_mod.loc[start_datetime1:end_datetime1].index, site_mod.loc[start_datetime1:end_datetime1], label='Model', color='#56DBB8')

    plt.title(f'Reference & Model data for {site} from {start_datetime1.strftime("%Y-%m-%d")} to {end_datetime1.strftime("%Y-%m-%d")}')
    plt.xlabel('Datetime')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)

    plt.xticks(datetime_range1, rotation=45)

    plt.show()

    
    
def shift_check_daily_summer(site, site_ref, site_mod, year):
    plt.figure(figsize=(18, 6))

    if year == 2015:
        date2 = pd.to_datetime('2015-10-25')
        
    elif year == 2016:
        date2 = pd.to_datetime('2016-10-30')
        
    elif year == 2017:
        date2 = pd.to_datetime('2017-10-29')

    elif year == 2018:
        date2 = pd.to_datetime('2018-10-28')
        
    elif year == 2019:
        date2 = pd.to_datetime('2019-10-27')
        
    elif year == 2020:
        date2 = pd.to_datetime('2020-10-25')
        
    elif year == 2021:
        date2 = pd.to_datetime('2021-10-31')
    else:
        raise ValueError(f"Year {year} not recognized.")

    start_datetime2 = date2 - pd.DateOffset(days=3)
    end_datetime2 = date2 + pd.DateOffset(days=3)

    datetime_range2 = pd.date_range(start=start_datetime2, end=end_datetime2, freq='D')

    plt.plot(site_ref.loc[start_datetime2:end_datetime2].index, site_ref.loc[start_datetime2:end_datetime2], label='Reference', color='#ECA546')
    plt.plot(site_mod.loc[start_datetime2:end_datetime2].index, site_mod.loc[start_datetime2:end_datetime2], label='Model', color='#56DBB8')

    plt.title(f'Reference & Model data for {site} from {start_datetime2.strftime("%Y-%m-%d")} to {end_datetime2.strftime("%Y-%m-%d")}')
    plt.xlabel('Datetime')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)

    plt.xticks(datetime_range2, rotation=45)

    plt.show()


    
    
    
def daily_ref_mod(site, site_ref, site_mod, month, year):
    plt.figure(figsize=(18, 6))

    days_in_month = calendar.monthrange(year, month)[1]

    ref_sum = site_ref.loc[f'{year}-{month:02d}-01 00:00:00+00:00':f'{year}-{month:02d}-{days_in_month} 23:00:00+00:00'].resample('D').sum()
    mod_sum = site_mod.loc[f'{year}-{month:02d}-01 00:00:00+00:00':f'{year}-{month:02d}-{days_in_month} 23:00:00+00:00'].resample('D').sum()
    
    ref_aligned, mod_aligned = ref_sum.align(mod_sum, fill_value=0)
    
    difference_line = mod_aligned - ref_aligned
    difference_line[ref_aligned==0] = float('nan')
    difference_line[mod_aligned==0] = float('nan')
    
    if not ref_aligned.empty and not mod_aligned.empty:
        plt.plot(difference_line, label='Difference', linestyle='--', color='#B18AF4')

    if not ref_sum.empty:
        plt.plot(ref_sum, label='Reference', color='#ECA546')
    if not mod_sum.empty:    
        plt.plot(mod_sum, label='Model', color='#56DBB8')


    plt.title(f'Reference & Model data for {site} in {year}-{month}')
    plt.xlabel('Datetime')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)

    plt.xticks(pd.date_range(start=f'{year}-{month:02d}-01', end=f'{year}-{month:02d}-{days_in_month}', freq='2D'), rotation=45)

    plt.show()  
    
    
        
    
def largest_bias(site, ref, mod):
    
    if ref.empty or mod.empty:
        print("DataFrames are not available.")
        return pd.DataFrame(), pd.DataFrame()

    bias_as = (mod - ref).sort_values()
    bias_de = (mod - ref).sort_values(ascending=False)

    print(f"Top 20 negative biases for {site}:\n{bias_as.head(20)}")
    print(f"Top 20 positive biases for {site}:\n{bias_de.head(20)}")
    
    return bias_as, bias_de


            
            
def daily_top_bias(site, site_ref, site_mod, bias):
    coms = []
    for idx in bias.head(10).index:
        years, months = idx.year, idx.month

        com = [months, years]

        if com not in coms:
            coms.append(com)
            daily_ref_mod(site, site_ref, site_mod, months, years)

            
            
            
def daily_sum_difference(site, site_ref, site_mod):
    
    ref_sum = site_ref.resample('M').sum(min_count=1)
    mod_sum = site_mod.resample('M').sum(min_count=1)

    ref_sum_aligned, mod_sum_aligned = ref_sum.align(mod_sum, fill_value=0)
    
    difference = mod_sum_aligned - ref_sum_aligned
    difference[ref_sum_aligned==0] = float('nan')
    difference[mod_sum_aligned==0] = float('nan')

    difference_as = difference[difference < 0].sort_values().head(50)
    difference_de = difference[difference > 0].sort_values(ascending=False).head(50)

    return difference_as, difference_de
    

        
def hourly_sum_difference(site, site_ref, site_mod):
    ref_sum = site_ref.resample('D').sum(min_count=1)
    mod_sum = site_mod.resample('D').sum(min_count=1)

    ref_sum_aligned, mod_sum_aligned = ref_sum.align(mod_sum, fill_value=0)

    difference = mod_sum_aligned - ref_sum_aligned
    difference[ref_sum_aligned==0] = float('nan')
    difference[mod_sum_aligned==0] = float('nan')

    difference_as = difference[difference < 0].sort_values().head(50)
    difference_de = difference[difference > 0].sort_values(ascending=False).head(50)

    return difference_as, difference_de

 
    
def daily_sum_ratio(site, site_ref, site_mod):
    
    ref_sum = site_ref.resample('M').sum(min_count=1)
    mod_sum = site_mod.resample('M').sum(min_count=1)

    ref_sum_aligned, mod_sum_aligned = ref_sum.align(mod_sum, fill_value=0)
    
    difference = mod_sum_aligned - ref_sum_aligned
    ratio = difference/mod_sum_aligned
    ratio[ref_sum_aligned==0] = float('nan')
    ratio[mod_sum_aligned==0] = float('nan')

    ratio_as = ratio[ratio < 0].sort_values().head(50)
    ratio_de = ratio[ratio > 0].sort_values(ascending=False).head(50)

    return ratio_as, ratio_de
    

        
def hourly_sum_ratio(site, site_ref, site_mod):
    ref_sum = site_ref.resample('D').sum(min_count=1)
    mod_sum = site_mod.resample('D').sum(min_count=1)

    ref_sum_aligned, mod_sum_aligned = ref_sum.align(mod_sum, fill_value=0)

    difference = mod_sum_aligned - ref_sum_aligned
    ratio = difference/mod_sum_aligned
    ratio[ref_sum_aligned==0] = float('nan')
    ratio[mod_sum_aligned==0] = float('nan')

    ratio_as = ratio[ratio < 0].sort_values().head(50)
    ratio_de = ratio[ratio > 0].sort_values(ascending=False).head(50)

    return ratio_as, ratio_de

    
def hourly_diff_ratio_merged(site, site_ref, site_mod):

    difference_as, difference_de = hourly_sum_difference(site, site_ref, site_mod)

    ratio_as, ratio_de = hourly_sum_ratio(site, site_ref, site_mod)
    
    merged_as = pd.merge(ratio_as, difference_as, how='outer', left_index=True, right_index=True)  
    merged_as.columns = ['ratio', 'difference']
    merged_as = merged_as.sort_values('ratio')

    merged_de = pd.merge(ratio_de, difference_de, how='outer', left_index=True, right_index=True)
    merged_de.columns = ['ratio', 'difference']
    merged_de = merged_de.sort_values('ratio', ascending=False)

    print(f"Top negative differences and ratios for {site}:\n{merged_as.head(20)}")
    print(f"Top positive differences and ratios for {site}:\n{merged_de.head(20)}")

    
    
def daily_diff_ratio_merged(site, site_ref, site_mod):

    difference_as, difference_de = daily_sum_difference(site, site_ref, site_mod)

    ratio_as, ratio_de = daily_sum_ratio(site, site_ref, site_mod)
    
    merged_as = pd.merge(ratio_as, difference_as, how='outer', left_index=True, right_index=True)  
    merged_as.columns = ['ratio', 'difference']
    merged_as = merged_as.sort_values('ratio')

    merged_de = pd.merge(ratio_de, difference_de, how='outer', left_index=True, right_index=True)
    merged_de.columns = ['ratio', 'difference']
    merged_de = merged_de.sort_values('ratio', ascending=False)

    print(f"Top negative differences and ratios for {site}:\n{merged_as.head(20)}")
    print(f"Top positive differences and ratios for {site}:\n{merged_de.head(20)}")
