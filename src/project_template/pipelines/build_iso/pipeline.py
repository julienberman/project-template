
from kedro.pipeline import Node, Pipeline
from project_template.pipelines.build_iso.nodes import build_iso

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        Node(
            func=build_iso,
            inputs="iso",
            outputs="iso_clean",
            name="node_build_iso"
        )
    ])
