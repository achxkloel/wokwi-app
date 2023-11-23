# wokwi-app

Application on Wokwi.com that simulates an ESP32 which:
- Reads DHT22 sensor data
- Sends it to a remote server
- Shows current time, WiFi status and DHT22 sensor data on SSD1306 display

## Run

1. Create project on Wokwi.com (MicroPython on ESP32) and copy the files
2. Or open an existing public link (https://wokwi.com/projects/381887099401512961)
3. Start simulation

## Client

Wokwi client application using DHT22 sensor, which measures temperature and humidity. These two values are checked every 10 seconds and if one of them changes, the data will be sent to the server.

Also all information shown on display.

Each function run asynchronous. HTTP requests via `urequests` library don't support async/await functionality, so after every request all of the remaining tasks are waiting for request to be completed.

## Mock server

Server created using Postman. All endpoints are used only for testing purposes and do not store received data.

**Server URL** - https://5420cb00-2496-4be0-ac62-279446417ea1.mock.pstmn.io

### API endpoints
- `POST /dht22` - receives DHT22 sensor information 
- `GET /dht22` - returns DHT22 sensor information

### JSON types

DHT22 sensor information

```JSON
{
    "temperature": "number",
    "humidity": "number"
}
```

## Wokwi-CI pipeline

Wokwi CLI is not working with this project. See error below.

```
Error: Error 4: Failed to start simulation: TypeError: Failed to parse URL from /assets/littlefs.wasm
    at APIClient.processResponse (C:\snapshot\dist\cli.cjs:13668:16)
    at APIClient.processMessage (C:\snapshot\dist\cli.cjs:13650:14)
    at _WebSocket.<anonymous> (C:\snapshot\dist\cli.cjs:13504:16)
    at callListener (C:\snapshot\dist\cli.cjs:9280:18)
    at _WebSocket.onMessage (C:\snapshot\dist\cli.cjs:9215:13)
    at _WebSocket.emit (node:events:537:28)
    at Receiver2.receiverOnMessage (C:\snapshot\dist\cli.cjs:10272:24)
    at Receiver2.emit (node:events:537:28)
    at Receiver2.dataMessage (C:\snapshot\dist\cli.cjs:8578:18)
    at Receiver2.getData (C:\snapshot\dist\cli.cjs:8507:21)
```

Probably the issue with the MicroPython within Wokwi CLI. \
Issue related to - https://github.com/wokwi/wokwi-features/issues/652
Possible solution - https://github.com/Josverl/wokwi_esp32_micropython/tree/fix/devcontainer or re-implement using Rust or Arduino :)

1. Install `wokwi-cli`
2. Create `WOKWI_CLI_TOKEN` and set it to environment variable
3. Run `wokwi-cli .`

It is possible to use wokwi-cli with Github Actions.
But it doesn't work due to the same error.