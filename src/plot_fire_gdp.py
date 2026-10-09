import argparse

from matplotlib.figure import Figure

import fire_gdp


def plot_fire_gdp(co2_file, gdp_file, country, out_file):
    data = fire_gdp.get_fire_gdp_year_data(
        co2_file,
        gdp_file,
        country,
    )

    gdp = [row[2] for row in data]
    forest_fires = [row[1] for row in data]

    fig = Figure()
    ax = fig.subplots()

    ax.scatter(gdp, forest_fires)
    ax.set_xlabel("GDP (millions of local currency)")
    ax.set_ylabel("Forest fires")
    ax.set_title(f"{country}: Forest Fires vs. GDP")

    fig.tight_layout()
    fig.savefig(out_file)


def main():
    parser = argparse.ArgumentParser(
        description="Plot forest fire emissions against GDP."
    )
    parser.add_argument(
        "--co2",
        required=True,
        help="Path to the Agrofood CO2 emissions CSV file.",
    )
    parser.add_argument(
        "--gdp",
        required=True,
        help="Path to the IMF GDP CSV file.",
    )
    parser.add_argument(
        "--country",
        required=True,
        help="Country to plot.",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output plot file.",
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
