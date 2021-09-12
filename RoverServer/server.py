from flask import Flask, send_file
import argparse
import datetime
import time
from Propulsion import propulsion_algo
from RoboticArm import arm_algo
from ControlModule import control_algo
import cv2
import time
app = Flask(__name__)

camera_spectro = 0
camera_micro = 0

@app.route("/propulsion")
def propulsion():
	prop = propulsion_algo.Propulsion()
	del prop
	return "Started propulsion!"

@app.route("/robotic_arm")
def robotic_arm():
	arm = arm_algo.Robotic_Arm()
	del arm
	return "Started arm!"

@app.route("/science")
def science():
	return "Started Science module!"

@app.route("/control")
def control():
	con = control_algo.Control()
	del con
	return "Started Control module!"

@app.route("/capture_spectro")
def capture_spectro():
	camera = cv2.VideoCapture(camera_spectro)
	time.sleep(2)
	ret, frame = camera.read()
	cv2.imwrite("file.jpg", frame)
	camera.release()
	return send_file('file.jpg', as_attachment = True, attachment_filename = 'file.jpg', mimetype = 'image/jpeg')

@app.route("/capture_micro")
def capture_micro():
	camera = cv2.VideoCapture(camera_micro)
	time.sleep(2)
	ret, frame = camera.read()
	cv2.imwrite("file.jpg", frame)
	camera.release()
	return send_file('file.jpg', as_attachment = True, attachment_filename = 'file.jpg', mimetype = 'image/jpeg')

if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=False, default = "0.0.0.0",
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=False, default = "8001",
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())
	# start the flask app
	app.run(host=args["ip"], port=args["port"],
		threaded=True, use_reloader=False, debug = True)
