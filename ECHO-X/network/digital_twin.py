# ECHO-X
# Digital Twin - Network Model
# Step 1

class Device:
    def __init__(self, name, device_type, security_level):
        self.name = name
        self.device_type = device_type
        self.security_level = security_level
        self.compromised = False

    def status(self):
        if self.compromised:
            return "COMPROMISED"

        return "SECURE"


class DigitalTwin:

    def __init__(self):
        self.devices = {}
        self.connections = {}

    # -----------------------------
    # Add a device to the network
    # -----------------------------

    def add_device(self, name, device_type, security_level):

        device = Device(
            name,
            device_type,
            security_level
        )

        self.devices[name] = device
        self.connections[name] = []

    # -----------------------------
    # Connect two devices
    # -----------------------------

    def connect(self, device_a, device_b):

        if device_a in self.devices and device_b in self.devices:

            self.connections[device_a].append(device_b)
            self.connections[device_b].append(device_a)

    # -----------------------------
    # Compromise a device
    # -----------------------------

    def compromise(self, device_name):

        if device_name in self.devices:

            self.devices[device_name].compromised = True

    # -----------------------------
    # Display network
    # -----------------------------

    def show_network(self):

        print("\n" + "=" * 55)
        print("              ECHO-X DIGITAL TWIN")
        print("=" * 55)

        for name, device in self.devices.items():

            print(
                f"\nDevice: {device.name}"
                f"\nType: {device.device_type}"
                f"\nSecurity Level: {device.security_level}/100"
                f"\nStatus: {device.status()}"
                f"\nConnections: {self.connections[name]}"
            )

        print("\n" + "=" * 55)


# =====================================================
# CREATE THE VIRTUAL COMPANY NETWORK
# =====================================================

network = DigitalTwin()


# -----------------------------
# Company devices
# -----------------------------

network.add_device(
    "Employee PC",
    "Endpoint",
    40
)

network.add_device(
    "Admin PC",
    "Endpoint",
    75
)

network.add_device(
    "Web Server",
    "Server",
    70
)

network.add_device(
    "App Server",
    "Server",
    80
)

network.add_device(
    "Database",
    "Database",
    95
)


# -----------------------------
# Network connections
# -----------------------------

network.connect(
    "Employee PC",
    "Web Server"
)

network.connect(
    "Admin PC",
    "App Server"
)

network.connect(
    "Web Server",
    "App Server"
)

network.connect(
    "App Server",
    "Database"
)


# =====================================================
# TEST THE DIGITAL TWIN
# =====================================================

print("\nCreating virtual company network...")

network.show_network()


# Simulate a compromised employee computer

print("\n⚠️ Simulating compromised Employee PC...")

network.compromise("Employee PC")


# Show network after compromise

network.show_network()