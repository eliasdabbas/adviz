"""Styling `DataFrame`s to make them more readable and skannable with heatmaps, bar charts, categorical colors, and plain text."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/05_style_table.ipynb.

# %% auto 0
__all__ = ['style_table']

# %% ../nbs/05_style_table.ipynb 3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# %% ../nbs/05_style_table.ipynb 4
def _category_to_color(categories, colorscale='D3'):
    colorscale = eval(f'px.colors.qualitative.{colorscale}')
    cat_dict = dict(enumerate(set(categories)))
    cat_dict = {v: colorscale[k] for k, v in cat_dict.items()}
    return [cat_dict[cat] for cat in categories]


# %% ../nbs/05_style_table.ipynb 5
def style_table(
    df,
    column_types,
    column_widths=None,
    title=None,
    precision=1,
    width=None,
    height=None,
    theme='plotly_white',
    font_size=None,
    title_font_size=None):
    """Convert a DataFrame to multiple charts (one for each column).

    Parameters
    ----------
    df : pandas.DataFrame
      Any DataFrame, but typically a small one, to display as a report.
    column_types : list
      A list of types, one for each column. Possible values are "bar", "heatmap", "category", and "text".
    column_widths : list
      A list of fractions that should add up to 1. Each fraction corresponds to a column.
    title : str
      The title of the chart.
    precision : int
      How many decimals of precision to display in numeric columns. This affects all numeric columns.
    width : int
      The width of the entire chart in pixels.
    height : int
      The height of the entire chart in pixels.
    theme : str
      The theme used for styling the entire chart.
    font_size : int
      The size of font of text and number on the chart in points.
    title_font_size : int
      The size of font of the title of the chart in points.
    Returns
    -------
    styled_table : plotly.graph_objects.Figure
      A Plotly Figure object that can be retroactively edited if desired.
    """
    if not set(column_types).issubset(["bar", "heatmap", "category", "text"]):
        raise ValueError("Please make sure you specify any of the following types:\n"
                         "'bar', 'heatmap', 'category', and 'text'")
    fig = make_subplots(
        rows=1,
        cols=df.shape[1],
        column_widths=column_widths,
        horizontal_spacing=0,
        subplot_titles=df.columns)
    categorical_scales = [data.y[0] for data in px.colors.qualitative.swatches().data][::-1]
    categorical_index = 0
    texttemplate = f'%{{text:,.{precision}f}}'
    for i, col in enumerate(df):
        if column_types[i] == 'heatmap':
            fig.add_heatmap(
                z=df[[col]],
                name=col,
                showscale=False,
                colorscale='cividis',
                hovertemplate=texttemplate,
                text=df[[col]],
                texttemplate=texttemplate,
                row=1,
                col=i+1)
        elif column_types[i] == 'bar':
            fig.add_bar(
                x=df[col],
                y=list(range(len(df))),
                showlegend=False,
                orientation='h',
                col=i+1,
                marker={'color': 'steelblue'},
                text=df[col],
                texttemplate=texttemplate,
                hovertemplate=texttemplate,
                row=1,
                name=col)
        elif column_types[i] == 'category':
            categorical_index += 1
            fig.add_bar(
                x=[10 for i in range(len(df))],
                y=list(range(len(df))),
                showlegend=False,
                marker={'color': _category_to_color(
                    df[col],
                    categorical_scales[categorical_index] if df[col].nunique() <= 10 else 'Dark24'),
                        'opacity': 1},
                row=1,
                col=i+1,
                name=col,
                orientation='h',
                text=df[col],
                hovertemplate='<b>%{text}')
        elif column_types[i] == 'text':
            fig.add_bar(
                x=[10 for i in range(len(df))],
                y=list(range(len(df))),
                orientation='h',
                showlegend=False,
                name=col,
                hovertemplate='<b>%{text}',
                marker={'color': 'white'},
                text=df[col],
                texttemplate='%{text}',
                row=1,
                col=i+1)
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, autorange='reversed')
    fig.update_layout(bargap=0, template=theme, width=width, height=height,
                      title=title, font_size=font_size, title_font_size=title_font_size)
    return fig
