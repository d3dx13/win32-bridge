import unittest
import random
import os
import cv2
import numpy as np
from src.win32_bridge.capture import CaptureWindow
import logging


class TestCreatingWindows(unittest.TestCase):

    def test_capture_nonexisting_window(self):
        with self.assertRaises(TimeoutError):
            CaptureWindow(str(random.getrandbits(128)), 0.0)

    def test_capture_powershell(self):
        os.chdir("win32")
        os.system("reboot_powershell.bat")
        cap = CaptureWindow("Windows PowerShell", 30.0)
        img = cap.get_image()
        img = cv2.cvtColor(cap.get_image(), cv2.COLOR_BGRA2GRAY)
        os.system("kill_powershell.bat")
        os.chdir("..")
        self.assertTrue(np.any(img > 0))


if __name__ == '__main__':
    unittest.main()
