#!/usr/bin/python3
from __future__ import print_function
import cv2 as cv
import argparse
import configparser
import time
import numpy as np
import curses
import importlib
import os

stdscr = curses.initscr()
stdscr.clear()
stdscr.refresh()
curses.start_color()


def main_screen():
	begin_x = 0; begin_y = 0
	height = 50; width = 40
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)#Title color
	curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_RED)#Message color            
	curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)# ValueColor 1 Yellow
	curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)# ValueColor 2 Red
	curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)# ValueColor 3  Green
	curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)# ValueColor 4  blue
	win = curses.newwin(height, width, begin_x, begin_y)
	win.attron(curses.color_pair(1))
	stdscr.addstr(0,0,"==== Detector v 0.2 PRAYSstudioSoft (C) 2018 ====\n",curses.color_pair(1))
	stdscr.addstr(1,0,"Cascade    :\n")
	stdscr.addstr(2,0,"Description:\n")
	stdscr.addstr(3,0,"Shapecheck :\n")	
	stdscr.addstr(4,0,"Shape      :\n")
	stdscr.addstr(5,0,"Math       :\n")	
	stdscr.addstr(6,0,"==== Press CTRL+C for Exit ======================\n",curses.color_pair(5))	
	stdscr.addstr(7,0,"Message    :\n",curses.A_REVERSE)
	stdscr.refresh()
	

def toLog(msg):
	stdscr.addstr(7,12," "+msg+"\n",curses.color_pair(2))
	stdscr.refresh()
	
def toInfo(s1,s2,s3,s4,s5):	
		stdscr.addstr(1,12,s1+"\n",curses.color_pair(3))
		stdscr.addstr(2,12,s2+"\n",curses.color_pair(6))
		if s3 == 'False':
			stdscr.addstr(3,12,s3+"\n",curses.color_pair(4))
		else:
			stdscr.addstr(3,12,s3+"\n",curses.color_pair(5))
			
		stdscr.addstr(4,12,s4+"\n")
		stdscr.addstr(5,12,s5+"\n",curses.color_pair(3))		
		stdscr.refresh()

main_screen()

# Loading configuration file
cfg = configparser.RawConfigParser()

if not cfg.read('first.conf'):
	toLog("Cannot open the configuration file! Exit!")
	exit()

toLog("load config file...")

class ROIframe:
	x = None
	y = None
	r = None
	frame = None
	description = None
	
class OBJincascade:
	# create array variables for the programm
	action = None
	shapecheck = False
	shape = None
	cascade = None
	description = None
	color = None 
	depth = 1
	scale = None
	neighbors= None
	minsize_w= None
	minsize_h= None
	maxsize_w= None
	maxsize_h= None
	include= None
	enabled= False
	
simpleobj = []

# get values from file
_camera = cfg.getint("general","camera")
_cntcsd = cfg.get("general","cascades")
_showis = cfg.getboolean("general","showwindow")
_framew = cfg.getint("general","framew")
_frameh = cfg.getint("general","frameh")

_brightness = cfg.get("general","brightness")
_contrast = cfg.get("general","contrast")
_saturation = cfg.get("general","saturation")
_gain =cfg.get("general","gain")

#color for object border
_color_green = (0,255,1)
_color_white = (255,255,255)
_color_black = (0,0,0)
_color_orange= (0,165,255)
_color_blue  = (255,0,0)

