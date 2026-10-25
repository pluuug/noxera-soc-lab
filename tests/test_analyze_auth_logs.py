import unittest
from src.analyze_auth_logs import analyze

def line(stamp, message):
    return f"{stamp} host sshd[1234]: {message}"

class AnalyzerTests(unittest.TestCase):
    def test_failures_within_window_trigger_rule_001(self):
        logs = [line(f"Oct 24 09:0{i}:00", f"Failed password for user{i} from 203.0.113.10 port 22 ssh2") for i in range(3)]
        result = analyze(logs, threshold=3, window_minutes=10)
        self.assertTrue(any(a["rule_id"] == "NX-SOC-001" for a in result["alerts"]))

    def test_success_after_failures_triggers_rule_002(self):
        logs = [line(f"Oct 24 09:0{i}:00", f"Failed password for user{i} from 203.0.113.10 port 22 ssh2") for i in range(3)]
        logs.append(line("Oct 24 09:04:00", "Accepted password for deploy from 203.0.113.10 port 22 ssh2"))
        result = analyze(logs, threshold=3, window_minutes=10)
        self.assertTrue(any(a["rule_id"] == "NX-SOC-002" for a in result["alerts"]))

    def test_success_before_failures_does_not_trigger_rule_002(self):
        logs = [line("Oct 24 09:00:00", "Accepted password for deploy from 203.0.113.10 port 22 ssh2")]
        logs += [line(f"Oct 24 09:0{i}:00", f"Failed password for user{i} from 203.0.113.10 port 22 ssh2") for i in range(1, 4)]
        result = analyze(logs, threshold=3, window_minutes=10)
        self.assertFalse(any(a["rule_id"] == "NX-SOC-002" for a in result["alerts"]))

    def test_failures_outside_window_do_not_trigger_rule_001(self):
        logs = [
            line("Oct 24 09:00:00", "Failed password for root from 203.0.113.10 port 22 ssh2"),
            line("Oct 24 09:20:00", "Failed password for admin from 203.0.113.10 port 22 ssh2"),
            line("Oct 24 09:40:00", "Failed password for deploy from 203.0.113.10 port 22 ssh2")]
        result = analyze(logs, threshold=3, window_minutes=10)
        self.assertFalse(any(a["rule_id"] == "NX-SOC-001" for a in result["alerts"]))

if __name__ == "__main__":
    unittest.main()
