import socket
import json

port = 11111

def summarize(records):
    income, expense = 0, 0
    for record in range(len(records)):
        if record["amount"] > 0:
            income += record["amount"]
        else:
            expense += record["amount"]
    return {
        "totalIncome": income,
        "totalExpense": expense,
        "netSpending": income + expense
    }

def classify_purpose(records):
    result = []
    for record in records:
        description = record.get("description", "").lower()
        if "rent" in description:
            label = "Housing"
        elif "food" in description:
            label = "Food"
        elif "uber" in description or "lyft" or "car" in description:
            label = "Transport"
        else:
            label = "Other"
        new_record = record.copy()
        new_record["classification"] = label
        result.append(new_record)
    return result

def classify_duration(records):
    result = []
    # for record in records:
        
        # IMPLEMENT LOGIC HERE, NEED TO FIGURE OUT

        # new_record = record.copy()
        # new_record["classification"] = label
        # result.append(new_record)
    return result

def listen(listener_socket):
    connection, address = listener_socket.accept()
    print(f"Connected on {address}")

    run = True
    while run:
        data = connection.recv(2048).decode()
        if not data:
            continue

        print("Listener received:", data)

        if data == "quit":
            connection.close()
            listen(listener_socket)
            return
        elif data == "close":
            connection.close()
            run = False
            break

        data = json.loads(data)
        action = data["action"]
        records = data.get("records", [])

        if action == "summary":
            response = summarize(records)
        elif action == "classify_purpose":
            response = classify_purpose(records)
        elif action == "classify_duration":
            response = classify_duration(records)
        else:
            response = {"error": "Unknown action"}

        connection.send(json.dumps(response).encode())


# Setup
listener_socket = socket.socket()
listener_socket.bind((socket.gethostname(), port))
listener_socket.listen(1)
listen(listener_socket)
listener_socket.close()