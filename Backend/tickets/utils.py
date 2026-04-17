# tickets/utils.py

def classify_ticket(description):
    description = description.lower()

    if "payment" in description or "bill" in description:
        return {"category": "billing", "priority": "medium"}

    elif "error" in description or "bug" in description:
        return {"category": "technical", "priority": "high"}

    elif "login" in description or "account" in description:
        return {"category": "account", "priority": "medium"}

    else:
        return {"category": "general", "priority": "low"}