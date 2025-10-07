# Imports classes and functions from different files in the same project
from blockchain import BlockchainManager
from encryption import EncryptionManager
from attack_sim import AttackSimulator
from logger import log_transaction, clear_logs, log_scan_event
from visualizer import make_plots
from ml_predictor import ThreatPredictor
# Imports some built-in modules
from collections import deque
import time, random, threading
import sys

# Imports different keyboard input modules
try:
    import msvcrt 
except ImportError:
    import tty, termios, select  

# Constants
NUM_EMPLOYEES = 2000                             # Total number of employees to "pay"
CHECK_INTERVAL = 100                             # How often to check for threats
PAYMENT_DELAY = 0.01                             # Time delay between each payment (in seconds)
ROLLING_WINDOW = 500                             # Number of past payments to keep track of for attack detection

# Main simulator class
class BlockchainPaymentSimulator:
    def __init__(self):
        # Setup all the parts needed: blockchain, encryption, attacks, and ML prediction
        self.bc = BlockchainManager()
        self.enc = EncryptionManager()
        self.attack = AttackSimulator(self.enc)
        self.threat_predictor = ThreatPredictor()

        # Number of employees paid so far
        self.paid = 0
        self.next_check = CHECK_INTERVAL
        self._stop = False

        # How many attack sessions have happened
        self.past_attacks = 0
        self.threat_scores = []
        self.recent_attacks = deque(maxlen=ROLLING_WINDOW)
        self.current_attack_session_counted = False
        self.total_attacks_cumulative = 0

        # Sends some fake ETH to the contract before starting
        try:
            tx_hash = self.bc.w3.eth.send_transaction({
                "from": self.bc.accounts[0],
                "to": self.bc.contract_address,
                "value": self.bc.w3.to_wei(50, "ether")
            })
            self.bc.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f">>>=== Funded Payroll contract {self.bc.contract_address} with 50 ETH ===<<<")
        except Exception as e:
            print(f"<!> Could not fund contract: {e}")

    def single_payment(self, emp_id: int):
        # Makes a single salary payment to one employee
        amount = 1000 + random.randint(0, 500)
        payload = f"{emp_id}:{amount}".encode()
        enc = self.enc.encrypt(payload)

        # Sends the salary on the blockchain
        try:
            receipt = self.bc.pay_salary(emp_id, self.bc.w3.to_wei(amount, "wei"))
            tx_hash = getattr(receipt, "transactionHash", None) if receipt else None
        except Exception as e:
            print(f"<!> Payment failed: {e}")
            tx_hash = None

        # Gets the current time (timestamp)
        ts = int(time.time())
        # Saves payment info to a log file
        log_transaction(emp_id, ts, amount, enc, tx_hash=tx_hash)
        self.paid += 1

        # Checks if there was an attack happening during this payment
        if self.attack.running and not self.current_attack_session_counted:
            self.recent_attacks.append(1)
            self.total_attacks_cumulative += 1
            self.current_attack_session_counted = True
        else:
            self.recent_attacks.append(0)

        print(f"-> SALARY OF {amount} wei SENT TO employee_{emp_id} [Transaction #{self.paid}]")
        time.sleep(PAYMENT_DELAY)

    def crowdsensing_check(self) -> int:
        # Runs the ML model to check for threats and decide when to scan next
        payments_since_last = CHECK_INTERVAL

        # Generates data to simulate recent payment behavior
        total_amount = sum([1000 + random.randint(0, 500) for _ in range(payments_since_last)])
        avg_amount = total_amount / payments_since_last
        unique_employees = min(payments_since_last, NUM_EMPLOYEES)
        past_attacks_in_window = sum(self.recent_attacks)

        next_interval = CHECK_INTERVAL
        threat_score = 0.0

        try:
            # The ML model predicts the next scan time and threat level
            result = self.threat_predictor.predict_interval(
                payments_since_last,
                total_amount,
                avg_amount,
                unique_employees,
                past_attacks_in_window
            )

            if isinstance(result, (tuple, list)) and len(result) >= 2:
                next_interval, threat_score = result[0], float(result[1])
            else:
                next_interval = int(result)
                threat_score = 0.0
        except Exception as e:
            print(f"<!> ML predictor error: {e}. Falling back to default interval {CHECK_INTERVAL}.")
        # Saves the results for analysis
        self.threat_scores.append((self.paid, next_interval, threat_score))

        try:
            # Logs this scan/check
            log_scan_event(
                step=self.paid,
                confidence=threat_score,
                scan_time=next_interval,
                attacks_detected=past_attacks_in_window,
                attacks_cumulative=self.total_attacks_cumulative
            )
        except Exception as e:
            print(f"<!> Failed to log scan event: {e}")

        try:
            # Changes encryption method to stay secure
            self.enc.switch_algorithm()
        except Exception:
            pass

        # Prints a report of this check
        print(f"__________________________________________________________________________________")
        print(f"[CROWDSENSE] payment {self.paid}, next_check={next_interval}, "
              f"Threat Score={threat_score:.4f}, algo={self.enc.current_algorithm()}, "
              f"recent_attacks(last {ROLLING_WINDOW})={past_attacks_in_window}, "
              f"cumulative_attacks={self.total_attacks_cumulative}")
        print(f"__________________________________________________________________________________")

        if not self.attack.running:
            # Resets the attack counter if no attack
            self.current_attack_session_counted = False

        return next_interval

    def run(self):
        # Start the simulation and handles keyboard commands in the background
        def input_listener():
            # Checks for keyboard input to trigger attacks or stop the simulation
            while not self._stop:
                key = None
                if 'msvcrt' in sys.modules:
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode().lower()
                else:
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                        tty.setraw(fd)
                        if select.select([sys.stdin], [], [], 0)[0]:
                            key = sys.stdin.read(1).lower()
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

                if key:
                    # Reacts to key presses
                    if key == 'x' and not self.attack.running:
                        self.attack.start()
                        self.past_attacks += 1
                        self.current_attack_session_counted = False
                        print(f"+----------------------------------/")
                        print(f"[ATTACK]=> Attack started!        /")
                        print(f"+--------------------------------/")
                    elif key == 'z':
                        if self.attack.running:
                            self.attack.stop()
                            print(f"+----------------------------------/")
                            print(f"[ATTACK]=> Attack stopped!        /")
                            print(f"+--------------------------------/")
                        else:
                            self._stop = True
                            print(f"+---------------------------------------/")
                            print(f"[SIMULATOR]=> Simulator stopping...     /")   
                            print(f"+-------------------------------------/")
                time.sleep(0.05)

        threading.Thread(target=input_listener, daemon=True).start()

        # Keeps making payments until done or told to stop
        while not self._stop and self.paid < NUM_EMPLOYEES:
            emp_id = random.randint(100000, 999999)
            self.single_payment(emp_id)

            # After certain number of payments, runs a threat check
            if self.paid >= self.next_check:
                self.next_check = self.paid + self.crowdsensing_check()

        try:
            # After all payments are done, it shows visual results
            make_plots(num_employees=NUM_EMPLOYEES)
        except Exception as e:
            print(f"<!> make_plots failed: {e}")

        # Shows how well ML-based checking worked
        self._print_efficiency_report()

        try:
            # Cleans the logs
            clear_logs()
        except Exception as e:
            print(f"<!> clear_logs failed: {e}")

        print(f"[SIMULATOR]==> Run finished. Total unique attack sessions: {self.past_attacks}")
        print("[SIMULATOR]==> Logs cleared, report generated !")

    def _print_efficiency_report(self):
        baseline_scans = NUM_EMPLOYEES // CHECK_INTERVAL
        ml_scans = len(self.threat_scores)
        efficiency = baseline_scans / ml_scans if ml_scans else 0
        print("\n+-------------------- Efficiency Report --------------------+")
        print(f"| ==> Static scanning (every {CHECK_INTERVAL} tx): {baseline_scans} scans              |")
        print(f"| ==> ML-based adaptive scanning: {ml_scans} scans                  |")
        print(f"| ==> Efficiency Gain: {efficiency:.2f}x                                |")
        print("+-----------------------------------------------------------+")

if __name__ == "__main__":
    sim = BlockchainPaymentSimulator()
    sim.run()

