import serial
import time
import threading
from config import SERIAL_PORT, BAUD_RATE, SERIAL_TIMEOUT


class SerialBridge:
    # Handles all serial communication between Python and the Arduino

    def __init__(self):
        self.connection = None
        self.connected = False
        self._lock = threading.Lock()
        self._monitor_thread = None
        self._monitoring = False
        self._alarm_printed = False
        self._pending_trigger = None
        self.alarm_event = threading.Event()
        self._reprint_menu = lambda: None

    def connect(self):
        try:
            self.connection = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT)
            start = time.time()
            while True:
                if self.connection.in_waiting:
                    line = self.connection.readline().decode("utf-8").strip()
                    if line == "ARDUINO_READY":
                        self.connected = True
                        time.sleep(0.5)
                        self.connection.reset_input_buffer()
                        self.connection.write(("READY_ACK\n").encode("utf-8"))
                        start2 = time.time()
                        while time.time() - start2 < 5:
                            if self.connection.in_waiting:
                                ack = self.connection.readline().decode("utf-8").strip()
                                if ack == "SYSTEM_READY":
                                    self._start_monitor()
                                    return True
                        self._start_monitor()
                        return True
                if time.time() - start > 10:
                    return False
        except serial.SerialException as e:
            print("Error: could not open serial port", SERIAL_PORT)
            self.connected = False
            return False

    def set_menu_callback(self, callback):
        self._reprint_menu = callback

    def _start_monitor(self):
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()

    def _monitor_loop(self):
        # Background thread watching for trigger messages from Arduino
        while self._monitoring and self.connected:
            try:
                with self._lock:
                    if self.connection and self.connection.in_waiting:
                        line = self.connection.readline().decode("utf-8").strip()
                        if line.startswith("TRIGGER:") and not self._alarm_printed:
                            self._alarm_printed = True
                            parts = line.split(":")
                            source = parts[2] if len(parts) >= 3 else "UNKNOWN"
                            self._pending_trigger = source
                            self.alarm_event.set()
                            print("\n!!! ALARM TRIGGERED !!!")
                            print("Triggered by:", source)
                            print()
                            self._reprint_menu()
                time.sleep(0.05)
            except Exception:
                break

    def reset_alarm_flag(self):
        self._alarm_printed = False
        self._pending_trigger = None
        self.alarm_event.clear()

    def disconnect(self):
        self._monitoring = False
        if self.connection and self.connection.is_open:
            self.connection.close()
            self.connected = False

    def _send_command(self, command, expected_prefix):
        if not self.connected or not self.connection.is_open:
            return None
        try:
            with self._lock:
                self.connection.write((command + "\n").encode("utf-8"))
                start = time.time()
                while time.time() - start < SERIAL_TIMEOUT:
                    if self.connection.in_waiting:
                        line = self.connection.readline().decode("utf-8").strip()
                        if line.startswith(expected_prefix):
                            return line
                        if line.startswith("TRIGGER:") and not self._alarm_printed:
                            self._alarm_printed = True
                            parts = line.split(":")
                            source = parts[2] if len(parts) >= 3 else "UNKNOWN"
                            self._pending_trigger = source
                            self.alarm_event.set()
                            print("\n!!! ALARM TRIGGERED !!!")
                            print("Triggered by:", source)
                            print()
                            self._reprint_menu()
            return None
        except serial.SerialException:
            return None

    def arm(self):
        response = self._send_command("ARM", "ARM_OK")
        return response == "ARM_OK"

    def disarm(self):
        response = self._send_command("DISARM", "DISARM_OK")
        if response == "DISARM_OK":
            self.reset_alarm_flag()
            return True
        return False

    def get_status(self):
        response = self._send_command("GET_STATUS", "STATUS:")
        if response and response.startswith("STATUS:"):
            return response.split(":")[1]
        return None

    def get_sensors(self):
        response = self._send_command("GET_SENSORS", "SENSORS:")
        if response and response.startswith("SENSORS:"):
            sensors = {}
            data = response[8:]
            if data:
                for entry in data.split(","):
                    parts = entry.split(":")
                    if len(parts) == 2:
                        sensors[parts[0]] = parts[1] == "1"
            return sensors
        return None

    def get_actuators(self):
        response = self._send_command("GET_ACTUATORS", "ACTUATORS:")
        if response and response.startswith("ACTUATORS:"):
            actuators = {}
            data = response[10:]
            if data:
                for entry in data.split(","):
                    parts = entry.split(":")
                    if len(parts) == 2:
                        actuators[parts[0]] = parts[1] == "1"
            return actuators
        return None

    def alarm_cutoff(self):
        response = self._send_command("ALARM_CUTOFF", "ALARM_CUTOFF")
        return response == "ALARM_CUTOFF"

    def listen_for_triggers(self):
        pass