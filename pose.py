#USE THE COCO MODEL!!!!!

#Do chosen_frames[pos-3] to account for cases like dolgopolov. If you use the COCO model like now
#it might work even if racket is blocking the shoulder
#Even if it doesn't work, then you will just film from the fron at 45 degrees.

#Trophy Position camera Infront at 45 degrees also facing player's back!
#Contact Point camera behind at 45 degrees facing player's back!
#I used to thing 45 degrees to the right, but to face the back the camera has to be placed to the left like in nadalpic.png!


#Include images of where to put the camera for contact point analysis
#and where to put it for trophy position analysis


#Trophy Position camera Infront!
#Contact Point camera behind!

#Or maybe both behind or infront at 80 degrees

#TAKE THE VIDEO FROM THE FRONT OR BEHIND AT 45 DEGREES!!

#Ok now you SHOULD do the 45 degrees in front of the player
#because behind the player, the racket may come in front which prevents detecting shoulders

#Maybe for shoulders, get the neck spoints[1]

#Maybe angle thecamera 45 degrees IN FRONT of the player

#chosen_frames[pos - 3] because some serve motions hella fast(migh make difference 0)

#Give the app time to register the background

#Maybe incorporate these functions into the actual kivy main.py so you can use a progress bar

#You justhave to get youtube premium and test it out with videos downloaded directly from Youtube to get correct differences
#instead of being screen recorded since it causes a lot of complications and false conclusions

# So....turns out when u screenrecord the video is automatically in around 60 fps i think, but not so sure


import cv2 as cv
import numpy as np
import math

