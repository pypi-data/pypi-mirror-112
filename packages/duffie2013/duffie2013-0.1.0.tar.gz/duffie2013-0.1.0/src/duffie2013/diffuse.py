"""
Formalisms to deal with the diffuse part of light.
"""


def diff_frac(rg, rg_ext):
    """Diffuse fraction of atmospheric radiation.

    References: eq2.10.1

    Args:
        rg (float): [W.m-2] or [MJ.m-2] measured radiation on flat surface on the ground
        rg_ext (float): [rg] theoretical extraterrestrial flat ground radiation

    Returns:
        (float): [-] fraction of diffuse in incoming radiation
    """
    if rg_ext < 1e-3:
        kt = 1.
    else:
        kt = rg / rg_ext

    if kt <= 0.2:
        return 1 - 0.09 * kt
    elif kt <= 0.8:
        return 0.9511 - 0.1604 * kt + 4.388 * kt ** 2 - 16.638 * kt ** 3 + 12.336 * kt ** 4
    else:
        return 0.165
