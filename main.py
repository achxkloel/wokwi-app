import sys
import time
import network # for WiFi connection
import urequests # for HTTP requests
from machine import Pin, I2C
from dht import DHT22
import ssd1306
import uasyncio
import ntptime

ntptime.host = "tik.cesnet.cz"
cet_offset = 3600

# Temperature and humidity sensor
dht22 = DHT22(Pin(23))

# OLED display
i2c = I2C(1, scl=Pin(22), sda=Pin(21))

# WiFi credentials
wifi_ssid = "Wokwi-GUEST"
wifi_password = ""

# Connection timeout limit (in seconds)
timeout_limit = 10

# HTTP
server_url = "https://5420cb00-2496-4be0-ac62-279446417ea1.mock.pstmn.io"
http_headers = { "Content-Typ": "application/json" }

wifi = network.WLAN(network.STA_IF)

# Connect to WiFi
async def connect_wifi ():
    wifi.active(True)

    if wifi.isconnected():
        return

    wifi.connect(wifi_ssid, wifi_password)
    print("Trying to connect to Wifi...")

    while not wifi.isconnected():
        await uasyncio.sleep_ms(200)

    print("Connected to", wifi_ssid)

# Send information from DHT22 sensor
async def send_dht22 (temperature, humidity):
    if not wifi.isconnected():
        return

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

def get_localtime ():
    ntptime.settime()
    return time.localtime(time.time() + cet_offset)

async def ssd1306_display ():
    # Init display
    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    t = None

    while True:
        is_connected = wifi.isconnected()

        if is_connected:
            t = get_localtime()

        oled.fill(0)
        oled.text('WiFi: ' + ("On" if is_connected else "Off"), 0, 0)
        oled.text('Date: ' + ("{:02d}.{:02d}.{}".format(t[2], t[1], t[0]) if is_connected else ""), 0, 10)
        oled.text('Time: ' + ("{:02d}:{:02d}".format(t[3], t[4]) if is_connected else ""), 0, 20)
        oled.text('Temp: ' + str(dht22.temperature()) + " C", 0, 30)
        oled.text('Humidity: ' + str(dht22.humidity()) + "%", 0, 40)
        oled.show()
        await uasyncio.sleep_ms(200)

async def listen_dht22 ():
    while True:
        dht22.measure()
        await uasyncio.sleep_ms(200)

async def send ():
    last_humidity = None
    last_temperature = None

    while True:
        curr_temperature = dht22.temperature()
        curr_humidity = dht22.humidity()

        if last_temperature != curr_temperature or last_humidity != curr_humidity:
            last_temperature = curr_temperature
            last_humidity = curr_humidity
            await send_dht22(curr_temperature, curr_humidity)

        await uasyncio.sleep(10)

async def main ():
    wifi_task = uasyncio.create_task(connect_wifi())
    ssd1306_task = uasyncio.create_task(ssd1306_display())
    dht22_task = uasyncio.create_task(listen_dht22())
    send_task = uasyncio.create_task(send())

    await wifi_task
    await ssd1306_task
    await dht22_task
    await send_task

uasyncio.run(main())