from automation.utils.validators import ValidadorCPF, ValidadorCNPJ


def test_validador_cpf_limpar_valido():
    validator = ValidadorCPF("123.456.789-09")
    assert validator.limpar() == "12345678909"


def test_validador_cpf_limpar_invalido():
    validator = ValidadorCPF("123")
    assert validator.limpar() is None


def test_validador_cnpj_limpar_valido():
    validator = ValidadorCNPJ("12.345.678/0001-90")
    assert validator.limpar() == "12345678000190"


def test_validador_cnpj_formatar_valido():
    validator = ValidadorCNPJ("12345678000190")
    assert validator.formatar() == "12.345.678/0001-90"


def test_validador_cnpj_formatar_invalido():
    validator = ValidadorCNPJ("123")
    assert validator.formatar() is None