#======================================================================#
# the function loading cascades files and create cascade array 		   #
#======================================================================#		
def loadCascades():
	tempCascades = []
	for i in range(0,int(_cntcsd)):
		tempCascades.append(cv.CascadeClassifier())
		
		#cascades_temp.append(cv.CascadeClassifier())
		if not tempCascades[i].load(cfg.get("cascade"+str(i),"file")):
			toLog("error in loadingthe cascade file: "+cfg.get("cascade"+str(i),"file")+" ignored")
		else:
			if not cfg.has_option("cascade"+str(i),"enabled"):
				_enabled = False
			else:
				_enabled = cfg.getboolean("cascade"+str(i),"enabled")
				
				if _enabled:
								
					if not cfg.has_option("cascade"+str(i),"description"):
						_description = "This is simple cascade"
					else:
						_description = cfg.get("cascade"+str(i),"description")
					if not cfg.has_option("cascade"+str(i),"shapecheck"):
						_shapecheck=False
					else:
						_shapecheck=cfg.getboolean("cascade"+str(i),"shapecheck")
					if not cfg.has_option("cascade"+str(i),"shape"):
						_shape = None
					else:
						_shape = cfg.get("cascade"+str(i),"shape")
					if not cfg.has_option("cascade"+str(i),"action"):
						_action = None
					else:
						_action = cfg.get("cascade"+str(i),"action")				
					if not cfg.has_option("cascade"+str(i),"color"):
						_color = _color_white
					else:
						if cfg.get("cascade"+str(i),"color") == "green":_color = _color_green
						if cfg.get("cascade"+str(i),"color") == "white":_color = _color_white
						if cfg.get("cascade"+str(i),"color") == "black":_color = _color_black
						if cfg.get("cascade"+str(i),"color") == "orange":_color = _color_orange
						if cfg.get("cascade"+str(i),"color") == "blue":	_color = _color_blue
					if not cfg.has_option("cascade"+str(i),"depth"):
						_depth = 1
					else:
						_depth = cfg.getint("cascade"+str(i),"depth")				
					if not cfg.has_option("cascade"+str(i),"scale"):
						_scale = 1
					else:
						_scale = cfg.getfloat("cascade"+str(i),"scale")				
					if not cfg.has_option("cascade"+str(i),"neighbors"):
						_neighbors = 1
					else:
						_neighbors = cfg.getint("cascade"+str(i),"neighbors")				
					if not cfg.has_option("cascade"+str(i),"minsize_w"):
						_minsize_w = 20
					else:
						_minsize_w = cfg.getint("cascade"+str(i),"minsize_w")				
					if not cfg.has_option("cascade"+str(i),"minsize_h"):
						_minsize_h = 20
					else:
						_minsize_h = cfg.getint("cascade"+str(i),"minsize_h")				
					if not cfg.has_option("cascade"+str(i),"maxsize_w"):
						_maxsize_w = 20
					else:
						_maxsize_w = cfg.getint("cascade"+str(i),"maxsize_w")				
					if not cfg.has_option("cascade"+str(i),"maxsize_h"):
						_maxsize_h = 20
					else:
						_maxsize_h = cfg.getint("cascade"+str(i),"maxsize_h")				
					if not cfg.has_option("cascade"+str(i),"include"):
						_include = None
					else:
						_file = os.path.exists(cfg.get("cascade"+str(i),"include")+".py")
					if _file:
						_include = cfg.get("cascade"+str(i),"include")				
					else:
						_include = None
					simpleobj.append({
						'cascade': cv.CascadeClassifier(cfg.get("cascade"+str(i),"file")),
						'shapecheck': _shapecheck,
						'shape': _shape,
						'action': _action,
						'description': _description,
						'color': _color,
						'depth': _depth,
						'scale': _scale,
						'neighbors': _neighbors,
						'minsize_w': _minsize_w,
						'minsize_h': _minsize_h,
						'maxsize_w': _minsize_w,
						'maxsize_h': _minsize_h,
						'include'  : _include,
						'enabled'  : _enabled})			
					# clear variables in memory
	del tempCascades
	del _description
	del _action
	del _shapecheck
	del _shape
#======================================================================#			
	
#======================================================================#
# The search circle in frame and get ROI					 		   #
#======================================================================#		
def getROIfromCircle(frm):	
		
		outRoi = ROIframe
		
		# give random ROI for create variable		
		roi = frm[:10,:10]		
		gray = cv.cvtColor(frm, cv.COLOR_BGR2GRAY)
		gray = cv.medianBlur(gray, 5)
		#gray = cv.equalizeHist(gray)

		rows = gray.shape[0]
		circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 10,
                               param1=120, param2=30,
                               minRadius=5, maxRadius=50)
                                                              
		if circles is not None:
			circles = np.round(circles[0, :]).astype("int")
			
			for (x, y, r) in circles:
				roi = frm[y-r-20:y+r+20,x-r-20:x+r+20]
				if roi.size:
					roi =cv.resize(roi,(100,100))
					#cv.circle(frm, (x, y), r, (0, 0, 200), 2)
					cv.rectangle(frm, (x - 5, y - 5), (x + 5, y + 5), (0, 0, 255), 1)
					outRoi.x =x
					outRoi.y =y
					outRoi.r =r
					outRoi.frame = roi
					outRoi.description = "ROI circle"
					#if roi is not None:
					#	cv.imshow("roi",roi)
					return outRoi
					#time.sleep(0.001)
					
		else:
			return None
	
