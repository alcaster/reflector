# Reflector
This repository consists application for client and server of reflector.
Reflector is application which make visualization on rgb led strip.
I can:
- listen for current output audio and display it.
- React to triggers for [ifttt](http://ifttt.com). F.ex on alarm clock turn on light.
- Set colors via rest api.

Video:
- [ ] To record

### Prerequsuitories
- \>Python 3.6
- Raspberry pi - any version(I use zero)
- PulseAudio and parec

## Client/
This application in one thread listens for audio output and every set period sends via queue to another thread. In separate thread is calculated [rms](https://en.wikipedia.org/wiki/Audio_power) over this period of time and send to server application via REST endpoint.

## Server/
This application is flask webserver which enables controling led strip via REST endpoints.

### Raspberry scheme
![Scheme](https://cdn-images-1.medium.com/max/2000/1*r30X-Br2KrpMM11rT-B4mQ.png)
