from flask_restful import Resource, reqparse


class RGB(Resource):
    def __init__(self, pins):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('r', type=int)
        self.parser.add_argument('g', type=int)
        self.parser.add_argument('b', type=int)
        self.pins = pins

    def get(self):
        return {'hello': 'world'}

    def post(self):
        request_args = self.parser.parse_args()
        r = request_args.r
        g = request_args.g
        b = request_args.b
        self.pins.set_value_to_all(r, g, b)


class Audio(Resource):
    def __init__(self, reflector, args, pins):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('val', type=int)
        self.reflector = reflector
        self.args = args
        self.pins = pins

    def post(self):
        request_args = self.parser.parse_args()
        val = request_args.val
        rgb = self.reflector.append(val)
        rgb = [int(self.args.mute_factor * i) for i in rgb]
        self.pins.set_value_to_all(*rgb)
