import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler 


# dash_map=pd.read_csv('data/dash_map.csv',index_col=0)

def plot_dashmap(dashmapData):
    
    # dash-map
    fig = px.choropleth(
                        dashmapData,
                        locations="location",
                        locationmode = "country names",
                        color="stringency_index",
                        hover_name="location",
                        color_continuous_scale="Viridis",
                        animation_frame="date"
        )

    fig.update_layout(
                    title_text = 'Overall Stringency Index 2020-2022(by month)',
                    title_x = 0.5,
                    geo=dict(showframe = False,showcoastlines = False),
                    width=2000,
                    height=600
        )
    
    return fig

def plot_rader(rader,country):
    
    mm = MinMaxScaler()

    mm_data = mm.fit_transform(rader[['restriction_gatherings','school_closures','stay_home_requirements','workplace_closures','containment_index']])
    
    new_rader=pd.DataFrame(data=mm_data*10,columns=['restriction_gatherings','school_closures','stay_home_requirements','workplace_closures','containment_index'])
    new_rader['location']=rader['location'] 
    new_rader=new_rader.groupby(by='location').mean().reset_index()
    new_rader=new_rader.loc[:,['location','restriction_gatherings','school_closures','stay_home_requirements','workplace_closures','containment_index']]

    row=new_rader.loc[new_rader['location']==country,['restriction_gatherings','school_closures','stay_home_requirements','workplace_closures','containment_index']]
    certain_row=row.values.tolist()
    rader_data=[]
    for ls in certain_row: 
        for x in ls: 
            rader_data.append(x) 
    
    # plot rader graph
    fig=go.Figure(data=go.Scatterpolar(
        r=rader_data,
        theta=['restriction_gatherings','school_closures','stay_home_requirements','workplace_closures','containment_index'],
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True
    )
    return fig

def plot_ndnv(basicdata,country):
    
    lines=basicdata[['location','Day','new_cases','new_deaths','new_vaccinations']]

    # calculate cumulative month data for each country 
    lines["new_day"] = lines["Day"].map(lambda x:x[:7])
    lines=lines.groupby(by=['location','new_day']).sum().reset_index()
    #plot line chart
    certain_country=lines.loc[lines['location']==country,:]

    # first double line chart
    fig = make_subplots(specs=[[{"secondary_y": True}]]) 
    # Add traces
    fig.add_trace(
        go.Scatter(x=certain_country['new_day'], y=certain_country['new_deaths'], name="new_death"),
        secondary_y=False,
    ) 
    fig.add_trace(
        go.Scatter(x=certain_country['new_day'], y=certain_country['new_vaccinations'], name="new_vaccinations"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text=f"New death and New vaccinations in {country}"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="new_death", secondary_y=False)
    fig.update_yaxes(title_text="new_vaccinations", secondary_y=True)

    return fig

def plot_ncnv(basicdata,country):
    
    lines=basicdata[['location','Day','new_cases','new_deaths','new_vaccinations']]

    # calculate cumulative month data for each country 
    lines["new_day"] = lines["Day"].map(lambda x:x[:7])
    lines=lines.groupby(by=['location','new_day']).sum().reset_index()
    
    #plot line chart
    certain_country=lines.loc[lines['location']==country,:]
    
    # first double line chart
    fig = make_subplots(specs=[[{"secondary_y": True}]]) 
    
    # Add traces
    fig.add_trace(
        go.Scatter(x=certain_country['new_day'], y=certain_country['new_cases'], name="new_cases"),
        secondary_y=False,
    ) 
    fig.add_trace(
        go.Scatter(x=certain_country['new_day'], y=certain_country['new_vaccinations'], name="new_vaccinations"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text=f"New case and New vaccinations in {country}"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Date")

    # Set y-axes titles
    fig.update_yaxes(title_text="new_death", secondary_y=False)
    fig.update_yaxes(title_text="new_vaccinations", secondary_y=True)

    return fig