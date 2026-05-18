"""
Profile-aware translation helpers.

Reads the active Quarto profile from the QUARTO_PROFILE environment variable
and exposes translated labels and field accessors. Defaults to English.

Usage:
    from .i18n import t, get_lang, get_localized_field

    print(t("region"))                      # "Region" or "Região"
    notes = get_localized_field(answer, "notes")  # picks notes_pt when lang=pt
"""

from __future__ import annotations

import os
from typing import Any, Dict, Mapping, Optional

DEFAULT_LANG = "en"
SUPPORTED_LANGS = ("en", "pt")


def get_lang() -> str:
    profile = os.environ.get("QUARTO_PROFILE", DEFAULT_LANG).lower()
    for token in profile.replace(",", " ").split():
        if token in SUPPORTED_LANGS:
            return token
    return DEFAULT_LANG


LABELS: Dict[str, Dict[str, str]] = {
    "en": {
        "coverage": "Coverage",
        "not_assessed": "Not assessed",
        "not_applicable": "Not applicable",
        "Free API access": "Free API access",
        "Free API and GUI access": "Free API and GUI access",
        "Free GUI access": "Free GUI access",
        "No": "No",
        "Yes": "Yes",
        "Yes, but only for approved researchers": "Yes, but only for approved researchers",
        "Yes, both API and GUI documentation": "Yes, both API and GUI documentation",
        "Yes, the API documentation": "Yes, the API documentation",
        "Yes, the GUI documentation": "Yes, the GUI documentation",
        "Yes, through both GUI and API": "Yes, through both GUI and API",
        "Yes, through the API": "Yes, through the API",
        "Yes, through the GUI": "Yes, through the GUI",
        "Yes, with full availability": "Yes, with full availability",
        "Yes, with partial availability": "Yes, with partial availability",
        "special_criteria": "Special Criteria",
        "accessibility": "Accessibility",
        "compliance": "Compliance",
        "completeness": "Completeness",
        "consistency": "Consistency",
        "relevance": "Relevance",
        "timeliness": "Timeliness",
        "accuracy": "Accuracy",
        "region": "Region",
        "answer": "Answer",
        "note": "Note",
        "platform": "Platform",
        "brazil": "Brazil",
        "eu": "EU",
        "uk": "UK",
        "average": "Average",
        "ugc_framework": "User-Generated Content",
        "ads_framework": "Advertising",
        "score_band_not_available": "Not Available",
        "score_band_negligible": "Negligible",
        "score_band_minimal": "Minimal",
        "score_band_deficient": "Deficient",
        "score_band_limited": "Limited",
        "score_band_meaningful": "Meaningful",
        "vlop_tooltip": "Very Large Online Platform (EU DSA)",
        "vlop_caption": "Very Large Online Platform designated under the EU Digital Services Act (DSA), subject to enhanced transparency and accountability obligations.",
    },
    "pt": {
        "coverage": "Cobertura",
        "not_assessed": "Não avaliada",
        "not_applicable": "Não se aplica",
        "Free API access": "Acesso gratuito via API",
        "Free API and GUI access": "Acesso gratuito via API e interface gráfica",
        "Free GUI access": "Acesso gratuito via interface gráfica",
        "No": "Não",
        "Yes": "Sim",
        "Yes, but only for approved researchers": "Sim, mas apenas para pesquisadores aprovados",
        "Yes, both API and GUI documentation": "Sim, tanto a documentação da API quanto da interface gráfica",
        "Yes, the API documentation": "Sim, a documentação da API",
        "Yes, the GUI documentation": "Sim, a documentação da interface gráfica",
        "Yes, through both GUI and API": "Sim, tanto pela interface gráfica quanto pela API",
        "Yes, through the API": "Sim, pela API",
        "Yes, through the GUI": "Sim, pela interface gráfica",
        "Yes, with full availability": "Sim, com disponibilidade completa",
        "Yes, with partial availability": "Sim, com disponibilidade parcial",
        "special_criteria": "Critérios especiais",
        "accessibility": "Acessibilidade",
        "compliance": "Conformidade",
        "completeness": "Completude",
        "consistency": "Consistência",
        "relevance": "Relevância",
        "timeliness": "Atualidade",
        "accuracy": "Acurácia",
        "region": "Região",
        "answer": "Resposta",
        "note": "Nota",
        "platform": "Plataforma",
        "brazil": "Brasil",
        "eu": "UE",
        "uk": "Reino Unido",
        "average": "Média",
        "ugc_framework": "Conteúdo gerado por usuários",
        "ads_framework": "Anúncios",
        "score_band_not_available": "Indisponível",
        "score_band_negligible": "Insignificante",
        "score_band_minimal": "Mínima",
        "score_band_deficient": "Insuficiente",
        "score_band_limited": "Limitada",
        "score_band_meaningful": "Significativa",
        "vlop_tooltip": "Plataforma Online de Grande Dimensão (DSA UE)",
        "vlop_caption": "Plataforma Online de Grande Dimensão, designada sob a Lei de Serviços Digitais (DSA) da UE e sujeita a obrigações reforçadas de transparência e responsabilização.",
    },
}


def t(key: str, lang: Optional[str] = None) -> str:
    """Translate a label key. Falls back to English then to the key itself."""
    active = (lang or get_lang())
    return (
        LABELS.get(active, {}).get(key)
        or LABELS["en"].get(key)
        or key
    )


def get_localized_field(
    record: Mapping[str, Any],
    field: str,
    lang: Optional[str] = None,
) -> Any:
    """Read `record[field_<lang>]` if present, else fall back to `record[field]`.

    Used for YAML records where translated variants live alongside the canonical
    English field, e.g. {"notes": "...", "notes_pt": "..."}.
    """
    active = (lang or get_lang())
    if active != "en":
        localized = record.get(f"{field}_{active}")
        if localized:
            return localized
    return record.get(field)
