# Spiral Art Drawing Program
# by Freya-The-Goddess

#import libraries
from PIL import Image, ImageDraw #Pillow (PIL fork)
import math
import time

#import parameters from params.py
from params import * 

#draw point of spiral with centre coordinates, radius, and color
def draw_point(canvas, x, y, r, color):
    canvas.ellipse([x-r, y-r, x+r, y+r], fill=color)

#get the average brightness for a point on input image
#returns the radius that the point should be drawn
def get_brightness(pixels, xo, yo):
    pixel_brightness_list = [] #store brightness values of sampled pixels to be averaged
    
    #for each pixel in the sampled area
    for x in range(int(xo - CALC.MONO_COLOR.SAMPLE_WIDTH), int(xo + CALC.MONO_COLOR.SAMPLE_WIDTH + 1)):
        for y in range(int(yo - CALC.MONO_COLOR.SAMPLE_WIDTH), int(yo + CALC.MONO_COLOR.SAMPLE_WIDTH + 1)):
            if x >= 0 and x < IMAGE.WIDTH and y >= 0 and y < IMAGE.HEIGHT: #sampled pixel is inside bounds of input image
                #get brightness value by scaling RGB values
                pixel_brightness = 255 - ((pixels[x,y][0]*0.299) + (pixels[x,y][1]*0.587) + (pixels[x,y][2]*0.114))

                #brightness and contrast adjustment
                pixel_brightness = int(MONO_COLOR.CONTRAST * (pixel_brightness - 128) + 128 + ((MONO_COLOR.BRIGHTNESS-1) * -255))
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

    point_radius = CALC.SPIRAL.MIN_POINT_RADIUS + float(avg_brightness / 255) * (CALC.SPIRAL.MAX_POINT_RADIUS - CALC.SPIRAL.MIN_POINT_RADIUS)
    return point_radius

#draw spiral to canvas
def draw_spiral(in_pixels, out_canvas):

    #used to save frames if GIF.ANIMATED = True
    frames = []
    steps = 0

    #used to draw spiral
    distance = 0.0 #from centre
    angle    = 0.0 #degrees
    count    = 0   #spirals

    #spiral drawing loop
    while angle <= 360 * CALC.SPIRAL.COUNT:
        x = IMAGE.WIDTH  * IMAGE.SCALE / 2 + math.cos(math.radians(angle))*distance;
        y = IMAGE.HEIGHT * IMAGE.SCALE / 2 + math.sin(math.radians(angle))*distance;

        #Draw point on canvas
        #If point is inside canvas bounds or within 10px margin outside canvas
        if x > -10 and x < IMAGE.WIDTH * IMAGE.SCALE + 10 and y > -10 and y < IMAGE.HEIGHT * IMAGE.SCALE + 10:
            brightness = get_brightness(in_pixels, x / IMAGE.SCALE, y / IMAGE.SCALE)
            draw_point(out_canvas, x, y, brightness, MONO_COLOR.LINE_COLOR)

        #Append GIF frame to array if animation is turned on
        if GIF.ANIMATED and steps < CALC.GIF.FRAME_INCREMENT:
            steps += 1
        elif GIF.ANIMATED and steps >= CALC.GIF.FRAME_INCREMENT:
            gif_frame = out_im.copy()
            gif_frame.thumbnail(CALC.GIF.GIF_SIZE)
            frames.append(gif_frame)
            steps = 0

        #increment distance from centre and angle
        distance += CALC.SPIRAL.INCREMENT
        angle += SPIRAL.DEGREES

        #increment count when rotation complete
        if count < int(angle/360):
            count = int(angle/360)

            #print progress every 10% (except for 100%)
            if int(count / CALC.SPIRAL.COUNT * 10) > int((count-1) / CALC.SPIRAL.COUNT * 10) and int(count / CALC.SPIRAL.COUNT) != 1:
                print(str(int(count / CALC.SPIRAL.COUNT * 10)*10) + "% in " + format_time(int(time.time() - start_time)) + "...")

    #Append final GIF frame
    if GIF.ANIMATED == True:
        gif_frame = out_im.copy()
        gif_frame.thumbnail(CALC.GIF.GIF_SIZE)
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
    print("Input image '" + FILE.INPUT_FILE + "'")
        
    if GIF.ANIMATED:
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
    in_im = Image.open(FILE.INPUT_FILE)
    in_im = in_im.resize(CALC.IMAGE.IMAGE_SIZE)
    in_pixels = in_im.load()
    
    #create output image and canvas
    out_im = Image.new("RGBA", CALC.IMAGE.CANVAS_SIZE, MONO_COLOR.BG_COLOR)
    out_canvas = ImageDraw.Draw(out_im)

    if GIF.ANIMATED:
        frames = draw_spiral(in_pixels, out_canvas)
    else:
        draw_spiral(in_pixels, out_canvas)

    #print elapsed time
    print("Completed in " + format_time(int(time.time() - start_time)) + " (" + str(int(time.time() - start_time)) + " seconds)")

    #save PNG file
    out_im.thumbnail(CALC.IMAGE.IMAGE_SIZE)
    out_im.save(FILE.OUTPUT_PNG_FILE)
    print("Final drawing saved as '" + FILE.OUTPUT_PNG_FILE + "'")

    #save GIF file
    if GIF.ANIMATED:
        if GIF.THUMBNAIL_FRAME: #include completed spiral as first frame of GIF
            frames[-1].save(FILE.OUTPUT_GIF_FILE, save_all=True, append_images=frames[0:], optimize=False, loop=0, duration=GIF.FRAME_TIME) #with thumbnail frame
        else:
            frames[0].save(FILE.OUTPUT_GIF_FILE, save_all=True, append_images=frames[1:], optimize=False, loop=0, duration=GIF.FRAME_TIME) #without thumbnail frame
        print("Animation saved as '" + FILE.OUTPUT_GIF_FILE + "'")
