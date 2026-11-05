COUNTRIES = {
    "brazil": "Brazil",
    "india": "India",
    "united_states": "United States of America",
    "united_kingdom":
        "United Kingdom of Great Britain and Northern Ireland",
}


rule all:
    input:
        expand(
            "results/{country}_fire_gdp.png",
            country=COUNTRIES.keys(),
        )


rule plot_fire_gdp:
    input:
        co2="data/Agrofood_co2_emission.csv",
        gdp="data/IMF_GDP.csv",
    output:
        "results/{country}_fire_gdp.png"
    params:
        country=lambda wildcards: COUNTRIES[wildcards.country]
    shell:
        """
        /Users/ashlynsloane/.pixi/envs/snakemake/bin/python \
            src/plot_fire_gdp.py \
            --co2 {input.co2} \
            --gdp {input.gdp} \
            --country "{params.country}" \
            --out {output}
        """
