import pandas as pd
import calendar
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import os


def ref_mod_interactive(site, site_ref, site_mod, site_directory=None):
    ref_aligned, mod_aligned = site_ref.align(site_mod, fill_value=0)
    
    difference = mod_aligned - ref_aligned
    difference[ref_aligned == 0] = float('nan')
    difference[mod_aligned == 0] = float('nan')

    fig = px.line(title=f'Reference & Model data for {site}', labels={'value': 'Values', 'index': 'Datetime'}, height=800)

    first_valid_index = site_ref.first_valid_index()
    last_valid_index = site_ref.last_valid_index()
    
    if not site_ref.empty:
        fig.add_trace(go.Scatter(x=site_ref.index, y=site_ref.values, name='Reference', mode='lines', connectgaps=False, line=dict(color='#ECA546')))

    if not site_mod.empty:
        site_mod_subset = site_mod.loc[first_valid_index:last_valid_index]
        fig.add_trace(go.Scatter(x=site_mod_subset.index, y=site_mod_subset.values, name='Model', mode='lines', connectgaps=False, line=dict(color='#56DBB8')))

    if not ref_aligned.empty and not mod_aligned.empty:
        difference_subset = difference.loc[first_valid_index:last_valid_index]
        fig.add_trace(go.Scatter(x=difference_subset.index, y=difference_subset.values, name='Difference', mode='lines', connectgaps=False, line=dict(color='#B18AF4')))

    fig.update_xaxes(tickangle=45, rangeslider=dict(visible=True))

    if site_directory:
        pio.write_html(fig, os.path.join(site_directory, f'{site}_whole_range.html'))
        pio.write_image(fig, os.path.join(site_directory, f'{site}_whole_range.png'))
    
    else:
        fig.show()

    
    
# def shift_check_start_end(site, site_ref, site_mod, time, site_directory=None, start=False):
#     plt.figure(figsize=(18, 6))

#     date = time.date()

#     if start==True:
#         start_datetime1 = pd.to_datetime(time)
#         end_datetime1 = pd.to_datetime(f'{date} 23:00:00+00:00')
#     else:
#         start_datetime1 = pd.to_datetime(f'{date} 00:00:00+00:00')
#         end_datetime1 = pd.to_datetime(time)
        
#     datetime_range1 = pd.date_range(start=start_datetime1, end=end_datetime1, freq='H')
 
#     plt.plot(site_ref.loc[start_datetime1:end_datetime1].index, site_ref.loc[start_datetime1:end_datetime1], label='Reference', color='#ECA546')
#     plt.plot(site_mod.loc[start_datetime1:end_datetime1].index, site_mod.loc[start_datetime1:end_datetime1], label='Model', color='#56DBB8')

#     plt.title(f'Reference & Model data for {site} at {time.strftime("%Y-%m-%d")}')
#     plt.xlabel('Datetime')
#     plt.ylabel('Values')
#     plt.legend()
#     plt.grid(True)

#     plt.xticks(datetime_range1, [dt.strftime('%H:%M') for dt in datetime_range1], rotation=45)
    
#     if site_directory:
#         plt.savefig(os.path.join(site_directory, f'{site}_shift_checking_{date}.png'))
#         plt.close()
#     else:
#         plt.show()    
     
    
    




def shift_check_start_end(site, site_ref, site_mod, time, site_directory=None, start=False):
    plt.figure(figsize=(18, 6))

    start_datetime1 = pd.to_datetime(time)
    
    if start:
        end_datetime1 = start_datetime1.normalize() + pd.Timedelta(days=1) - pd.Timedelta(minutes=15)
    else:
        start_datetime1 = start_datetime1.normalize()
        # Calculate the end of the day as the last 15-minute interval of the day
        end_of_day = start_datetime1 + pd.Timedelta(days=1) - pd.Timedelta(minutes=15)
        end_datetime1 = end_of_day

    # Ensure the start and end times are in the same time zone as the reference data
    if start_datetime1.tzinfo != end_datetime1.tzinfo:
        if end_datetime1.tzinfo:
            start_datetime1 = start_datetime1.tz_convert(end_datetime1.tzinfo)
        else:
            end_datetime1 = end_datetime1.tz_localize(start_datetime1.tzinfo)

    datetime_range1 = pd.date_range(start=start_datetime1, end=end_datetime1, freq='H')

    plt.plot(site_ref.loc[start_datetime1:end_datetime1].index, site_ref.loc[start_datetime1:end_datetime1], label='Reference', color='#ECA546')
    plt.plot(site_mod.loc[start_datetime1:end_datetime1].index, site_mod.loc[start_datetime1:end_datetime1], label='Model', color='#56DBB8')

    plt.title(f'Reference & Model data for {site} on {time.strftime("%Y-%m-%d")}')
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)

    plt.xticks(datetime_range1, [dt.strftime('%H:%M') for dt in datetime_range1], rotation=45)

    # Save or show the plot based on the site directory
    if site_directory:
        plt.savefig(os.path.join(site_directory, f'{site}_shift_checking_{time.strftime("%Y-%m-%d")}.png'))
        plt.close()
    else:
        plt.show()

        
        
def largest_difference(site, site_ref, site_mod):
    ref_aligned, mod_aligned = site_ref.align(site_mod, fill_value=0)
    
    difference = mod_aligned - ref_aligned
    difference[ref_aligned==0] = float('nan')
    difference[mod_aligned==0] = float('nan')
    
    bias_as = difference[difference < 0].sort_values().head(20)
    bias_as.name = 'difference'
    bias_de = difference[difference > 0].sort_values(ascending=False).head(20)
    bias_de.name = 'difference'
    
    return bias_as, bias_de


def largest_ratio(site, site_ref, site_mod):
    ref_aligned, mod_aligned = site_ref.align(site_mod, fill_value=0)

    difference = mod_aligned - ref_aligned
    ratio = difference/mod_aligned
    ratio[ref_aligned==0] = float('nan')
    ratio[mod_aligned==0] = float('nan')

    ratio_as = ratio[ratio < 0].sort_values().head(50)
    ratio_as.name = 'ratio'
    ratio_de = ratio[ratio > 0].sort_values(ascending=False).head(50)
    ratio_de.name = 'ratio'

    return ratio_as, ratio_de


def diff_ratio_merged(site, site_ref, site_mod):

    difference_as, difference_de = largest_difference(site, site_ref, site_mod)

    ratio_as, ratio_de = largest_ratio(site, site_ref, site_mod)
    
    merged_as = pd.merge(difference_as, ratio_as, how='outer', left_index=True, right_index=True)  
    merged_as.columns = ['difference', 'ratio']
    merged_as = merged_as.sort_values('difference')

    merged_de = pd.merge(difference_de, ratio_de, how='outer', left_index=True, right_index=True)
    merged_de.columns = ['difference', 'ratio']
    merged_de = merged_de.sort_values('difference', ascending=False)

#     print(f"Top negative differences and ratios for {site}:\n{merged_as.head(20)}")
#     print(f"Top positive differences and ratios for {site}:\n{merged_de.head(20)}")

    return merged_as, merged_de

