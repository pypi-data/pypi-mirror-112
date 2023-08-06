import subprocess
import shutil
import platform


class MissingUsbPlugNotification(Exception):
    pass


class USBPlugNotification:
    def __init__(self, vendorid, productid):
        if not shutil.which("usb-plug-notification"):
            raise MissingUsbPlugNotification(
                f"usb-plug-notification not found, try to install usb-plug-notification-{platform.system().lower()}"
            )

        self.p = subprocess.Popen(
            [
                "usb-plug-notification",
                f"--idvendor={vendorid:X}",
                f"--idproduct={productid:X}",
            ],
            stdout=subprocess.PIPE,
        )

    def get_notification(self):
        return self.p.stdout.readline().decode("utf8")[:-1]
