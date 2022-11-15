# Spiral Art Drawing Program
# by Freya Corlis-Richards

import params as P #import parameters from PARAMS.py file
from PIL import Image, ImageDraw #python Image Library
import math
import time


#draw point of spiral with centre coordinates, radius, and color
def draw_point(canvas, x, y, r, color):
    canvas.ellipse([x-r, y-r, x+r, y+r], fill=color)


#get the average brightness for a point on input image
#returns the radius that the point should be drawn
def get_brightness(pixels, xo, yo):
    pixel_brightness_list = [] #store brightness values of sampled pixels to be averaged
    
    #for each pixel in the sampled area
    for x in range(int(xo - P.CALC.MONO_COLOR.SAMPLE_WIDTH), int(xo + P.CALC.MONO_COLOR.SAMPLE_WIDTH + 1)):
        for y in range(int(yo - P.CALC.MONO_COLOR.SAMPLE_WIDTH), int(yo + P.CALC.MONO_COLOR.SAMPLE_WIDTH + 1)):
            if x >= 0 and x < P.IMAGE.WIDTH and y >= 0 and y < P.IMAGE.HEIGHT: #sampled pixel is inside bounds of input image
                #get brightness value by scaling RGB values
                pixel_brightness = 255 - ((pixels[x,y][0]*0.299) + (pixels[x,y][1]*0.587) + (pixels[x,y][2]*0.114))

                #brightness and contrast adjustment
                pixel_brightness = int(P.MONO_COLOR.CONTRAST * (pixel_brightness - 128) + 128 + ((P.MONO_COLOR.BRIGHTNESS-1) * -255))
                if pixel_brightness < 0 :
                    pixel_brightness = 0
                elif pixel_brightness > 255:
                    pixel_brightness = 255

                #append value to list to be averaged
                pixel_brightness_list.append(pixel_brightness)

    if pixel_brightness_list != []:
        avg_brightness = sum(pixel_brightness_list) / len(pixel_brightness_list) #calculate average brightness value
    else: #no pixels within sampled range (out of canvas)
        avg_brightness = 255

    point_radius = P.CALC.SPIRAL.MIN_POINT_RADIUS + float(avg_brightness / 255) * (P.CALC.SPIRAL.MAX_POINT_RADIUS - P.CALC.SPIRAL.MIN_POINT_RADIUS)
    return point_radius


#draw spiral to canvas
def draw_spiral(in_pixels, out_canvas):

    #used to save frames if P.GIF.ANIMATED = True
    frames = []
    steps = 0

    #used to draw spiral
    distance = 0.0 #from centre
    angle    = 0.0 #degrees
    count    = 0   #spirals

    #spiral drawing loop
    while angle <= 360 * P.CALC.SPIRAL.COUNT:
        x = P.IMAGE.WIDTH  * P.IMAGE.SCALE / 2 + math.cos(math.radians(angle))*distance;
        y = P.IMAGE.HEIGHT * P.IMAGE.SCALE / 2 + math.sin(math.radians(angle))*distance;

        #Draw point on canvas
        #If point is inside canvas bounds or within 10px margin outside canvas
        if x > -10 and x < P.IMAGE.WIDTH * P.IMAGE.SCALE + 10 and y > -10 and y < P.IMAGE.HEIGHT * P.IMAGE.SCALE + 10:
            brightness = get_brightness(in_pixels, x / P.IMAGE.SCALE, y / P.IMAGE.SCALE)
            draw_point(out_canvas, x, y, brightness, P.MONO_COLOR.LINE_COLOR)

        #Append GIF frame to array if animation is turned on
        if P.GIF.ANIMATED and steps < P.CALC.GIF.FRAME_INCREMENT:
            steps += 1
        elif P.GIF.ANIMATED and steps >= P.CALC.GIF.FRAME_INCREMENT:
            gif_frame = out_im.copy()
            gif_frame.thumbnail(P.CALC.GIF.GIF_SIZE)
            frames.append(gif_frame)
            steps = 0

        #increment distance from centre and angle
        distance += P.CALC.SPIRAL.INCREMENT
        angle += P.SPIRAL.DEGREES

        #increment count when rotation complete
        if count < int(angle/360):
            count = int(angle/360)

            #print progress every 10% (except for 100%)
            if int(count / P.CALC.SPIRAL.COUNT * 10) > int((count-1) / P.CALC.SPIRAL.COUNT * 10) and int(count / P.CALC.SPIRAL.COUNT) != 1:
                print(str(int(count / P.CALC.SPIRAL.COUNT * 10)*10) + "% in " + format_time(int(time.time() - start_time)) + "...")

    #Append final GIF frame
    if P.GIF.ANIMATED == True:
        gif_frame = out_im.copy()
        gif_frame.thumbnail(P.CALC.GIF.GIF_SIZE)
        frames.append(gif_frame)
        return frames


#Format time string from seconds to mm:ss or hh:mm:ss for printing
def format_time(seconds):
    if seconds < 60*60: #mm:ss
        minutes = seconds // 60
        seconds %= 60
        return "%02i:%02i" % (minutes, seconds)
    else: #hh:mm:ss
        hours = seconds // (60*60)
        seconds %= (60*60)
        minutes = seconds // 60
        seconds %= 60
        return "%02i:%02i:%02i" % (hours, minutes, seconds)


#print start of program header
def print_header():
    print("--------------------------\nSpiral Drawing Program\nby Freya Corlis-Richards\n--------------------------")
    print("Input image '" + P.FILE.INPUT_FILE + "'")
        
    if P.GIF.ANIMATED:
        print("Animation ON")
    else:
        print("Animation OFF")
    
    print("--------------------------")
    print("Starting spiral drawing...")


if __name__ == "__main__":
    #start of program header
    print_header()
    
    start_time = time.time() #time at start of main code to calculate elapsed time

    #open input image
    in_im = Image.open(P.FILE.INPUT_FILE)
    in_im = in_im.resize(P.CALC.IMAGE.IMAGE_SIZE)
    in_pixels = in_im.load()
    
    #create output image and canvas
    out_im = Image.new("RGBA", P.CALC.IMAGE.CANVAS_SIZE, P.MONO_COLOR.BG_COLOR)
    out_canvas = ImageDraw.Draw(out_im)

    if P.GIF.ANIMATED:
        frames = draw_spiral(in_pixels, out_canvas)
    else:
        draw_spiral(in_pixels, out_canvas)

    #print elapsed time
    print("Completed in " + format_time(int(time.time() - start_time)) + " (" + str(int(time.time() - start_time)) + " seconds)")

    #save PNG file
    out_im.thumbnail(P.CALC.IMAGE.IMAGE_SIZE)
    out_im.save(P.FILE.OUTPUT_PNG_FILE)
    print("Final drawing saved as '" + P.FILE.OUTPUT_PNG_FILE + "'")

    #save GIF file
    if P.GIF.ANIMATED:
        if P.GIF.THUMBNAIL_FRAME: #include completed spiral as first frame of GIF
            frames[-1].save(P.FILE.OUTPUT_GIF_FILE, save_all=True, append_images=frames[0:], optimize=False, loop=0, duration=P.GIF.FRAME_TIME) #with thumbnail frame
        else:
            frames[0].save(P.FILE.OUTPUT_GIF_FILE, save_all=True, append_images=frames[1:], optimize=False, loop=0, duration=P.GIF.FRAME_TIME) #without thumbnail frame
        print("Animation saved as '" + P.FILE.OUTPUT_GIF_FILE + "'")
        