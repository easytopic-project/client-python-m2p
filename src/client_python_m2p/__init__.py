import pika
import time
import json

class M2P:

    def __init__(self, queue_host, host_port, specs, user_callback):
        self.queue_host = queue_host
        self.host_port = host_port
        self.specs = specs
        self.RECONNECT_TIMEOUT = 3
        self.RECONNECT_MAX = 30
        self.ch = None
        self.user_callback = user_callback


    def __getConnection(self):
        retries = 0
        try:
            print("Connection succeed")
            return pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.queue_host, port=self.host_port, client_properties={"module_specs": self.specs})
            )
        except:
            retries += 1
            if (retries > self.RECONNECT_MAX):
                raise Exception("Failed to connect to server")
            print("Connection failed, attempt " + str(retries) +
                ". Retrying in " + str(self.RECONNECT_TIMEOUT) + " seconds...", flush=True)
            time.sleep(self.RECONNECT_TIMEOUT)
            return self.__getConnection(self.queue_host, self.host_port, self.specs)

    def callback(self, ch, method, properties, body):
        print("Running python test", flush=True)

        msg = json.loads(body)

        msg = self.user_callback(msg)

        ch.basic_publish(exchange="", routing_key=id + "-out", body=json.dumps(msg))

        print("Results sent.", flush=True)

    def connect(self):
        connection = self.__getConnection()
        ch = connection.channel()
        ch.queue_declare(self.specs["id"] + "-in", durable=True)
        ch.queue_declare(self.specs["id"] + "-out", durable=True)
        self.ch = ch

    def run(self):
        self.ch.basic_consume(queue=self.specs["id"] + "-in", on_message_callback=self.callback, auto_ack=True)
        print("Waiting for messages in " + self.specs["id"] + "-in" +
            ". Output will be sended to " + self.specs["id"] + "-out" + ". To exit press CTRL+C", flush=True)
        self.ch.start_consuming()
