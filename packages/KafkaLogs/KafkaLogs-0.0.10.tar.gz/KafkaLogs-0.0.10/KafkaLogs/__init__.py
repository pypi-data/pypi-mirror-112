import logging
from datetime import datetime
import json
from decouple import AutoConfig
import requests
import os
import time
from confluent_kafka import Producer

dir_path = os.path.abspath(os.curdir)
extra_tags={}
config = AutoConfig(search_path=dir_path)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# con = logging.StreamHandler()
# con.setLevel(logging.INFO)
# formatter = logging.Formatter('%(message)s')
# con.setFormatter(formatter)
# logger.addHandler(con)

def set_tags(key,value):
        extra_tags[key]=value
def get_tags(key):
        if key in extra_tags:
                return  extra_tags[key]
        return None
def merge_two_dicts(x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z
def _log(msg, application, level,execution_time, user_id, extra_data):
        now =datetime.now().strftime("%y%m%d")
        environment = 'development' if config("ENVIRONMENT") == None or config("ENVIRONMENT")=="" else config("ENVIRONMENT")
        application = 'unknown' if config("APPLICATION") == None or config("APPLICATION")=="" else config("APPLICATION")
        team = config("TEAM")
        app_group = config("APPLICATION_GROUP")

        conf_kafka = {'bootstrap.servers': config("KAFKA_BROKERS"), 'acks': 'all', 'compression.codec': 'gzip'}
        obj_producer = Producer(**conf_kafka)

        original_data={
            "message": msg,
            "level": level,
            "application": application,
            "team" : team,
            "app_group" : app_group,
            "environment": environment,
            "user_id": user_id,
            "execution_time": execution_time,
            "extra_data": extra_data,
            "timestamp": int(time.time())
        }
        data=merge_two_dicts(original_data, extra_tags)
        # print(data)

        if str(config("AGENT")).lower() == "file":
            handler = logging.FileHandler(config('DIR')+now+'.log')
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.warning(json.dumps(data)+"\n")
            logger.removeHandler(handler)

        if str(config("AGENT")).lower() == "kafka":
            try:
                obj_producer.poll(0)
                # obj_producer.produce(config("TOPIC"), json.dumps(data)+"\n")
                obj_producer.produce(config("TOPIC"), json.dumps(data))
                obj_producer.flush()
            except Exception as e:
                print(e)

        return data

def _notify(msg):
        url=config("NOTIFY_URL")
        requests.post(url, data = {"message": json.dumps(msg), "channel": msg['application']})


def warning(msg, application=None,  execution_time=None, user_id=None, extra_data=None):
        _log(msg, application,config('WARNING') ,execution_time, user_id, extra_data)

def info(msg, application=None,  execution_time=None, user_id=None, extra_data=None):
        _log(msg, application,config('INFO') ,execution_time, user_id, extra_data)

def error(msg, application=None,  execution_time=None, user_id=None, extra_data=None):
        _log(msg, application,config('ERROR') ,execution_time, user_id, extra_data)

def critical(msg, application=None,  execution_time=None, user_id=None, extra_data=None):
        _notify(_log(msg, application,config('CRITICAL') ,execution_time, user_id, extra_data))

def metrics(msg, application=None,  execution_time=None, user_id=None, extra_data=None):
        _log(msg, application,config('METRIC') ,execution_time, user_id, extra_data)

