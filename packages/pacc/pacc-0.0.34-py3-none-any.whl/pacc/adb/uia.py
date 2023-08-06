from uiautomator import Device


class UIAutomator:
    def __init__(self, serial):
        """
        :param serial: device ID or device IPv4 address
        """
        self.device = Device(serial)

    def click(self, resourceID):
        """
        :param resourceID:
        :return:
        """
        if self.device(resourceId=resourceID).exists:
            self.device(resourceId=resourceID).click()
            return True
        return False

