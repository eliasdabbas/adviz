# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_url_structure.ipynb.

# %% auto 0
__all__ = ['url_structure']

# %% ../nbs/02_url_structure.ipynb 3
import advertools as adv
import adviz
import pandas as pd
pd.options.display.max_colwidth = 120
import plotly.express as px

# %% ../nbs/02_url_structure.ipynb 4
_texttemplate = '<b>%{label} </b><br><br>Directory: <b>%{parent}/%{label}</b><br>Count: %{value:,}<br>%{percentParent:.1%} of %{parent}<br>'

# %% ../nbs/02_url_structure.ipynb 5
def url_structure(
    url_list,
    items_per_level=10,
    height=600,
    width=None,
    theme='none',
    domain='example.com',
    title='URL Structure'):
    """
    Create a treemap for each URL path directory /dir_1/dir_2/dir_3/...
    """
    urldf = adv.url_to_df(url_list)
    dir1_top_n = urldf['dir_1'].value_counts().head(items_per_level).index.tolist() + ['Others:']
    urldf['dir_1_clean'] = [x if x in dir1_top_n else 'Others:' for x in urldf['dir_1']]
    top_n_df = pd.DataFrame(dir1_top_n, columns=['dir_1_top_n'])

    dir2_valcounts = []

    for top_n in top_n_df['dir_1_top_n']:
        tempdf = urldf[urldf['dir_1_clean'].eq(top_n)]
        valcountsdf = adviz.value_counts_plus(tempdf['dir_2'], show_top=items_per_level, style=False)
        valcountsdf = valcountsdf.assign(dir_1_value=top_n)
        dir2_valcounts.append(valcountsdf)
    dir2_df = pd.concat(dir2_valcounts, ignore_index=True)[['data', 'count', 'dir_1_value']]
    treemap_df = pd.merge(
        top_n_df,
        dir2_df,
        left_on='dir_1_top_n',
        right_on='dir_1_value',
        how='left')
    fig = px.treemap(
        treemap_df.dropna(), 
        path=[px.Constant(domain), 'dir_1_top_n', 'data'], 
        branchvalues='total',
        maxdepth=2,
        width=width,
        height=height,
        title=title,
        template=theme,
        values='count')
    fig.data[0].marker.line.width = 0.01
    fig.data[0].marker.pad = dict.fromkeys('lrbt', 0)
    fig.data[0]['texttemplate'] = _texttemplate
    fig.data[0]['hovertemplate'] = _texttemplate
    fig.update_traces(pathbar={'edgeshape': '/'})
    return fig