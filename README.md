# Smarter Technologies — Package Sorter

Solution to the Core Engineering Technical Screen.

## Problem

Write `sort(width, height, length, mass)` that returns the stack name for a robotic-arm dispatcher.

- `bulky` — volume (`W * H * L`) ≥ 1,000,000 cm³ **or** any single dimension ≥ 150 cm
- `heavy` — mass ≥ 20 kg

Stacks:
- `STANDARD` — neither bulky nor heavy
- `SPECIAL` — exactly one of (bulky, heavy)
- `REJECTED` — both bulky and heavy

## Files

- `sort.py` — the `sort()` function (pure, no side effects)
- `test_sort.py` — pytest suite covering happy paths, boundary values, edge cases, and input validation

## Run

```bash
pip install pytest
pytest -v
```

or

```bash
python test_sort.py
```

## Design notes

- Thresholds (`1_000_000` cm³, `150` cm, `20` kg) are module-level constants, not magic numbers.
- Boundaries are inclusive (`>=`) per the spec ("greater than or equal to").
- Input validation rejects non-numeric, `None`, `bool`, and negative values. `bool` is special-cased because Python's `bool` inherits from `int`, which would otherwise pass the `Real` check silently.
- Volume is computed once and reused.
- Returns one of three string literals — no enum or custom type, since the spec asks for a string.

## Classification decision table

| bulky | heavy | stack      |
|-------|-------|------------|
| no    | no    | STANDARD   |
| yes   | no    | SPECIAL    |
| no    | yes   | SPECIAL    |
| yes   | yes   | REJECTED   |

## Time spent

~20 minutes including tests.
