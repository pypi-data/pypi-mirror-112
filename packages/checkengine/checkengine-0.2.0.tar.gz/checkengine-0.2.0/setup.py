# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['checkengine']

package_data = \
{'': ['*'], 'checkengine': ['_constraints/*']}

install_requires = \
['pyspark==3.0.3']

setup_kwargs = {
    'name': 'checkengine',
    'version': '0.2.0',
    'description': 'Data-quality checks for PySpark',
    'long_description': '## Summary\n\nThe goal of this project is to implement a data validation library for PySpark. The library should detect the incorrect structure of the data, unexpected values in columns, and anomalies in the data.\n\n## How to install\n\nTHERE IS NO PACKAGE YET!!!\n\n## How to use\n\n```\nfrom checkengine.validate_df import ValidateSparkDataFrame\n\nresult = ValidateSparkDataFrame(spark_session, spark_data_frame) \\\n        .is_not_null("column_name") \\\n        .are_not_null(["column_name_2", "column_name_3"]) \\\n        .is_min("numeric_column", 10) \\\n        .is_max("numeric_column", 20) \\\n        .is_unique("column_name") \\\n        .are_unique(["column_name_2", "column_name_3"]) \\\n        .is_between("numeric_column_2", 10, 15) \\\n        .has_length_between("text_column", 0, 10) \\\n        .mean_column_value("numeric_column", 10, 20) \\\n        .median_column_value("numeric_column", 5, 15) \\\n        .text_matches_regex("text_column", "^[a-z]{3,10}$") \\\n        .one_of("text_column", ["value_a", "value_b"]) \\\n        .one_of("numeric_column", [123, 456]) \\\n        .execute()\n\nresult.correct_data #rows that passed the validation\nresult.erroneous_data #rows rejected during the validation\nresults.errors a summary of validation errors (three fields: column_name, constraint_name, number_of_errors)\n```\n\n## How to build\n\n1. Install the Poetry build tool.\n\n2. Run the following commands:\n\n```\ncd check-engine-lib\npoetry build\n```\n\n## How to test locally\n\n### Run all tests\n\n```\ncd check-engine-lib\npoetry run pytest tests/\n```\n\n### Run a single test file\n\n```\ncd check-engine-lib\npoetry run pytest tests/test_between_integer.py\n```\n\n### Run a single test method\n\n```\ncd check-engine-lib\npoetry run pytest tests/test_between_integer.py -k \'test_should_return_df_without_changes_if_all_are_between\'\n```\n\n## How to test in Docker\n\n```\ndocker build -t check-engine-test check-engine-lib/. && docker run check-engine-test\n```\n',
    'author': 'Bartosz Mikulski',
    'author_email': 'mail@mikulskibartosz.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mikulskibartosz/check-engine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
