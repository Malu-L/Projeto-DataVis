from dash import Dash
from dash import html, dcc, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from readfile import *

# List of all aptions for the radio button
all_generos = ['Feminino', 'Masculino', 'Feminino e Masculino']

# Function to return the dataframe and the color based on the selected genre
def return_df_genero(selected_genero):
    if selected_genero == "Feminino":
        df = df_paris_women.copy()
        color = ["red"]
    elif selected_genero == "Masculino":
        df = df_paris_men.copy()
        color = ["blue"]
    elif selected_genero == "Feminino e Masculino":
        df = df_paris_geral.copy()
        color = ["blue", "red"]
    else:
        df = pd.DataFrame()  # Default empty dataframe

    return df, color

# Inicializing the Dash app
app = Dash(__name__)

# Defining the layout of the app
app.layout = html.Div([
    # Title of the app
    html.H1(children='Dados de Vôlei nas Olimpíadas de Paris', style={'bold': 'True', 'color': '#153f5c', 'text-align': 'center'}),
    
    # Radio button to select the genre
    dcc.RadioItems(
        all_generos, # List of all options
        'Feminino e Masculino', # Default Button
        id='generos-radio', # ID of the radio button
        inline=True,
        style={'display': 'flex', 'gap': '10px', 'color': '#153f5c', 'align-items': 'center', 'justify-content': 'center'}
    ),
    html.Div([
        html.Div([
            html.H2(children = "Todos Os Países", style={'text-align': 'center', 'color': '#153f5c'}),
            html.Div([
                # Graph to show the pie chart
                dcc.Graph(id='pie_chart_all_countries', style={'flex': '1'}),
                # Graph to show the scatter chart
                dcc.Graph(id='scatter_chart', style={'flex': '1'}),
            ], style={'display': 'flex'}),
            html.Div([
                # Graph to show the stacked bars chart
                dcc.Graph(id='scatter_chart_attacks_blocks', style={'flex': '1'})
            ], style={'display': 'flex'}),
            # Graph to show the stacked bars chart
            dcc.Graph(id='stacked_bars_chart', style={'flex': '1'})
        ], style={'flex': '1', 'border-width': '1px','border-style': 'solid', 'border-color': 'black', "border-radius": "10px",
                    "margin-right": "20px"}),
        html.Div([
            html.Div([
                html.H2(children = "Por País", style={'text-align': 'center', 'color': '#153f5c'}),
                # Dropdown to select the country (The options of countries will be based on the selected genre)
                dcc.Dropdown(
                    id="country"
                ),
                html.Div([
                    # Graph to show the pie chart
                    dcc.Graph(id='pie_chart', style={'flex': '1'}),
                    # Graph to show the scatter chart by country
                    dcc.Graph(id='scatter_chart_country', style={'flex': '1'})
                ], style={'display': 'flex'}),
                html.Div([
                    # Graph to show the acumulative chart of points
                    dcc.Graph(id='points_acc_chart_country', style={'flex': '1'}),
                    # Graph to show the acumulative chart of errors
                    dcc.Graph(id='points_err_chart_country', style={'flex': '1'})
                ], style={'display': 'flex'})
            ], style={'border-width': '1px','border-style': 'solid', 'border-color': 'black', "border-radius": "10px"}),
            html.Div([
                html.H2(children = "Por Jogador", style = {'text-align': 'center', 'color': '#153f5c'}),
                # Dropdown to select the player (The options of players will be based on the selected genre and country)
                dcc.Dropdown(
                    id="player"
                ),
                # Graph to show the player statistics
                dcc.Graph(id='players_chart')
            ], style={'border-width': '1px','border-style': 'solid', 'border-color': 'black', "border-radius": "10px",
                      'margin-top': '8px'}),
        ], style={'flex': '1'}),
    ], style={'display': 'flex', 'flex': '1', 'margin': '15px'}),
])