def frames(path,fps):
    backSub = cv.createBackgroundSubtractorMOG2()

    cap = cv.VideoCapture(path)

    bigboi = []


    no = 0
    circle_areas = []
    number = []
    loc = []
    chosen_frames = []
    radii = []

    bigplaces = []


    while True:
        no = no + 1

        print(no)

        ret, frame = cap.read()
        if ret == False:
            break

        fgMask = backSub.apply(frame)

        #if no < fps * 1: #First 5 seconds for registering the background
        #(I am using 1 TEMPORARILY because the sample videos do not give time for registering the background and so 5 won't work)
            #continue

        kernel = cv.getStructuringElement(cv.MORPH_CROSS, (5,5))

        #fgMask = cv.morphologyEx(fgMask, cv.MORPH_CLOSE, kernel)#Might remove this since already filtering out areas < 50(line 68)
        #fgMask = cv.morphologyEx(fgMask, cv.MORPH_OPEN, kernel)

        frame2 = cv.bitwise_and(frame, frame, mask = fgMask)

        hsv_frame = cv.cvtColor(frame2, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_frame, np.array([20, 40, 40]), np.array([80, 255, 255])) #Might change this Probably(higher)#4

        contoursdirty,hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contoursdirty = [cnt for cnt in contoursdirty if cv.contourArea(cnt) > 50]#50

        areas = [cv.contourArea(cnt) for cnt in contoursdirty]
        convexhulls = [cv.approxPolyDP(cnt, 0.03 * cv.arcLength(cnt,True), True) for cnt in contoursdirty]
        boundingcircleareas = [math.pi * (cv.minEnclosingCircle(cnt)[1] ** 2) for cnt in contoursdirty]
        contours = [contoursdirty[i] for i in range(len(contoursdirty)) if areas[i] / boundingcircleareas[i] > 0.5] #Change

        #Try this: Find the contour that is furthest from the rest of the contours
        try:
            round = []
            for cnt in contours:
                area = cv.contourArea(cnt)
                (x,y),radius = cv.minEnclosingCircle(cnt)
                carea = math.pi * (radius ** 2)
                roundness = abs(1-(area/carea))
                round.append(roundness)
            closest = min(round)
            i = round.index(closest)

            cnt = contours[i]
            epsilon = cv.arcLength(cnt, True)
            hull = cv.approxPolyDP(cnt, 0.03 * epsilon, True)
            (x,y), radius = cv.minEnclosingCircle(cnt)

            #Make sure motion is continuous

            #Try to use arrays instead of lists
            coordinates = np.array([x,y]).reshape(-1, 1)

            carea = math.pi * (radius ** 2)

            #cv.circle(frame, (int(x), int(y)), int(radius), (255,0,0), 3)
            #cv.circle(frame, (int(x), int(y)), int(0.1 * radius), (255,0,0), -1)
            #cv.drawContours(frame, [hull], 0, (0,0,255), 3)

            radii.append(int(radius))
            number.append(no)
            loc.append(coordinates)
            chosen_frames.append(frame)

        except:
            pass

    y_co = [int(loc[i][1]) for i in range(len(loc))]
    height,width,channels = chosen_frames[0].shape

    bigheight = min(y_co)
    pos = y_co.index(bigheight)

    pos = pos - 3 #Accounting for dologpolov cases

    bigplace = number[pos]
    bigframe = chosen_frames[pos] #chosen_frames[pos - 3] because some serve motions hella fast(migh make difference 0)

    bigframes = (bigframe,int(loc[pos][0]), int(loc[pos][1])) #Maybe append p-5 or something(for cases: Dolgopolov)

    #Contact:

    x_co = loc[pos][0]

    radius = radii[pos]

    changes = []

    #Impact point is usually between 0.2 and 0.5 seconds after maximum point os serve. But more data makes it more accurate
    #Because some frames are replicated since, screen recording is at 60 fps while video plays at 30 fps,
    #The time stamp where this ends(mainly at 1second), is actually longer than what you see

    #You justhave to get youtube premium and test it out with videos downloaded directly from Youtube
    #instead of being screen recorded since it causes a lot of complications and false conclusions
    for s in loc[int(pos + 0.2 * fps): int(pos + 1*fps)]: #Minimize these differences

        try:
            changes.append(int(x_co - s[0]))
        except:
            pass

    #Maybe get rid of all this, and instead divide these frames into 15 points twice instead of 10

    deluxe = [i for i in enumerate(changes) if abs(i[1]) <= 10 * radius] #might change the idfference to make it bigger

    l = len(deluxe)

    try:
        bruh = deluxe[-1]
        off = bruh[0]

        final_f = chosen_frames[int(pos + 0.2*fps) : int(pos + 0.2*fps + off)]
        final_loc = loc[int(pos + 0.2*fps) : int(pos + 0.2*fps + off )]
        final_r = radii[int(pos + 0.2*fps) : int(pos + 0.2*fps + off)]
        finale = []

        #Finally nigga this works

        #Might not need to use all that wrist detection, you MIGHT get the contact frame solely from checking the realtime speed
        for i in range(len(final_loc)):
            try:

                # Get the horizontal speed in real time in m/s :
                #Get radius of ball currently in pixel
                #Divide distance moved within one frame by radius of ball in pixels
                #This will will give u number of ball radii in the given distance
                #Multiply that by the actual radius in meters and this takes place within one frame
                #Distance per frame = Distance per (1/240 seconds) = Distance * 240
                #Then multiple by frame rate to get distance moved in one sec


                #Triple all differences because screen recording is at 60fps

                #For actual program with normal videos(without screenrecording) use difference of 1 only
                # i-3 NOT i+3 because with i+3 the last few frames are removed which might be essential
                speed_now = ((final_loc[i][0] - final_loc[i-3][0]) / (1.5 * final_r[i]) ) * 0.0343 #(Radius probably undersetimated)
                speed_now = float(speed_now * fps) #Might make this 60 since screen recording is at 60fps??

                if abs(speed_now) < 2 and (0.5*radius < final_r[i] < 2*radius): #Might lower threshold of 2 for speed_now
                    finale.append(final_f[i])
            except:
                pass
    except:

        finale = chosen_frames[int(pos + 0.2*fps) : int(pos + fps)] #Might make this smaller ma brudda lol

    return (bigframes,bigplace,fps,finale)


