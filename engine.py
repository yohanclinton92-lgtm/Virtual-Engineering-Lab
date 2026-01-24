def is_number(x):
    return isinstance(x, (int, float))


def run_experiment(experiment, user_inputs):
    context = {}
    context.update(user_inputs)

    results = {}
    feedback = []

    # --------------------
    # Constraints
    # --------------------
    for constraint in experiment.get("constraints", []):
        try:
            if not eval(constraint["rule"], {}, context):
                return {
                    "status": "error",
                    "message": constraint["error"]
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Constraint error: {e}"
            }

    # --------------------
    # Calculations
    # --------------------
    try:
        for calc in experiment.get("calculations", []):
            exec(calc, {}, context)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Calculation error: {e}"
        }

    # --------------------
    # Outputs
    # --------------------
    for out in experiment.get("outputs", []):
        val = context.get(out)
        if is_number(val):
            results[out] = round(val, 4)
        else:
            results[out] = val

    # --------------------
    # Diagnostics
    # --------------------
    for diag in experiment.get("diagnostics", []):
        try:
            if eval(diag["condition"], {}, context):
                feedback.append(diag["message"])
        except Exception:
            pass

    # --------------------
    # Effectiveness (optional)
    # --------------------
    eff = None
    if is_number(context.get("effectiveness")):
        eff = context["effectiveness"]
    elif is_number(context.get("conversion")):
        eff = context["conversion"]
    elif is_number(context.get("percentage")):
        eff = context["percentage"] / 100

    if eff is not None:
        results["effectiveness"] = round(float(eff), 4)

    return {
        "status": "success",
        "results": results,
        "feedback": feedback
    }
