import requests
import logging
from prometheus_client import Counter, Gauge, generate_latest

log = logging.getLogger("tasmota-exporter")  # use logger from flask app

class Tasmota_instance:
    metric_name = {
        "Total": "tasmota_energy_total_kWh",
        "Yesterday": "tasmota_energy_total_yesterday_kWh",
        "Today": "tasmota_energy_total_today_kWh",
        "Power": "tasmota_active_power_W",
        "ApparentPower": "tasmota_apparent_power_VA",
        "ReactivePower": "tasmota_reactive_power_VAr",
        "Factor": "tasmota_power_factor",
        "Voltage": "tasmota_voltage_V",
        "Current": "tasmota_current_A"
    }
     
    def __init__(self, ip: str) -> None:
        self.url = f"http://{ip}/cm?cmnd=Status+10"
        
    def get_raw_metric_info(self) -> dict:
        log.info("Requesting raw data from Tasmota Smart Plug")
        url = self.url 
        try:
            res = requests.get(url)
            res.raise_for_status()  # raises error if http req was unsuccesful
            raw_json = res.json()
        except requests.exceptions.HTTPError as http_err:
            log.error(f"Error fetching Tasmota info: {http_err}")
    
        raw_metrics = raw_json["StatusSNS"]["ENERGY"]
        log.info("Found:" + str([key for key in raw_metrics]))
        
        return raw_metrics

    def generate_prom_metric(self, raw_metrics: dict) -> dict:
        metric_name = self.metric_name
        prom_metrics = {}
        
        for metric in raw_metrics:
            if metric not in metric_name:
                log.info(f"Metric {metric} not included in name mapping")
                continue
            prom_metrics[metric] = Gauge(metric_name[metric], f"- Tasmota Metric: {metric}")

        return prom_metrics
    