"""
# Defining the layout of the app
app.layout = html.Div([
    # Title of the app
    html.H1(children='Dados de Vôlei nas Olimpíadas de Paris', style={'color': '#117029'}),
    # Radio button to select the genre
    dcc.RadioItems(
        all_generos, # List of all options
        'Feminino e Masculino', # Default Button
        id='generos-radio' # ID of the radio button
    ),
    # --------------- Divs All countries ----------------
    # Div to show the pie chart all countries
    html.Div([
        # Graph to show the pie chart
        dcc.Graph(id='pie_chart_all_countries')
    ]),
    html.Div([
        # Graph to show the scatter chart
        dcc.Graph(id='scatter_chart')
    ]),
    html.Div([
        # Graph to show the stacked bars chart
        dcc.Graph(id='scatter_chart_attacks_blocks')
    ]),
    html.Div([
        # Graph to show the stacked bars chart
        dcc.Graph(id='stacked_bars_chart') # all countries
    ]),
    # -------------------- Divs by country --------------------
    # Div to show the pie chart
    html.Div([
        # Dropdown to select the country (The options of countries will be based on the selected genre)
        dcc.Dropdown(
            id="country"
        ),
        # Graph to show the pie chart
        dcc.Graph(id='pie_chart')
    ]),
    html.Div([
        # Graph to show the scatter chart by country
        dcc.Graph(id='scatter_chart_country')
    ]),
    html.Div([
        # Graph to show the scatter chart
        dcc.Graph(id='points_acc_chart_country')
    ]),
    html.Div([
        # Graph to show the scatter chart
        dcc.Graph(id='points_err_chart_country')
    ]),
    # ---------------- Divs all countries: PS - Ainda tentar fazer por país ----------------
    # html.Div([
    #     # Graph to show the stacked bars chart
    #     dcc.Graph(id='scatter_chart_attacks_blocks')
    # ]),
    # ---------------- Divs by player ----------------
    # Div to show the player statistics
    html.Div([
        # Dropdown to select the player (The options of players will be based on the selected genre and country)
        dcc.Dropdown(
            id="player"
        ),
        # Graph to show the player statistics
        dcc.Graph(id='players_chart')
    ]),
])
"""
# Callback to update the pie chart of all countries
@app.callback(
    Output("pie_chart_all_countries", "figure"),
    Input("generos-radio", "value")
)
def generate_pie_chart_all_countries(selected_genero):
    df, _ = return_df_genero(selected_genero)

    labels = ['Ataque', 'Bloqueio', 'Saque']
    sizes = [
        df['Attack-Points'].sum(),
        df['Block-Points'].sum(),
        df['Serve-Points'].sum()
    ]

    fig = px.pie(values=sizes, names=labels, hole=0.3)
    # Update the traces to change the colors of the percentage numbers and add white lines between divisions
    fig.update_traces(
        textinfo='percent',
        textfont=dict(color='white'),  # Change the color and size of the percentage numbers
        marker=dict(
            line=dict(color='white', width=3)  # Add white lines between the divisions
        )
    )

    # Update the layout
    fig.update_layout(
        showlegend=True,
        title = "Distribuição de Pontos por Categoria",
        title_x=0.5
    )
    
    return fig

