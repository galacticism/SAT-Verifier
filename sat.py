# Polynomial Time SAT Verifier

def is_sat(formula, assignment):
    """
    Check if a given assignment of truth values to the variables satisfies a formula.
    
    Parameters:
    formula -- a list of elements, where each element is either:
               - a clause (list of literals) in CNF form, or
               - a tuple (A, B) representing an implication A → B
               Positive numbers represent variables, negative numbers represent negated variables.
    assignment -- a list where assignment[i] represents the truth value of variable i+1
                  1 means True, 0 means False
    
    Returns:
    True if the assignment satisfies the formula, False otherwise
    """
    # convert to CNF
    cnf_formula = []
    for element in formula:
        if isinstance(element, tuple) and len(element) == 2:
            # convert implication to or
            antecedent, consequent = element
            negated_antecedent = -antecedent
            implication_clause = [negated_antecedent, consequent]
            cnf_formula.append(implication_clause)
        else:
            cnf_formula.append(element)
    # check satisfiability
    for clause in cnf_formula:
        clause_satisfied = False
        for literal in clause:
            var_idx = abs(literal) - 1 
            
            if var_idx < len(assignment):
                if literal > 0 and assignment[var_idx] == 1:
                    clause_satisfied = True
                    break
                elif literal < 0 and assignment[var_idx] == 0:
                    clause_satisfied = True
                    break
        
        if not clause_satisfied:
            return False
    
    return True

# Add these examples at the bottom:
from cnf_converter import parse_to_cnf

# Test with English-like formulas
test_formulas = [
    ("p implies (q or r)", [1, 1, 0]),  # p=True, q=True, r=False
    ("p implies (q or r)", [1, 0, 0]),  # p=True, q=False, r=False (should be False)
    ("p implies (q or r)", [0, 0, 0]),  # p=False, q=False, r=False (should be True)
]

print("\nTesting English-like formulas:")
for formula, assignment in test_formulas:
    cnf = parse_to_cnf(formula)
    result = is_sat(cnf, assignment)
    print(f"\nFormula: {formula}")
    print(f"CNF format: {cnf}")
    print(f"Assignment: {assignment}")
    print(f"Result: {result}")

