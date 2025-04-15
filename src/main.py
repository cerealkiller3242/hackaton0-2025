def multiply(a, b):
        return a * b
  
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

def subtract(a, b):
    return a - b

"""
Commit: Issue 1 – Implementar la función de suma
"""
def add(a, b):
    return a + b
  
def calculate(expression: str):
    # Si la cadena está vacía o contiene solo espacios en blanco, se considera inválida.
    if not expression.strip():
        raise ValueError("Empty expression")
    tokens = tokenize(expression)
    result, pos = parse_expression(tokens, 0)
    if pos != len(tokens):
        raise SyntaxError("Invalid syntax")
    return result


def tokenize(expression: str):
    tokens = []
    i = 0
    while i < len(expression):
        ch = expression[i]
        if ch.isspace():
            i += 1
            continue
        if ch in "+-*/()":
            tokens.append(ch)
            i += 1
        elif ch.isdigit() or ch == '.':
            num_chars = []
            dot_count = 0
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                if expression[i] == '.':
                    dot_count += 1
                    if dot_count > 1:
                        raise ValueError("Invalid number format")
                num_chars.append(expression[i])
                i += 1
            tokens.append(''.join(num_chars))
        else:
            raise ValueError(f"Invalid character: {ch}")
    return tokens


def parse_expression(tokens, pos):
    # Se analiza el término (suma/resta tienen menor precedencia que * y /)
    value, pos = parse_term(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ('+', '-'):
        op = tokens[pos]
        pos += 1
        right, pos = parse_term(tokens, pos)
        if op == '+':
            value = add(value, right)
        else:
            value = subtract(value, right)
    return value, pos


def parse_term(tokens, pos):
    # Se analiza el factor; los operadores * y / tienen mayor precedencia.
    value, pos = parse_factor(tokens, pos)
    while pos < len(tokens) and tokens[pos] in ('*', '/'):
        op = tokens[pos]
        pos += 1
        right, pos = parse_factor(tokens, pos)
        if op == '*':
            value = multiply(value, right)
        else:
            value = divide(value, right)
    return value, pos


def parse_factor(tokens, pos):
    # Manejo de operadores unarios + y -
    if pos < len(tokens) and tokens[pos] in ('+', '-'):
        op = tokens[pos]
        pos += 1
        factor, pos = parse_factor(tokens, pos)
        return (factor if op == '+' else -factor), pos

    # Manejo de paréntesis
    if tokens[pos] == '(':
        pos += 1  # consumir '('
        value, pos = parse_expression(tokens, pos)
        if pos >= len(tokens) or tokens[pos] != ')':
            raise SyntaxError("Missing closing parenthesis")
        pos += 1  # consumir ')'
        return value, pos

    # En otro caso, se espera un número
    try:
        token = tokens[pos]
        # Se decide si el número es entero o decimal
        number = float(token) if '.' in token else int(token)
    except ValueError:
        raise ValueError(f"Invalid number: {tokens[pos]}")
    pos += 1
    return number, pos

# Para permitir que este módulo se ejecute de forma independiente.
if __name__ == "__main__":
    while True:
        try:
            user_input = input("Ingrese una operación (o 'c' para limpiar): ")
            # Si el usuario presiona 'c', se limpia la entrada (en este ejemplo se ignora y se continúa)
            if user_input.strip().lower() == 'c':
                continue
            result = calculate(user_input)
            print("Resultado:", result)
        except Exception as e:
            print("Error:", e)