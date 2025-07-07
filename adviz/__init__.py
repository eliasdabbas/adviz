__version__ = "0.0.24"

from dash_bootstrap_templates import load_figure_template

from .ecdf import ecdf
from .flag import country_code_flag, flag
from .racing_chart import racing_chart
from .serp_heatmap import serp_heatmap
from .status_codes import status_codes
from .style_table import style_table
from .url_structure import url_structure
from .value_counts import value_counts
from .value_counts_plus import value_counts_plus

load_figure_template("all")
