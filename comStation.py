import threading
import time
from collections import deque
import typing as tp

from drivers.sds011 import SDS011
from config import CONFIG


def _read_data_thread(sensor: SDS011, q: deque) -> None:
    while True:
        meas = sensor.query()
        timestamp = int(time.time())
        q.append((meas, timestamp))


class COMStation:
    """
    Reads data from a serial port
    """

    def __init__(self) -> None:
        self.sensor = SDS011(CONFIG["port"])
        self.q = deque(maxlen=1)
        threading.Thread(target=_read_data_thread, args=(self.sensor, self.q)).start()

    def get_data(self) -> tp.Tuple[float, float]:
        threading.Timer(self.get_data, 60)
        if self.q:
            values = self.q[0]
            pm = values[0]
            pm25 = pm[0]
            pm10 = pm[1]
        return pm25, pm10

if __name__ == "__main__":
    s = COMStation()
    threading.Thread(s.get_data).start()