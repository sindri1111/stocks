

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
    'xaxis2':dict(type="category", showticklabels=False, gridcolor=colors['tickcolors'],
                  showgrid=False),
    'yaxis2':dict(color=colors['tickcolors'], gridcolor=colors['tickcolors'],
                  showgrid=False),
    'margin':{'t': 0,'l':0,'b':0,'r':10}
}