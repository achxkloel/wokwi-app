import sys
import time
import network # for WiFi connection
import urequests # for HTTP requests
from machine import Pin
from dht import DHT22

# Button
button = Pin(26, Pin.IN, Pin.PULL_UP)

# LED
led = Pin(18, Pin.OUT)

# Temperature and humidity sensor
dht22 = DHT22(Pin(23))

# WiFi credentials
wifi_ssid = "Wokwi-GUEST"
wifi_password = ""

# Connection timeout limit (in seconds)
timeout_limit = 10

# HTTP
server_url = "https://5420cb00-2496-4be0-ac62-279446417ea1.mock.pstmn.io"
http_headers = { "Content-Typ": "application/json" }

# Connect to WiFi
def connect_wifi ():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(wifi_ssid, wifi_password)

    if not wifi.isconnected():
        print("Waiting for connection...")
        timeout = 0
        while (not wifi.isconnected() and timeout < timeout_limit):
            timeout = timeout + 1
            time.sleep(1) 

    if wifi.isconnected():
        print("Connected to", wifi_ssid)
    else:
        print("Failed to connect to", wifi_ssid)
        sys.exit()

# Send information about LED state
def send_led_state (state):
    try:
        url = server_url + "/led_state"
        print("Sending LED state...")
        print("Value =", state)
        data = { "led_state": state }
        response = urequests.post(url, json = data, headers = http_headers)
        response.close()
    except:
        print("Failed to send data to", url)

# Send information from DHT22 sensor
def send_dht22 (temperature, humidity):
    try:
        url = server_url + "/dht22"
        print("Sending DHT22 data...")
        print("Temperature =", temperature)
        print("Humidity =", humidity)
        data = { "temperature": temperature, "humidity": humidity }
        response = urequests.post(url, json = data, headers = http_headers)
        response.close()
    except:
        print("Failed to send data to", url)

# Connecting to WiFi
connect_wifi()

# By default button is not pressed (value = 1)
last_btn_value = 1

# Default dht22 values
last_humidity = -1
last_temperature = -1

# Main loop
while True:
    # curr_btn_value = button.value()

    # if curr_btn_value == 0:
    #     led.value(1)
    # else:
    #     led.value(0)

    # if last_btn_value != curr_btn_value:
    #     last_btn_value = curr_btn_value
    #     send_led_state(led.value() == 1)

    dht22.measure()
    curr_temperature = dht22.temperature()
    curr_humidity = dht22.humidity()

    if last_temperature != curr_temperature or last_humidity != curr_humidity:
        # Asserts for Wokwi-CI
        assert 0 <= curr_humidity <= 100, "Humidity out of range"
        assert -40 <= curr_temperature <= 80, "Temperature out of range"
        print("DHT22 values are in valid range")

        last_temperature = curr_temperature
        last_humidity = curr_humidity
        send_dht22(curr_temperature, curr_humidity)

    time.sleep(2)
