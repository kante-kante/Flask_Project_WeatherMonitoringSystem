#!/usr/bin/env python
# PPD42NS.py
# 2015-11-22
# Public Domain
'''
해당 코드는 라즈베리파이에서 동작시키는 코드입니다.
RPi, smbus 등의 모듈을 라즈베리파이에서 다운로드해야 합니다.
'''

import pigpio
import requests
import smbus
import RPi.GPIO as GPIO
import time


class sensor:
    """
   A class to read a Shinyei PPD42NS Dust Sensor, e.g. as used
   in the Grove dust sensor.
   This code calculates the percentage of low pulse time and
   calibrated concentration in particles per 1/100th of a cubic
   foot at user chosen intervals.
   You need to use a voltage divider to cut the sensor output
   voltage to a Pi safe 3.3V (alternatively use an in-line
   20k resistor to limit the current at your own risk).
   """

    def __init__(self, pi, gpio):
        """
        Instantiate with the Pi and gpio to which the sensor
        is connected.
        """
        self.pi = pi
        self.gpio = gpio
        self._start_tick = None
        self._last_tick = None
        self._low_ticks = 0
        self._high_ticks = 0
        pi.set_mode(gpio, pigpio.INPUT)
        self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

    def read(self):
        """
        Calculates the percentage low pulse time and calibrated
        concentration in particles per 1/100th of a cubic foot
        since the last read.
        For proper calibration readings should be made over
        30 second intervals.
        Returns a tuple of gpio, percentage, and concentration.
        """
        interval = self._low_ticks + self._high_ticks
        if interval > 0:
            ratio = float(self._low_ticks) / float(interval) * 100.0
            conc = 1.1 * pow(ratio, 3) - 3.8 * pow(ratio, 2) + 520 * ratio + 0.62;
        else:
            ratio = 0
            conc = 0.0
        self._start_tick = None
        self._last_tick = None
        self._low_ticks = 0
        self._high_ticks = 0
        return (self.gpio, ratio, conc)

    def _cbf(self, gpio, level, tick):
        if self._start_tick is not None:
            ticks = pigpio.tickDiff(self._last_tick, tick)
            self._last_tick = tick
            if level == 0:  # Falling edge.
                self._high_ticks = self._high_ticks + ticks
            elif level == 1:  # Rising edge.
                self._low_ticks = self._low_ticks + ticks
            else:  # timeout level, not used
                pass
        else:
            self._start_tick = tick
            self._last_tick = tick


pin_to_circuit = 3


def rc_time(pin_to_circuit):
    GPIO.setmode(GPIO.BOARD)
    count = 0

    GPIO.setwarnings(False)
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(1)

    GPIO.setup(pin_to_circuit, GPIO.IN)
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
    return count
    GPIO.cleanup(3)


water_sensor = 12


def rain(water_sensor):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(water_sensor, GPIO.IN)
    if GPIO.input(water_sensor):
        active_time = time.time()
        print("It's sunny!")
        return "It's Sunny"

    else:
        active_time = time.time()
        print("Raining")
        return "Raining"

    GPIO.cleanup(12)


if __name__ == "__main__":
    import time
    import pigpio
    # import send_all
    import Adafruit_DHT

    sensor = Adafruit_DHT.DHT11
    pin = 4
    pi = pigpio.pi()  # Connect to Pi.
    s = sensor(pi, 8)
    # s = send_all.sensor(pi, 8)

    while True:
        time.sleep(3)  # Use 30 for a properly calibrated reading.
        g, r, c = s.read()

        rc = rc_time(pin_to_circuit)
        ra = rain(water_sensor)
        # 스크립트가 인터럽트 될때 catch하고, 올바르게 cleanp
        # try:
        #     # 메인 루프
        #     while True:
        #         print (rc_time(pin_to_circuit))  # 조도 센서의 값 출력
        # except KeyboardInterrupt:
        #     pass
        # finally:
        #    GPIO.cleanup()  # 사용했던 모든 포트에 대해서 정리

        h, t = Adafruit_DHT.read_retry(sensor, pin)
        if h is not None and t is not None:
            print("Temperature = {0:0.1f}*c Humidity = {1:0.1f}%".format(h, t))
        else:
            print('Read error')
        print("gpio={} ratio={:.1f} conc={} pcs per 0.01 cubic foot".
              format(g, r, int(c)))
        URL = 'http://192.168.219.5:5000/api/add'

        data = {
            # "api_key": "e681ec59-2073-4f50-9874-de837899fdbd",
            "api_key": "c4640b4a-1965-4be8-820a-e5f50c472b24",
            "dust_ratio": r,
            "h_ratio": h,
            "t_ratio": t,
            "lux": rc,
            "weather": ra

        }
        print(data)
        headers = {'Content-type': 'application/json'}
        response = requests.post(URL, json=data, headers=headers)
        print('')
        print('code: ', response.status_code)
        print(response.text)

    pi.stop()  # Disconnect from Pit