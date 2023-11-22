# wokwi-app

Application on Wokwi.com that simulates an ESP32 reading sensor data and sending it to a remote server.

## Run

1. Create project on Wokwi.com (MicroPython on ESP32) and copy the files
2. Or open an existing public link (https://wokwi.com/projects/381887099401512961)
3. Start simulation

## Client

Wokwi client application using DHT22 sensor, which measures temperature and humidity. These two values are checked every two seconds and if one of them changes, the data is sent to the server.

Originally, the client had another option. There is a button connected to the circuit. When the user press and hold it, the diode lights up and the server receives a message about this diode.

## Mock server

Server created using Postman. All endpoints are used only for testing purposes and do not store received data.

**Server URL** - https://5420cb00-2496-4be0-ac62-279446417ea1.mock.pstmn.io

### API endpoints
- `POST /dht22` - receives DHT22 sensor information 
- `GET /dht22` - returns DHT22 sensor information
- `POST /led_state` - receives LED state
- `GET /led_state` - returns LED state

### JSON types

DHT22 sensor information

```JSON
{
    "temperature": "number",
    "humidity": "number"
}
```

LED state information

```JSON
{
    "led_state": "number"
}
```

## Wokwi-CI pipeline

1. Install `wokwi-cli`
2. Create `WOKWI_CLI_TOKEN` and set it to environment variable
3. Run `wokwi-cli .`

Is is possible to use wokwi-cli with Github Actions.
CI pipeline is not completely working now because file `wokwi.toml` does not have all required definitions (`firmware`, `elf`).