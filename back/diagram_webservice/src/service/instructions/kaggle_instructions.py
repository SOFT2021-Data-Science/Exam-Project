from .abstract_instructions import AbstractInstruction
from .param import Param
from .model import Model
from logic.kaggle import kaggle_get_list_of_all_values_in_row_by_column_name

genders = [
    gender.lower()
    for gender in kaggle_get_list_of_all_values_in_row_by_column_name("sex")
]
country = kaggle_get_list_of_all_values_in_row_by_column_name("country")


class KaggleInstruction(AbstractInstruction):
    """Instructions for the Kaggle dataset. Implements AbstractInstruction

    :param AbstractInstruction: Instructions for what the frontend must display. Stored with redis
    :type AbstractInstruction: ABC
    """

    def __init__(self):
        linear_regression_params = {
            "country": Param(country, "enum").as_json(),
            "gender": Param(genders, "enum").as_json(),
        }
        kmeans_clustering_params = {
            "country": Param(country, "enum").as_json(),
            "gender": Param(genders, "enum").as_json(),
            "clusters": Param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "range").as_json(),
        }
        kmeans_elbow_params = {
            "country": Param(country, "enum").as_json(),
            "gender": Param(genders, "enum").as_json(),
            "clusters": Param([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "range").as_json(),
        }
        comparison_genders_single_country_params = {
            "country": Param(country, "enum").as_json(),
        }
        comparison_two_countries = {
            "country_1": Param(country, "enum").as_json(),
            "country_2": Param(country, "enum").as_json(),
            "gender": Param(genders, "enum").as_json(),
        }

        linear_regression_model = Model(
            "linear_regression",
            linear_regression_params,
        ).as_json()

        kmeans_clustering_model = Model(
            "kmeans/clustering", kmeans_clustering_params
        ).as_json()

        kmeans_elbow_model = Model("kmeans/elbow", kmeans_elbow_params).as_json()

        compare_country_comparison_genders_model = Model(
            "compare/country_comparison_genders",
            comparison_genders_single_country_params,
        ).as_json()

        compare_countries_comparison = Model(
            "compare/countries_comparison", comparison_two_countries
        ).as_json()

        self.dataset_name = "kaggle"

        self.models = [
            linear_regression_model,
            kmeans_clustering_model,
            kmeans_elbow_model,
            compare_country_comparison_genders_model,
            compare_countries_comparison
        ]

        self.dataset_link = (
            "https://www.kaggle.com/russellyates88/suicide-rates-overview-1985-to-2016"
        )

        self.description = """
        Content:
        
        This compiled dataset pulled from four other datasets linked by time and place, and was built to find signals correlated to increased suicide rates among different cohorts globally, across the socio-economic spectrum.

        References: 
        
        United Nations Development Program. (2018). Human development index (HDI). Retrieved from http://hdr.undp.org/en/indicators/137506

        World Bank. (2018). World development indicators: GDP (current US$) by country:1985 to 2016. Retrieved from http://databank.worldbank.org/data/source/world-development-indicators#

        [Szamil]. (2017). Suicide in the Twenty-First Century [dataset]. Retrieved from https://www.kaggle.com/szamil/suicide-in-the-twenty-first-century/notebook

        World Health Organization. (2018). Suicide prevention. Retrieved from http://www.who.int/mental_health/suicide-prevention/en/
        """

        super().set_instruction()