# Callback to update the stacked bars chart based on the selected genre
@app.callback(
    Output("stacked_bars_chart", "figure"),
    Input("generos-radio", "value")
)
def generate_stacked_bars(selected_genero):
    df, _ = return_df_genero(selected_genero)
    metrics = ['Points-attacks', 'Succesful-blocks', 'Successful-dig', 'Succesful-receive', 'serve-points', 'Successful-setter', "Team"]
    name_categories = ['Pontos de Ataque', 'Pontos de Bloqueio', 'Sucesso de Defesa', 'Sucesso de Recepção de Saque', 'Pontos de Saque', 'Sucesso de Passe']

    # Get the dataframe countries
    countries = (df["Team"].unique()).tolist()
    countries.sort()

    # Do a new dataframe with the sum of the metrics per country
    df_compare_countries = pd.DataFrame()
    df_compare_countries["Team"] = countries
    df_compare_countries = df[metrics].groupby("Team").sum()
    df_compare_countries["Team"] = countries

    # Colors for each subcategory
    colors = ["#003f5c", "#665191", "#a05195", "#d45087", "#f95d6a", "#ff7c43", "#ffa600"]

    # Get the categories
    categories = df_compare_countries.columns.to_list()[0:len(df_compare_countries.columns)-1] # Remove the last column (Team)

    # Create figure
    fig = go.Figure()

    # Initialize the bottom to zero
    bottom = np.zeros(len(countries))

    # Plotting the stacked bar chart
    for category_i in range(len(categories)): # Loop through each category
        y_axis = [] # Initialize the y_axis to an empty list
        for i in range(len(countries)): # Loop through each country to get the values for the current category
            y_axis.append(df_compare_countries[categories[category_i]][df_compare_countries["Team"] == countries[i]].values[0])
        # Add the bar trace
        fig.add_trace(go.Bar(
            x=countries,
            y=y_axis,
            name=name_categories[category_i],
            marker_color=colors[category_i]
        ))
        bottom += y_axis  # Update the bottom plus the current y_axis

    # Update the layout for stacked bars
    fig.update_layout(
        barmode='stack',
        title='Comparação de Países por Métricas',
        title_x=0.5,
        xaxis=dict(title='Países'),
        yaxis=dict(title='Quantidade de Sucessos')
    )

    # Add annotation text under the legend
    fig.add_annotation(
        text="*Sucesso: Desencadeou ou Impediu ponto",
        xref="paper", yref="paper",
        x=1.4, y=0.53,
        showarrow=False,
        font=dict(size=10)
    )

    return fig

# Callback to update the scatter chart based on the selected genre
@app.callback(
    Output("scatter_chart", "figure"),
    Input("generos-radio", "value")
)
def generate_scatter_chart(selected_genero):
    df, _ = return_df_genero(selected_genero)
    df = df[
    (df['Points-attacks'] > 0) |
    (df["Succesful-receive"] > 0) |
    (df["Successful-setter"] > 0)]

    # Create figure
    markers = ['circle', 'triangle-up', 'star', 'triangle-down', 'square', 'x', 'diamond']
    
    fig = go.Figure()

    # Ataques
    fig.add_trace(go.Scatter(
        x=df['Attempts-shots-attack'],
        y=df['Points-attacks'],
        mode='markers',
        name='Ataques',
        marker=dict(symbol=markers[0], size=8, color='blue', line=dict(width=2, color='black'))
    ))

    # Recepções
    fig.add_trace(go.Scatter(
        x=df['Attemps-receive'],
        y=df['Succesful-receive'],
        mode='markers',
        name='Recepções',
        marker=dict(symbol=markers[1], size=8, color='green', line=dict(width=2, color='black'))
    ))

    # Levantamentos
    fig.add_trace(go.Scatter(
        x=df['Attempts-setter'],
        y=df['Successful-setter'],
        mode='markers',
        name='Levantamentos',
        marker=dict(symbol=markers[5], size=8, color='red', line=dict(width=1, color='black'))
    ))

    # Update layout
    fig.update_layout(
        title='Correlação entre Tentativas e Sucessos',
        title_x=0.5,
        xaxis_title='Número de Tentativas',
        yaxis_title='Número de Sucessos',
        legend_title='Categorias',
        template='plotly_white'
    )

    return fig

# Callback to update the options of the country dropdown based on the selected genre
@app.callback(
    Output('country', 'options'),
    Input('generos-radio', 'value'))

# Function to update the options of the country dropdown based on the selected genre
def set_country_options(selected_genero):
    df, _ = return_df_genero(selected_genero)

    df = df.sort_values(by="Team") # Sorting the dataframe by the column "Team" (Alphabetical order)
    # Creating the options for the dropdown based on the unique values of the column "Team"
    country_options = [{'label': country, 'value': country} for country in df['Team'].unique()]

    return country_options

