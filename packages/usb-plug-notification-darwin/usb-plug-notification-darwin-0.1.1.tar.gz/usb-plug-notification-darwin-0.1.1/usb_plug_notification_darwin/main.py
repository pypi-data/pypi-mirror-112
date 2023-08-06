import objc
import CoreFoundation
import PyObjCTools.AppHelper
import pkgutil
import click

objc.parseBridgeSupport(
    pkgutil.get_data("usb_plug_notification_darwin", "IOKit.bridgesupport"),
    globals(),
    objc.pathForFramework("/System/Library/Frameworks/IOKit.framework"),
)


def iterate(it):
    result = []
    while 1:
        n = IOIteratorNext(it)
        if not n:
            break
        result.append(n)
    return result


kIONotifications = (
    kIOFirstPublishNotification,
    kIOTerminatedNotification,
)


def _main(idVendor, idProduct, callback):
    PyObjCTools.AppHelper.installMachInterrupt()

    port = IONotificationPortCreate(kIOMasterPortDefault)

    @objc.callbackFor(IOServiceAddMatchingNotification)
    def _callback(refcon, iterator):
        iterate(iterator)
        if kIONotifications[refcon] == kIOFirstPublishNotification:
            callback("plug")
        elif kIONotifications[refcon] == kIOTerminatedNotification:
            callback("unplug")

    for i, v in enumerate(kIONotifications):
        matching = IOServiceMatching(kIOUSBDeviceClassName)
        matching["idVendor"] = idVendor
        matching["idProduct"] = idProduct

        _, it = IOServiceAddMatchingNotification(port, v, matching, _callback, i, None)
        iterate(it)

    CoreFoundation.CFRunLoopAddSource(
        CoreFoundation.CFRunLoopGetCurrent(),
        IONotificationPortGetRunLoopSource(port),
        CoreFoundation.kCFRunLoopDefaultMode,
    )
    CoreFoundation.CFRunLoopRun()


@click.command()
@click.option("--idvendor", required=True, help="Hexadecimal idVendor")
@click.option("--idproduct", required=True, help="Hexadecimal idProduct")
def main(idvendor, idproduct):
    def callback(action):
        print(action, flush=True)

    _main(int(idvendor, 16), int(idproduct, 16), callback)
