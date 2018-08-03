import argparse

import pigpio
from flask import Flask
from flask_restful import Resource, Api, reqparse

from pins import PINS
from reflector import Reflector

parser = argparse.ArgumentParser(description='Display "sound" on led diodes connected to raspberry')
parser.add_argument('--mute_factor', type=float, default=0.8, help='Colors are to bright, might need to mute max level')
args = parser.parse_args()

pi = pigpio.pi()
app = Flask(__name__)
api = Api(app)

reflector = Reflector(50)
pins = PINS(pi)


class Lights(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('val', type=int)

    def get(self):
        return {'hello': 'world'}

    def post(self):
        request_args = self.parser.parse_args()
        val = request_args.val
        rgb = reflector.append(val)
        rgb = [int(args.mute_factor * i) for i in rgb]
        pins.set_value_to_all(*rgb)


api.add_resource(Lights, '/lights')

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=8016)
    finally:
        pi.set_PWM_dutycycle(PINS.RED, 0)
        pi.set_PWM_dutycycle(PINS.GREEN, 0)
        pi.set_PWM_dutycycle(PINS.BLUE, 0)