# Callback to update the value of the country dropdown
@app.callback(
    Output('country', 'value'),
    Input('country', 'options'))
def set_country_value(available_options):
    return available_options[0]['value'] if available_options else None

# Callback to update the pie chart based on the selected country
@app.callback(
    Output("pie_chart", "figure"),
    Input("country", "value"),
    Input("generos-radio", "value")
)
def generate_pie_chart_country(selected_country, selected_genero):
    if not selected_country:
        return go.Figure()
    df, _ = return_df_genero(selected_genero)

    df = df[(df['Team'] == selected_country)]

    labels = ['Ataque', 'Bloqueio', 'Saque']
    sizes = [
        df['Attack-Points'].sum(),
        df['Block-Points'].sum(),
        df['Serve-Points'].sum()
    ]

    fig = px.pie(values=sizes, names=labels, hole=0.3)
    # Update the traces to change the colors of the percentage numbers and add white lines between divisions
    fig.update_traces(
        textinfo='percent',
        textfont=dict(color='white'),  # Change the color and size of the percentage numbers
        marker=dict(
            line=dict(color='white', width=3)  # Add white lines between the divisions
        )
    )

    # Update the layout
    fig.update_layout(
        showlegend=True,
        title = "Distribuição de Pontos por Categoria de um País",
        title_x=0.5
    )
    
    return fig

# Callback to update the scatter chart based on the selected genre
@app.callback(
    Output("scatter_chart_country", "figure"),
    Input("generos-radio", "value"),
    Input("country", "value")
)
def generate_scatter_chart_country(selected_genero, selected_country):
    if not selected_country:
        return go.Figure()
    df, _ = return_df_genero(selected_genero)

    df = df[(df['Team'] == selected_country)]
    df = df[
    (df['Points-attacks'] > 0) |
    (df["Succesful-receive"] > 0) |
    (df["Successful-setter"] > 0)]

    # Create figure
    markers = ['circle', 'triangle-up', 'star', 'triangle-down', 'square', 'x', 'diamond']
    
    fig = go.Figure()

    # Ataques
    fig.add_trace(go.Scatter(
        x=df['Attempts-shots-attack'],
        y=df['Points-attacks'],
        mode='markers',
        name='Ataques',
        marker=dict(symbol=markers[0], size=8, color='blue', line=dict(width=2, color='black'))
    ))

    # Recepções
    fig.add_trace(go.Scatter(
        x=df['Attemps-receive'],
        y=df['Succesful-receive'],
        mode='markers',
        name='Recepções',
        marker=dict(symbol=markers[1], size=8, color='green', line=dict(width=2, color='black'))
    ))

    # Levantamentos
    fig.add_trace(go.Scatter(
        x=df['Attempts-setter'],
        y=df['Successful-setter'],
        mode='markers',
        name='Levantamentos',
        marker=dict(symbol=markers[5], size=8, color='red', line=dict(width=1, color='black'))
    ))

    # Update layout
    fig.update_layout(
        title='Correlação entre Tentativas e Sucessos de um País',
        title_x=0.5,
        xaxis_title='Número de Tentativas',
        yaxis_title='Número de Sucessos',
        legend_title='Categorias',
        template='plotly_white'
    )

    return fig

# Callback to update the scatter chart of attack X block based on the selected genre and team
@app.callback(
    Output("scatter_chart_attacks_blocks", "figure"),
    Input("generos-radio", "value"),
    Input("country", "value")
)
def generate_scatter_attacks_blocks(selected_genero, selected_country):
    fig = go.Figure()

    return fig

