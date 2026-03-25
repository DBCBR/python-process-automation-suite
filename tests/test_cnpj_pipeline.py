from automation.pipelines.cnpj_pipeline import CNPJPipeline


def test_extract_uses_provided_list():
    pipeline = CNPJPipeline(cnpj_list=["12.345.678/0001-90"])

    extracted = pipeline.extract()

    assert extracted == ["12.345.678/0001-90"]


def test_extract_from_text_removes_duplicates():
    text = "CNPJ A: 12.345.678/0001-90 e CNPJ B: 12.345.678/0001-90"
    pipeline = CNPJPipeline(text_source=text)

    extracted = pipeline.extract()

    assert extracted == ["12.345.678/0001-90"]


def test_transform_filters_invalid_and_enriches(monkeypatch):
    pipeline = CNPJPipeline(cnpj_list=["12.345.678/0001-90", "invalido"])

    def fake_consultar_cnpj(cnpj):
        if cnpj == "12345678000190":
            return {"cnpj": cnpj, "razao_social": "Empresa Teste"}
        return None

    monkeypatch.setattr(
        "automation.pipelines.cnpj_pipeline.consultar_cnpj", fake_consultar_cnpj
    )

    transformed = pipeline.transform(pipeline.cnpj_list)

    assert transformed == [{"cnpj": "12345678000190", "razao_social": "Empresa Teste"}]


def test_load_returns_standard_payload():
    pipeline = CNPJPipeline()
    data = [{"cnpj": "12345678000190"}]

    result = pipeline.load(data)

    assert result["pipeline"] == "CNPJ Pipeline"
    assert result["status"] == "success"
    assert result["total_processed"] == 1
    assert result["results"] == data
