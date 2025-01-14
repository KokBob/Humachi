import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import random
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Initial coordinates for body parts
coords = {
    'Head': (0, 6),
    'Chest': (0, 4),
    'Abdomen': (0, 2),
    'Left Arm': (-1.5, 4),
    'Right Arm': (1.5, 4),
    'Left Leg': (-0.5, 0),
    'Right Leg': (0.5, 0)
}

# Generate initial time series data for body parts
body_parts_data = {part: [random.uniform(0, 1) for _ in range(10)] for part in coords.keys()}
time_index = list(range(10))

# App layout
app.layout = html.Div([
    html.H1("Human Body Simulation", style={'text-align': 'center'}),
    dcc.Graph(id='body-visualization'),
    html.Div(id='body-part-info', style={'margin-top': '20px', 'text-align': 'center'}),
    dcc.Graph(id='time-series-graph'),
    dcc.Interval(
        id='interval-update',
        interval=1000,  # Update every second
        n_intervals=0
    )
])

# Update the body visualization with movement
@app.callback(
    Output('body-visualization', 'figure'),
    Input('interval-update', 'n_intervals')
)
def update_body_visualization(n):
    # Simulate movement with sine wave oscillation
    movement = np.sin(n / 2) * 0.2  # Adjust amplitude and frequency
    dynamic_coords = {
        part: (x + random.uniform(-0.1, 0.1), y + movement if part != 'Head' else y + movement / 2)
        for part, (x, y) in coords.items()
    }
    
    x_coords = [v[0] for v in dynamic_coords.values()]
    y_coords = [v[1] for v in dynamic_coords.values()]
    labels = list(dynamic_coords.keys())
    
    # Create figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers+text',
        text=labels,
        textposition='top center',
        marker=dict(size=10, color='blue'),
        hoverinfo='text'
    ))
    fig.update_layout(
        title="Human Body with Movement",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        height=600
    )
    return fig

# Update the time series for the selected body part
@app.callback(
    [Output('time-series-graph', 'figure'),
     Output('body-part-info', 'children')],
    [Input('body-visualization', 'hoverData'),
     Input('interval-update', 'n_intervals')]
)
def update_time_series(hover_data, n):
    selected_part = 'Head'  # Default to 'Head' if no hover
    if hover_data is not None:
        selected_part = hover_data['points'][0]['text']
    
    # Simulate new data for the selected body part
    body_parts_data[selected_part].append(random.uniform(0, 1))
    body_parts_data[selected_part] = body_parts_data[selected_part][-10:]  # Keep last 10 points
    
    # Create time series plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_index,
        y=body_parts_data[selected_part],
        mode='lines+markers',
        name=selected_part
    ))
    fig.update_layout(
        title=f"Time Series for {selected_part}",
        xaxis_title="Time",
        yaxis_title="Value",
        height=400
    )
    
    return fig, f"Currently viewing time series for: {selected_part}"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
