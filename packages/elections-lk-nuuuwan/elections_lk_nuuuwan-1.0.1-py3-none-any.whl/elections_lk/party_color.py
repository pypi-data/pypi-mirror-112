"""Party Color Utils."""

PARTY_TO_COLOR_OR_PARTY = {
    'UNP': (0, 0.5, 0),
    'NDF': 'UNP',
    'SLFP': (0, 0, 0.9),
    'PA': 'SLFP',
    'UPFA': 'SLFP',
    'SLPP': (0.5, 0, 0),
    'SLMP': (0.9, 0, 0.5),
    'ACTC': (0.9, 0.5, 0),
    'JVP': (0.9, 0, 0),
    'NMPP': 'JVP',
}
UNKNOWN_PARTY_COLOR = (0.5, 0.5, 0.5)


def get_rgb_color(party_id):
    """Get RGB color of party."""
    if party_id not in PARTY_TO_COLOR_OR_PARTY:
        return UNKNOWN_PARTY_COLOR
    color_or_party = PARTY_TO_COLOR_OR_PARTY[party_id]
    if isinstance(color_or_party, tuple):
        return color_or_party
    return get_rgb_color(color_or_party)


def _default_p_to_a(p):
    min_p = 0.45
    return max(0, p - min_p) / (1 - min_p)


def get_rgba_color(
    party_id,
    p_votes,
    p_to_a=_default_p_to_a,
):
    """Get RGBA color of party."""
    (r, g, b) = get_rgb_color(party_id)
    return (r, g, b, p_to_a(p_votes))
