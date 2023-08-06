# labtex

## Purpose

I wrote this package with the intention of providing a single solution to the repetitive tasks in a lab environment. Whether you are doing error propagation, linear regression or LaTeX tables by hand, this package aims to expedite the process.

## Features

- Measurement and MeasurementList classes with automatic:
  - Error propagation
  - Unit parsing and propagation
- Linear regression
- Automatic table generation in three styles
- Automatic plot generation with matplotlib
- Template LaTeX file output with the generated figures and tables included

## Installation

```
pip3 install labtex
```

## Usage

For ease of use, you can import the package globally with
```python
from labtex import *
```
Alternatively do `import labtex as lt`.

Single measurements can be instantiated with `Measurement(value,uncertainty,unit)`.
```python
x = Measurement(1.1,0.3,"m")
y = Measurement(2.22,0.4,"m")
z = Measurement(314,10,"V")
```

Measurement instances support all operations and math functions with the error and units automatically propagated.
```python
print(x)
# 1.1 ± 0.3 m

print(x + y)
# 3.3 ± 0.5 m

print(x * z)
# 340 ± 90 V m

print(x ** 2)
# 1.2 ± 0.7 m^2

print(Measurement.tan(x))
# 2 ± 1 
```

For a list of measurements, the `MeasurementList` class functions identically to the `Measurement` class, only now taking a list of values.

```python
heights = MeasurementList([185,183,182,194,184,177],0,"cm")

print(heights)
# [185, 183, 182, 194, 184, 177] ± 5 cm

print(200 - heights)
# [15, 17, 18, 6, 16, 23] ± 5 cm
```

With two `MeasurementList`s, they can be linearly regressed with the `LinearRegression` class.
```python
voltages = MeasurementList([1.3,3,5,7,8.5,10],0,"V")
temperatures = MeasurementList([23,55,67,82,88,96],0,"C")
```

## Contributions

Feel free to submit a pull request.
