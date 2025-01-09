"""Configuration for world_map.py."""

# Page options
PAGE_SIZE_MM = (420, 297)
FILENAME = 'world_map.png'
SAVEFIG_KWARGS = {}  # passed to ax.savefig

# Country options
ALLOWED_COUNTRY_COLORS = [  # exactly 7 colors required
    'tab:orange',
    'tab:green',
    'tab:red',
    'tab:purple',
    'tab:brown',
    'tab:gray',
    'tab:olive',
]
COUNTRY_ALPHA = 0.5
LARGE_COUNTRY_FONTSIZE = 8
SMALL_COUNTRY_FONTSIZE  = 4
COUNTRY_AREA_THRESH = 500  # dimensionless threshold for switching font sizes
COUNTRY_BORDER_KWARGS = {
    'edgecolor': '0.5',
    'linewidth': 0.3
}
COUNTRY_LABEL_KWARGS = {  # passed to ax.text
    'weight': 'bold',
}
ADJUSTTEXT_KWARGS = {  # passed to adjustText.adjust_text
    'time_lim': 10,
    'arrowprops': {"arrowstyle": '-', "color": 'k'},
}
MIN_ARROW_LENGTH = 1  # labels that are moved further than this have arrows

# Ocean options
OCEAN_KWARGS = {}  # passed to ax.add_feature
BASIN_LABEL_KWARGS = {  # passed to ax.text
    'color': 'tab:blue',
}
COASTLINE_KWARGS = {  # passed to ax.coastlines
    'linewidth': 0.3,
}
LAKE_KWARGS = {  # passed to ax.add_feature
    'edgecolor': 'blue',
    'linewidth': 0.3
}

# Gridline options
MAJOR_GRIDLINE_SPACING = 20  # in degrees
MAJOR_GRIDLINE_KWARGS = {  # passed to ax.gridlines
    'color': 'blue',
    'linewidth': 0.5,
    'formatter_kwargs': {
        'direction_label': False,
        'degree_symbol': '',
    },
    'xlabel_style': {
        'color': 'blue',
    },
    'ylabel_style': {
        'color': 'blue',
    },
}
MINOR_GRIDLINE_KWARGS = {  # passed to ax.gridlines
    'color': ('blue', 0.4),
    'linewidth': 0.5,
}

# Tropic and polar circle options
TROPICS_LAT = 23.43604  # in degrees
TROPICS_CIRCLES_KWARGS = {  # passed to ax.hlines
    'color': 'blue',
    'linewidth': 0.5,
    'linestyle': (0, (12, 12)),
}
