"""
Validators module for Brazilian documents (CPF and CNPJ).
"""


class ValidadorCPF:
    """Validator for Brazilian CPF (Cadastro de Pessoas Físicas)."""

    def __init__(self, documento_bruto):
        """
        Initialize CPF validator.

        Args:
            documento_bruto: Raw CPF string with or without formatting
        """
        self.documento = documento_bruto

    def limpar(self):
        """
        Clean CPF removing formatting characters.

        Returns:
            Cleaned CPF string with 11 digits or None if invalid
        """
        if self.documento is None or self.documento == "":
            return None
        limpo = str(self.documento).strip().replace(".", "").replace("-", "")
        if len(limpo) != 11:
            return None
        return limpo

    def formatar(self):
        """
        Format CPF to standard format: XXX.XXX.XXX-XX.

        Returns:
            Formatted CPF string or None if invalid
        """
        self.limpar()
        if self.documento is None or len(self.documento) != 11:
            return None
        return f"{self.documento[:3]}.{self.documento[3:6]}.{self.documento[6:9]}-{self.documento[9:]}"


class ValidadorCNPJ:
    """Validator for Brazilian CNPJ (Cadastro Nacional da Pessoa Jurídica)."""

    def __init__(self, documento_bruto):
        """
        Initialize CNPJ validator.

        Args:
            documento_bruto: Raw CNPJ string with or without formatting
        """
        self.documento = documento_bruto

    def limpar(self):
        """
        Clean CNPJ removing formatting characters.

        Returns:
            Cleaned CNPJ string with 14 digits or None if invalid
        """
        if self.documento is None or self.documento == "":
            return None
        limpo = (
            str(self.documento)
            .strip()
            .replace(".", "")
            .replace("/", "")
            .replace("-", "")
        )
        if len(limpo) != 14:
            return None
        return limpo

    def formatar(self):
        """
        Format CNPJ to standard format: XX.XXX.XXX/XXXX-XX.

        Returns:
            Formatted CNPJ string or None if invalid
        """
        limpo = self.limpar()
        if limpo is None:
            return None
        return f"{limpo[:2]}.{limpo[2:5]}.{limpo[5:8]}/{limpo[8:12]}-{limpo[12:]}"
