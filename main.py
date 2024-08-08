#SHoulders could be slanted downwards. Account for that in pose.py after perfecting main.py, and make the slant angle 30 degrees

#Do pos-3 or pos-7 in pose.py to account for Dolgopolov like cases

#Add time needed for the contact

#Add try and except error messages

#There is a problem with the output of the kneebend angle.
#If the angle is less than 90, the program outputs the 180 - angle

#Add website

#COCO model worked from the back at 45 degrees even when the racket was blocking the shoulders!!!

#Write intellectual vitality essay abt computer vision(it being creepy), and abt artificial intelligence and skynet

#The COCO model was used. It was more accurate but 1.5 times slower
#If COCO model is used both trophy position and contactpoint could be analyzed from the front at 45 degrees!

#Trophy Position camera Infront at 45 degrees also facing player's back!
#Contact Point camera behind at 45 degrees facing player's back!
#I used to thing 45 degrees to the right, but to face the back the camera has to be placed to the left!

#Include images of where to put the camera for contact point analysis
#and where to put it for trophy position analysis

#TAKE THE VIDEO FROM THE FRONT AT 45 DEGREES!!

#Ok now you SHOULD do the 45 degrees in front of the player
#because behind the player, the racket may come in front which prevents detecting shoulders

#Maybe angle thecamera 45 degrees IN FRONT of the player

#I dis pos - 3 for the trophy pose in pose.py because some players have fast serve motions(might change it tho)

#Without using kivy.resources.resource_finder('nameoffile'), IT WON't WORK!!

#Camera NEEDS to be at 45 degree angle with all of the toss in sight

#Give the players advice and how much it matters whether they have the elements of the serve or # NOTE:
#For example: You on't bend your knees enough, however there are players who get without bending knees like

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

import webbrowser
import cv2 as cv
import numpy as np
import pose


#NOW ANALYZE THE CONTACT POINT


#Add a screen at the beginning for inputting age, height and other things
#Example: If old, not much need to bend knees

class WindowManager(ScreenManager):

    pass



