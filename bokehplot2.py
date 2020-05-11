from bokeh.io import curdoc
import numpy as np
import pandas as pd

from bokeh.plotting import figure

from bokeh.models import Legend, HoverTool, ColumnDataSource, Panel,HBar, Select,FactorRange,RadioGroup, Div
from bokeh.models.widgets import  Slider, Tabs

from bokeh.layouts import column, row, WidgetBox

from math import pi
import bokeh.palettes as c

from os.path import dirname, join

#data_raw = pd.read_csv(join(dirname(__file__),'data','Motor_Vehicle_Collisions_Crashes.csv'))

dataList=[]
for i in range(0,2): #41
    dataList.append(pd.read_csv('splitData/Motor_Vehicle_Collisions_Crashes_'+str(i)+".csv", low_memory=False))
data_raw=dataList[0]
for i in range(1,len(dataList)):
    data_raw=pd.concat([data_raw,dataList[i]])


injured_killed = list(['NUMBER OF PERSONS INJURED','NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED','NUMBER OF PEDESTRIANS KILLED',
                       'NUMBER OF CYCLIST INJURED','NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST INJURED','NUMBER OF MOTORIST KILLED'])

data_raw[injured_killed] = data_raw[injured_killed].fillna(0)

data_raw['NUMBER OF PERSONS INJURED'] = data_raw["NUMBER OF PERSONS INJURED"].astype(str).astype(float).astype(int)
data_raw['NUMBER OF PERSONS KILLED'] = data_raw["NUMBER OF PERSONS KILLED"].astype(str).astype(float).astype(int)
data_raw['NUMBER OF PEDESTRIANS INJURED'] = data_raw["NUMBER OF PEDESTRIANS INJURED"].astype(str).astype(float).astype(int)
data_raw['NUMBER OF PEDESTRIANS KILLED'] = data_raw["NUMBER OF PEDESTRIANS KILLED"].astype(str).astype(float).astype(int)

data_raw['NUMBER OF CYCLIST INJURED'] = data_raw["NUMBER OF CYCLIST INJURED"].astype(str).astype(float).astype(int)
data_raw['NUMBER OF CYCLIST KILLED'] = data_raw["NUMBER OF CYCLIST KILLED"].astype(str).astype(float).astype(int)

data_raw['NUMBER OF MOTORIST INJURED'] = data_raw["NUMBER OF MOTORIST INJURED"].astype(str).astype(float).astype(int)
data_raw['NUMBER OF MOTORIST KILLED'] = data_raw["NUMBER OF MOTORIST KILLED"].astype(str).astype(float).astype(int)

data_raw['CRASH_DATE_TIME'] = pd.to_datetime(data_raw['CRASH DATE'].str[0:10]+' '+data_raw['CRASH TIME'], format = '%m/%d/%Y %H:%M',infer_datetime_format=True)
data_raw['Year'] = data_raw['CRASH_DATE_TIME'].dt.year
data_raw['Hour'] = data_raw['CRASH_DATE_TIME'].dt.hour
data_raw['ON STREET NAME'] = data_raw['ON STREET NAME'].str.strip()
data_raw['OFF STREET NAME'] = data_raw['OFF STREET NAME'].str.strip()
def intersection(df):
    inter = str(str(df['ON STREET NAME'])+', '+str(df['CROSS STREET NAME']))
    return inter
data_raw['Intersection'] = data_raw.apply(intersection, axis = 1)


