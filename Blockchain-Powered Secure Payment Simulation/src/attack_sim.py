import threading, time, random
from logger import log_transaction

class AttackSimulator:
    def __init__(self, encryption_manager):
        # running: tells if simulator should keep making fake attacks
        self.running = False
        self.enc = encryption_manager

    def start(self):
        # Turns on the simulator and start a background thread that runs the _run()
        self.running = True
        # daemon=True makes the thread stop automatically when the main program ends
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        # Tells the simulator to stop
        self.running = False

    def _run(self):
        # Keeps making fake attack messages while running is True
        while self.running:
            # makes a fake employee id and a fake amount
            fake_emp = random.randint(900000, 999999)
            fake_amount = random.randint(1, 9999)
            
            payload = f"fake:{fake_emp}:{fake_amount}".encode()
            # encrypts the payload
            enc = self.enc.encrypt(payload)
           
            # logs this fake transaction
            # it passes a made-up tx_hash and channel to mark it as fake
            log_transaction(fake_emp, time.time(), fake_amount, enc, tx_hash="FAKE_TX", channel="fake")
            
            # pauses for a short time so it don't flood the system too fast
            time.sleep(0.05)

