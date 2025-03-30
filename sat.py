# Polynomial Time SAT Verifier

def is_sat(cnf_formula, assignment):
    """
    Check if a given assignment of truth values to the variables in a formula satisfies the formula.
    
    Parameters:
    cnf_formula -- a list of clauses, where each clause is a list of literals
                   positive numbers represent variables, negative numbers represent negated variables
    assignment -- a list where assignment[i] represents the truth value of variable i+1
                  1 means True, 0 means False
    
    Returns:
    True if the assignment satisfies the formula, False otherwise
    """
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

print("Example 1:", is_sat([[1, 2], [1, 3], [2, 3]], [1, 1, 0]))
print("Example 2:", is_sat([[1, 2], [-1, 3], [-2, -3]], [0, 1, 1]))
print("Example 3:", is_sat([[1, 2], [1, 3], [2, 3]], [0, 0, 0]))