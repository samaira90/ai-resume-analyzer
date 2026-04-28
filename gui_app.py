import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext
import tkinter as tk
from tkinter import messagebox
import csv

getcontext().prec = 28

# Global storage for export
results_data = []

def calculate():
    global results_data
    results_data = []

    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())

        result = a + b

        # Float
        err_float = abs(result - c)
        results_data.append(("Float", result, err_float))

        # Float32
        res32 = np.float32(a) + np.float32(b)
        err32 = abs(float(res32) - c)
        results_data.append(("Float32", res32, err32))

        # Float64
        res64 = np.float64(a) + np.float64(b)
        err64 = abs(float(res64) - c)
        results_data.append(("Float64", res64, err64))

        # Decimal
        res_dec = Decimal(str(a)) + Decimal(str(b))
        err_dec = abs(float(res_dec) - c)
        results_data.append(("Decimal", float(res_dec), err_dec))

        # Display
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Method\tResult\t\tError\n")
        for r in results_data:
            output_text.insert(tk.END, f"{r[0]}\t{r[1]}\t{r[2]}\n")

    except:
        messagebox.showerror("Error", "Please enter valid numbers")


def plot_graph():
    values = list(range(1, 200))

    errors_float = []
    errors_float32 = []
    errors_decimal = []

    for n in values:
        calc_float = 0.0
        for _ in range(n):
            calc_float += 0.1
        expected = n * 0.1
        errors_float.append(abs(calc_float - expected) * 1000000)

        calc_f32 = np.float32(0.0)
        for _ in range(n):
            calc_f32 += np.float32(0.1)
        expected_f32 = np.float32(n) * np.float32(0.1)
        errors_float32.append(abs(float(calc_f32 - expected_f32)) * 1000000)

        calc_dec = Decimal("0.0")
        for _ in range(n):
            calc_dec += Decimal("0.1")
        expected_dec = Decimal(n) * Decimal("0.1")
        errors_decimal.append(float(abs(calc_dec - expected_dec)) * 1000000)

    plt.plot(values, errors_float, label="Float")
    plt.plot(values, errors_float32, label="Float32")
    plt.plot(values, errors_decimal, label="Decimal")

    plt.xlabel("Number of Additions")
    plt.ylabel("Error (scaled x1e6)")
    plt.title("Floating Point Error Comparison")

    plt.legend()
    plt.grid()
    plt.show()


def export_csv():
    if not results_data:
        messagebox.showwarning("Warning", "No data to export!")
        return

    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Method", "Result", "Error"])
        writer.writerows(results_data)

    messagebox.showinfo("Success", "Results exported as results.csv")


# GUI setup
root = tk.Tk()
root.title("Floating Point Error Analyzer")
root.geometry("500x500")

tk.Label(root, text="Enter A:").pack()
entry_a = tk.Entry(root)
entry_a.pack()

tk.Label(root, text="Enter B:").pack()
entry_b = tk.Entry(root)
entry_b.pack()

tk.Label(root, text="Expected Result:").pack()
entry_c = tk.Entry(root)
entry_c.pack()

tk.Button(root, text="Calculate", command=calculate).pack(pady=5)
tk.Button(root, text="Show Graph", command=plot_graph).pack(pady=5)
tk.Button(root, text="Export CSV", command=export_csv).pack(pady=5)

output_text = tk.Text(root, height=10)
output_text.pack()

root.mainloop()