"""
Smarter Technologies — Core Engineering Technical Screen
Package sorter for the robotic arm dispatcher.

Rules:
    bulky  : volume (W * H * L) >= 1_000_000 cm^3 OR any dimension >= 150 cm
    heavy  : mass >= 20 kg

Stacks:
    STANDARD : neither bulky nor heavy
    SPECIAL  : bulky XOR heavy (exactly one)
    REJECTED : bulky AND heavy
"""

from numbers import Real

_BULKY_VOLUME = 1_000_000
_BULKY_DIM = 150
_HEAVY_MASS = 20


def sort(width, height, length, mass):
    """Return the stack name for a package with the given dimensions and mass.

    Args:
        width, height, length: package dimensions in centimeters
        mass: package mass in kilograms

    Returns:
        "STANDARD", "SPECIAL", or "REJECTED"

    Raises:
        TypeError if any argument is not a real number.
        ValueError if any argument is negative.
    """
    for name, val in (("width", width), ("height", height),
                      ("length", length), ("mass", mass)):
        if isinstance(val, bool) or not isinstance(val, Real):
            raise TypeError(f"{name} must be a real number, got {type(val).__name__}")
        if val < 0:
            raise ValueError(f"{name} must be non-negative, got {val}")

    volume = width * height * length
    is_bulky = (volume >= _BULKY_VOLUME
                or width >= _BULKY_DIM
                or height >= _BULKY_DIM
                or length >= _BULKY_DIM)
    is_heavy = mass >= _HEAVY_MASS

    if is_bulky and is_heavy:
        return "REJECTED"
    if is_bulky or is_heavy:
        return "SPECIAL"
    return "STANDARD"
