test -e ssshtest || wget -q \
    https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest

. ssshtest

file_name="test/func/fire_gdp.png"

rm -f "$file_name"

run test_plot_runs python src/plot_fire_gdp.py \
    --co2 test/data/test_co2.csv \
    --gdp test/data/test_gdp.csv \
    --country Brazil \
    --out "$file_name"

assert_exit_code 0
assert_equal "$file_name" "$(ls "$file_name")"

rm -f "$file_name"
