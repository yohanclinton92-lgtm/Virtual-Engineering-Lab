def is_number(x):
    return isinstance(x, (int, float))


def run_experiment(experiment, user_inputs):
    context = {}
    context.update(user_inputs)

    results = {}
    feedback = []

    # Calculations
    try:
        for calc in experiment.get("calculations", []):
            exec(calc, {}, context)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    # Outputs
    for out in experiment.get("outputs", []):
        val = context.get(out)
        if is_number(val):
            results[out] = round(val, 4)
        else:
            results[out] = val

    # Diagnostics
    for d in experiment.get("diagnostics", []):
        try:
            if eval(d["condition"], {}, context):
                feedback.append(d["message"])
        except:
            pass

    return {
        "status": "success",
        "results": results,
        "feedback": feedback,
        "context": context
    }
