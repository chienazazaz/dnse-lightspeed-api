import json
import random
import time
import os
import logging

from requests import request
from paho.mqtt import client as mqtt_client
from paho.mqtt.client import MQTTv5
from paho.mqtt.subscribeoptions import SubscribeOptions

class ClientConfig:
    BROKER = "datafeed-lts.dnse.com.vn"
    PORT = 443
    TOPICS = (
        "plaintext/quotes/derivative/OHLC/1/VN30F1M",
        "plaintext/quotes/stock/tick/+",
    )


    USERNAME = os.getenv("DNSE_USERNAME", "")
    USER_ID = os.getenv("DNSE_ID", "")
    CLIENT_ID = f"dnse-price-json-mqtt-ws-sub-{USER_ID}-{random.randint(0, 1000)}"
    FIRST_RECONNECT_DELAY = 1
    RECONNECT_RATE = 2
    MAX_RECONNECT_COUNT = 12
    MAX_RECONNECT_DELAY = 60

class DNSEClient():
    def __init__(self):
        pass

    def get_token(self):
        res = request(
            method="POST",
            url = "https://services.entrade.com.vn/dnse-user-service/api/auth",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={
                "username": ClientConfig.USERNAME,
                "password": os.getenv("DNSE_PASSWORD", ""),
            },
        ).json()
        print(res,123123123)

        return res.get("token", None)

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc,properties):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(
                callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
                client_id=ClientConfig.CLIENT_ID,
                protocol=MQTTv5,
                transport="websockets",
                )
        

        client.on_connect = on_connect

        client.tls_set_context()
        client.ws_set_options(path="/wss")

        client.username_pw_set(ClientConfig.USER_ID, self.get_token())

        client.connect(ClientConfig.BROKER, ClientConfig.PORT, keepalive=120)

        return client

    def on_disconnect(self, userdata, flags, rc, properties):
        logging.info("Disconnected with result code: %s", rc)
        reconnect_count, reconnect_delay = 0, ClientConfig.FIRST_RECONNECT_DELAY
        while reconnect_count < ClientConfig.MAX_RECONNECT_COUNT:
            logging.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)
            try:
                self.client.reconnect()
                logging.info("Reconnected successfully!")
                return
            except Exception as err:
                logging.error("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= ClientConfig.RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, ClientConfig.MAX_RECONNECT_DELAY)
            reconnect_count += 1
        logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)


    def subscribe(self,client):

        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        topic_tuple = [(topic, SubscribeOptions(qos=2)) for topic in ClientConfig.TOPICS]
        client.subscribe(topic_tuple)
        client.on_message = on_message



    def on_message( client, userdata, msg):
        logging.debug(f"Topic: {msg.topic}, msg: {msg.payload}")
        payload = json.JSONDecoder().decode(msg.payload.decode())

        logging.debug(f"payload: {payload}")
        logging.debug(f'symbol: {payload["symbol"]}')


    def run(self):
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s: %(message)s", level=logging.DEBUG
        )
        self.client = self.connect_mqtt()
        self.client.on_disconnect = self.on_disconnect
        self.subscribe(self.client)
        self.client.loop_forever()