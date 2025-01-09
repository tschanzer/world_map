"""Script to generate a world map."""

import adjustText
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import numpy as np
import shapely
from matplotlib import ticker

from config import *  # pylint: disable=wildcard-import


def argmax(values):
    """Returns the index of the max value."""
    return max(range(len(values)), key=values.__getitem__)


def largest_piece_centroid(poly):
    """
    Finds the centroid of the largest piece of a Polygon/MultiPolygon.

    Args:
        poly: shapely.Polygon or shapely.MultiPolygon.

    Returns:
        x, y: The coordinates of the centroid of the largest piece.
    """

    if isinstance(poly, shapely.Polygon):
        x = poly.centroid.x
        y = poly.centroid.y
    else:
        areas = [g.area for g in poly.geoms]
        largest_geom = poly.geoms[argmax(areas)]
        x = largest_geom.centroid.x
        y = largest_geom.centroid.y
    return x, y


def patch_length(patch):
    """Returns the length of a FancyArrowPatch."""
    vertices = patch.get_path().vertices
    return np.linalg.norm(np.diff(vertices, axis=0), axis=1).sum()


def plot_countries(ax):
    """Plot countries and their names on the map."""
    shpfilename = shpreader.natural_earth(
        resolution='50m', category='cultural', name='admin_0_countries')
    countries = shpreader.Reader(shpfilename).records()
    country_labels = []
    country_colors = []
    for country in countries:
        color = ALLOWED_COUNTRY_COLORS[country.attributes['MAPCOLOR7']-1]
        ax.add_geometries(
            country.geometry,
            facecolor=(color, COUNTRY_ALPHA),
            crs=ccrs.PlateCarree(),
            zorder=1,
        )
        if country.geometry.area > COUNTRY_AREA_THRESH:
            fontsize = LARGE_COUNTRY_FONTSIZE
        else:
            fontsize = SMALL_COUNTRY_FONTSIZE
        t = ax.text(
            *largest_piece_centroid(country.geometry),
            country.attributes['NAME'].upper(),
            ha='center',
            va='center',
            size=fontsize,
            color=color,
            **COUNTRY_LABEL_KWARGS,
        )

        if country.geometry.area < COUNTRY_AREA_THRESH:
            country_colors.append(color)
            country_labels.append(t)

    return country_colors, country_labels


def label_ocean_basins(ax):
    """Label ocean basins on the map."""
    shpfilename = shpreader.natural_earth(
        resolution='110m', category='physical', name='geography_marine_polys')
    water_bodies = shpreader.Reader(shpfilename).records()
    for body in water_bodies:
        if body.attributes['scalerank'] == 0:
            ax.text(
                *largest_piece_centroid(body.geometry),
                body.attributes['name'].upper(),
                ha='center',
                va='center',
                **BASIN_LABEL_KWARGS,
            )


def draw_gridlines(ax):
    """Draw lat/lon gridlines on the map."""
    ax.gridlines(
        draw_labels=True,
        xlocs=ticker.MultipleLocator(MAJOR_GRIDLINE_SPACING),
        ylocs=ticker.MultipleLocator(MAJOR_GRIDLINE_SPACING),
        **MAJOR_GRIDLINE_KWARGS,
    )
    ax.gridlines(
        xlocs=ticker.MultipleLocator(
            MAJOR_GRIDLINE_SPACING, MAJOR_GRIDLINE_SPACING/2),
        ylocs=ticker.MultipleLocator(
            MAJOR_GRIDLINE_SPACING, MAJOR_GRIDLINE_SPACING/2),
        **MINOR_GRIDLINE_KWARGS,
    )


def draw_tropics_circles(ax):
    """Draw tropics and polar circles on the map."""
    ax.hlines(
        [-TROPICS_LAT, TROPICS_LAT - 90, 90 - TROPICS_LAT, TROPICS_LAT],
        xmin=ax.get_xlim()[0],
        xmax=ax.get_xlim()[1],
        transform=ccrs.PlateCarree(),
        **TROPICS_CIRCLES_KWARGS,
    )


def adjust_country_labels(country_colors, country_labels):
    """Adjust country labels on the map to prevent overlaps."""
    _, patches = adjustText.adjust_text(
        country_labels, min_arrow_len=0, **ADJUSTTEXT_KWARGS)
    for i, patch in enumerate(patches):
        if patch_length(patch) < MIN_ARROW_LENGTH:
            patch.remove()
        else:
            patch.set(color=country_colors[i])


def main():
    """Generate a world map."""
    fig = plt.figure(
        figsize=(PAGE_SIZE_MM[0]/25.4, PAGE_SIZE_MM[1]/25.4),
        constrained_layout=True,
    )
    ax = fig.add_subplot(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.add_feature(cfeature.OCEAN.with_scale('50m'), **OCEAN_KWARGS)
    ax.add_feature(cfeature.BORDERS.with_scale('50m'), **COUNTRY_BORDER_KWARGS)
    ax.coastlines('50m', **COASTLINE_KWARGS)
    ax.add_feature(cfeature.LAKES.with_scale('50m'), **LAKE_KWARGS)

    country_colors, country_labels = plot_countries(ax)
    label_ocean_basins(ax)
    draw_gridlines(ax)
    draw_tropics_circles(ax)
    adjust_country_labels(country_colors, country_labels)

    fig.savefig(FILENAME, **SAVEFIG_KWARGS)
    plt.close()

if __name__ == '__main__':
    main()
