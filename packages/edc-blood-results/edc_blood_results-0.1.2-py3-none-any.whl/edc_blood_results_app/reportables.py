from edc_reportable import site_reportables
from edc_reportable.grading_data import daids_july_2017 as grading_data
from edc_reportable.normal_data.africa import normal_data

site_reportables.register(
    name="my_reportables", normal_data=normal_data, grading_data=grading_data
)
