import requests
import logging

log = logging.getLogger("tasmota-exporter")  # use logger from flask app

def tasmota_request(url: str) -> dict:
    
    log.info("Requesting data from tasmota")
    
    try:
        res = requests.get(url)
        res.raise_for_status()  # raises error if http req was unsuccesful
        content = res.json()
    except requests.exceptions.HTTPError as http_err:
        log.error(f"Error fetching Tasmota info: {http_err}")
    
    
    return content

def format_prometheus(data: dict, device: str) -> str:
    metric_type = {
        "tasmota_energy_total_kWh": "counter",
        "tasmota_energy_total_yesterday_kWh": "counter",
        "tasmota_energy_total_today_kWh": "counter",
        "tasmota_active_power_W": "gauge",
        "tasmota_apparent_power_VA": "gauge",
        "tasmota_reactive_power_VAr": "gauge",
        "tasmota_power_factor": "gauge",
        "tasmota_voltage_V": "gauge",
        "tasmota_current_A": "gauge"
    }