data_raw['VEHICLE TYPE CODE 1'] = data_raw['VEHICLE TYPE CODE 1'].str.title()
data_raw['VEHICLE TYPE CODE 2'] = data_raw['VEHICLE TYPE CODE 2'].str.title()
data_raw['VEHICLE TYPE CODE 3'] = data_raw['VEHICLE TYPE CODE 3'].str.title()
data_raw['VEHICLE TYPE CODE 4'] = data_raw['VEHICLE TYPE CODE 4'].str.title()
data_raw['VEHICLE TYPE CODE 5'] = data_raw['VEHICLE TYPE CODE 5'].str.title()
data_raw['CONTRIBUTING FACTOR VEHICLE 1'] = data_raw['CONTRIBUTING FACTOR VEHICLE 1'].str.title()
data_raw['CONTRIBUTING FACTOR VEHICLE 2'] = data_raw['CONTRIBUTING FACTOR VEHICLE 2'].str.title()
data_raw['CONTRIBUTING FACTOR VEHICLE 3'] = data_raw['CONTRIBUTING FACTOR VEHICLE 3'].str.title()
data_raw['CONTRIBUTING FACTOR VEHICLE 4'] = data_raw['CONTRIBUTING FACTOR VEHICLE 4'].str.title()
data_raw['CONTRIBUTING FACTOR VEHICLE 5'] = data_raw['CONTRIBUTING FACTOR VEHICLE 5'].str.title()
data_raw['Intersection'] = data_raw['Intersection'].str.title()
data_raw.replace('Station Wagon/Sport Utility Vehicle', 'Sport Utility / Station Wagon', inplace = True)


data_raw_filtered = data_raw[(data_raw['VEHICLE TYPE CODE 1'] != 'PASSENGER VEHICLE') & (data_raw['VEHICLE TYPE CODE 2'] != 'PASSENGER VEHICLE')
            & (data_raw['VEHICLE TYPE CODE 3'] != 'PASSENGER VEHICLE') & (data_raw['VEHICLE TYPE CODE 4'] != 'PASSENGER VEHICLE') & 
           (data_raw['VEHICLE TYPE CODE 5'] != 'PASSENGER VEHICLE')]

data_raw_filtered = data_raw[(data_raw['VEHICLE TYPE CODE 1'] != 'UNKNOWN') & (data_raw['VEHICLE TYPE CODE 2'] != 'UNKNOWN')
            & (data_raw['VEHICLE TYPE CODE 3'] != 'UNKNOWN') & (data_raw['VEHICLE TYPE CODE 4'] != 'UNKNOWN') & 
           (data_raw['VEHICLE TYPE CODE 5'] != 'UNKNOWN')]

data_raw_filtered = data_raw[(data_raw['VEHICLE TYPE CODE 1'] != 'OTHER') & (data_raw['VEHICLE TYPE CODE 2'] != 'OTHER')
            & (data_raw['VEHICLE TYPE CODE 3'] != 'OTHER') & (data_raw['VEHICLE TYPE CODE 4'] != 'OTHER') & 
           (data_raw['VEHICLE TYPE CODE 5'] != 'OTHER')]

data_raw_filtered = data_raw[(data_raw['CONTRIBUTING FACTOR VEHICLE 1'] != 'Unspecified') & (data_raw['CONTRIBUTING FACTOR VEHICLE 2'] != 'Unspecified')
           & (data_raw['CONTRIBUTING FACTOR VEHICLE 3'] != 'Unspecified') & (data_raw['CONTRIBUTING FACTOR VEHICLE 4'] != 'Unspecified') &
            (data_raw['CONTRIBUTING FACTOR VEHICLE 5'] != 'Unspecified')]


data_filtered_marco_part = data_raw_filtered[['CRASH DATE', 'Intersection','Hour','ON STREET NAME','CROSS STREET NAME',
                      'CONTRIBUTING FACTOR VEHICLE 1', 'CONTRIBUTING FACTOR VEHICLE 2','CONTRIBUTING FACTOR VEHICLE 3','CONTRIBUTING FACTOR VEHICLE 4', 'CONTRIBUTING FACTOR VEHICLE 5',
                      'VEHICLE TYPE CODE 1','VEHICLE TYPE CODE 2','VEHICLE TYPE CODE 3','VEHICLE TYPE CODE 4','VEHICLE TYPE CODE 5']]

