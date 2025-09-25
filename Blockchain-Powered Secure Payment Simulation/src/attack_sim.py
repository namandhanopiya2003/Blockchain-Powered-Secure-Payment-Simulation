import threading, time, random
from logger import log_transaction

class AttackSimulator:
    def __init__(self, encryption_manager):
        self.running = False
        self.enc = encryption_manager

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            fake_emp = random.randint(900000, 999999)
            fake_amount = random.randint(1, 9999)
            payload = f"fake:{fake_emp}:{fake_amount}".encode()
            enc = self.enc.encrypt(payload)
            log_transaction(fake_emp, time.time(), fake_amount, enc, tx_hash="FAKE_TX", channel="fake")
            time.sleep(0.05)
