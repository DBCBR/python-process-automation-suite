import pytest

from automation.pipelines.base_pipeline import BasePipeline


class SuccessPipeline(BasePipeline):
    def __init__(self):
        super().__init__(name="Success")

    def extract(self):
        return [1, 2, 3]

    def transform(self, data):
        return [x * 2 for x in data]

    def load(self, data):
        return {"status": "ok", "data": data}


class FailurePipeline(BasePipeline):
    def __init__(self):
        super().__init__(name="Failure")

    def extract(self):
        return [1]

    def transform(self, data):
        raise RuntimeError("transform error")

    def load(self, data):
        return data


def test_base_pipeline_run_success_sets_completed_status():
    pipeline = SuccessPipeline()

    result = pipeline.run()

    assert result == {"status": "ok", "data": [2, 4, 6]}
    assert pipeline.status == "completed"


def test_base_pipeline_run_failure_sets_failed_status():
    pipeline = FailurePipeline()

    with pytest.raises(RuntimeError):
        pipeline.run()

    assert pipeline.status == "failed"