top_ten_vec_type_1 = data_filtered_marco_part['VEHICLE TYPE CODE 1'].value_counts()[:10].index.tolist()
top_ten_vec_type_2 = data_filtered_marco_part['VEHICLE TYPE CODE 2'].value_counts()[:10].index.tolist()
top_ten_vec_type_3 = data_filtered_marco_part['VEHICLE TYPE CODE 3'].value_counts()[:10].index.tolist()
top_ten_vec_type_4 = data_filtered_marco_part['VEHICLE TYPE CODE 4'].value_counts()[:10].index.tolist()
top_ten_vec_type_5 = data_filtered_marco_part['VEHICLE TYPE CODE 5'].value_counts()[:10].index.tolist()
data_inter = data_filtered_marco_part[~data_filtered_marco_part['ON STREET NAME'].isna() & ~data_filtered_marco_part['CROSS STREET NAME'].isna()]
top_ten_inter = data_inter['Intersection'].value_counts()[:10].index.tolist()


data_filt_vec_type_1 = data_filtered_marco_part[data_filtered_marco_part['VEHICLE TYPE CODE 1'].isin(top_ten_vec_type_1)].drop(['ON STREET NAME', 'CROSS STREET NAME'], axis = 'columns')
data_filt_vec_type_2 = data_filtered_marco_part[data_filtered_marco_part['VEHICLE TYPE CODE 2'].isin(top_ten_vec_type_2)].drop(['ON STREET NAME', 'CROSS STREET NAME'], axis = 'columns')
data_filt_vec_type_3 = data_filtered_marco_part[data_filtered_marco_part['VEHICLE TYPE CODE 3'].isin(top_ten_vec_type_3)].drop(['ON STREET NAME', 'CROSS STREET NAME'], axis = 'columns')
data_filt_vec_type_4 = data_filtered_marco_part[data_filtered_marco_part['VEHICLE TYPE CODE 4'].isin(top_ten_vec_type_4)].drop(['ON STREET NAME', 'CROSS STREET NAME'], axis = 'columns')
data_filt_vec_type_5 = data_filtered_marco_part[data_filtered_marco_part['VEHICLE TYPE CODE 5'].isin(top_ten_vec_type_5)].drop(['ON STREET NAME', 'CROSS STREET NAME'], axis = 'columns')
data_filt_inter = data_filtered_marco_part[data_filtered_marco_part['Intersection'].isin(top_ten_inter)].drop(['ON STREET NAME', 'CROSS STREET NAME'], axis = 'columns')


top_ten_con_fac1 = data_filtered_marco_part['CONTRIBUTING FACTOR VEHICLE 1'].value_counts()[:10].index.tolist()
top_ten_con_fac2 = data_filtered_marco_part['CONTRIBUTING FACTOR VEHICLE 2'].value_counts()[:10].index.tolist()
top_ten_con_fac3 = data_filtered_marco_part['CONTRIBUTING FACTOR VEHICLE 3'].value_counts()[:10].index.tolist()
top_ten_con_fac4 = data_filtered_marco_part['CONTRIBUTING FACTOR VEHICLE 4'].value_counts()[:10].index.tolist()
top_ten_con_fac5 = data_filtered_marco_part['CONTRIBUTING FACTOR VEHICLE 5'].value_counts()[:10].index.tolist()
top_ten_con_facint = data_filt_inter['CONTRIBUTING FACTOR VEHICLE 1'].value_counts()[:10].index.tolist()
top_ten_con_fac1.insert(0,'All')
top_ten_con_fac2.insert(0,'All')
top_ten_con_fac3.insert(0,'All')
top_ten_con_fac4.insert(0,'All')
top_ten_con_fac5.insert(0,'All')
top_ten_con_facint.insert(0,'All')

hour_range =[str(x) for x in np.arange(1,25,1)]
color=c.viridis(10)



