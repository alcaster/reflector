import pigpio
from flask import Flask, Response
from flask_restful import Resource, Api, reqparse

# from server.reflector import Reflector
from pins import PINS
from reflector import Reflector

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
        args = self.parser.parse_args()
        val = args.val
        rgb = reflector.append(val)
        pins.set_value_to_all(*rgb)


api.add_resource(Lights, '/lights')

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=8016)
    finally:
        pi.set_PWM_dutycycle(PINS.RED, 0)
        pi.set_PWM_dutycycle(PINS.GREEN, 0)
        pi.set_PWM_dutycycle(PINS.BLUE, 0)
