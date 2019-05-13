import datetime
import os

from flask import request
from flask_restful import Resource, reqparse


class RGB(Resource):
    def __init__(self, pins):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('r', type=int)
        self.parser.add_argument('g', type=int)
        self.parser.add_argument('b', type=int)
        self.parser.add_argument('token', type=str)
        self.pins = pins

    def post(self):
        request_args = self.parser.parse_args()

        if not request.remote_addr.startswith('192.168'):
            if os.getenv("TOKEN") != request_args.token:
                return 400

        r = request_args.r
        g = request_args.g
        b = request_args.b
        self.pins.set_value_to_all(r, g, b)


class Audio(Resource):
    def __init__(self, reflector, args, pins):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('val', type=int)
        self.parser.add_argument('token', type=str)

        self.reflector = reflector
        self.args = args
        self.pins = pins

    def post(self):
        request_args = self.parser.parse_args()
        if os.getenv("TOKEN") != request_args.token:
            return 400

        val = request_args.val
        rgb = self.reflector.append(val)
        rgb = [int(self.args.mute_factor * i) for i in rgb]
        self.pins.set_value_to_all(*rgb)


class Sun(Resource):
    """
    On execution iterates from (0,0,0) to (255,255,0)
    """

    def __init__(self, pins, scheduler):
        self.pins = pins

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('time', type=int, help="Time in ms")
        self.parser.add_argument('off', type=int, help="Time to turn off lights in ms")
        self.parser.add_argument('token', type=str)
        self.scheduler = scheduler
        self.default_time_off = 600_000  # 10min

    def post(self):
        request_args = self.parser.parse_args()
        if os.getenv("TOKEN") != request_args.token:
            return 400
        time = request_args.time
        interval = time / 255
        for i in range(255):
            self.scheduler.add_job(func=self.pins.set_value_to_all, trigger="date",
                                   run_date=datetime.datetime.now() + datetime.timedelta(milliseconds=i * interval),
                                   args=(i, i, 0))

        turn_off = request_args.off if request_args.off is not None else self.default_time_off
        self.scheduler.add_job(func=self.pins.set_value_to_all, trigger="date",
                               run_date=datetime.datetime.now() + datetime.timedelta(milliseconds=turn_off),
                               args=(0, 0, 0))
