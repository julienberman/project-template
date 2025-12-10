from kedro.pipeline import Pipeline

from project_template.pipelines import build_iso
from project_template.pipelines import build_wdi

def register_pipelines() -> dict[str, Pipeline]:
    pipeline_build_iso = build_iso.create_pipeline()
    pipeline_build_wdi = build_wdi.create_pipeline()
    
    return {
        "__default__": pipeline_build_iso + pipeline_build_wdi,
        "build_iso": pipeline_build_iso,
        "build_wdi": pipeline_build_wdi,
    }
