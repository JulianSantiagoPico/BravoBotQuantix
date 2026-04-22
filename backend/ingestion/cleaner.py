import re
import unicodedata


def _deduplicate_lines(texto: str) -> str:
    seen_short: set[str] = set()
    result = []
    for line in texto.split("\n"):
        stripped = line.strip()
        if not stripped:
            result.append(line)
            continue
        if len(stripped) <= 120 and stripped in seen_short:
            continue
        if len(stripped) <= 120:
            seen_short.add(stripped)
        result.append(line)
    return "\n".join(result)


def clean_text(texto: str) -> str:
    texto = unicodedata.normalize("NFC", texto)

    texto = re.sub(r"[ \t]+", " ", texto)

    texto = re.sub(r"\n{3,}", "\n\n", texto)

    texto = re.sub(r"[^\w\s.,;:¿?¡!()\-/\n\"\'%@#áéíóúüñÁÉÍÓÚÜÑ]", " ", texto)

    texto = re.sub(r" {2,}", " ", texto)

    texto = _deduplicate_lines(texto)

    return texto.strip()
