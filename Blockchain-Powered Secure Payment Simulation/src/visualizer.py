import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Set the folders where output images will be saved
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUTPUT_DIR = DATA_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Sets the paths to the log files
TRANSACTIONS_LOG = DATA_DIR / "transactions.json"
ATTACKS_LOG = DATA_DIR / "attacks.json"
SCAN_LOG = OUTPUT_DIR / "scan_log.json"

# It creates and saves three charts using the log data:
# Visual 1: Payments over time
# Visual 2: Confidence over time
# Visual 3: Scan time vs Attacks
def make_plots(num_employees):

    # Try to read the transaction log
    try:
        with open(TRANSACTIONS_LOG, "r") as f:
            transactions = json.load(f)
    except:
        transactions = []

    # Try to read the attacks log
    try:
        with open(ATTACKS_LOG, "r") as f:
            attacks = json.load(f)
    except:
        attacks = []

    # Try to read the scan log
    try:
        with open(SCAN_LOG, "r") as f:
            scans = json.load(f)
    except:
        scans = []

    # ----- Visual 1: Payments over time -----
    if transactions:
        amounts = [t["amount"] for t in transactions]
        plt.figure(figsize=(10,5))
        sns.lineplot(x=range(len(amounts)), y=amounts)
        plt.title("Payments over time")
        plt.xlabel("Scan step")
        plt.ylabel("Amount")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "payments_over_time.png")
        plt.close()

    # ----- Visual 2: Confidence over time -----
    if scans:
        steps = [s["step"] for s in scans]
        confidence = [s["confidence"] for s in scans]

        plt.figure(figsize=(12,6))
        sns.lineplot(x=steps, y=confidence, marker="o", label="Threat Score")
        plt.title("ML Threat over Transaction Timeline")
        plt.xlabel("Total Transactions Processed")
        plt.ylabel("Threat Score")
        plt.xlim(0, num_employees) 
        plt.ylim(0, 1)        

        for x, y in zip(steps, confidence):
            plt.text(x, y + 0.02, f"{y:.2f}", fontsize=8, ha='center')

        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "confidence_over_time.png")
        plt.close()

    # ----- Visual 3: Scan time vs Attacks -----
    if scans:
        steps = [s["step"] for s in scans]
        scan_times = [s["scan_time"] for s in scans]
        attacks_detected = [s["attacks_detected"] for s in scans]
        attacks_cumulative = [s.get("attacks_cumulative", 0) for s in scans]

        plt.figure(figsize=(10,5))
        sns.lineplot(x=steps, y=scan_times, marker="s", label="Scan Time")
        sns.lineplot(x=steps, y=attacks_detected, marker="^", label="Rolling-window Attacks")
        sns.lineplot(x=steps, y=attacks_cumulative, marker="o", label="Cumulative Attacks", linewidth=2)
        plt.title("Scan Time Adjustment vs Attacks")
        plt.xlabel("Scan Step")
        plt.ylabel("Scan interval")
        plt.legend()
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "scan_time_vs_attacks.png")
        plt.close()

    # Prints message saying the plots were saved
    print(f"__________________________________________________________________________________")
    print(f"[visualizer]==> Plots saved in {OUTPUT_DIR}")

