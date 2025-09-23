import json, random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)

dataset = []

NUM_SAMPLES = 250_000

for _ in range(NUM_SAMPLES):
    payments_since_last = random.randint(50, 150)

    base_salaries = [random.randint(900, 1500) for _ in range(payments_since_last)]
    total_amount = sum(base_salaries)
    avg_amount = total_amount / payments_since_last

    unique_employees = max(1, int(payments_since_last * random.uniform(0.7, 1.0)))

    past_attacks = random.choices(range(11), weights=[30,25,15,10,6,5,4,3,1,1,0])[0]

    if past_attacks >= 7:
        next_interval = random.choices([50, 100], weights=[85, 15])[0]
    elif past_attacks == 0:
        next_interval = random.choices([100, 150], weights=[20, 80])[0]
    elif past_attacks <= 2:
        next_interval = random.choices([100, 150], weights=[30, 70])[0]
    else:
        next_interval = random.choices([50, 100, 150], weights=[20, 60, 20])[0]
    
    dataset.append({
        "payments_since_last": payments_since_last,
        "total_amount": total_amount,
        "avg_amount": avg_amount,
        "unique_employees": unique_employees,
        "past_attacks": past_attacks,
        "next_interval": next_interval
    })

with open(DATA_DIR / "ml_dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

print(f"Generated {NUM_SAMPLES:,}-entry JSON dataset with realistic variation at data/ml_dataset.json")
