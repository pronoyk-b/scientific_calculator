import tkinter as tk
from tkinter import ttk
import math

def nPr(n, r):
    return math.factorial(n) // math.factorial(n - r)

def nCr(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

class ScientificCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Scientific Calculator")
        self.window.geometry("400x600")
        self.window.resizable(False, False)
        
        # Variables
        self.current_theme = "light"
        self.is_scientific_mode = False
        self.current_expression = ""
        
        # Colors
        self.themes = {
            "light": {
                "bg": "#f0f0f0",
                "button": "#ffffff",
                "text": "#000000",
                "display_bg": "#ffffff",
                "special_btn": "#ff9999"
            },
            "dark": {
                "bg": "#2d2d2d",
                "button": "#3d3d3d",
                "text": "#ffffff",
                "display_bg": "#1e1e1e",
                "special_btn": "#8b0000"
            }
        }
        
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        # Display
        self.display = tk.Entry(self.window, font=("Arial", 24), justify="right", bd=10)
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        # Mode switch
        self.mode_button = ttk.Button(self.window, text="Scientific Mode: OFF", command=self.toggle_mode)
        self.mode_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Theme switch
        self.theme_button = ttk.Button(self.window, text="Dark Theme", command=self.toggle_theme)
        self.theme_button.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
        # Buttons for normal mode
        self.create_normal_buttons()
        
        # Scientific mode buttons (initially hidden)
        self.scientific_buttons = []
        self.create_scientific_buttons()
        
    def create_normal_buttons(self):
        normal_buttons = [
            'C', '⌫', '(', ')',
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            '%'
        ]
        
        row = 2
        col = 0
        
        for button in normal_buttons:
            cmd = lambda x=button: self.click(x)
            btn = tk.Button(self.window, text=button, width=8, height=2, 
                          font=("Arial", 12, "bold"), relief="raised",
                          command=cmd)
            if button in ['C', '⌫']:
                btn.config(bg=self.themes[self.current_theme]["special_btn"])
            btn.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 3:
                col = 0
                row += 1
    
    def create_scientific_buttons(self):
        scientific_buttons = [
            ['sin', 'cos', 'tan', 'n!'],
            ['sin⁻¹', 'cos⁻¹', 'tan⁻¹', '%'],
            ['nPr', 'nCr', 'π', 'e'],
            ['log', 'ln', 'sqrt', 'x²']
        ]
        
        row = 7
        for button_row in scientific_buttons:
            col = 0
            for button in button_row:
                cmd = lambda x=button: self.click(x)
                btn = tk.Button(self.window, text=button, width=8, height=2,
                              font=("Arial", 12, "bold"), relief="raised",
                              command=cmd)
                btn.grid(row=row, column=col, padx=2, pady=2)
                btn.grid_remove()  # Hide initially
                self.scientific_buttons.append(btn)
                col += 1
            row += 1
    
    def toggle_mode(self):
        self.is_scientific_mode = not self.is_scientific_mode
        if self.is_scientific_mode:
            self.mode_button.config(text="Scientific Mode: ON")
            self.window.geometry("400x700")
            for btn in self.scientific_buttons:
                btn.grid()
        else:
            self.mode_button.config(text="Scientific Mode: OFF")
            self.window.geometry("400x600")
            for btn in self.scientific_buttons:
                btn.grid_remove()
    
    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.theme_button.config(text="Light Theme" if self.current_theme == "dark" else "Dark Theme")
        self.apply_theme()
    
    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.window.config(bg=theme["bg"])
        self.display.config(bg=theme["display_bg"], fg=theme["text"])
        
        for child in self.window.winfo_children():
            if isinstance(child, tk.Button):
                child.config(
                    bg=theme["button"],
                    fg=theme["text"],
                    activebackground=theme["button"],
                    activeforeground=theme["text"]
                )
    
    def click(self, key):
        if key == '=':
            try:
                # Replace trigonometric function patterns with math module calls
                expression = self.current_expression
                
                # Handle percentage calculations
                if '%' in expression:
                    if '*' in expression:  # Format: 5% * 13 (5% of 13)
                        percent, number = expression.split('*')
                        percent = float(percent.replace('%', ''))
                        number = float(number)
                        result = (percent/100) * number
                    else:  # Simple percentage: 5%
                        number = float(expression.replace('%', ''))
                        result = number/100
                else:
                    # Handle trigonometric functions and their inverses
                    trig_functions = {
                        'sin(': 'math.sin(math.radians',
                        'cos(': 'math.cos(math.radians',
                        'tan(': 'math.tan(math.radians',
                        'sin⁻¹(': 'math.degrees(math.asin',
                        'cos⁻¹(': 'math.degrees(math.acos',
                        'tan⁻¹(': 'math.degrees(math.atan'
                    }
                    
                    for func, replacement in trig_functions.items():
                        if func in expression:
                            expression = expression.replace(func, f"{replacement}(")
                    
                    # Handle permutation and combination
                    if 'P' in expression:
                        n, r = map(int, expression.split('P'))
                        if n > 100 or r > 100:  # Prevent large numbers
                            raise ValueError("Numbers too large for permutation")
                        result = nPr(n, r)
                    elif 'C' in expression:
                        n, r = map(int, expression.split('C'))
                        if n > 100 or r > 100:  # Prevent large numbers
                            raise ValueError("Numbers too large for combination")
                        result = nCr(n, r)
                    else:
                        result = eval(expression)
                
                # Format result to prevent very long numbers
                if isinstance(result, float):
                    result = '{:.10f}'.format(result).rstrip('0').rstrip('.')
                elif isinstance(result, int) and len(str(result)) > 15:
                    result = '{:.10e}'.format(result)
                
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.current_expression = str(result)
            except ValueError as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(e))
                self.current_expression = ""
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.current_expression = ""
        
        elif key == 'C':
            self.display.delete(0, tk.END)
            self.current_expression = ""
            
        elif key == '⌫':
            self.current_expression = self.current_expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current_expression)
        
        elif key in ['sin', 'cos', 'tan', 'sin⁻¹', 'cos⁻¹', 'tan⁻¹']:
            self.current_expression += key + "("
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current_expression)
            
        elif key == 'n!':
            try:
                num = int(float(self.current_expression))
                if num < 0:
                    raise ValueError("Cannot calculate factorial of negative number")
                if num > 100:
                    raise ValueError("Number too large for factorial")
                result = math.factorial(num)
                # Format result for large numbers
                if len(str(result)) > 15:
                    result = '{:.10e}'.format(result)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.current_expression = str(result)
            except ValueError as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(e))
                self.current_expression = ""
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.current_expression = ""
            
        elif key in ['nPr', 'nCr']:
            self.current_expression += key[1]  # Add just P or C
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current_expression)
            
        elif key == 'sqrt':
            try:
                result = math.sqrt(float(self.current_expression))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.current_expression = str(result)
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.current_expression = ""
        
        elif key == 'x²':
            try:
                result = float(self.current_expression) ** 2
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.current_expression = str(result)
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.current_expression = ""
        
        elif key == 'π':
            self.current_expression += str(math.pi)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current_expression)
        
        elif key == 'e':
            self.current_expression += str(math.e)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current_expression)
        
        elif key == '%':
            if '*' not in self.current_expression:  # If no multiplication, add % symbol
                self.current_expression += '%'
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current_expression)
        
        else:
            self.current_expression += str(key)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current_expression)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = ScientificCalculator()
    calculator.run()
