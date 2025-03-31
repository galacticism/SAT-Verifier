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
    A list of clauses in CNF format suitable for the SAT verifier
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
            return left, pos + 1
        
        # Handle basic variables
        if tokens[start].isalpha() and tokens[start] not in ['implies', 'and', 'or', 'not']:
            var_num = var_map[tokens[start]]
            if start + 1 < len(tokens) and tokens[start + 1] in ['implies', 'and', 'or']:
                operator = tokens[start + 1]
                right, pos = parse_expression(tokens, start + 2)
                
                if operator == 'implies':
                    # A implies B becomes (-A or B) in CNF
                    return ([[-var_num, right[0][0]]], pos)
                elif operator == 'or':
                    # Combine literals in the OR clause
                    if isinstance(right, list) and len(right) == 1:
                        return ([[var_num] + right[0]], pos)
                    return ([[var_num, right]], pos)
                elif operator == 'and':
                    # Return both clauses for AND
                    if isinstance(right, list):
                        return ([[var_num]], pos) + right
                    return ([[var_num], right], pos)
            return [[var_num]], start + 1
        
        raise ValueError(f"Unexpected token: {tokens[start]}")
    
    try:
        result, _ = parse_expression(tokens)
        return result
    except Exception as e:
        raise ValueError(f"Failed to parse formula: {str(e)}")

# Example usage
if __name__ == "__main__":
    formula = "p implies (q or r)"
    cnf = parse_to_cnf(formula)
    print(f"Original: {formula}")
    print(f"CNF format: {cnf}")
    
    # Print variable mapping
    var_map_reverse = {v: k for k, v in var_map.items()}
    print("\nVariable mapping:")
    for num, var in var_map_reverse.items():
        print(f"{var} -> {num}")
    