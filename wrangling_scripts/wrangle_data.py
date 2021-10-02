import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import plotly
from collections import namedtuple
from collections import defaultdict


def data_melt(df, value_variables=["1990", "2015"]):
    """return tidy data"""

    return df.melt(id_vars="Country Name", value_vars=value_variables)


def data_list(df, year_labels=["1990", "2015"]):
    """return data as list of country, year, measure tuples"""
    data_list = []
    year = [int(year) for year in year_labels]

    for country in df["Country Name"].unique():
        measure = df.loc[df["Country Name"] == country, year_labels].values.tolist()[0]
        data_list.append((country, year, measure))

    return data_list


def filterdata(dataset, keepcolumns=["Country Name", "1990", "2015"]):

    df = pd.read_csv(dataset, skiprows=4)
    df = df.loc[:, keepcolumns]
    countrylist = [
        "United States",
        "China",
        "Japan",
        "Germany",
        "United Kingdom",
        "India",
        "France",
        "Brazil",
        "Italy",
        "Canada",
    ]
    df = df.loc[df["Country Name"].isin(countrylist), :]

    return df


def return_figures():
    Countrydata = namedtuple("Countrydata", "country year measure")
    figures = []

    # figure 1
    df = filterdata("data/API_AG.LND.ARBL.HA.PC_DS2_en_csv_v2.csv")

    df_list = data_list(df)
    country_data = [Countrydata(*countryinfo) for countryinfo in df_list]

    figure = go.Figure()
    for data in country_data:
        figure.add_trace(
            go.Scatter(x=data.year, y=data.measure, mode="lines", name=data.country)
        )
    figure.update_layout(
        title="Change in Hectares Arable Land <br> per Person 1990 to 2015",
        xaxis_tickmode="linear",
        xaxis_title="Year",
        xaxis_tick0=1990,
        xaxis_dtick=25,
        yaxis_title="Percent",
    )
    figures.append(figure)

    # figure 2

    # figure = go.Figure()
    # figure.add_trace(go.Bar(name="1990", x=df["Country Name"], y=df["1990"]))
    # figure.add_trace(go.Bar(name="2015", x=df["Country Name"], y=df["2015"]))
    figure = go.Figure(
        [
            go.Bar(name="1990", x=df["Country Name"], y=df["1990"]),
            go.Bar(name="2015", x=df["Country Name"], y=df["2015"]),
        ]
    )
    figure.update_layout(
        barmode="group",
        title="Hectares Arable Land per Person",
        yaxis_title="Hectares per person",
    )
    figures.append(figure)

    # figure 3
    df = filterdata("data/API_SP.RUR.TOTL.ZS_DS2_en_csv_v2_9948275.csv")

    df_list = data_list(df)
    country_data = [Countrydata(*countryinfo) for countryinfo in df_list]

    figure = go.Figure()
    for data in country_data:
        figure.add_trace(
            go.Scatter(x=data.year, y=data.measure, mode="lines", name=data.country)
        )
    figure.update_layout(
        title="Change in Rural Population <br> (Percent of Total Population)",
        xaxis_tickmode="linear",
        xaxis_title="Year",
        xaxis_tick0=1990,
        xaxis_dtick=25,
        yaxis_title="Percent",
    )
    figures.append(figure)

    # figure 4
    year_labels = [str(year_label) for year_label in range(1990, 2016)]
    variable_labels = ["Country Name"] + year_labels
    df1 = filterdata(
        "data/API_SP.RUR.TOTL_DS2_en_csv_v2_9914824.csv", keepcolumns=variable_labels
    )
    df2 = filterdata(
        "data/API_AG.LND.FRST.K2_DS2_en_csv_v2_9910393.csv", keepcolumns=variable_labels
    )

    df1_list = data_list(df1, year_labels)
    df2_list = data_list(df2, year_labels)

    dict_list = defaultdict(list)
    pairs = list(zip(df1_list, df2_list))

    for pair in pairs:
        for country_data in pair:
            dict_list[country_data[0]].append(country_data[2])

    country_names = df1["Country Name"].unique().tolist()

    figure = go.Figure()
    for country in country_names:
        figure.add_trace(
            go.Scatter(
                x=dict_list[country][0],
                y=dict_list[country][1],
                mode="markers",
                name=country,
            )
        )
    figure.update_layout(
        title="Rural Population vs Forested Area",
        xaxis_tickmode="linear",
        xaxis_title="Rural Population",
        yaxis_title="Forested Area",
        xaxis_type="log",
        yaxis_type="log",
    )

    figures.append(figure)

    # figure 5
    df = filterdata("data/API_SP.RUR.TOTL_DS2_en_csv_v2_9914824.csv")

    figure = go.Figure([go.Bar(name="2015", x=df["Country Name"], y=df["2015"]),])
    figure.update_layout(
        title="Total Rural Population by Country", yaxis_title="Rural Population",
    )
    figures.append(figure)

    return figures
