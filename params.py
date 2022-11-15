# Spiral Art Drawing Program
# by Freya Corlis-Richards

#USER DEFINED PARAMETERS
#Modify these to change the output of the spiral drawer

#Filename Parameters
class FILE:
    INPUT_FILE          = "source.png" #input filename or path
    OUTPUT_PNG_FILE     = "spiral.png"
    OUTPUT_GIF_FILE     = "spiral.gif" #only used if GIF.ANIMATED = True

#Image Size Parameters
class IMAGE:
    WIDTH               = 1000  #px width of input and output images
    HEIGHT              = 1000  #px height of input and output images
    SCALE               = 4     #scale of PIL canvas
    CIRCLE_CROPPING     = True  #True - Circle Cropping / False - Square Cropping (takes longer)

#Animated GIF Parameters
class GIF:
    ANIMATED            = True  #create animated GIF (takes longer)
    GIF_SCALE           = 0.5   #scale of GIF image file
    FRAMES_PER_ROTATION = 4     #GIF frames per spiral rotation
    FRAME_TIME          = 10    #ms per GIF frame
    THUMBNAIL_FRAME     = True  #include completed spiral as first frame of GIF

#Background and Line Color Parameters
#and Monochrome Adjustment Scalers
class MONO_COLOR:
    BG_COLOR   = (255,255,255)  #RGB of background color
    LINE_COLOR = (  0,  0,  0)  #RGB of line color

    #monochrome adjustment scalers
    SMOOTHING           = 1.0   #Brightness smoothing scaler (takes longer) 0 Least / 1 Most / >1 Oversampling
    CONTRAST            = 1.0   #Contrast adjustment scaler   0-1 Less Contrast   / 1 No Change / >1  More Contrast
    BRIGHTNESS          = 1.0   #Brightness adjustment scaler 0-1 Less Brightness / 1 No Change / 1-2 More Brightness

#Spiral spacing parameters
class SPIRAL:
    DEGREES             = 0.05  #degrees per increment
    SPACING             = 10    #px offset per rotation
    MIN_LINE_PIXELS     = 0.5   #px width of thinnest line (white in source image)



#CALCULATED PARAMETERS
#Warning! modifying these variables may break the program
class CALC:
    class IMAGE:
        IMAGE_SIZE =  (IMAGE.WIDTH, IMAGE.HEIGHT)
        CANVAS_SIZE = (int(IMAGE.WIDTH * IMAGE.SCALE), int(IMAGE.HEIGHT * IMAGE.SCALE))

    class GIF:
        GIF_SIZE = (int(IMAGE.WIDTH * GIF.GIF_SCALE), int(IMAGE.HEIGHT * GIF.GIF_SCALE))
        FRAME_INCREMENT = (360 / SPIRAL.DEGREES) / GIF.FRAMES_PER_ROTATION  #loop cycles per gif frame
      
    class MONO_COLOR:
        SAMPLE_WIDTH = int(SPIRAL.SPACING / 2 * MONO_COLOR.SMOOTHING)       #width of pixel brightness sampling

    class SPIRAL:
        INCREMENT = SPIRAL.SPACING / (360 / SPIRAL.DEGREES / IMAGE.SCALE)   #radius offset per increment
        if IMAGE.CIRCLE_CROPPING:
            COUNT = int(IMAGE.WIDTH / SPIRAL.SPACING / 2)                   #number of spirals for circle
        else:
            COUNT = int(IMAGE.WIDTH / SPIRAL.SPACING / 1.4)                 #number of spirals for full square
        MIN_POINT_RADIUS = SPIRAL.MIN_LINE_PIXELS * IMAGE.SCALE             #thinnest point - white
        MAX_POINT_RADIUS = SPIRAL.SPACING / 2 * IMAGE.SCALE * 0.95          #thickest point - black (95% of spiral spacing)
