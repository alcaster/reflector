import argparse
import pigpio
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

from endpoints import RGB, Audio
from pins import PINS
from reflector import Reflector

load_dotenv()

parser = argparse.ArgumentParser(description='Display "sound" on led diodes connected to raspberry')
parser.add_argument('--mute_factor', type=float, default=0.8, help='Colors are to bright, might need to mute max level')
args = parser.parse_args()

reflector = Reflector(50)
pi = pigpio.pi()
pins = PINS(pi)
app = Flask(__name__)

api = Api(app)
api.add_resource(RGB, '/rgb', resource_class_kwargs={'pins': pins})
api.add_resource(Audio, '/audio', resource_class_kwargs={'reflector': reflector, "args": args, "pins": pins})

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=8016)
    finally:
        pi.set_PWM_dutycycle(PINS.RED, 0)
        pi.set_PWM_dutycycle(PINS.GREEN, 0)
        pi.set_PWM_dutycycle(PINS.BLUE, 0)
