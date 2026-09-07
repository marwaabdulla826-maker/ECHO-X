# =========================================================
# ECHO-X
# Automatic Digital Twin Builder - Step 23
# =========================================================

from network.digital_twin import DigitalTwin
from scanner.network_scanner import NetworkScanner


class AutomaticTwinBuilder:

    def __init__(self, network_range):

        self.network_range = network_range

        self.scanner = NetworkScanner(
            network_range
        )

        self.twin = DigitalTwin()

    # =====================================================
    # DETERMINE DEVICE TYPE
    # =====================================================

    def detect_device_type(
        self,
        device
    ):

        ports = device.get(
            "open_ports",
            []
        )

        if 445 in ports:

            return "Windows Host"

        if 22 in ports:

            return "Linux/SSH Host"

        if 443 in ports or 80 in ports:

            return "Web Host"

        return "Network Device"

    # =====================================================
    # CALCULATE SECURITY LEVEL
    # =====================================================

    def calculate_security_level(
        self,
        device
    ):

        ports = device.get(
            "open_ports",
            []
        )

        security = 100

        # SMB
        if 445 in ports:

            security -= 20

        # RDP
        if 3389 in ports:

            security -= 20

        # Telnet
        if 23 in ports:

            security -= 30

        # FTP
        if 21 in ports:

            security -= 15

        return max(
            security,
            0
        )

    # =====================================================
    # BUILD DIGITAL TWIN
    # =====================================================

    def build(self):

        print("\n")
        print("=" * 70)

        print(
            "          ECHO-X AUTOMATIC DIGITAL TWIN"
        )

        print("=" * 70)

        print(
            f"\nNetwork: "
            f"{self.network_range}"
        )

        # -------------------------------------------------
        # Discover devices
        # -------------------------------------------------

        devices = self.scanner.discover()

        if not devices:

            print(
                "\n❌ No devices discovered."
            )

            return None

        print("\n")
        print(
            "🧩 Building Digital Twin..."
        )

        # -------------------------------------------------
        # Add devices
        # -------------------------------------------------

        device_names = []

        for index, device in enumerate(
            devices,
            start=1
        ):

            ip = device["ip"]

            hostname = device.get(
                "hostname",
                "Unknown"
            )

            device_type = (
                self.detect_device_type(
                    device
                )
            )

            security_level = (
                self.calculate_security_level(
                    device
                )
            )

            # Create unique internal name
            name = (
                hostname
                if hostname != "Unknown"
                else f"Device-{index}"
            )

            # Prevent duplicate names
            if name in device_names:

                name = (
                    f"{name}-{index}"
                )

            device_names.append(
                name
            )

            self.twin.add_device(
                name,
                device_type,
                security_level
            )

            print(
                f"\n✓ Added: {name}"
            )

            print(
                f"  IP: {ip}"
            )

            print(
                f"  Type: {device_type}"
            )

            print(
                f"  Security Level: "
                f"{security_level}/100"
            )

        # -------------------------------------------------
        # Create basic connections
        # -------------------------------------------------

        if len(device_names) > 1:

            print("\n")
            print(
                "🔗 Creating network relationships..."
            )

            for i in range(
                len(device_names) - 1
            ):

                source = device_names[i]

                target = device_names[i + 1]

                self.twin.connect(
                    source,
                    target
                )

                print(
                    f"  {source} ↔ {target}"
                )

        # -------------------------------------------------
        # Display Twin
        # -------------------------------------------------

        print("\n")
        print("=" * 70)

        print(
            "              DIGITAL TWIN READY"
        )

        print("=" * 70)

        self.twin.show_network()

        print("\n")
        print(
            "🧠 ECHO-X now has a virtual representation "
            "of the discovered environment."
        )

        print("=" * 70)

        return self.twin


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)

    print(
        "        ECHO-X AUTOMATIC DIGITAL TWIN"
    )

    print(
        "                    STEP 23"
    )

    print("=" * 70)

    print(
        "\n⚠️ Only scan networks you own or have permission to test."
    )

    network_input = input(
        "\nEnter authorized network (example: 192.168.100.0/24): "
    ).strip()

    if not network_input:

        print(
            "\n❌ No network provided."
        )

    else:

        builder = AutomaticTwinBuilder(
            network_input
        )

        builder.build()