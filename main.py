import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext

# Set high precision for Decimal
getcontext().prec = 28

print("=== Floating Point Error Analyzer ===\n")

# 🔹 User Input
a = float(input("Enter first number (e.g., 0.1): "))
b = float(input("Enter second number (e.g., 0.2): "))
c = float(input("Enter expected result (e.g., 0.3): "))

print("\n--- Basic Float Calculation ---")
result = a + b
error = abs(result - c)

print("Result:", result)
print("Expected:", c)
print("Error:", error)

# 🔹 NumPy Comparison
print("\n--- NumPy Precision Comparison ---")

a32 = np.float32(a)
b32 = np.float32(b)
res32 = a32 + b32

a64 = np.float64(a)
b64 = np.float64(b)
res64 = a64 + b64

print("float32:", res32)
print("float64:", res64)

# 🔹 Decimal (High Precision)
print("\n--- High Precision (Decimal) ---")

a_dec = Decimal(str(a))
b_dec = Decimal(str(b))
res_dec = a_dec + b_dec

print("Decimal Result:", res_dec)

# 🔹 Table Output
print("\n--- Comparison Table ---")
print("{:<10} {:<20} {:<20}".format("Method", "Result", "Error"))

methods = [
    ("Float", result),
    ("Float32", res32),
    ("Float64", res64),
    ("Decimal", float(res_dec))
]

for name, val in methods:
    err = abs(val - c)
    print("{:<10} {:<20} {:<20}".format(name, val, err))

# 🔹 Graph: Error Growth
print("\nGenerating graph...")

values = [i for i in range(1, 200)]

errors_float = []
errors_float32 = []
errors_decimal = []

from decimal import Decimal

for n in values:
    # 🔵 Normal float
    calc_float = 0.0
    for _ in range(n):
        calc_float += 0.1
    expected = n * 0.1
    errors_float.append(abs(calc_float - expected) * 1000000)

    # 🟢 Float32
    calc_f32 = np.float32(0.0)
    for _ in range(n):
        calc_f32 += np.float32(0.1)
    expected_f32 = np.float32(n) * np.float32(0.1)
    errors_float32.append(abs(float(calc_f32 - expected_f32)) * 1000000)

    # 🔴 Decimal (high precision)
    calc_dec = Decimal("0.0")
    for _ in range(n):
        calc_dec += Decimal("0.1")
    expected_dec = Decimal(n) * Decimal("0.1")
    errors_decimal.append(float(abs(calc_dec - expected_dec)) * 1000000)

# 📊 Plot all lines
plt.plot(values, errors_float, label="Float")
plt.plot(values, errors_float32, label="Float32")
plt.plot(values, errors_decimal, label="Decimal")

plt.xlabel("Number of Additions")
plt.ylabel("Error (scaled x1e6)")
plt.title("Floating Point Error Comparison")

plt.legend()   # 🔥 important
plt.grid()

plt.show()