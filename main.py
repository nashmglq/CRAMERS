import tkinter as tk
from tkinter import messagebox


#GROUP:
# LAYUG, ONAIRE
# MAGLAQUI, STEVEN NASH
def calculate_determinant(matrix, val=1):
    n = len(matrix)
    if n == 1:
        return val * matrix[0][0]
    else:
        sign = -1
        det = 0
        for i in range(n):
            mtx = []
            for j in range(1, n):
                buff = []
                for k in range(n):
                    if k != i:
                        buff.append(matrix[j][k])
                mtx.append(buff)
            sign *= -1
            det += val * calculate_determinant(mtx, sign * matrix[0][i])
        return det


def cramer(matrix, results, order):
    main_det = calculate_determinant(matrix)
    if main_det != 0:
        resolution = []
        matrices = []
        sub_dets = []
        for r in range(order):
            matrix_sub = []
            for i in range(order):
                matrix_sub.append([])
                for j in range(order):
                    if j == r:
                        matrix_sub[i].append(results[i])
                    else:
                        matrix_sub[i].append(matrix[i][j])
            sub_det = calculate_determinant(matrix_sub)
            sub_dets.append(sub_det)
            ans = sub_det / main_det
            resolution.append(ans)
            matrices.append(matrix_sub)
        return main_det, resolution, matrices, sub_dets
    else:
        return main_det, [], [], []


def parse_equations(equations):
    matrix = []
    results = []
    for equation in equations:
        equation = equation.replace(' ', '')
        terms = equation.split('=')
        result = float(terms[1])
        results.append(result)
        terms = terms[0].split('+')
        row = []
        for term in terms:
            if term[-1] in ['x', 'y', 'z', 'w']:
                coefficient = term[:-1]
            else:
                coefficient = term
            coefficient = coefficient if coefficient else '1'  # Set to '1' if coefficient is empty
            if '.' in coefficient:
                row.append(float(coefficient))
            else:
                row.append(int(coefficient))
        matrix.append(row)
    return matrix, results



def solve_equations():
    size = size_var.get()
    order = int(size[0])
    equations = [entry.get() for entry in equation_entries]
    matrix, results = parse_equations(equations)
    main_det, resolution, matrices, sub_dets = cramer(matrix, results, order)
    if main_det != 0:
        display_matrices(root, main_det, matrices, resolution, equations, sub_dets)
        solution_text = '\n'.join([f'{["x", "y", "z", "w"][r]} = {round(resolution[r], 2)}' for r in range(order)])
        messagebox.showinfo("Solution", f"Equation Roots:\n{solution_text}")
    else:
        messagebox.showerror("Error", "Impossible to finish algorithm.\nThe determinant of the main matrix is EQUAL to 0.")


def add_equation():
    order = size_var.get()

    if order == "1x1":
        example_equation = "Ex. 2x = 1"
    elif order == "2x2":
        example_equation = "Ex. 2x + 2y = 3"
    elif order == "3x3":
        example_equation = "Ex. 3x + 2y + 2z = 3"
    elif order == "4x4":
        example_equation = "Ex. 2x + 2y + 5z + 10w = 32"

    if len(equation_entries) < int(order[0]):
        eq_frame = tk.Frame(equation_frame)
        eq_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(eq_frame, text=f"Equation {len(equation_entries)+1}: {example_equation}").pack(side=tk.LEFT)
        entry = tk.Entry(eq_frame)
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        equation_entries.append(entry)
    else:
        messagebox.showinfo("Info", "You have added the maximum number of equations for the selected matrix size.")


def display_matrices(root, main_det, matrices, resolution, equations, sub_dets):
    matrix_window = tk.Toplevel(root)
    matrix_window.title("Solving Process")

    equations_frame = tk.Frame(matrix_window)
    equations_frame.pack(padx=10, pady=5)

    max_terms = max(len(eq.split('+')) for eq in equations)
    for i, equation in enumerate(equations):
        equation = equation.replace(' ', '')
        terms = equation.split('=')
        terms = terms[0].split('+')
        coeffs = [term[:-1] if term[-1] in ['x', 'y', 'z', 'w'] else term for term in terms]
        coeffs = ['1' if coeff == '' else coeff for coeff in coeffs]  # Replace empty coefficients with '1'
        while len(coeffs) < max_terms:
            coeffs.append('0')
        for j, coeff in enumerate(coeffs):
            coeff_label = tk.Label(equations_frame, text=coeff)
            coeff_label.grid(row=i + 1, column=j, padx=5, pady=2, sticky="nsew")

    det_frame = tk.Frame(matrix_window)
    det_frame.pack(padx=10, pady=5)
    det_label_main = tk.Label(det_frame, text=f"Determinant:")
    det_label_main.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")
    det_value_main = tk.Label(det_frame, text=f"{main_det}")
    det_value_main.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")

    for i, (matrix, value, sub_det) in enumerate(zip(matrices, resolution, sub_dets)):
        frame = tk.Frame(matrix_window)
        frame.pack(padx=10, pady=5)
        variable = ['x', 'y', 'z', 'w'][i]

        matrix_label = tk.Label(frame, text=f"Intermediate Matrix {variable}")
        matrix_label.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

        for j, row in enumerate(matrix):
            for k, element in enumerate(row):
                label = tk.Label(frame, text=str(element))
                label.grid(row=j + 1, column=k, padx=5, pady=2, sticky="nsew")

        det_label_sub = tk.Label(frame, text=f"Sub Det: {sub_det}")
        det_label_sub.config(font=("Arial", 10, "bold"))
        det_label_sub.grid(row=len(matrix) + 1, column=0, padx=5, pady=2, sticky="nsew")

        det_label = tk.Label(frame, text=f"{variable.capitalize()} : ")
        det_label.config(font=("Arial", 10, "bold"))
        det_label.grid(row=len(matrix) + 2, column=0, padx=5, pady=2, sticky="nsew")

        det_value = tk.Label(frame, text=f"{value}")
        det_value.grid(row=len(matrix) + 2, column=1, padx=5, pady=2, sticky="nsew")

    roots_frame = tk.Frame(matrix_window)
    roots_frame.pack(padx=10, pady=5)
    roots_label = tk.Label(roots_frame, text="Roots:")
    roots_label.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")
    for i, root in enumerate(resolution):
        root_label = tk.Label(roots_frame, text=f"{['x', 'y', 'z', 'w'][i]} = {round(root, 2)}")
        root_label.grid(row=i + 1, column=0, padx=5, pady=2, sticky="nsew")



root = tk.Tk()
root.title("Linear Equation Solver")

size_var = tk.StringVar(root)
size_var.set("1x1")

size_frame = tk.Frame(root)
size_frame.pack(fill=tk.X, padx=5, pady=5)
tk.Label(size_frame, text="Matrix Size:").pack(side=tk.LEFT)
size_option = tk.OptionMenu(size_frame, size_var, "1x1", "2x2", "3x3", "4x4")
size_option.pack(side=tk.LEFT)

add_button = tk.Button(size_frame, text="Add Equations", command=add_equation)
add_button.pack(side=tk.LEFT, padx=(10, 0))

equation_frame = tk.Frame(root)
equation_frame.pack(fill=tk.X, padx=5, pady=5)

equation_entries = []

solve_button = tk.Button(root, text="Solve", command=solve_equations)
solve_button.pack(pady=5)

root.mainloop()
