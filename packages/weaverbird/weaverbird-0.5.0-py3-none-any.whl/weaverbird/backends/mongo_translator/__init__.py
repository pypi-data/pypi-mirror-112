from typing import List

from weaverbird.pipeline import Pipeline, steps
from weaverbird.types import DomainToTableIdentifier


def translate_pipeline(
    pipeline: Pipeline, domain_to_table_identifier: DomainToTableIdentifier
) -> List[dict]:
    result = []

    for step in pipeline.steps:
        if isinstance(step, steps.SelectStep):
            result.append({"$project": {col: 1 for col in step.columns}})

    return result
