import requests
import logging

log = logging.getLogger("tasmota-exporter")  # use logger from flask app

def tasmota_request(url: str) -> dict:    
    log.info("Requesting data from Tasmota Smart Plug")
    
    try:
        res = requests.get(url)
        res.raise_for_status()  # raises error if http req was unsuccesful
        content = res.json()
    except requests.exceptions.HTTPError as http_err:
        log.error(f"Error fetching Tasmota info: {http_err}")
 
    return content

def format_prometheus(data: dict, device: str) -> str:
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
    
    metric_type = {
        "Total": "counter",
        "Yesterday": "counter",
        "Today": "counter",
        "Power": "gauge",
        "ApparentPower": "gauge",
        "ReactivePower": "gauge",
        "Factor": "gauge",
        "Voltage": "gauge",
        "Current": "gauge"
    }

    energy = data["StatusSNS"]["ENERGY"]

    log.info("Found:" + str([key for key in energy]))

    formatted_output = ""

    for metric, value in energy.items():
        if metric in metric_name:
            formatted_output += (
                f'# TYPE {metric_name[metric]} {metric_type[metric]}\n'
                f'{metric_name[metric]}{{device="{device}"}} {value}\n'
            )
             
    return formatted_output 