# Callback to update the acumulative chart of points based on the selected genre and team
@app.callback(
    Output("points_acc_chart_country", "figure"),
    Input("generos-radio", "value"),
    Input("country", "value")
)
def generate_acc_chart_country(selected_genero, selected_country):
    df, _ = return_df_genero(selected_genero)

    pontos_recepcao = df[df['Team'] == selected_country].groupby('Player-Name')['Succesful-blocks'].sum()
    pontos_ataque = df[df['Team'] == selected_country].groupby('Player-Name')['Points-attacks'].sum()
    pontos_saque = df[df['Team'] == selected_country].groupby('Player-Name')['serve-points'].sum()

    pontos_totais = pd.DataFrame({
    'Pontos Recepcao': pontos_recepcao,
    'Pontos Ataque': pontos_ataque,
    'Pontos Saque': pontos_saque
    }).fillna(0)

    pontos_totais['Total Pontos'] = pontos_totais.sum(axis=1)
    pontos_totais = pontos_totais.sort_values(by='Total Pontos', ascending=False)
    pontos_totais['Cumulativo'] = pontos_totais['Total Pontos'].cumsum() / pontos_totais['Total Pontos'].sum() * 100

    fig = go.Figure()

    # Add bar trace for total points
    fig.add_trace(go.Bar(
        x=pontos_totais.index,
        y=pontos_totais['Total Pontos'],
        name='Total de Pontos',
        marker_color='#0095CC',
        marker_line=dict(width=2.5, color='black'),
        yaxis='y1'
    ))

    # Add line trace for cumulative percentage
    fig.add_trace(go.Scatter(
        x=pontos_totais.index,
        y=pontos_totais['Cumulativo'],
        name='Cumulativo (%)',
        mode='lines+markers',
        marker=dict(symbol='circle', size=8, color='green', line=dict(width=2, color='black')),
        yaxis='y2'
    ))

    # Update layout
    fig.update_layout(
        title='Análise Acumulativa de Pontos por Jogador',
        xaxis_title='Jogador',
        yaxis=dict(
            title='Total de Pontos',
            side='left',
            showgrid=False,
            showline=True,
            ticks="outside",
            titlefont=dict(color="#1f77b4"),
            tickfont=dict(color="#1f77b4")
        ),
        yaxis2=dict(
            title='Porcentagem Cumulativa (%)',
            overlaying='y',
            side='right',
            showgrid=False,
            showline=True,
            range=[0, 110],
            ticks="outside",
            titlefont=dict(color="green"),
            tickfont=dict(color="green")
        ),
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.5)'),
        xaxis=dict(tickangle=90),
        template='plotly_white'
    )

    return fig

# Callback to update the acumulative chart of errors based on the selected genre and team
@app.callback(
    Output("points_err_chart_country", "figure"),
    Input("generos-radio", "value"),
    Input("country", "value")
)
def generate_err_chart_country(selected_genero, selected_country):
    df, _ = return_df_genero(selected_genero)

    erros_recepcao = df[df['Team'] == selected_country].groupby('Player-Name')['Errors-receive'].sum()
    erros_ataque = df[df['Team'] == selected_country].groupby('Player-Name')['Errors-attack'].sum()
    erros_saque = df[df['Team'] == selected_country].groupby('Player-Name')['Errors-serve'].sum()

    erros_totais = pd.DataFrame({
    'Erros Recepcao': erros_recepcao,
    'Erros Ataque': erros_ataque,
    'Erros Saque': erros_saque
    }).fillna(0)

    erros_totais['Total de Erros'] = erros_totais.sum(axis=1)
    erros_totais = erros_totais.sort_values(by='Total de Erros', ascending=False)
    erros_totais['Cumulativo'] = erros_totais['Total de Erros'].cumsum() / erros_totais['Total de Erros'].sum() * 100

    fig = go.Figure()

    # Add bar trace for total points
    fig.add_trace(go.Bar(
        x=erros_totais.index,
        y=erros_totais['Total de Erros'],
        name='Total de Erros',
        marker_color='#0095CC',
        marker_line=dict(width=2.5, color='black'),
        yaxis='y1'
    ))

    # Add line trace for cumulative percentage
    fig.add_trace(go.Scatter(
        x=erros_totais.index,
        y=erros_totais['Cumulativo'],
        name='Cumulativo (%)',
        mode='lines+markers',
        marker=dict(symbol='circle', size=8, color='red', line=dict(width=2, color='black')),
        yaxis='y2'
    ))

    # Update layout
    fig.update_layout(
        title='Análise Acumulativa de Erros por Jogador',
        xaxis_title='Jogador',
        yaxis=dict(
            title='Total de Erros',
            side='left',
            showgrid=False,
            showline=True,
            ticks="outside",
            titlefont=dict(color="#0095CC"),
            tickfont=dict(color="#0095CC")
        ),
        yaxis2=dict(
            title='Porcentagem Cumulativa (%)',
            overlaying='y',
            side='right',
            showgrid=False,
            showline=True,
            range=[0, 110],
            ticks="outside",
            titlefont=dict(color="red"),
            tickfont=dict(color="red")
        ),
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.5)'),
        xaxis=dict(tickangle=90),
        template='plotly_white'
    )

    return fig

