import pyudev
import gi.repository.Gio
import click
import time


@click.command()
@click.option("--idvendor", required=True, help="Hexadecimal idVendor")
@click.option("--idproduct", required=True, help="Hexadecimal idProduct")
def main(idvendor, idproduct):
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by("usb")
    gsettings = gi.repository.Gio.Settings.new("org.gnome.desktop.session")
    last_t = 0
    idvendor = int(idvendor, 16)
    idproduct = int(idproduct, 16)
    for device in iter(monitor.poll, None):
        matched_idVendor, matched_idProduct, matched_bcdDevice = device.get(
            "PRODUCT"
        ).split("/")
        if idvendor == int(matched_idVendor, 16) and idproduct == int(
            matched_idProduct, 16
        ):
            if last_t > (time.time() - 0.1):
                continue
            if device.action == "add":
                print("plug", flush=True)
                last_t = time.time()
            elif device.action == "remove":
                print("unplug", flush=True)
                last_t = time.time()
