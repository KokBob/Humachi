# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 14:47:47 2025

@author: CIM2BJ
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Create a basic human body outline using scatter plot
body_parts = {
    'Head': (0, 6),
    'Chest': (0, 4),
    'Abdomen': (0, 2),
    'Left Arm': (-1.5, 4),
    'Right Arm': (1.5, 4),
    'Left Leg': (-0.5, 0),
    'Right Leg': (0.5, 0)
}

# Prepare scatter plot points
x_coords = [coords[0] for coords in body_parts.values()]
y_coords = [coords[1] for coords in body_parts.values()]
labels = list(body_parts.keys())

fig = go.Figure()

# Add scatter points for body parts
fig.add_trace(go.Scatter(
    x=x_coords,
    y=y_coords,
    mode='markers+text',
    text=labels,
    textposition='top center',
    marker=dict(size=10, color='blue'),
    hoverinfo='text'
))

# Set the layout to resemble a human body
fig.update_layout(
    title="Human Body Visualization",
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    showlegend=False,
    height=600
)

# App layout
app.layout = html.Div([
    html.H1("Human Body Dashboard", style={'text-align': 'center'}),
    dcc.Graph(id='body-visualization', figure=fig),
    html.Div(id='body-part-info', style={'margin-top': '20px', 'text-align': 'center'})
])

# Callbacks for interactivity
@app.callback(
    Output('body-part-info', 'children'),
    [Input('body-visualization', 'hoverData')]
)
def display_body_part_info(hover_data):
    if hover_data is not None:
        body_part = hover_data['points'][0]['text']
        return f"You hovered over: {body_part}"
    return "Hover over a body part to see details."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