def make_layout(data_frame,vec_type,top_ten_con_fac,top_ten_vec_type):
    
    if vec_type!='Intersection':
        n = vec_type[-1]
    else:
        n = str(1)
        
    def make_dataset(selected_con_factor):
        if selected_con_factor != 'All':
            data_filt_vec_type_con_factor = data_frame[data_frame['CONTRIBUTING FACTOR VEHICLE '+ n] == selected_con_factor]
        else:
            data_filt_vec_type_con_factor = data_frame
            
        count_by_hour_and_vec_type = data_filt_vec_type_con_factor.groupby(['Hour',vec_type]).count()['CRASH DATE'].unstack()
        count_by_hour_and_vec_type = count_by_hour_and_vec_type.div(count_by_hour_and_vec_type.sum(axis =0), axis =1)
        count_by_hour_and_vec_type = count_by_hour_and_vec_type.reset_index()
        count_by_hour_and_vec_type['Hour'] = count_by_hour_and_vec_type['Hour'] + 0.5
        #print('i am here')
        return ColumnDataSource(count_by_hour_and_vec_type)
    
    def style(p):
        # Title 
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p
    
    def make_plot(src):
        # Blank plot with correct labels
        p = figure(x_range = FactorRange(factors=hour_range),plot_width = 950, plot_height = 500,
                   title = 'Collision per hour on Day',toolbar_location=None, x_axis_label = 'Time (Hour)', y_axis_label = 'Proportion')
        
        items = [] 
        bar ={} # to store vbars
        ### here we will do a for loop:
        for indx,i in enumerate(top_ten_vec_type):
            bar[i] = p.vbar(x='Hour',  top=i, source= src, color=color[indx], muted_color=None, muted_alpha=0.1,fill_alpha=0.5, muted = True, width=1) 
            items.append((i, [bar[i]]))
            #print(items)
        legend = Legend(items=items, location=(20,40))
        p.add_layout(legend, 'right') 
        p.legend.click_policy="mute"
        
        # Styling
        p = style(p)

        return p
    
    def update(attr, old, new):
        
        new_src = make_dataset(select_factor.value)

        src.data.update(new_src.data)

        
    
    #### my code
    select_factor = Select(title="Contributing factor vehicle "+ n, value=top_ten_con_fac[0], options=top_ten_con_fac)
    select_factor.on_change('value', update)
    
    src = make_dataset(select_factor.value)
    
    p = make_plot(src)
    
    # Put controls in a single element
    controls = WidgetBox(select_factor)
    
    # Create a row layout
    layout = column(controls, p)
    return layout


vec_type_list = list(['VEHICLE TYPE CODE 1','VEHICLE TYPE CODE 2','VEHICLE TYPE CODE 3','VEHICLE TYPE CODE 4',
'VEHICLE TYPE CODE 5', 'Intersection'])

# Make a tabs with the layout
layout_1 = make_layout(data_filt_vec_type_1,vec_type_list[0],top_ten_con_fac1,top_ten_vec_type_1)
layout_2 = make_layout(data_filt_vec_type_2,vec_type_list[1],top_ten_con_fac2,top_ten_vec_type_2)
layout_3 = make_layout(data_filt_vec_type_3,vec_type_list[2],top_ten_con_fac3,top_ten_vec_type_3)
layout_4 = make_layout(data_filt_vec_type_4,vec_type_list[3],top_ten_con_fac4,top_ten_vec_type_4)
layout_5 = make_layout(data_filt_vec_type_5,vec_type_list[4],top_ten_con_fac5,top_ten_vec_type_5)
layout_inter = make_layout(data_filt_inter,vec_type_list[5],top_ten_con_facint,top_ten_inter)
    
tab_1 = Panel(child=layout_1, title = vec_type_list[0].title())
tab_2 = Panel(child=layout_2, title = vec_type_list[1].title())
tab_3 = Panel(child=layout_3, title = vec_type_list[2].title())
tab_4 = Panel(child=layout_4, title = vec_type_list[3].title())
tab_5 = Panel(child=layout_5, title = vec_type_list[4].title())
tab_inter = Panel(child=layout_inter, title = vec_type_list[5])
    
tabs = Tabs(tabs=[tab_1, tab_2, tab_3, tab_4, tab_5, tab_inter])
curdoc().add_root(tabs)