#======================================================================#
# the start detection objects configured from file			 		   #
#======================================================================#		
def startDetector():	
	# Load cascades files
	loadCascades()
	# Open camera from config value
	capture = cv.VideoCapture(_camera)
	if capture.isOpened():
		toLog("Camera is open!")
	else:
		toLog("Error! - Cannot open camera: "+str(_camera))
		exit()
	
	# If framew and frameh in config file is a set 
	if (_framew is not None) and (_frameh is not None):
		# set frame size
		capture.set(cv.CAP_PROP_FRAME_WIDTH,_framew)
		capture.set(cv.CAP_PROP_FRAME_HEIGHT,_frameh)
	# setting brightness	
	if (_brightness != "default"):
		capture.set(cv.CAP_PROP_BRIGHTNESS,int(_brightness))
	# setting contrast
	if (_contrast != "default"):		
		capture.set(cv.CAP_PROP_CONTRAST,int(_contrast))
	# setting saturation
	if (_saturation !="default"):
		capture.set(cv.CAP_PROP_SATURATION,int(_saturation))
	# setting GAIN
	if (_gain !="default"):
		capture.set(cv.CAP_PROP_GAIN,int(_gain))	
	
	while True:		
		
		toInfo("","","","","")
		toLog("--- no events ---")
		#time.sleep(0.01)
		
		ret, frame = capture.read()    
		#fps = capture.get(cv.CAP_PROP_FPS)
		
		if frame is None:
			print("can`t capturing frame! Break")
			break
		# give gray frame	
		frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)				
		frame_gray = cv.equalizeHist(frame_gray)

		for i in range(0,len(simpleobj)):
			if simpleobj[i]['shapecheck']:
				# shape check is circle
				if simpleobj[i]['shape'] == "circle":
					CIRCLE_ROI = getROIfromCircle(frame)
					if CIRCLE_ROI is not None:
						#objects[i] = cascades[i].detectMultiScale(CIRCLE_ROI.frame, 1.05, 1, minSize=(30,30))			
						temp_cascade = simpleobj[i]['cascade'].detectMultiScale(CIRCLE_ROI.frame, simpleobj[i]['scale'], simpleobj[i]['neighbors'], minSize=(simpleobj[i]['minsize_w'],simpleobj[i]['minsize_h']))			
						for (x,y,w,h) in temp_cascade:
							toInfo(str(i),simpleobj[i]['description'],str(simpleobj[i]['shapecheck']),simpleobj[i]['shape'],str(len(temp_cascade)))
							toLog("Object detected!")							
							cv.rectangle(frame,(CIRCLE_ROI.x-CIRCLE_ROI.r,CIRCLE_ROI.y-CIRCLE_ROI.r)
							,(CIRCLE_ROI.x+CIRCLE_ROI.r,CIRCLE_ROI.y+CIRCLE_ROI.r),simpleobj[i]['color'],simpleobj[i]['depth'])
							if simpleobj[i]['include'] is not None:
								_module_action = importlib.import_module(simpleobj[i]['include'])
								_module_action.run()
							
				# more shapes....
			else:
				for i in range(0,len(simpleobj)):
					#objects[i] = cascades[i].detectMultiScale(frame_gray, 1.05, 5, minSize=(30,30))				
					temp_cascade = simpleobj[i]['cascade'].detectMultiScale(frame_gray, simpleobj[i]['scale'], simpleobj[i]['neighbors'], minSize=(simpleobj[i]['minsize_w'],simpleobj[i]['minsize_h']))			
					
					for (x,y,w,h) in temp_cascade:
						toInfo(str(i),simpleobj[i]['description'],str(simpleobj[i]['shapecheck']),simpleobj[i]['shape'],str(len(temp_cascade)))
						toLog("Object detected!")						
						cv.rectangle(frame,(x,y),(x+w,y+h),simpleobj[i]['color'],simpleobj[i]['depth'])				
						if simpleobj[i]['include'] is not None:
							_module_action = importlib.import_module(simpleobj[i]['include'])
							_module_action.run()
						
		
				
		if _showis:
			cv.imshow("detector",frame)		
			# wait press ESC key	
			k = cv.waitKey(30) & 0xff   
			if k == 27:
				toLog("The User exit of the programm!")
				break
			
	# clean and destroy window
	capture.release()
	cv.destroyAllWindows()
	

startDetector()