# Use try and except if someone types in wrong data
class Window1(Screen):

    filepath = ObjectProperty(None)
    fps = ObjectProperty(None)
    dominant = ObjectProperty(None)
    next1 = ObjectProperty(None)

    kneebend, slant, dropangle = (0,0,0)
    spoints = []
    knee, shoulder, elbow = (0,0,0)

    def btn(self):
        smanager = self.manager

        try:
            smanager.remove_widget(self.window22)
            smanager.remove_widget(self.window23)
        except:
            pass

        self.next1.bind(on_release = self.next11)

        black = np.zeros((750,500,3), np.uint8)
        cv.rectangle(black, (0,0), (500,750), (0,0,255), -1)
        y0, dy = 50, 50
        dy1 = 60

        black2 = black.copy()

        black3 = np.zeros((750,500,3), np.uint8)
        cv.rectangle(black3, (0,0), (500,750), (0,0,255), -1)

        black4 = np.zeros((500,700,3), np.uint8)
        cv.rectangle(black4, (0,0), (700,500), (0,0,255), -1)
        y0, dy = 50, 40

        #If someone types in incorrect or blank data, print out an error message
        #Add a button that shows a Popup for the users to compare their trophy positions with the pros

        path = str(self.filepath.text)
        fps = float(self.fps.text)
        dominant = str(self.dominant.text)

        #This gives you the path to files within your app so they can be used on any computer
        #Without using kivy.resources.resource_finder('nameoffile'), IT WON't WORK!!
        protoFile = kivy.resources.resource_find('pose_deploy_linevec.prototxt') #COCO model used(more accurate/but slower)
        weightsFile = kivy.resources.resource_find('pose_iter_440000.caffemodel') #COCO model used(more accurate/but slower)

        self.big = pose.frames(path,fps)

        kneebend, slant, overunder, spoints, knee, self.shoulder, self.elbow = pose.pose(self.big, dominant,protoFile,weightsFile)

        if slant >= 90:

            slant = 180 - slant

        #Screen 2
        w,h = Window.size

        if kneebend > 150: #

            kneetext = ['  With a kneebend angle',
                    'of around {angle} degrees, your'.format(angle = int(kneebend)),
                    'knee bend is too shallow.',
                    'As a result, you are not',
                    'generating enough leg drive',
                    'and might lack extra easy',
                    'power. However, if you are',
                    'a bit on the older side or',
                    'have bad knees this is not',
                    'a necessity. You can still',
                    'have a great serve!']

            for i, line in enumerate(kneetext):
                y = y0 + i*dy
                cv.putText(black2, line, (5, y ), 3, 1, (0,0,0), 2)

            kneebuf1 = cv.flip(black2, 0)
            kneebuf1 = cv.resize(kneebuf1, (int(0.5 * w),int(0.75 * h)), interpolation = cv.INTER_AREA)
            kneebuf2 = kneebuf1.tostring()
            knee_texture = Texture.create(size=(kneebuf1.shape[1], kneebuf1.shape[0]), colorfmt='bgr')
            knee_texture.blit_buffer(kneebuf2, colorfmt='bgr', bufferfmt='ubyte')

        elif 50 <= kneebend <= 150:

            kneetext = ['With a kneebend angle',
                    'of around {angle} degrees'.format(angle = int(kneebend)),
                    'you have a very solid',
                    'knee bend which acts as',
                    'a good base for driving',
                    'up and generating power.',
                    'It is not too deep which',
                    'might injure your knees',
                    'and neither it too shallow',
                    'which means not enough',
                    'leg drive will be produced']

            for i, line in enumerate(kneetext):
                y = y0 + i*dy
                cv.putText(black2, line, (5, y ), 3, 1, (0,0,0), 2)

            kneebuf1 = cv.flip(black2, 0)
            kneebuf1 = cv.resize(kneebuf1, (int(0.5 * w),int(0.75 * h)), interpolation = cv.INTER_AREA)
            kneebuf2 = kneebuf1.tostring()
            knee_texture = Texture.create(size=(kneebuf1.shape[1], kneebuf1.shape[0]), colorfmt='bgr')
            knee_texture.blit_buffer(kneebuf2, colorfmt='bgr', bufferfmt='ubyte')

        elif kneebend < 50:

            kneetext = ['With a kneebend angle of',
                        'around {angle} degrees you'.format(angle = int(kneebend)),
                        'have a very deep knee',
                        'bend. In other words, you',
                        'are bending your knees',
                        'too much which means you',
                        'have the potential to',
                        'injure yourself from repeti-',
                        'tive strain on the knees.']

            for i, line in enumerate(kneetext):
                y = y0 + i*dy
                cv.putText(black2, line, (5, y ), 3, 1, (0,0,0), 2)

            kneebuf1 = cv.flip(black2, 0)
            kneebuf1 = cv.resize(kneebuf1, (int(0.5 * w),int(0.75 * h)), interpolation = cv.INTER_AREA)
            kneebuf2 = kneebuf1.tostring()
            knee_texture = Texture.create(size=(kneebuf1.shape[1], kneebuf1.shape[0]), colorfmt='bgr')
            knee_texture.blit_buffer(kneebuf2, colorfmt='bgr', bufferfmt='ubyte')

        #cv.imshow('Knee', knee)
        #cv.waitKey(0)
        buf1 = cv.flip(knee, 0)
        buf1 = cv.resize(buf1, (int(w/2),h), interpolation = cv.INTER_AREA)
        buf2 = buf1.tostring()
        kneeimage_texture = Texture.create(size=(buf1.shape[1], buf1.shape[0]), colorfmt='bgr')
        kneeimage_texture.blit_buffer(buf2, colorfmt='bgr', bufferfmt='ubyte')

        #Add buttons to the float layout screen NOT THE POPUP SCREEN

        class Window2(Screen):

            def __init__(self, **kwargs):
                super(Window2, self).__init__(**kwargs)

                fl2 = FloatLayout()

                fl2.add_widget(Image(pos_hint = {"x": 0, 'y':0}, size_hint = (0.5,1), texture = kneeimage_texture))
                fl2.add_widget(Image(pos_hint = {"x": 0.5, 'y':0.25}, size_hint = (0.5,0.75), texture = knee_texture))
                prev2 = Button(text = 'Previous Slide', size_hint =(0.25,0.25), pos_hint = {"x": 0.5, 'y':0})
                prev2.bind(on_release = self.prev2)

                next2 = Button(text = 'Next Slide', size_hint =(0.25,0.25), pos_hint = {"x": 0.75, 'y':0})
                next2.bind(on_release = self.next2)
                fl2.add_widget(prev2)
                fl2.add_widget(next2)

                self.add_widget(fl2)

            def prev2(self,instance):
                smanager = self.manager
                smanager.current = 'first'
                smanager.transition.direction = "right"

            def next2(self,instance):
                smanager = self.manager
                smanager.current = 'third'
                smanager.transition.direction = "left"

            pass

        #Screen 3

        shouldertext = ['The shoulder over shoulder',
                'motion is very important',
                'for generating power. At',
                'the beginning of the serve',
                'the shoulder of the non-',
                'dominant hand should be',
                'above the shoulder of the',
                'dominant hand. Click on',
                'the "Analyze" button below',
                'to get the details on how',
                'well you do this motion']

        for i, line in enumerate(shouldertext):
            y = y0 + i*dy1
            cv.putText(black3, line, (5, y ), 3, 1, (0,0,0), 2)

        shoulderbuf1 = cv.flip(black3, 0)
        shoulderbuf1 = cv.resize(shoulderbuf1, (int(0.5 * w),int(0.5 * h)), interpolation = cv.INTER_AREA)
        shoulderbuf2 = shoulderbuf1.tostring()
        shoulder_texture = Texture.create(size=(shoulderbuf1.shape[1], shoulderbuf1.shape[0]), colorfmt='bgr')
        shoulder_texture.blit_buffer(shoulderbuf2, colorfmt='bgr', bufferfmt='ubyte')

        #if slant  < 20 :


        buf1 = cv.flip(self.shoulder, 0)
        buf1 = cv.resize(buf1, (int(w/2),h), interpolation = cv.INTER_AREA)
        buf2 = buf1.tostring()
        image_texture = Texture.create(size=(buf1.shape[1], buf1.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf2, colorfmt='bgr', bufferfmt='ubyte')

        class Window3(Screen):
            def __init__(self, **kwargs):
                super(Window3, self).__init__(**kwargs)

                fl3 = FloatLayout()

                fl3.add_widget(Image(pos_hint = {"x": 0, 'y':0}, size_hint = (0.5,1), texture = image_texture))
                fl3.add_widget(Image(pos_hint = {"x": 0.5, 'y':0.5}, size_hint = (0.5,0.5), texture = shoulder_texture))

                button3 = Button(text = 'Analyze', size_hint =(0.5,0.25), pos_hint = {"x": 0.5, 'y':0.25})
                button3.bind(on_release = self.show_popup)

                #fl3.add_widget(Button(text = 'Educate Me!', underline = True, pos_hint = {'x':0.5, 'y':0.2}, size_hint = (0.5, 0.2), on_release = self.open3))

                prev3 = Button(text = 'Previous Slide', size_hint =(0.25,0.25), pos_hint = {"x": 0.5, 'y':0})
                prev3.bind(on_release = self.prev3)

                next3 = Button(text = 'Next Slide', size_hint =(0.25,0.25), pos_hint = {"x": 0.75, 'y':0})
                next3.bind(on_release = self.next3)

                fl3.add_widget(button3)
                fl3.add_widget(prev3)
                fl3.add_widget(next3)

                self.add_widget(fl3)

            def prev3(self,instance):
                smanager = self.manager
                smanager.current = 'second'
                smanager.transition.direction = "right"

            def next3(self,instance):
                smanager = self.manager
                smanager.current = 'fourth'
                smanager.transition.direction = "left"

            def open3(self,instance):
                webbrowser.open('https://youtu.be/YkmZXYVgKjE')

            def show_popup(self,instance):
                y0,dy = 30, 40
                black = np.zeros((400,1200,3), np.uint8)
                cv.rectangle(black, (0,0), (1200,400), (0,0,255), -1)
                black = black[0:400,0:900]

                w,h = Window.size

                temp3 = FloatLayout()

                content = GridLayout(cols = 1)
                #subcontent = GridLayout(cols = 2)


                #subcontent.add_widget(Image(size = (int(w/2),int(2/3 * h)), texture = image_texture))
                sample = kivy.resources.resource_find('federer2.jpg')
                sample = cv.imread(sample)
                sample = cv.resize(sample,(int(0.5*w),int(0.6*h)), interpolation = cv.INTER_AREA)
                samplebuf1 = cv.flip(sample, 0)
                samplebuf2 = samplebuf1.tostring()
                sample_texture = Texture.create(size=(samplebuf1.shape[1], samplebuf1.shape[0]), colorfmt='bgr')
                sample_texture.blit_buffer(samplebuf2, colorfmt='bgr', bufferfmt='ubyte')
                #subcontent.add_widget(Image(source = sample, size = (int(w/2),int(2/3 * h))))
                #content .add_widget(subcontent)

                temp3.add_widget(Image(pos_hint = {'x':0,'y':0.4}, size_hint = (0.5,0.6), texture = image_texture))
                temp3.add_widget(Image(pos_hint = {'x':0.5,'y':0.4}, size_hint = (0.5,0.6), texture = sample_texture))

                if slant < 25: #Might change and increase this difference

                    slantext = [ 'It seems like you are not doing the shoulder',
                            'over shoulder motion very well. Your shoulders',
                            'are angled horizontally at an angle of {angle} degrees'.format(angle = int(slant)),
                            'which prevents optimal power. To illustrate this,',
                            "compare Roger Federer's serve with your own. You",
                            'can see how his shoulders are angled upwards and',
                            'more vertically. To improve your shoulder over',
                            "shoulder motion, click on the 'Learn More!' button",
                            'below.']

                    for i, line in enumerate(slantext):
                        y = y0 + i*dy
                        cv.putText(black, line, (5, y ), 3, 1, (0,0,0), 2)

                    slantbuf1 = cv.flip(black, 0)
                    slantbuf1 = cv.resize(slantbuf1, (int(w),int(0.29*h)), interpolation = cv.INTER_AREA)
                    slantbuf2 = slantbuf1.tostring()
                    slant_texture = Texture.create(size=(slantbuf1.shape[1], slantbuf1.shape[0]), colorfmt='bgr')
                    slant_texture.blit_buffer(slantbuf2, colorfmt='bgr', bufferfmt='ubyte')

                else:

                    slantext = [   'It seems like you are doing the shoulder over',
                                    'shoulder motion very well! Your shoulders',
                                    'are angled or slanted at an angle of {angle} degrees'.format(angle = int(slant)),
                                    'which allows you to reach optimal power and',
                                    "accuracy. To illustrate this compare Federer's",
                                    "serve  to the right with your own. You can see",
                                    'how his shoulders are angled and slanted just',
                                    'like yours as shown by the red line. For more',
                                    'information on shoulder over shoulder, click on',
                                    "the 'Learn More!' button below!"] #Remove the links phrase and add red line to image
                    for i, line in enumerate(slantext):
                        y = y0 + i*dy
                        cv.putText(black, line, (5, y ), 3, 1, (0,0,0), 2)

                    slantbuf1 = cv.flip(black, 0)
                    slantbuf1 = cv.resize(slantbuf1, (int(w),int(0.29 * h)), interpolation = cv.INTER_AREA)
                    slantbuf2 = slantbuf1.tostring()
                    slant_texture = Texture.create(size=(slantbuf1.shape[1], slantbuf1.shape[0]), colorfmt='bgr')
                    slant_texture.blit_buffer(slantbuf2, colorfmt='bgr', bufferfmt='ubyte')


                #temp3.add_widget(Image(pos_hint = {"x": 0, 'y':0.2}, size_hint = (1,0.8), texture = slant_texture ))
                #temp3.add_widget(Button(text = 'Click To Find More About This Motion!', underline = True, pos_hint = {"x": 0, 'y':0}, size_hint = (1,0.2)))

                temp3.add_widget(Image(pos_hint = {"x": 0, 'y':0.1}, size_hint = (1,0.3), texture = slant_texture ))
                temp3.add_widget(Button(text = 'Learn More!', underline = True, pos_hint = {'x':0, 'y':0}, size_hint = (1, 0.1), on_release = self.open3))



                content.add_widget(temp3)

                #()
                P = Popup(title = 'Shoulder Over Shoulder For You', content = content, size=(w,h))
                P.open()

            pass

        #Screen 4

        dropbuf1 = cv.flip(self.elbow, 0)
        dropbuf1 = cv.resize(dropbuf1, (int(w/2),h), interpolation = cv.INTER_AREA)
        dropbuf2 = dropbuf1.tostring()
        drop_texture = Texture.create(size=(dropbuf1.shape[1], dropbuf1.shape[0]), colorfmt='bgr')
        drop_texture.blit_buffer(dropbuf2, colorfmt='bgr', bufferfmt='ubyte')

        elbowtext =['During the tennis serve motion, the',
                    'elbow of the hitting arm should be',
                    'high like in the top right image. If',
                    'the elbow drops too much as with the',
                    'bottom left image, you will lose serve',
                    'speed and power. It can also lead to',
                    'more stress on the wrist, elbow and',
                    'shoulder which might result in an',
                    'injury. Click on the "Analyze" button',
                    'below to see if you are guilty of this',
                    'problem!']

        for i, line in enumerate(elbowtext):
            y = y0 + i*dy
            cv.putText(black4, line, (5, y ), 3, 1, (0,0,0), 2)

        elbowbuf1 = cv.flip(black4, 0)
        elbowbuf1 = cv.resize(elbowbuf1, (int(w/2),int(h/2)), interpolation = cv.INTER_AREA)
        elbowbuf2 = elbowbuf1.tostring()
        elbow_texture = Texture.create(size=(elbowbuf1.shape[1], elbowbuf1.shape[0]), colorfmt='bgr')
        elbow_texture.blit_buffer(elbowbuf2, colorfmt='bgr', bufferfmt='ubyte')

        class Window4(Screen):
            def __init__(self, **kwargs):
                super(Window4, self).__init__(**kwargs)

                fl4 = FloatLayout()

                fl4.add_widget(Image(pos_hint = {"x": 0, 'y':0}, size_hint = (0.5,0.5), source = kivy.resources.resource_find('bad.png')))
                fl4.add_widget(Image(pos_hint = {"x": 0, 'y':0.5}, size_hint = (0.5,0.5), source = kivy.resources.resource_find('good.png')))
                fl4.add_widget(Image(pos_hint = {"x": 0.5, 'y':0.5}, size_hint = (0.5,0.5), texture = elbow_texture))

                button4 = Button(text = 'Analyze', size_hint =(0.5,0.25), pos_hint = {"x": 0.5, 'y':0.25})
                button4.bind(on_release = self.show_popup4)

                prev4 = Button(text = 'Previous Slide', size_hint =(0.5,0.25), pos_hint = {"x": 0.5, 'y':0})
                prev4.bind(on_release = self.prev4)

                #next4 = Button(text = 'Next Slide', size_hint =(0.25,0.25), pos_hint = {"x": 0.75, 'y':0})
                #next4.bind(on_release = self.next3)

                fl4.add_widget(button4)
                fl4.add_widget(prev4)
                #fl4.add_widget(next4)

                self.add_widget(fl4)

            def prev4(self,instance):
                smanager = self.manager
                smanager.current = 'third'
                smanager.transition.direction = "right"

            #def next4(self,instance):
                #smanager = self.manager
                #smanager.current = 'fifth'
                #smanager.transition.direction = "left"
            def open4(self,instance):
                webbrowser.open('http://www.racquetfit.com/articles/Coaching/how_your_body_may_be_responsible_for_low_elbow_in_the_tennis_serve')

            def show_popup4(self, instance):

                y0,dy = 30, 40
                black = np.zeros((400,1200,3), np.uint8)
                cv.rectangle(black, (0,0), (1200,400), (0,0,255), -1)
                black = black[0:400,0:900]

                w,h = Window.size
                temp4 = FloatLayout()

                content = GridLayout(cols = 1)

                if overunder == 'High':

                    sample = kivy.resources.resource_find('good.png')
                    sample = cv.imread(sample)
                    sample = cv.resize(sample,(int(0.5*w),int(0.6*h)), interpolation = cv.INTER_AREA)
                    samplebuf1 = cv.flip(sample, 0)
                    samplebuf2 = samplebuf1.tostring()
                    sample_texture = Texture.create(size=(samplebuf1.shape[1], samplebuf1.shape[0]), colorfmt='bgr')
                    sample_texture.blit_buffer(samplebuf2, colorfmt='bgr', bufferfmt='ubyte')

                    elbowtext = [   "Your elbow is not dropping significantly below",
                                    'your shoulders! Therefore, you are free from a',
                                    'very common tennis problem! Your technique in',
                                    'this aspect is just like the model photo to the',
                                    "right! All in all you have nothing to worry about",
                                    'when it comes to the elbow drop! If you want to',
                                    'find out more about this issue, click on the',
                                    '"Learn More!" button below.']

                    for i, line in enumerate(elbowtext):
                        y = y0 + i*dy
                        cv.putText(black, line, (5, y ), 3, 1, (0,0,0), 2)

                    elbowbuf1 = cv.flip(black, 0)
                    elbowbuf1 = cv.resize(elbowbuf1, (int(w),int(h/3)), interpolation = cv.INTER_AREA)
                    elbowbuf2 = elbowbuf1.tostring()
                    elbow_texture = Texture.create(size=(elbowbuf1.shape[1], elbowbuf1.shape[0]), colorfmt='bgr')
                    elbow_texture.blit_buffer(elbowbuf2, colorfmt='bgr', bufferfmt='ubyte')

                if overunder == 'Low':

                    sample = kivy.resources.resource_find('bad.png')
                    sample = cv.imread(sample)
                    sample = cv.resize(sample,(int(0.5*w),int(0.6*h)), interpolation = cv.INTER_AREA)
                    samplebuf1 = cv.flip(sample, 0)
                    samplebuf2 = samplebuf1.tostring()
                    sample_texture = Texture.create(size=(samplebuf1.shape[1], samplebuf1.shape[0]), colorfmt='bgr')
                    sample_texture.blit_buffer(samplebuf2, colorfmt='bgr', bufferfmt='ubyte')


                    elbowtext = [   "As you can see from the image to the left,",
                                    'your elbow is dropping too much which is',
                                    'restricting you from reaching your full serve',
                                    'potential. It can also lead to injuries down',
                                    "the line. To correct this issue, I would",
                                    'click on the "Learn More!" button below.',
                                    'http/oogogog' ]

                    for i, line in enumerate(elbowtext):
                        y = y0 + i*dy
                        cv.putText(black, line, (5, y ), 3, 1, (0,0,0), 2)

                    elbowbuf1 = cv.flip(black, 0)
                    elbowbuf1 = cv.resize(elbowbuf1, (int(w),int(h/3)), interpolation = cv.INTER_AREA)
                    elbowbuf2 = elbowbuf1.tostring()
                    elbow_texture = Texture.create(size=(elbowbuf1.shape[1], elbowbuf1.shape[0]), colorfmt='bgr')
                    elbow_texture.blit_buffer(elbowbuf2, colorfmt='bgr', bufferfmt='ubyte')

                temp4.add_widget(Image(pos_hint = {'x':0,'y':0.4}, size_hint = (0.5,0.6), texture = drop_texture))
                temp4.add_widget(Image(pos_hint = {'x':0.5,'y':0.4}, size_hint = (0.5,0.6), texture = sample_texture))
                temp4.add_widget(Image(pos_hint = {"x": 0, 'y':0.1}, size_hint = (1,0.3), texture = elbow_texture ))
                temp4.add_widget(Button(text = 'Learn More!', underline = True, pos_hint = {'x':0, 'y':0}, size_hint = (1, 0.1), on_release = self.open4))

                content.add_widget(temp4)

                P = Popup(title = 'Your Elbow Drop', content = content, size=(800,800))
                P.open()



        smanager = self.manager

        self.window2 = Window2(name = 'second')
        self.window3 = Window3(name='third')
        self.window4 = Window4(name='fourth')

        smanager.add_widget(self.window2)
        smanager.add_widget(self.window3)
        smanager.add_widget(self.window4)

        smanager.current = 'second'
        smanager.transition.direction = "left"

    def contact(self):

        smanager = self.manager
        try:
            smanager.remove_widget(self.window2)
            smanager.remove_widget(self.window3)
            smanager.remove_widget(self.window4)
        except:
            pass


        self.next1.bind(on_release = self.next11)

        black = np.zeros((750,500,3), np.uint8)
        cv.rectangle(black, (0,0), (500,750), (0,0,255), -1)
        y0, dy = 50, 50

        black2 = black.copy()

        black3 = np.zeros((750,500,3), np.uint8)
        cv.rectangle(black3, (0,0), (500,750), (0,0,255), -1)

        black33 = black3.copy()

        black4 = np.zeros((500,700,3), np.uint8)
        cv.rectangle(black4, (0,0), (700,500), (0,0,255), -1)
        y0, dy = 50, 40

        #If someone types in incorrect or blank data, print out an error message
        #Add a button that shows a Popup for the users to compare their trophy positions with the pros

        path = str(self.filepath.text)
        fps = float(self.fps.text)
        dominant = str(self.dominant.text)

        protoFile = kivy.resources.resource_find('pose_deploy_linevec.prototxt') #COCO model used(more accurate/but slower)
        weightsFile = kivy.resources.resource_find('pose_iter_440000.caffemodel')

        #This gives you the path to files within your app so they can be used on any computer
        #Without using kivy.resources.resource_finder('nameoffile'), IT WON't WORK!!
        #protoFile = kivy.resources.resource_find('pose_deploy_linevec.prototxt') #COCO model used(more accurate/but slower)
        #weightsFile = kivy.resources.resource_find('pose_iter_440000.caffemodel') #COCO model used(more accurate/but slower)
        #Measure how long it's gonna take depending on number of frames of video
        self.big = pose.frames(path,fps)
        armbend, realframe, realpoints, slant2, realframe1 = pose.contact(self.big[3], dominant, protoFile, weightsFile)

        if slant2 >= 90:

            slant2 = 180 - slant2

        w,h = Window.size

        armtext =  ['During The Contact Point',
                    'of the serve your arm',
                    'needs to be completely stra',
                    '-ight in order to generate',
                    'effortless power. Click on',
                    'the "Analyze" button below',
                    "to find out if you're doing",
                    'this part of the serve well!']

        for i, line in enumerate(armtext):
            y = y0 + i*dy
            cv.putText(black3, line, (5, y ), 3, 1, (0,0,0), 2)

        armbuf1 = cv.flip(black3, 0)
        armbuf1 = cv.resize(armbuf1, (int(0.5 * w),int(0.5 * h)), interpolation = cv.INTER_AREA)
        armbuf2 = armbuf1.tostring()
        arm_texture = Texture.create(size=(armbuf1.shape[1], armbuf1.shape[0]), colorfmt='bgr')
        arm_texture.blit_buffer(armbuf2, colorfmt='bgr', bufferfmt='ubyte')

        #if slant  < 20 :


        buf1 = cv.flip(realframe, 0)
        buf1 = cv.resize(buf1, (int(w/2),h), interpolation = cv.INTER_AREA)
        buf2 = buf1.tostring()
        image_texture = Texture.create(size=(buf1.shape[1], buf1.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf2, colorfmt='bgr', bufferfmt='ubyte')

        class Window5(Screen):
            def __init__(self, **kwargs):
                super(Window5, self).__init__(**kwargs)

                fl5 = FloatLayout()

                fl5.add_widget(Image(pos_hint = {"x": 0, 'y':0}, size_hint = (0.5,1), texture = image_texture))
                fl5.add_widget(Image(pos_hint = {"x": 0.5, 'y':0.5}, size_hint = (0.5,0.5), texture = arm_texture))

                button5 = Button(text = 'Analyze', size_hint =(0.5,0.25), pos_hint = {"x": 0.5, 'y':0.25})
                button5.bind(on_release = self.show_popup)

                prev5 = Button(text = 'Previous Slide', size_hint =(0.25,0.25), pos_hint = {"x": 0.5, 'y':0})
                prev5.bind(on_release = self.prev5)

                next5 = Button(text = 'Next Slide', size_hint =(0.25,0.25), pos_hint = {"x": 0.75, 'y':0})
                next5.bind(on_release = self.next5)

                fl5.add_widget(button5)
                fl5.add_widget(prev5)
                fl5.add_widget(next5)

                self.add_widget(fl5)

            def prev5(self,instance):
                smanager = self.manager
                smanager.current = 'first'
                smanager.transition.direction = "right"

            def next5(self,instance):
                smanager = self.manager
                smanager.current = 'third'
                smanager.transition.direction = "left"

            def show_popup(self,instance):
                y0,dy = 30, 40
                black = np.zeros((400,1200,3), np.uint8)
                cv.rectangle(black, (0,0), (1200,400), (0,0,255), -1)
                black = black[0:400,0:900]

                w,h = Window.size

                content = GridLayout(cols = 1)
                subcontent = GridLayout(cols = 2)


                subcontent.add_widget(Image(size = (int(w/2),int(2/3 * h)), texture = image_texture))
                sample = kivy.resources.resource_find('federercontact.png')
                subcontent.add_widget(Image(source = sample, size = (int(w/2),int(2/3 * h))))
                content .add_widget(subcontent)

                if armbend >= 150: #Might change and increase this difference

                    straighttext = ['With a slight bend of around {angle} degrees, your'.format(angle = int(180-armbend)),
                                    'arm appears to be relatively straight throughout',
                                    'the contact point! It seems you are all set and',
                                    'for this part of the serve. But by all means,',
                                    "check for your self and compare with image of",
                                    'Roger Federer to the right. It is very possible',
                                    'for errors to occure during this phase!']

                    for i, line in enumerate(straighttext):
                        y = y0 + i*dy
                        cv.putText(black, line, (5, y ), 3, 1, (0,0,0), 2)

                    straightbuf1 = cv.flip(black, 0)
                    straightbuf1 = cv.resize(straightbuf1, (int(w),int(1/3 * h)), interpolation = cv.INTER_AREA)
                    straightbuf2 = straightbuf1.tostring()
                    straight_texture = Texture.create(size=(straightbuf1.shape[1], straightbuf1.shape[0]), colorfmt='bgr')
                    straight_texture.blit_buffer(straightbuf2, colorfmt='bgr', bufferfmt='ubyte')

                else:

                    straighttext = [    'Judging from the photo to the right, you are',
                                        'bending your arm too much during the contact',
                                        'point. To be specific, you are bending your',
                                        'arm by nearly 34 degrees. So you need to work'.format(angle = int(180 - armbend)),
                                        "more on keeping your arm straight throughout",
                                        "contact. But by all means, please compare",
                                        'yourself with the image of Roger Federer to',
                                        'the right. It is very possible for the program',
                                        'to make mistakes and inaccurate judgements in',
                                        'this phase of the serve!']

                    for i, line in enumerate(straighttext):
                        y = y0 + i*dy
                        cv.putText(black, line, (5, y ), 3, 1, (0,0,0), 2)

                    straightbuf1 = cv.flip(black, 0)
                    straightbuf1 = cv.resize(straightbuf1, (int(w),int(1/3 * h)), interpolation = cv.INTER_AREA)
                    straightbuf2 = straightbuf1.tostring()
                    straight_texture = Texture.create(size=(straightbuf1.shape[1], straightbuf1.shape[0]), colorfmt='bgr')
                    straight_texture.blit_buffer(straightbuf2, colorfmt='bgr', bufferfmt='ubyte')

                content.add_widget(Image(size=(int(w),int(1/3 * h)),texture = straight_texture ))


                P = Popup(title = 'Shoulder Over Shoulder For You', content = content, size=(800,800))
                P.open()

            pass

        #SHoulda Pve SHoulda

        shouldertext = ['Just like in the trophy pos',
                        '-ition, the shoulder over',
                        'shoulder motion is also',
                        'essential throughout the',
                        'contact point. It helps',
                        'in generating effortless',
                        'power. Click on the analy-',
                        '-ze button below to see',
                        'an image of how well you',
                        'do this motion!']

        for i, line in enumerate(shouldertext):
            y = y0 + i*dy
            cv.putText(black33, line, (5, y ), 3, 1, (0,0,0), 2)

        shoulderbuf1 = cv.flip(black33, 0)
        shoulderbuf1 = cv.resize(shoulderbuf1, (int(0.5 * w),int(0.5 * h)), interpolation = cv.INTER_AREA)
        shoulderbuf2 = shoulderbuf1.tostring()
        shoulder_texture = Texture.create(size=(shoulderbuf1.shape[1], shoulderbuf1.shape[0]), colorfmt='bgr')
        shoulder_texture.blit_buffer(shoulderbuf2, colorfmt='bgr', bufferfmt='ubyte')

        #if slant  < 20 :


        buf1 = cv.flip(realframe1, 0)
        buf1 = cv.resize(buf1, (int(w/2),h), interpolation = cv.INTER_AREA)
        buf2 = buf1.tostring()
        simage_texture = Texture.create(size=(buf1.shape[1], buf1.shape[0]), colorfmt='bgr')
        simage_texture.blit_buffer(buf2, colorfmt='bgr', bufferfmt='ubyte')

        class Window6(Screen):
            def __init__(self, **kwargs):
                super(Window6, self).__init__(**kwargs)

                fl6 = FloatLayout()

                fl6.add_widget(Image(pos_hint = {"x": 0, 'y':0}, size_hint = (0.5,1), texture = simage_texture))
                fl6.add_widget(Image(pos_hint = {"x": 0.5, 'y':0.5}, size_hint = (0.5,0.5), texture = shoulder_texture))

                button6 = Button(text = 'Analyze', size_hint =(0.5,0.25), pos_hint = {"x": 0.5, 'y':0.25})
                button6.bind(on_release = self.show_popup)

                prev6 = Button(text = 'Previous Slide', size_hint =(0.5,0.25), pos_hint = {"x": 0.5, 'y':0})
                prev6.bind(on_release = self.prev6)

                #next6 = Button(text = 'Next Slide', size_hint =(0.25,0.25), pos_hint = {"x": 0.75, 'y':0})
                #next6.bind(on_release = self.next6)

                fl6.add_widget(button6)
                fl6.add_widget(prev6)
                #fl6.add_widget(next6)

                self.add_widget(fl6)

            def prev6(self,instance):
                smanager = self.manager
                smanager.current = 'second'
                smanager.transition.direction = "right"

            def next6(self,instance):
                smanager = self.manager
                smanager.current = 'fourth'
                smanager.transition.direction = "left"

            def show_popup(self,instance):

                y0,dy = 30, 40
                black = np.zeros((400,1200,3), np.uint8)
                cv.rectangle(black, (0,0), (1200,400), (0,0,255), -1)
                black = black[0:400,0:900]

                w,h = Window.size

                content = GridLayout(cols = 1)
                subcontent = GridLayout(cols = 2)


                subcontent.add_widget(Image(size = (int(w/2),int(2/3 * h)), texture = simage_texture))
                sample = kivy.resources.resource_find('shoulderscontact.png')
                subcontent.add_widget(Image(source = sample, size = (int(w/2),int(2/3 * h))))
                content .add_widget(subcontent)

                if slant2 < 25: #Might change and increase this difference

                    slanttext = ['It seems like you are not doing the shoulder over',
                                    'shoulder motion very well. As you can see from',
                                    'photo to the left, your shoulders are angled more',
                                    'horizontally at an angle of around {angle} degrees.'.format(angle = int(slant2)),
                                    "If you feel like the program has made a mistake,",
                                    'pleae compare yourself with the image of Roger',
                                    'Federer to the right, you can see that his',
                                    'shoulders are angled more vertically. To correct',
                                    'this issue, check out the following link:',
                                    'htttps:oogabooga'] #Add the link

                    for i, line in enumerate(slanttext):
                        y = y0 + i*dy
                        cv.putText(black, line, (5, y ), 3, 1, (0,0,0), 2)

                    slantbuf1 = cv.flip(black, 0)
                    slantbuf1 = cv.resize(slantbuf1, (int(w),int(1/3 * h)), interpolation = cv.INTER_AREA)
                    slantbuf2 = slantbuf1.tostring()
                    slant_texture = Texture.create(size=(slantbuf1.shape[1], slantbuf1.shape[0]), colorfmt='bgr')
                    slant_texture.blit_buffer(slantbuf2, colorfmt='bgr', bufferfmt='ubyte')

                else:

                    slanttext = ['You are doing great! From the picture to the left,',
                                    'it seems like you are doing the shoulder over',
                                    'shoulder motion correctly! You can compare your-',
                                    '-self with the image of Roger Federer to the right.',
                                    "You can see how the shoulder of his dominant",
                                    'hand is over and above the shoulder of his',
                                    'non-dominant hand(just like you!)']

                    for i, line in enumerate(slanttext):
                        y = y0 + i*dy
                        cv.putText(black, line, (5, y ), 3, 1, (0,0,0), 2)

                    slantbuf1 = cv.flip(black, 0)
                    slantbuf1 = cv.resize(slantbuf1, (int(w),int(1/3 * h)), interpolation = cv.INTER_AREA)
                    slantbuf2 = slantbuf1.tostring()
                    slant_texture = Texture.create(size=(slantbuf1.shape[1], slantbuf1.shape[0]), colorfmt='bgr')
                    slant_texture.blit_buffer(slantbuf2, colorfmt='bgr', bufferfmt='ubyte')

                content.add_widget(Image(size=(int(w),int(1/3 * h)),texture = slant_texture ))


                P = Popup(title = 'Shoulder Over Shoulder For You', content = content, size=(800,800))
                P.open()

            pass

        self.window22 = Window5(name = 'second')
        self.window23 = Window6(name = 'third')
        smanager = self.manager
        smanager.add_widget(self.window22)
        smanager.add_widget(self.window23)
        smanager.current = 'second'
        smanager.transition.direction = "left"


    def next11(self,instance):
        smanager = self.manager
        smanager.current = 'second'
        smanager.transition.direction = "left"


kv = Builder.load_file("tech.kv")

class TechApp(App):
    def build(self):

        return kv


if __name__ == "__main__":
    TechApp().run()

#Ok now you SHOULD do the 45 degrees in front of the player
#because behind the player, the racket may come in front which prevents detecting shoulders
