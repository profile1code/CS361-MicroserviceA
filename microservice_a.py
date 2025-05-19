from flask import Flask, request, jsonify

app = Flask(__name__)

# Modifiable lists to add keywords and possible labels
purpose_key = [
    (["rent", "apartment", "house"], "Housing"),
    (["food", "eat"], "Food"),
    (["uber", "lyft", "transport", "car"], "Transport"),
    (["tv", "entertainment", "game", "fun"], "Entertainment"),
    (["school", "tuition", "book"], "Education"),
]

duration_key = [
    (["month"], "Monthly"),
    (["week"], "Weekly"),
    (["single", "one-time", "once"], "One-Time"),
]

port = 11111

def summarize(records):
    """This function takes a list of financial records and returns a summary of 
    income, expense and net spending."""
    income, expense = 0, 0
    for record in records:
        if record["amount"] > 0:
            income += record["amount"]
        else:
            expense += record["amount"]
    return {
        "totalIncome": income,
        "totalExpense": expense,
        "netSpending": income + expense
    }

def classify(records, key_list):
    """This function takes a list of records and classifies each record by the given list."""
    result = []
    for record in records:
        description = record["description"].lower()
        label = "Other"
        found = False
        for keys, value in key_list:  # Go through each of the key pairs given in parameter
            for key in keys:
                if key in description:
                    label = value
                    found = True
                    break  # Once 1 value found, just break
            if found:
                break
        new_record = record.copy()
        new_record["classification"] = label
        result.append(new_record)
    return result

@app.route("/summary", methods=["POST"])
def summary_route():
    data = request.get_json()
    records = data.get("records", [])
    return jsonify(summarize(records))

@app.route("/classify/purpose", methods=["POST"])
def classify_purpose_route():
    data = request.get_json()
    records = data.get("records", [])
    return jsonify(classify(records, purpose_key))

@app.route("/classify/duration", methods=["POST"])
def classify_duration_route():
    data = request.get_json()
    records = data.get("records", [])
    return jsonify(classify(records, duration_key))

if __name__ == "__main__":
    app.run(host = 0, port = port)
