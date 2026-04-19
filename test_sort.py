"""Tests for the package sorter."""

import pytest
from sort import sort


class TestStandard:
    def test_small_and_light(self):
        assert sort(10, 10, 10, 5) == "STANDARD"

    def test_zero_dimensions_and_mass(self):
        assert sort(0, 0, 0, 0) == "STANDARD"

    def test_just_below_every_threshold(self):
        # volume 999,999.999..., all dims < 150, mass < 20
        assert sort(149, 149, 45.04, 19.999) == "STANDARD"


class TestSpecialBulky:
    def test_volume_exactly_at_threshold(self):
        # 100 * 100 * 100 = 1,000,000 -> bulky
        assert sort(100, 100, 100, 5) == "SPECIAL"

    def test_volume_above_threshold(self):
        assert sort(200, 200, 200, 5) == "SPECIAL"

    def test_width_at_dimension_threshold(self):
        assert sort(150, 10, 10, 5) == "SPECIAL"

    def test_height_at_dimension_threshold(self):
        assert sort(10, 150, 10, 5) == "SPECIAL"

    def test_length_at_dimension_threshold(self):
        assert sort(10, 10, 150, 5) == "SPECIAL"

    def test_dimension_well_above_threshold_but_small_volume(self):
        # long and thin: 200 cm x 1 cm x 1 cm -> volume 200, but dim 200 >= 150
        assert sort(200, 1, 1, 5) == "SPECIAL"


class TestSpecialHeavy:
    def test_mass_exactly_at_threshold(self):
        assert sort(10, 10, 10, 20) == "SPECIAL"

    def test_mass_above_threshold(self):
        assert sort(10, 10, 10, 50) == "SPECIAL"


class TestRejected:
    def test_bulky_by_volume_and_heavy(self):
        assert sort(100, 100, 100, 20) == "REJECTED"

    def test_bulky_by_dimension_and_heavy(self):
        assert sort(150, 1, 1, 20) == "REJECTED"

    def test_obvious_both(self):
        assert sort(200, 200, 200, 50) == "REJECTED"


class TestInputValidation:
    def test_string_input_rejected(self):
        with pytest.raises(TypeError):
            sort("10", 10, 10, 5)

    def test_none_input_rejected(self):
        with pytest.raises(TypeError):
            sort(None, 10, 10, 5)

    def test_bool_input_rejected(self):
        # bools are technically Real in Python; caller almost certainly didn't mean that
        with pytest.raises(TypeError):
            sort(True, 10, 10, 5)

    def test_negative_dimension_rejected(self):
        with pytest.raises(ValueError):
            sort(-1, 10, 10, 5)

    def test_negative_mass_rejected(self):
        with pytest.raises(ValueError):
            sort(10, 10, 10, -1)


class TestFloats:
    def test_float_dimensions_work(self):
        # 99.99^3 ~= 999,700 < 1M, all dims < 150
        assert sort(99.99, 99.99, 99.99, 5) == "STANDARD"

    def test_float_at_volume_threshold(self):
        # 100.0 * 100.0 * 100.0 = 1,000,000 exactly -> bulky
        assert sort(100.0, 100.0, 100.0, 5) == "SPECIAL"

    def test_float_mass_heavy(self):
        assert sort(10, 10, 10, 20.0) == "SPECIAL"


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
