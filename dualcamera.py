from picamera import mmalobj as mo, mmal
from picamera import PiCamera
from time import sleep
from signal import pause

print("starting camera feed...")
##-- SETTINGS --##
eye_box_size = 330
box_center_y = 300
box_middle_offset = 190

screen_middle = int(800/2)
half_box_size = int(eye_box_size/2)

camera = mo.MMALCamera()
splitter = mo.MMALSplitter()
render_left = mo.MMALRenderer()
render_right = mo.MMALRenderer()

#Brigthens image
camera.control.params[mmal.MMAL_PARAMETER_BRIGHTNESS] = .6
#Sets camera exposure for nighttime
camera.control.params[mmal.MMAL_PARAMETER_ISO]=800

fx = camera.control.params[mmal.MMAL_PARAMETER_COLOUR_EFFECT]
fx.u = 32768
fx.v = 65536
camera.control.params[mmal.MMAL_PARAMETER_COLOUR_EFFECT] = fx

#print(mp.u)

#AttributeError: 'MMALCamera' object has no attribute 'image_effect'
#mmal.MMAL_PARAM_IMAGEFX_COLOURPOINT = 0
#clp = mmal.MMAL_PARAM_IMAGEFX_COLOURPOINT
#camera.image_effect = clp


#Set camera formats
camera.outputs[0].framerate=30
camera.outputs[0].framesize=(1080,1080)
camera.outputs[0].commit()

#Prepare displayregion
display_region = render_left.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION]
display_region.set = mmal.MMAL_DISPLAY_SET_FULLSCREEN | mmal.MMAL_DISPLAY_SET_DEST_RECT
display_region.fullscreen = False

#renderer display regions on screen space
#rect format: (minX, minY, width, height)
#Left eye render
display_region.dest_rect = mmal.MMAL_RECT_T((screen_middle - box_middle_offset) - half_box_size, box_center_y - half_box_size, eye_box_size, eye_box_size)
render_left.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION]=display_region
#Right eye render
display_region.dest_rect = mmal.MMAL_RECT_T((screen_middle + box_middle_offset) - half_box_size, box_center_y - half_box_size, eye_box_size, eye_box_size)
render_right.inputs[0].params[mmal.MMAL_PARAMETER_DISPLAYREGION]=display_region

#Connect both renderers to sources
splitter.connect(camera.outputs[0])
render_left.connect(splitter.outputs[0])
render_right.connect(splitter.outputs[1])

#Enable Renderers
splitter.enable()
render_left.enable()
render_right.enable()

#Continue rendering unil interrupted
pause()
