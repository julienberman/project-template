from kedro.pipeline import Node, Pipeline

from project_template.pipelines.build_wdi.nodes import build_gdp_nominal, build_gdp_ppp, build_wdi

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        Node(
            func=build_gdp_nominal,
            inputs=dict(gdp_nominal="gdp_nominal", globals="params:globals"),
            outputs="gdp_nominal_clean",
            name="build_gdp_nominal"
        ),
        Node(
            func=build_gdp_ppp,
            inputs=dict(gdp_ppp="gdp_ppp", globals="params:globals"),
            outputs="gdp_ppp_clean",
            name="build_gdp_ppp"
        ),
        Node(
            func=build_wdi,
            inputs=dict(gdp_nominal="gdp_nominal_clean", gdp_ppp="gdp_ppp_clean", iso="iso_clean"),
            outputs="wdi_clean",
            name="build_wdi"
        )
    ])
