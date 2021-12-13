import win32gui
import win32ui
import win32con
import time
import numpy as np
import os
import logging


class CaptureWindow:
    def __init__(self, window_name, timeout=60.0, retry_timeout=1.0):
        self._hwnd = 0
        self.capture_prepare(window_name)
        timer_start = time.perf_counter()
        while self.capture_prepare() < 0:
            time.sleep(retry_timeout)
            if time.perf_counter() > timer_start + timeout:
                raise TimeoutError

    def __del__(self):
        if self._hwnd != 0:
            self.capture_close()

    def capture_prepare(self, windowname=None):
        if windowname is not None:
            self.windowname = windowname
        self._hwnd = win32gui.FindWindow(None, self.windowname)
        if self._hwnd == 0:
            logging.debug(f"Window \"{self.windowname}\" does not exist")
            return -1
        self._wDC = win32gui.GetWindowDC(self._hwnd)
        self._dcObj = win32ui.CreateDCFromHandle(self._wDC)
        self._cDC = self._dcObj.CreateCompatibleDC()
        self._dataBitMap = win32ui.CreateBitmap()
        return 0

    def get_image(self):
        self.image_dimensions = win32gui.GetWindowRect(self._hwnd)
        self._dataBitMap.CreateCompatibleBitmap(self._dcObj, self.image_dimensions[2] - self.image_dimensions[0],
                                                self.image_dimensions[3] - self.image_dimensions[1])
        self._cDC.SelectObject(self._dataBitMap)
        self._cDC.BitBlt((0, 0), (
            self.image_dimensions[2] - self.image_dimensions[0],
            self.image_dimensions[3] - self.image_dimensions[1]), self._dcObj, (0, 0), win32con.SRCCOPY)
        signedIntsArray = self._dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.image_dimensions[3] - self.image_dimensions[1],
                     self.image_dimensions[2] - self.image_dimensions[0], 4)
        return img

    def capture_close(self):
        try:
            self._dcObj.DeleteDC()
        except win32ui.error:
            pass
        try:
            self._cDC.DeleteDC()
        except win32ui.error:
            pass
        win32gui.ReleaseDC(self._hwnd, self._wDC)
        win32gui.DeleteObject(self._dataBitMap.GetHandle())
