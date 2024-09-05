import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Load the dataset
df = pd.read_csv('C:\\Users\\Lenovo\\Documents\\dashdata\\superstore.csv')

# Check the first few rows of the dataframe
print(df.head())

# Handle missing or incorrect columns
required_columns = ['Category', 'Sales', 'Region', 'Sub.Category', 'Profit']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# Aggregate data for the visualizations
category_sales = df.groupby('Category')['Sales'].sum().reset_index()
fig1 = px.bar(category_sales, x='Category', y='Sales', title='Total Sales by Category', color='Category')

region_sales = df.groupby('Region')['Sales'].sum().reset_index()
fig2 = px.bar(region_sales, x='Region', y='Sales', title='Total Sales by Region', color='Region')

subcat_profit = df.groupby('Sub.Category')['Profit'].sum().reset_index()
fig3 = px.bar(subcat_profit, x='Sub.Category', y='Profit', title='Total Profit by Sub-Category', color='Sub.Category')

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define layout
app.layout = html.Div(style={'backgroundColor': '#2E2E2E'}, children=[
    html.H1("Global Superstore Dashboard", style={'text-align': 'center', 'color': '#FFFFFF'}),

    html.Div([
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': category, 'value': category} for category in df['Category'].unique()],
            value=df['Category'].unique()[0],  # Set default value
            style={
                'width': '60%',
                'padding': '5px',
                'backgroundColor': '#F0F0F0',  # Light gray background
                'color': '#000000',  # Black text color
                'border': '1px solid #CCCCCC',  # Light border color
                'fontSize': '18px',
                'margin': 'auto',  # Center align the dropdown
                'borderRadius': '5px',  # Rounded corners
                'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.2)'  # Add shadow for depth
            },
            clearable=False
        ),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in df['Region'].unique()],
            value=df['Region'].unique()[0],  # Set default value
            style={
                'width': '60%',
                'padding': '5px',
                'backgroundColor': '#F0F0F0',  # Light gray background
                'color': '#000000',  # Black text color
                'border': '1px solid #CCCCCC',  # Light border color
                'fontSize': '18px',
                'margin': 'auto',  # Center align the dropdown
                'borderRadius': '5px',  # Rounded corners
                'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.2)'  # Add shadow for depth
            },
            clearable=False
        ),
    ], style={'padding': '20px', 'text-align': 'center'}),

    html.Div([
        dcc.Graph(id='sales-by-category', figure=fig1, style={'height': '400px'}),
        dcc.Graph(id='sales-by-region', figure=fig2, style={'height': '400px'}),
        dcc.Graph(id='profit-by-subcategory', figure=fig3, style={'height': '400px'})
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(3, 1fr)', 'gap': '20px', 'padding': '20px'}),

    html.Div(id='output-container', children=[], style={'padding': '20px'}),

    html.Div(id='scroll-container', style={'margin-top': '50px'}),
    
    html.Div([
        html.Button('Download Data', id='download-button', n_clicks=0),
        dcc.Download(id='download-data')
    ], style={'text-align': 'center', 'padding': '20px'})
])

# Define callback to update graphs and scroll to the graph based on selected category
@app.callback(
    [Output(component_id='output-container', component_property='children'),
     Output(component_id='scroll-container', component_property='children')],
    [Input(component_id='category-dropdown', component_property='value'),
     Input(component_id='region-dropdown', component_property='value')]
)
def update_graph(selected_category, selected_region):
    filtered_df = df[(df['Category'] == selected_category) & (df['Region'] == selected_region)]
    
    # Line plot for sales distribution
    fig = px.line(
        filtered_df, 
        x='Sub.Category', 
        y='Sales', 
        color='Region', 
        markers=True, 
        title=f'Sales Distribution for {selected_category} in {selected_region}'
    )
    fig.update_layout(
        plot_bgcolor='#2E2E2E',
        paper_bgcolor='#2E2E2E',
        font_color='white'
    )
    
    # Creating a div with an id that the browser can scroll to
    return '', html.Div([
        html.H2(f'Sales Distribution for {selected_category} in {selected_region}', style={'color': '#FFFFFF'}),
        dcc.Graph(figure=fig, style={'height': '400px'})
    ], id='scroll-target', style={'padding': '20px', 'text-align': 'center', 'border-top': '2px solid #FFFFFF'})

@app.callback(
    Output('download-data', 'data'),
    Input('download-button', 'n_clicks'),
    prevent_initial_call=True
)
def download_data(n_clicks):
    if n_clicks > 0:
        return dcc.send_data_frame(df.to_csv, 'filtered_data.csv')

# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