# Callback to update the options of the player dropdown based on the selected genre and country
@app.callback(
    Output('player', 'options'),
    Input('generos-radio', 'value'),
    Input('country', 'value')
)
# Function to update the options of the player dropdown based on the selected genre and country
def set_players_options(selected_genero, selected_country):
    df, _ = return_df_genero(selected_genero)

    df = df.sort_values(by="Player-Name") # Sorting the dataframe by the column "Player-Name" (Alphabetical order)
    # Creating the options for the dropdown based on the unique values of the column "Player-Name"
    player_options = [{'label': i, 'value': i} for i in df[df["Team"] == selected_country]["Player-Name"].unique()]

    return player_options

# Callback to update the value of the player dropdown
@app.callback(
    Output('player', 'value'),
    Input('player', 'options'))
def set_player_value(available_options):
    return available_options[0]['value'] if available_options else None

# Callback to update the player statistics based on the selected player
@app.callback(
    Output("players_chart", "figure"),
    Input("player", "value"),
    Input("generos-radio", "value")
)
def generate_player_statistics(player, selected_genero):
    if not player:
        return go.Figure()

    df, color = return_df_genero(selected_genero)
    player_data = df[df['Player-Name'] == player]

    # Metrics to be displayed in the polar chart
    metrics = ['Attack-Points', 'Block-Points', 'Total-dig', 'Total-receive', 'Serve-Points', 'Total-setter']
    # metrics = ['Success-percent-attack', 'Efficiency-percent-block', 'Success-percent-dig', 'Success-percent-receive', 'Success-percent-serve', 'Success-percent-setter']
    # metrics = ['Points-attacks', 'Succesful-blocks', 'Successful-dig', 'Succesful-receive','serve-points', 'Successful-setter']

    fig = go.Figure() # Create a new figure

    # Add the player data to the polar chart
    for i, (idx, row) in enumerate(player_data.iterrows()):
        fig.add_trace(go.Scatterpolar(
            r=row[metrics].values,
            theta=['Ataque', 'Bloqueio', 'Defesa', 'Defesa de Saque', 'Saque', 'Levantar/Setter'],
            fill='toself',
            name=f"{row['Player-Name']} ({row['Team']})",
            marker=dict(
                size=10
            ),
            line=dict(
                width=3,
                color=color[i]
            )
        ))

    # Update the polar chart
    fig.update_polars(
        angularaxis=dict(
            rotation=0,
            direction="clockwise",
            showline=True,
            linecolor="black",
            showticklabels=True,
            ticks="outside",
            tickwidth=1,
            ticklen=1,
            tickcolor="black",
            tickfont=dict(
                family="Arial",
                size=20,
                color="black"
            ),
            showgrid=True
        ),
        radialaxis=dict(
            showline=True,
            range=[0, player_data[metrics].max().max()*1.1],
            showticklabels=False
        )
    )
    # Update the layout
    fig.update_layout(
        showlegend=False,
        title = "Estatísticas do Jogador",
        title_x=0.5
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)