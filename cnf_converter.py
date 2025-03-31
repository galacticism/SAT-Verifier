# Polynomial Time SAT Verifier - CNF Converter

def tokenize(formula):
    """
    Convert a string formula into tokens.
    Example: "p implies (q or r)" -> ["p", "implies", "(", "q", "or", "r", ")"]
    """
    formula = formula.replace("(", " ( ").replace(")", " ) ")
    return formula.lower().split()

def parse_to_cnf(formula):
    """
    Convert a boolean logic formula written in English to CNF format.
    
    Parameters:
    formula -- a string like "p implies (q or r)"
    
    Returns:
    A tuple (cnf_formula, var_map) where:
    - cnf_formula is a list of clauses in CNF format suitable for the SAT verifier
    - var_map is a dictionary mapping variable names to numbers
    """
    tokens = tokenize(formula)
    
    # Convert variable names to numbers (p -> 1, q -> 2, etc.)
    var_map = {}
    current_var = 1
    for token in tokens:
        if token.isalpha() and token not in ['implies', 'and', 'or', 'not']:
            if token not in var_map:
                var_map[token] = current_var
                current_var += 1
    
    def parse_expression(tokens, start=0):
        if start >= len(tokens):
            return None, start
        
        # Handle parentheses
        if tokens[start] == '(':
            left, pos = parse_expression(tokens, start + 1)
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError("Missing closing parenthesis")
            pos += 1  # Skip the closing parenthesis
            
            # Check if there's an operator after the parentheses
            if pos < len(tokens) and tokens[pos] in ['implies', 'and', 'or']:
                operator = tokens[pos]
                right, new_pos = parse_expression(tokens, pos + 1)
                
                if operator == 'implies':
                    if isinstance(right[0], list):
                        return ([[-l for l in left[0]] + right[0]], new_pos)
                    return ([[-l for l in left[0]] + [right[0][0]]], new_pos)
                elif operator == 'or':
                    if isinstance(right[0], list):
                        return ([left[0] + right[0]], new_pos)
                    return ([left[0] + [right[0][0]]], new_pos)
                elif operator == 'and':
                    result = left
                    result.extend(right)
                    return result, new_pos
            
            return left, pos
        
        # Handle basic variables
        if tokens[start].isalpha() and tokens[start] not in ['implies', 'and', 'or', 'not']:
            var_num = var_map[tokens[start]]
            if start + 1 < len(tokens) and tokens[start + 1] in ['implies', 'and', 'or']:
                operator = tokens[start + 1]
                right, pos = parse_expression(tokens, start + 2)
                
                if operator == 'implies':
                    # A implies B becomes (-A or B) in CNF
                    if isinstance(right, list) and len(right) > 1:
                        # If right side is multiple clauses (e.g., q and r),
                        # we need to create an implication for each clause
                        result = []
                        for clause in right:
                            result.append([-var_num] + (clause if isinstance(clause, list) else [clause[0]]))
                        return result, pos
                    elif isinstance(right[0], list):
                        return ([[-var_num] + right[0]], pos)
                    return ([[-var_num, right[0][0]]], pos)
                elif operator == 'or':
                    # Combine literals in the OR clause
                    if isinstance(right, list) and len(right) == 1:
                        if isinstance(right[0], list):
                            return ([[var_num] + right[0]], pos)
                        return ([[var_num, right[0][0]]], pos)
                    return ([[var_num, right]], pos)
                elif operator == 'and':
                    # Return both clauses for AND
                    if isinstance(right, list):
                        result = [[var_num]]
                        result.extend(right)
                        return result, pos
                    return [[var_num], right], pos
            return [[var_num]], start + 1
        
        raise ValueError(f"Unexpected token: {tokens[start]}")
    
    try:
        result, _ = parse_expression(tokens)
        return result, var_map
    except Exception as e:
        raise ValueError(f"Failed to parse formula: {str(e)}")

# Example usage
if __name__ == "__main__":
    formulas = [
        "p implies (q or r)",
        "p and q",
        "p or q",
        "(p or q) and r",
        "(p implies q) and r",
        "p implies (q and r)"
    ]
    
    for formula in formulas:
        print(f"\nTesting: {formula}")
        cnf, var_map = parse_to_cnf(formula)
        print(f"CNF format: {cnf}")
        print("Variable mapping:")
        for var, num in var_map.items():
            print(f"{var} -> {num}")
    