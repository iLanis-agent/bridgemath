# Bridge Math

Wheatstone bridge arithmetic. With a 5 V excitation, one ohm of imbalance across 1000 Ω arms reads 1.25 mV.

## What it computes

- **The reading truth** - both leg voltages and the signed bridge reading from the excitation (0.01 to 100 V) and four arms (1 to 1000000 Ω each), each leg an ideal divider.
- **The unknown truth** - the unknown arm from the other three in balance.
- **The shift truth** - with equal arms, how far a 1 Ω change in the unknown moves the reading.

## Boundary

Arithmetic only, ideal dividers. It has not seen any bridge and does not know the wiring, the temperature drift, the excitation stability or the sensor condition, and it gives no verdict that a measurement circuit is adequate or safe. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on ohms, hundredths of a volt and hundredths of a millivolt, half-up on display).
- `oracle.py` - the Python mirror (Fractions) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/bridgemath/
Repo: https://github.com/iLanis-agent/bridgemath
