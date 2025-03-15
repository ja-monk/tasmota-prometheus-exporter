from flask import Flask, request
import logging
from logging.handlers import RotatingFileHandler
import env

app = Flask("tasmota-exporter")

# Logging config
log_handler = RotatingFileHandler("logs/tasmota_exporter.log", maxBytes=100000, backupCount=2)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)
log = app.logger

import tasmota_query    # import after setting up logger as this uses same logger

@app.route("/metrics")
def tasmota_to_prometheus():
    url = f"http://{env.tasmota_ip}/cm?cmnd=Status+10"
    content = tasmota_query.tasmota_request(url)
    
    print(content)

    return content

if __name__ == "__main__":
    log.info("Starting Tasmota Prometheus Exporter")
    app.run(host="0.0.0.0", port=5000, debug=True)