def pose(big,dominant, protoFile, weightsFile):

    # Make this different for lefties and righties
    #Detect and append only the points u need so u don't wate time on detectting unneeded points
    n = 0

    fps = big[2]
    numbers = big[1]

    nPoints = 15
    important = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]

    net = cv.dnn.readNetFromCaffe(protoFile, weightsFile)


    frame = big[0][0]
    xcenter = big[0][1]
    ycenter = big[0][2]

    height,width,channels = frame.shape
    threshold = 0.1

    inpBlob = cv.dnn.blobFromImage(frame, 1.0 / 255, (width,height), (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inpBlob)
    output = net.forward()

    H = output.shape[2]
    W = output.shape[3]

    spoints = []

    for i in important:

        probMap = output[0, i, :, :]
        minVal, prob, minLoc, point = cv.minMaxLoc(probMap)

        x = (width * point[0]) / W
        y = (height * point[1]) / H

        if prob > threshold :
            spoints.append((int(x), int(y)))
        else :
            spoints.append(None)


    chest = spoints[13]

    if 'right' in dominant.lower():

        #spoints[5] = spoints[1]

        try:
            #Knees

            #Maybe analyze left knee if ur taking video from the front
            rhip = spoints[8]
            rknee = spoints[9]
            rankle = spoints[10]

            kneehip = np.array((spoints[8][0] - spoints[9][0] , spoints[8][1] - spoints[9][1]))
            kneeankle = np.array((spoints[10][0] - spoints[9][0] , spoints[10][1] - spoints[9][1]))

            unit_kneehip =  kneehip / np.linalg.norm(kneehip)
            unit_kneeankle = kneeankle / np.linalg.norm(kneeankle)
            dot_product = np.dot(unit_kneehip, unit_kneeankle)

            kneebend = np.arccos(dot_product) * (180 / math.pi)

            kneeframe = frame.copy()
            cv.line(kneeframe, rankle, rknee, (0,0,255), 2)
            cv.line(kneeframe, rknee, rhip, (0,0,255), 2)

            #Shoulder Over Shoulder

            rshoulder = spoints[2]
            lshoulder = spoints[5]

            x0 = lshoulder[0]
            y0 = lshoulder[1]

            x1 = rshoulder[0]
            y1 = rshoulder[0]

            a_line = (y0-y1) / (x0-x1)
            b_line = (y1*x0 - y0*x1) / (x0-x1)

            rightleft = np.array((spoints[5][0] - spoints[2][0] , spoints[5][1] - spoints[2][1]))
            horizontal = np.array([1,0])

            unit_rightleft =  rightleft / np.linalg.norm(rightleft)
            unit_horizontal = horizontal / np.linalg.norm(horizontal)
            dot_product2 = np.dot(unit_rightleft, unit_horizontal)

            slant = np.arccos(dot_product2) * (180 / math.pi)

            shoulderframe = frame.copy()
            cv.line(shoulderframe, rshoulder, lshoulder, (0,0,255), 2)

            # Elbow Drop

            #First elbow must be below line connecting shoulders for there to be a fault
            #For elbow drop, get line connecting shoulders.
            #Then get the angle between  the line connecting the shoulders
            # and the line connecting the hitting shoulder and the hitting elbow
            relbow = spoints[3]
            lelbow = spoints[6]

            x_elbow = relbow[0]
            y_elbow = relbow[1]

            combare = (a_line * x_elbow) + b_line

            #Right shoulder to rightelbow for righty
            elbowdrop = np.array((spoints[3][0] - spoints[2][0] , spoints[3][1] - spoints[2][1]))

            unit_drop = elbowdrop / np.linalg.norm(elbowdrop)
            unit_leftright = -1 * unit_rightleft
            dot_product3 = np.dot(unit_leftright, unit_drop)

            dropangle = np.arccos(dot_product3) * (180 / math.pi)

            if dropangle <= 20 or y_elbow <= combare: #Might change this value of 20
                overunder = 'High'
            else:
                overunder = 'Low'


            elbowframe = frame.copy()
            cv.line(elbowframe, rshoulder, lshoulder, (0,0,255), 2)
            cv.line(elbowframe, rshoulder, relbow, (0,0,255), 2)


        except:
            #Knees

            lhip = spoints[11]
            lknee = spoints[12]
            lankle = spoints[13]

            kneehip = np.array((spoints[11][0] - spoints[12][0] , spoints[11][1] - spoints[12][1]))
            kneeankle = np.array((spoints[13][0] - spoints[12][0] , spoints[13][1] - spoints[12][1]))

            unit_kneehip =  kneehip / np.linalg.norm(kneehip)
            unit_kneeankle = kneeankle / np.linalg.norm(kneeankle)
            dot_product = np.dot(unit_kneehip, unit_kneeankle)

            kneebend = np.arccos(dot_product) * (180 / math.pi)

            kneeframe = frame.copy()
            cv.line(kneeframe, lankle, lknee, (0,0,255), 2)
            cv.line(kneeframe, lknee, lhip, (0,0,255), 2)

            #Shoulder Over Shoulder

            rshoulder = spoints[2]
            lshoulder = spoints[5]

            x0 = lshoulder[0]
            y0 = lshoulder[1]

            x1 = rshoulder[0]
            y1 = rshoulder[0]

            a_line = (y0-y1) / (x0-x1)
            b_line = (y1*x0 - y0*x1) / (x0-x1)

            rightleft = np.array((spoints[5][0] - spoints[2][0] , spoints[5][1] - spoints[2][1]))
            horizontal = np.array([1,0])

            unit_rightleft =  rightleft / np.linalg.norm(rightleft)
            unit_horizontal = horizontal / np.linalg.norm(horizontal)
            dot_product2 = np.dot(unit_rightleft, unit_horizontal)

            slant = np.arccos(dot_product2) * (180 / math.pi)

            shoulderframe = frame.copy()
            cv.line(shoulderframe, rshoulder, lshoulder, (0,0,255), 2)



            # Elbow Drop

            #First elbow must be below line connecting shoulders for there to be a fault
            #For elbow drop, get line connecting shoulders.
            #Then get the angle between  the line connecting the shoulders
            # and the line connecting the hitting shoulder and the hitting elbow

            relbow = spoints[3]
            lelbow = spoints[6]

            x_elbow = relbow[0]
            y_elbow = relbow[1]

            combare = (a_line * x_elbow) + b_line

            #Right shoulder to rightelbow for righty
            elbowdrop = np.array((spoints[3][0] - spoints[2][0] , spoints[3][1] - spoints[2][1]))

            unit_drop = elbowdrop / np.linalg.norm(elbowdrop)
            unit_leftright = -1 * unit_rightleft
            dot_product3 = np.dot(unit_leftright, unit_drop)

            dropangle = np.arccos(dot_product3) * (180 / math.pi)

            if dropangle <= 20 or y_elbow <= combare:
                overunder = 'High'
            else:
                overunder = 'Low'



            elbowframe = frame.copy()
            cv.line(elbowframe, rshoulder, lshoulder, (0,0,255), 2)
            cv.line(elbowframe, rshoulder, relbow, (0,0,255), 2)

    elif 'left' in dominant.lower():

        #spoints[2] = spoints[1]

        try:
            #Knees

            lhip = spoints[11]
            lknee = spoints[12]
            lankle = spoints[13]

            kneehip = np.array((spoints[11][0] - spoints[12][0] , spoints[11][1] - spoints[12][1]))
            kneeankle = np.array((spoints[13][0] - spoints[12][0] , spoints[13][1] - spoints[12][1]))

            unit_kneehip =  kneehip / np.linalg.norm(kneehip)
            unit_kneeankle = kneeankle / np.linalg.norm(kneeankle)
            dot_product = np.dot(unit_kneehip, unit_kneeankle)

            kneebend = np.arccos(dot_product) * (180 / math.pi)

            kneeframe = frame.copy()
            cv.line(kneeframe, lankle, lknee, (0,0,255), 2)
            cv.line(kneeframe, lknee, lhip, (0,0,255), 2)

            #Shoulder Over Shoulder

            rshoulder = spoints[2]
            lshoulder = spoints[5]

            x0 = lshoulder[0]
            y0 = lshoulder[1]

            x1 = rshoulder[0]
            y1 = rshoulder[0]

            a_line = (y0-y1) / (x0-x1)
            b_line = (y1*x0 - y0*x1) / (x0-x1)

            leftright = np.array((spoints[2][0] - spoints[5][0] , spoints[2][1] - spoints[5][1]))
            horizontal_left = np.array([-1,0])

            unit_leftright =  leftright / np.linalg.norm(leftright)
            unit_horizontal_left = horizontal_left / np.linalg.norm(horizontal_left)
            dot_product2 = np.dot(unit_leftright, unit_horizontal_left)

            slant = np.arccos(dot_product2) * (180 / math.pi)

            shoulderframe = frame.copy()
            cv.line(shoulderframe, rshoulder, lshoulder, (0,0,255), 2)

            # Elbow Drop

            #First elbow must be below line connecting shoulders for there to be a fault
            #For elbow drop, get line connecting shoulders.
            #Then get the angle between  the line connecting the shoulders
            # and the line connecting the hitting shoulder and the hitting elbow

            relbow = spoints[3]
            lelbow = spoints[6]

            x_elbow = lelbow[0]
            y_elbow = lelbow[1]

            combare = (a_line * x_elbow) + b_line

            #Left shoulder to left elbow for lefty
            elbowdrop = np.array((spoints[6][0] - spoints[5][0] , spoints[6][1] - spoints[5][1]))

            unit_drop = elbowdrop / np.linalg.norm(elbowdrop)
            unit_rightleft = -1 * unit_leftright
            dot_product3 = np.dot(unit_rightleft, unit_drop)

            dropangle = np.arccos(dot_product3) * (180 / math.pi)

            if dropangle <= 20 or y_elbow <= combare:
                overunder = 'High'
            else:
                overunder = 'Low'

            elbowframe = frame.copy()
            cv.line(elbowframe, rshoulder, lshoulder, (0,0,255), 2)
            cv.line(elbowframe, lshoulder, lelbow, (0,0,255), 2)

        except:

            #Knees

            rhip = spoints[8]
            rknee = spoints[9]
            rankle = spoints[10]

            kneehip = np.array((spoints[8][0] - spoints[9][0] , spoints[8][1] - spoints[9][1]))
            kneeankle = np.array((spoints[10][0] - spoints[9][0] , spoints[10][1] - spoints[9][1]))

            unit_kneehip =  kneehip / np.linalg.norm(kneehip)
            unit_kneeankle = kneeankle / np.linalg.norm(kneeankle)
            dot_product = np.dot(unit_kneehip, unit_kneeankle)

            kneebend = np.arccos(dot_product) * (180 / math.pi)

            kneeframe = frame.copy()
            cv.line(kneeframe, rankle, rknee, (0,0,255), 2)
            cv.line(kneeframe, rknee, rhip, (0,0,255), 2)

            #Shoulder Over Shoulder

            rshoulder = spoints[2]
            lshoulder = spoints[5]

            x0 = lshoulder[0]
            y0 = lshoulder[1]

            x1 = rshoulder[0]
            y1 = rshoulder[0]

            a_line = (y0-y1) / (x0-x1)
            b_line = (y1*x0 - y0*x1) / (x0-x1)

            leftright = np.array((spoints[2][0] - spoints[5][0] , spoints[2][1] - spoints[5][1]))
            horizontal_left = np.array([-1,0])

            unit_leftright =  leftright / np.linalg.norm(leftright)
            unit_horizontal_left = horizontal_left / np.linalg.norm(horizontal_left)
            dot_product2 = np.dot(unit_leftright, unit_horizontal_left)

            slant = np.arccos(dot_product2) * (180 / math.pi)

            shoulderframe = frame.copy()
            cv.line(shoulderframe, rshoulder, lshoulder, (0,0,255), 2)

            # Elbow Drop

            #First elbow must be below line connecting shoulders for there to be a fault
            #For elbow drop, get line connecting shoulders.
            #Then get the angle between  the line connecting the shoulders
            # and the line connecting the hitting shoulder and the hitting elbow

            relbow = spoints[3]
            lelbow = spoints[6]

            x_elbow = lelbow[0]
            y_elbow = lelbow[1]

            combare = (a_line * x_elbow) + b_line

            #Left shoulder to left elbow for lefty
            elbowdrop = np.array((spoints[6][0] - spoints[5][0] , spoints[6][1] - spoints[5][1]))

            unit_drop = elbowdrop / np.linalg.norm(elbowdrop)
            unit_rightleft = -1 * unit_leftright
            dot_product3 = np.dot(unit_rightleft, unit_drop)

            dropangle = np.arccos(dot_product3) * (180 / math.pi)

            if dropangle <= 20 or y_elbow <= combare:
                overunder = 'High'
            else:
                overunder = 'Low'


            elbowframe = frame.copy()
            cv.line(elbowframe, lshoulder, rshoulder, (0,0,255), 2)
            cv.line(elbowframe, lshoulder, lelbow, (0,0,255), 2)

    return kneebend, slant, overunder, spoints, kneeframe, shoulderframe, elbowframe

# Analyzing Contact Position:

#Maybe incorporate these functions into the actual kivy main.py so you can use a progress bar
def contact(finale,dominant, protoFile, weightsFile):
    #Take the frame where wrist is maximum
    #Get the 10 or 20(depending on fps) frames before it
    #Then get 10  or 20(depending on fps) frames after it
    #Find when the direction change of the ball is maximum within the period
    nPoints = 15
    important = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]

    net = cv.dnn.readNetFromCaffe(protoFile, weightsFile)

    l = len(finale)

    k = 0

    height,width,channels = finale[0].shape

    initialframe = 0
    spoints = []
    ymin = int(height)
    z = 0

    for i in range(0,11):

        k = k+1
        print(k)

        frame = finale[int(i * ((l-1)/10))] #Maybe divide into 20 frames instead(Much more accurate but more time)

        height,width,channels = frame.shape
        threshold = 0.1

        inpBlob = cv.dnn.blobFromImage(frame, 1.0 / 255, (width,height), (0, 0, 0), swapRB=False, crop=False)
        net.setInput(inpBlob)
        output = net.forward()

        H = output.shape[2]
        W = output.shape[3]

        points = []

        for no in important:

            probMap = output[0, no, :, :]
            minVal, prob, minLoc, point = cv.minMaxLoc(probMap)

            x = (width * point[0]) / W
            y = (height * point[1]) / H

            if prob > threshold :

                points.append((int(x), int(y)))
            else :
                points.append(None)


        if 'right' in dominant.lower():

            try:

                if points[4][1] <= ymin: #This detects the wrist(cdifficult to detect), maybe detect elbow
                    ymin = points[4][1]

                    initialframe = frame
                    spoints = points
                    z = i

            except:
                pass

        if 'left' in dominant.lower():

            try:

                if points[7][1] <= ymin: #This detects the wrist(cdifficult to detect), maybe detect elbow
                    ymin = points[7][1]

                    initialframe = frame
                    spoints = points
                    z = i

            except:
                pass

    k = 0

    initialframe = 0
    spoints = []
    ymin = int(height)

    print(z)
    if z == 0:
        finale2 = finale[int( (z * ((l-1)/10)) - 1) : int( ((z+1) * ((l-1)/10)) + 1)]
    elif z == 10:
        finale2 = finale[int( ((z-1) * ((l-1)/10)) + 1): int( (z * ((l-1)/10)) - 1)]
    else:
        finale2 = finale[int( ((z-1) * ((l-1)/10)) + 1) : int( ((z+1) * ((l-1)/10)) - 1) ]


    l2 = len(finale2)
    print(l2)

    metapoints = []
    z = 0

    for i in range(0,11):

        k = k+1
        print(k)

        frame = finale2[int(i * ((l2-1)/10))] #If i = 10, you are still using the frame before the last and not including last

        height,width,channels = frame.shape
        threshold = 0.1

        inpBlob = cv.dnn.blobFromImage(frame, 1.0 / 255, (width,height), (0, 0, 0), swapRB=False, crop=False)
        net.setInput(inpBlob)
        output = net.forward()

        H = output.shape[2]
        W = output.shape[3]

        points = []

        for no in important:

            probMap = output[0, no, :, :]
            minVal, prob, minLoc, point = cv.minMaxLoc(probMap)

            x = (width * point[0]) / W
            y = (height * point[1]) / H

            if prob > threshold :

                points.append((int(x), int(y)))
            else :
                points.append(None)

        metapoints.append(points)

        if 'right' in dominant.lower():

            try:
                if points[4][1] <= ymin: #This detects the wrist(cdifficult to detect), maybe detect elbow
                    z = i
                    ymin = points[4][1]

                    initialframe = frame
                    spoints = points
            except:
                pass

        if 'left' in dominant.lower():

            try:

                if points[7][1] <= ymin: #This detects the wrist(cdifficult to detect), maybe detect elbow
                    z = i
                    ymin = points[7][1]

                    initialframe = frame
                    spoints = points

            except:
                pass


        #With 10 frame division it is still not quite accurate
        #The correct highest wrist point frame is detected, but some frames after it which are more representative
        #of the contactpoint are ignored
        #Try 20 frames next or maybe keep only the quarter of frames from finale

    #Instead of showing frame(z+3) like below
    #store the frame and metapoints[z+3] into a variable and analyze it with pose


    #Maybe incorporate these functions into the actual kivy main.py so you can use a progress bar

    #Maybe be increase the try and except block below up to z+5?
    try:
        realframe = finale2[int( (z+3) * ((l2-1)/10))]
        realpoints = metapoints[z+3]
    except:
        try:
            realframe = finale2[int( (z+2) * ((l2-1)/10))]
            realpoints = metapoints[z+2]
        except:
            try:
                realframe = finale2[int( (z+1) * ((l2-1)/10))]
                realpoints = metapoints[z+1]
            except:
                try:
                    realframe = finale2[int( (z) * ((l2-1)/10))]
                    realpoints = metapoints[z]
                except:
                    pass
    try:
        realpoints[4] = (realpoints[4][0] + 5, realpoints[4][1]) #Might change this difference
    except:
        pass

    try:
        realpoints[7] = (realpoints[7][0] - 5, realpoints[7][1]) #Might change this difference
    except:
        pass

    if 'right' in dominant.lower():

        rshoulder = realpoints[2]
        lshoulder = realpoints[5]

        leftright = np.array((spoints[2][0] - spoints[5][0] , spoints[2][1] - spoints[5][1]))
        horizontal_right = np.array([1,0])

        unit_leftright =  leftright / np.linalg.norm(leftright)
        unit_horizontal_right = horizontal_right / np.linalg.norm(horizontal_right)
        dot_product = np.dot(unit_leftright, unit_horizontal_right)

        slant2 = np.arccos(dot_product) * (180 / math.pi)
        realframe1 = realframe.copy()
        cv.line(realframe1, rshoulder, lshoulder, (0,0,255), 2)

        relbow  = realpoints[3]
        rwrist = realpoints[4]

        elbowshoulder = np.array((realpoints[2][0] - realpoints[3][0] , realpoints[2][1] - realpoints[3][1]))
        elbowrist = np.array((realpoints[4][0] - realpoints[3][0] , realpoints[4][1] - realpoints[3][1]))

        unit_elbowshoulder =  elbowshoulder / np.linalg.norm(elbowshoulder)
        unit_elbowrist = elbowrist / np.linalg.norm(elbowrist)
        dot_product2 = np.dot(unit_elbowshoulder, unit_elbowrist)

        armbend = np.arccos(dot_product2) * (180 / math.pi)

        realframe2 = realframe.copy()
        cv.line(realframe2, realpoints[2], realpoints[3], (0,0,255), 2)
        cv.line(realframe2, realpoints[3], realpoints[4], (0,0,255), 2)

    if 'left' in dominant.lower():

        lshoulder = realpoints[5]
        rshoulder = realpoints[2]

        rightleft = np.array((spoints[5][0] - spoints[2][0] , spoints[5][1] - spoints[2][1]))
        horizontal_left = np.array([-1,0])

        unit_rightleft =  rightleft / np.linalg.norm(rightleft)
        unit_horizontal_left = horizontal_left / np.linalg.norm(horizontal_left)
        dot_product = np.dot(unit_rightleft, unit_horizontal_left)

        slant2 = np.arccos(dot_product) * (180 / math.pi)
        realframe1 = realframe.copy()
        cv.line(realframe1, rshoulder, lshoulder, (0,0,255), 2)

        lelbow  = realpoints[6]
        lwrist = realpoints[7]

        elbowshoulder = np.array((realpoints[5][0] - realpoints[6][0], realpoints[5][1] - realpoints[6][1]))
        elbowrist = np.array((realpoints[7][0] - realpoints[6][0], realpoints[7][1] - realpoints[6][1]))

        unit_elbowshoulder =  elbowshoulder / np.linalg.norm(elbowshoulder)
        unit_elbowrist = elbowrist / np.linalg.norm(elbowrist)
        dot_product2 = np.dot(unit_elbowshoulder, unit_elbowrist)

        armbend = np.arccos(dot_product2) * (180 / math.pi)

        realframe2 = realframe.copy()
        cv.line(realframe2, realpoints[5], realpoints[6], (0,0,255), 2)
        cv.line(realframe2, realpoints[6], realpoints[7], (0,0,255), 2)

    return armbend, realframe2, realpoints, slant2, realframe1



#Filming diagonally in front also gives more space to take the camera back, and thereby definitely
#including the entirety of the ball toss act in the video, even at the peak

#Should be for 3.5, maybe 4.0, players and above

#Maybe incorporate these functions into the actual kivy main.py so you can use a progress bar

#TAKE THE VIDEO FROM THE FRONT AT 45 DEGREES!!

#big = frames('/Users/mahshi/Desktop/Technique/thiem.mov',240)
#real = contact(big[3], 'leftyyy', 'pose_deploy_linevec.prototxt', 'pose_iter_440000.caffemodel')
#cv.imwrite('/Users/mahshi/Desktop/nadalpic.png', real[1])
