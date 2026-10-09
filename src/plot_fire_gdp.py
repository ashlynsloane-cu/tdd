import argparse
import math
import os

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

import fire_gdp


def short_country_name(country):
    names = {
        "United States of America": "United States",
        "United Kingdom of Great Britain and Northern Ireland":
            "United Kingdom",
    }

    return names.get(country, country)


def linear_fit(x_values, y_values):
    n_values = len(x_values)

    x_mean = sum(x_values) / n_values
    y_mean = sum(y_values) / n_values

    x_ss = sum(
        (value - x_mean) ** 2
        for value in x_values
    )

    y_ss = sum(
        (value - y_mean) ** 2
        for value in y_values
    )

    covariance = sum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(x_values, y_values)
    )

    if x_ss == 0:
        slope = 0.0
    else:
        slope = covariance / x_ss

    intercept = y_mean - (slope * x_mean)

    if x_ss == 0 or y_ss == 0:
        correlation = 0.0
    else:
        correlation = covariance / math.sqrt(x_ss * y_ss)

    return slope, intercept, correlation


def plot_fire_gdp(co2_file, gdp_file, country, out_file):
    data = fire_gdp.get_fire_gdp_year_data(
        co2_file,
        gdp_file,
        country,
    )

    if len(data) == 0:
        raise ValueError(
            "No overlapping fire and GDP data found for "
            + country
        )

    years = [row[0] for row in data]
    fire_values = [row[1] for row in data]
    gdp_values = [row[2] for row in data]

    slope, intercept, correlation = linear_fit(
        gdp_values,
        fire_values,
    )

    fitted_values = [
        intercept + (slope * value)
        for value in gdp_values
    ]

    sorted_pairs = sorted(
        zip(gdp_values, fitted_values),
        key=lambda pair: pair[0],
    )

    figure = Figure(figsize=(8, 6))
    FigureCanvas(figure)
    axis = figure.add_subplot(1, 1, 1)

    axis.scatter(
        gdp_values,
        fire_values,
        s=45,
        alpha=0.9,
        label="Observed data",
    )

    axis.plot(
        [pair[0] for pair in sorted_pairs],
        [pair[1] for pair in sorted_pairs],
        linewidth=2,
        label=f"Linear fit (r = {correlation:.3f})",
    )

    axis.set_title(
        short_country_name(country) + ": Forest Fires vs. GDP"
    )
    axis.set_xlabel("GDP (millions of local currency)")
    axis.set_ylabel("Forest fires")

    axis.grid(True, alpha=0.3)
    axis.legend(frameon=False)

    axis.text(
        0.02,
        0.98,
        (
            f"n = {len(data)}\n"
            f"Years: {min(years)}–{max(years)}\n"
            f"Pearson r = {correlation:.3f}"
        ),
        transform=axis.transAxes,
        ha="left",
        va="top",
        bbox={
            "boxstyle": "round",
            "facecolor": "white",
            "alpha": 0.85,
            "edgecolor": "0.8",
        },
    )

    axis.xaxis.set_major_formatter(
        FuncFormatter(lambda value, _: f"{value:,.0f}")
    )
    axis.tick_params(axis="x", rotation=30)

    figure.tight_layout()

    output_dir = os.path.dirname(out_file)

    if output_dir != "":
        os.makedirs(output_dir, exist_ok=True)

    figure.savefig(
        out_file,
        dpi=200,
        bbox_inches="tight",
    )


def main():
    parser = argparse.ArgumentParser(
        description="Plot forest-fire emissions versus GDP."
    )

    parser.add_argument(
        "--co2",
        required=True,
        help="Input CO2 CSV file",
    )

    parser.add_argument(
        "--gdp",
        required=True,
        help="Input GDP CSV file",
    )

    parser.add_argument(
        "--country",
        required=True,
        help="Country to plot",
    )

    parser.add_argument(
        "--out",
        required=True,
        help="Output PNG file",
    )

    args = parser.parse_args()

    plot_fire_gdp(
        args.co2,
        args.gdp,
        args.country,
        args.out,
    )


if __name__ == "__main__":
    main()
