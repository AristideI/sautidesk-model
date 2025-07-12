import random
import json

# Enums
TICKET_PRIORITIES = ["LOW", "MEDIUM", "HIGH"]
TICKET_STATES = ["OPEN", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CLOSED"]
TICKET_SOURCES = ["MANUAL", "AI"]
TICKET_TYPES = [
    "TICKET",
    "INCIDENT",
    "QUESTION",
    "REQUEST",
    "PROBLEM",
    "SUGGESTION",
    "OTHER",
]

# Organisation tags
org_tags = {
    "MTN": [
        "calling",
        "network",
        "billing",
        "mobile money",
        "airtime",
        "data bundle",
        "sim card",
        "subscription",
        "sms",
        "balance",
    ],
    "CanalBox": [
        "internet",
        "router",
        "wifi",
        "modem",
        "slow speed",
        "disconnection",
        "installation",
        "fiber",
        "ISP",
        "no signal",
    ],
    "REG": [
        "electricity",
        "power outage",
        "billing",
        "pole damage",
        "line cut",
        "high voltage",
        "meter issue",
        "transformer",
        "connection delay",
        "voltage drop",
    ],
    "Wasac": [
        "water supply",
        "pipe burst",
        "meter",
        "leak",
        "billing",
        "sewage",
        "no water",
        "water quality",
        "low pressure",
        "disconnection",
    ],
    "ALU": [
        "grades",
        "course registration",
        "wifi",
        "finance",
        "student ID",
        "exam schedule",
        "library",
        "hostel",
        "IT support",
        "portal access",
    ],
    "Other": [
        "account",
        "login",
        "feedback",
        "suggestion",
        "bug",
        "feature request",
        "support",
        "general",
        "technical issue",
        "complaint",
    ],
}

# Issue templates (30 per category)
issue_templates = {
    "MTN": [
        "I can't make or receive calls.",
        "Mobile money transaction failed.",
        "Network is very weak at my location.",
        "Airtime purchase didn't go through.",
        "Data bundle expired too quickly.",
        "SIM card isn't detected.",
        "Balance check service not working.",
        "Subscribed service activated without permission.",
        "Can't send or receive SMS.",
        "Unexpected charges on my bill.",
    ]
    * 3,
    "CanalBox": [
        "My internet connection keeps dropping.",
        "Router doesn't connect to the network.",
        "WiFi is very slow lately.",
        "Fiber optic cable cut.",
        "Modem not showing any signal.",
        "Disconnection without notice.",
        "Cannot access some websites.",
        "Poor speed despite premium plan.",
        "Technical support is not reachable.",
        "Installation delayed for a week.",
    ]
    * 3,
    "REG": [
        "Power outage since last night.",
        "High voltage damaged my appliances.",
        "Electricity bill seems incorrect.",
        "Fallen electric pole is dangerous.",
        "No electricity for two days.",
        "Transformer exploded nearby.",
        "Meter reading is not accurate.",
        "Frequent power cuts during the day.",
        "Light flickers constantly.",
        "Connection is pending since last week.",
    ]
    * 3,
    "Wasac": [
        "No water for two days.",
        "Water pipe burst on the road.",
        "My water meter is faulty.",
        "Water smells and is brown.",
        "Bill is unusually high.",
        "Sewage leaking near my home.",
        "Water pressure is too low.",
        "There was a disconnection without notice.",
        "Requesting a new water connection.",
        "Unhygienic water being supplied.",
    ]
    * 3,
    "ALU": [
        "Grades are not updated in portal.",
        "Course registration is failing.",
        "WiFi not working in hostels.",
        "Unable to access finance records.",
        "Lost my student ID card.",
        "Exam timetable not published.",
        "Library account is locked.",
        "Portal access denied.",
        "Room allocation issue in hostel.",
        "Lecture schedules are missing.",
    ]
    * 3,
    "Other": [
        "Login failed repeatedly.",
        "App crashes after login.",
        "I want to give feedback.",
        "Feature request: dark mode.",
        "Bug found on dashboard.",
        "General complaint about service.",
        "Technical support needed urgently.",
        "Account deletion is not working.",
        "Suggestion for user onboarding.",
        "Mobile layout broken.",
    ]
    * 3,
}


# Title generator
def generate_title(description):
    if "internet" in description or "WiFi" in description:
        return "Internet issue"
    elif "bill" in description or "payment" in description:
        return "Billing issue"
    elif "power" in description or "electricity" in description:
        return "Electricity issue"
    elif "water" in description:
        return "Water issue"
    elif "grade" in description or "course" in description:
        return "Academic issue"
    elif "login" in description:
        return "Login issue"
    return "General support request"


# Main data generator
def generate_data(n=500):
    dataset = []

    for _ in range(n):
        org = random.choice(list(issue_templates.keys()))
        text = random.choice(issue_templates[org])
        title = generate_title(text)
        tag = random.choice(org_tags[org])

        sample = {
            "text": text,
            "label": {
                "title": title,
                "description": text,
                "state": random.choice(TICKET_STATES),
                "priority": random.choice(
                    TICKET_PRIORITIES if org != "REG" else ["HIGH"]
                ),
                "assignedTo": None,
                "ownedBy": f"user_{random.randint(1000, 9999)}",
                "organisation": org,
                "tags": tag,
                "source": random.choice(TICKET_SOURCES),
                "type": random.choice(TICKET_TYPES),
            },
        }

        dataset.append(sample)

    return dataset


# Save generated data
data = generate_data(5000)

with open("data/training_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Synthetic training data generated and saved to data/training_data.json")
