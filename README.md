# Fire Emissions and GDP

This project combines forest-fire emissions data with GDP data by country and
year using test-driven development.

## Data

The two full data files can be downloaded with:

```bash
mkdir -p data

curl -L \
  "https://docs.google.com/uc?export=download&id=1AsXP_OGs1O_TDeXiZjk3fYV1SrG4vwXF" \
  -o data/Agrofood_co2_emission.csv

curl -L \
  "https://docs.google.com/uc?export=download&id=19YEPysdnK7VCXuAe9Og9pwYkNT5CbQzr" \
  -o data/IMF_GDP.csv
```

The full data files are stored in `data/` and are not committed to the
repository. Small test data files are stored in `test/data/`.

## Introduction

This analysis examines the relationship between forest-fire emissions and GDP
over time within individual countries. Forest-fire emissions come from the
Agrofood CO2 emissions dataset, while GDP comes from the IMF GDP dataset.

GDP is reported in millions of each country's local currency, so countries are
analyzed separately rather than pooling GDP values across countries.

Assignment 6 examined four countries in detail: Brazil, India, the United
States of America, and the United Kingdom of Great Britain and Northern
Ireland. The Assignment 8 Snakemake workflow expands the analysis to include
Argentina, Australia, Canada, and China.

## Results

The relationship between GDP and forest-fire emissions differed among the four
countries.

Brazil showed a weak negative association between GDP and forest-fire
emissions (Pearson r = -0.189, n = 25). India showed a similar weak negative
association (r = -0.192, n = 16).

The United States of America showed essentially no linear association
(r = 0.000, n = 31).

The United Kingdom of Great Britain and Northern Ireland showed the strongest
negative association among the four countries examined
(r = -0.496, n = 26).

These results are descriptive associations and do not demonstrate that changes
in GDP cause changes in forest-fire emissions.

### Brazil

![Brazil forest-fire emissions versus GDP](results/brazil_fire_gdp.png)

### India

![India forest-fire emissions versus GDP](results/india_fire_gdp.png)

### United States of America

![United States forest-fire emissions versus GDP](results/united_states_fire_gdp.png)

### United Kingdom of Great Britain and Northern Ireland

![United Kingdom forest-fire emissions versus GDP](results/united_kingdom_fire_gdp.png)

### Argentina

![Argentina forest-fire emissions versus GDP](results/argentina_fire_gdp.png)

### Australia

![Australia forest-fire emissions versus GDP](results/australia_fire_gdp.png)

### Canada

![Canada forest-fire emissions versus GDP](results/canada_fire_gdp.png)

### China

![China forest-fire emissions versus GDP](results/china_fire_gdp.png)

## Methods

The Agrofood CO2 dataset contains one row per country and year. The `Area`,
`Year`, and `Forest fires` columns were used. The IMF GDP dataset contains one
row per country, with individual years stored as columns.

The `get_fire_gdp_year_data()` function matches the two datasets by country and
year. Years with missing forest-fire values, missing GDP values, or years not
present in the GDP header are excluded.

Scatter plots were generated separately for each country using
`src/plot_fire_gdp.py`.

To reproduce the plots, run:

```bash
mkdir -p results

python src/plot_fire_gdp.py \
  --co2 data/Agrofood_co2_emission.csv \
  --gdp data/IMF_GDP.csv \
  --country Brazil \
  --out results/brazil_fire_gdp.png

python src/plot_fire_gdp.py \
  --co2 data/Agrofood_co2_emission.csv \
  --gdp data/IMF_GDP.csv \
  --country India \
  --out results/india_fire_gdp.png

python src/plot_fire_gdp.py \
  --co2 data/Agrofood_co2_emission.csv \
  --gdp data/IMF_GDP.csv \
  --country "United States of America" \
  --out results/united_states_fire_gdp.png

python src/plot_fire_gdp.py \
  --co2 data/Agrofood_co2_emission.csv \
  --gdp data/IMF_GDP.csv \
  --country "United Kingdom of Great Britain and Northern Ireland" \
  --out results/united_kingdom_fire_gdp.png
```

Pearson correlation coefficients were calculated separately within each
country using the matched year-level GDP and forest-fire values.

## Testing

Run the unit tests with:

```bash
python -m unittest discover -s test/unit -p "test_*.py" -v
```

Run the functional test with:

```bash
bash test/func/test_fire_gdp.sh
```

Run style checks with:

```bash
pycodestyle src/fire_gdp.py src/plot_fire_gdp.py test/unit/test_fire_gdp.py
```

## Snakemake Workflow

The analysis is managed with Snakemake. The workflow uses a country wildcard
to generate forest-fire emissions versus GDP plots for multiple countries
using the same plotting rule.

The current workflow generates plots for:

- Argentina
- Australia
- Brazil
- Canada
- China
- India
- United States of America
- United Kingdom of Great Britain and Northern Ireland

To preview the jobs Snakemake would run without executing them:

    snakemake -n

To run the complete workflow with one core:

    snakemake -j 1

Snakemake tracks the input data and output plots so that completed outputs do
not need to be regenerated unless an input changes or an output is missing.

## Workflow Testing Ideas

Workflow testing should verify both the individual analysis code and the
connections between workflow steps.

Possible workflow tests include:

1. Run `snakemake -n` to verify that Snakemake can construct the workflow DAG
   without syntax or dependency errors.
2. Run the workflow on small test input files and confirm that all expected
   output files are created.
3. Delete one expected output file and rerun Snakemake to verify that only the
   missing or outdated output is regenerated.
4. Check that running Snakemake again after a successful workflow reports that
   all requested files are present and up to date.
5. Test invalid or missing input files and confirm that the workflow fails
   rather than silently producing incorrect output.
6. Compare outputs generated from known test data with expected results.
7. Run the existing unit and functional tests together with the workflow in
   continuous integration so that changes to the analysis code cannot silently
   break the workflow.
