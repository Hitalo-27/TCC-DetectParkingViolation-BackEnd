def dms_to_decimal(value, ref):
    """Recebe string '(23.0, 34.0, 20.1396)' e converte para decimal."""
    try:
        # Remove parênteses e quebra em partes
        cleaned = value.replace("(", "").replace(")", "")
        d, m, s = [float(x) for x in cleaned.split(",")]

        decimal = d + (m / 60) + (s / 3600)

        if ref in ["S", "W"]:
            decimal = -decimal

        return decimal
    except Exception:
        return None