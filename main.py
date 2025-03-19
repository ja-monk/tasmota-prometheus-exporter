#!/usr/bin/env python

from flask import Flask, Response
import logging
from logging.handlers import RotatingFileHandler
import signal
import sys

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

import tasmota    # import after setting up logger as this uses same logger

@app.route("/metrics")
def tasmota_to_prometheus() -> Response:
    energy_data = tas.get_raw_metric_info()

    for metric, value in energy_data.items():
        if metric in prom_metrics:
            prom_metrics[metric].set(value)

    result = []
    for metric in prom_metrics:
        result.append(tasmota.generate_latest(prom_metrics[metric]))

    return Response(result, mimetype="text/plain")

def signal_handler(signum, frame):
    sig_name = signal.Signals(signum).name
    message = f"Signal caught: {sig_name} ({signum})"
    log.info(message)
    log.info("Exiting")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    log.info("Starting Tasmota Prometheus Exporter")

    # global object as this is used in each request to metrics endpoint
    global tas 
    tas = tasmota.Tasmota_instance(env.tasmota_ip)
    
    raw_metrics = tas.get_raw_metric_info()
    
    # globally defined metrics which are then set to values on each request to metrics endpoint
    global prom_metrics
    prom_metrics = tas.generate_prom_metric(raw_metrics)

    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()