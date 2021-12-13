import unittest
import random
import os
import cv2
import numpy as np
from src.win32_bridge.capture import CaptureWindow
import logging
import time


class TestCreatingWindows(unittest.TestCase):

    def call_cmd(self, name):
        os.chdir("win32")
        os.system(name)
        os.chdir("..")

    def test_capture_nonexisting_window(self):
        with self.assertRaises(TimeoutError):
            CaptureWindow(str(random.getrandbits(128)), 0.0)

    def test_capture_powershell(self, fps_timeout=1.0):
        self.call_cmd("reboot_powershell.bat")
        cap = CaptureWindow("Windows PowerShell", 30.0)
        img = cap.get_image()
        img = cv2.cvtColor(cap.get_image(), cv2.COLOR_BGRA2GRAY)
        self.assertTrue(len(img.shape) == 2 and img.shape[0] > 0 and img.shape[1] > 0, f"Image size wrong {img.shape}")
        self.assertTrue(np.any(img > 0), "Image is empty")
        time_start = time.perf_counter()
        fps_counter = 0
        while time.perf_counter() < time_start + fps_timeout:
            try:
                img = cap.get_image()
            except Exception as e:
                logging.warning(f"frame dropped, reason: {str(e)}")
            else:
                fps_counter += 1
        logging.warning(f"fps: {1.0 * fps_counter / fps_timeout}")
        self.assertTrue(fps_counter > 0, "Did not catch any image")
        self.call_cmd("kill_powershell.bat")


if __name__ == '__main__':
    unittest.main()
