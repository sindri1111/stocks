

colors = {
    'background': '#222',
    'text': '#2d2d2d',
    'tickcolors': "#E90"
}

graph_layout = {
    'uirevision': True,
    'plot_bgcolor': colors['background'],
    'paper_bgcolor': colors['background'],
    'xaxis':dict(type="category", showticklabels=False, gridcolor=colors['tickcolors']),
    'yaxis':dict(color=colors['tickcolors'], gridcolor=colors['tickcolors']),

}