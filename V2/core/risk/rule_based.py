def rule_based_risk_flags(clause):
    """
    Returns list of risk flags detected in the clause, empty list if none.
    """
    clause_l = clause.lower()
    risks = []
    if "unlimited liability" in clause_l:
        risks.append("Unlimited liability")
    if "indemnify" in clause_l:
        risks.append("Indemnification obligation")
    if "penalty" in clause_l or "late fee" in clause_l:
        risks.append("Penalty clause")
    if "termination for convenience" in clause_l:
        risks.append("Termination risk")
    # Add more rule patterns as needed
    return risks
