# THE TIME STARTS RUNNING ON THE FIRST TIME WHEN THE USER CLICK ON THE INPUT BOX , AFTER THE USER PRESS "RESET" THE TIME STARTS AUTOMTICALLY

import pygame
from pygame.locals import *
import sys
import time
import random

# 750 x 500    


class Game:
    
   
    def __init__(self):
        self.w=750
        self.h=500
        self.reset=True
        self.active = False
        self.input_text=''
        self.word = ''
        self.time_start = time.time()
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255,213,102)
        self.TEXT_C = (0,0,0)
        self.RESULT_C = (250,250,250)
        
       
        pygame.init()
        self.open_img = pygame.image.load('type-speed-open.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))
        
        self.bg = pygame.image.load('background.jpg')
        self.bg = pygame.transform.scale(self.bg,(self.w,self.h))


        self.screen = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Type Speed test')

    
    def lang(self,screen):

        self.lang_img = pygame.image.load('language.jpg')
        self.lang_img = pygame.transform.scale(self.lang_img, (self.w,self.h))
        self.screen.blit(self.lang_img,(0,0))

        #Position of the languages text
        self.draw_text(screen,"English", self.w/2 - 120, self.h - 70, 26, (22, 91, 255))
        self.draw_text(screen,"Deutsch", self.w/2 + 120, self.h - 70, 26, (22, 91, 255))

        action = False


        while action == False:

            for event in pygame.event.get():

                x,y = pygame.mouse.get_pos()

                #Position of English language box
                if event.type == pygame.MOUSEBUTTONUP and (x>=220 and x<=285 and y>=415 and y<=450):
                    self.filess = "english.txt"
                    action = True
                
                #Position of German language box
                elif event.type == pygame.MOUSEBUTTONUP and (x>=460 and x<=525 and y>=415 and y<=450):
                    self.filess = "german.txt"
                    action = True

                #To quit the application in the "Choosing Language" window
                elif event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit()

        return self.filess
        
       
        
    def draw_text(self, screen, msg, x, y ,fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    
    def get_sentence(self):
        
        #If the user quitted from the language window it will return AttributeError()
        try:
            f = open(self.filess,'r')
            sentences = f.readlines()
            sentence = random.choice(sentences).strip()
            return sentence

        except:
            sys.exit()


    def show_results(self, screen):

        if not self.end:

            #Calculate time
            self.total_time = time.time() - self.time_start
            
            #Calculate accuracy
            count = 0
            for i,c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.word)*100
           
            #Calculate words per minute
            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)


            self.results = 'Time:'+str(round(self.total_time)) +" secs   Accuracy:"+ str(round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))
            
            #Draw icon image
            self.time_img = pygame.image.load('icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150,150))

            #Display the image behind the "Reset" text
            screen.blit(self.time_img, (self.w/2-75,self.h-140))

            #The poisition of "Reset" text
            self.draw_text(screen,"Reset",self.w/2 ,self.h - 70, 26, (50,50,50))
            
            print(self.results)
            pygame.display.update()


    def run(self):
        self.reset_game()
    
        self.running=True
        while(self.running):
            clock = pygame.time.Clock()

            #Draw the rectangle within the input box
            self.screen.fill((0,0,0), (50,250,650,50))

            #Draw the frame around the rectangle
            pygame.draw.rect(self.screen,self.HEAD_C, (50,250,650,50), 2)

            #Update the characters that the user enters
            self.draw_text(self.screen, self.input_text, self.w/2 ,274, 26,(250,250,250))
            pygame.display.update()

            for event in pygame.event.get():
                
                #To quit the program in the "Typing" window
                if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()

                    #Position of input box
                    if(x>=50 and x<=650 and y>=250 and y<=300):
                        self.active = True
                        self.input_text = ''

                    #Position of "Reset" box
                    if(x>=310 and x<=510 and y>=390 and self.end):
                        self.reset_game()
                        x,y = pygame.mouse.get_pos()
         
                elif event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:

                    if self.active and not self.end:

                        #To submit the user written characters
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, self.w/2, 350, 28, self.RESULT_C)  
                            self.end = True
                        
                        #To remove the user characters
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            
            pygame.display.update()
             
        #Frame rate        
        clock.tick(60)


    def reset_game(self):

        #Print the opening image
        self.screen.blit(self.open_img, (0,0))
        pygame.display.update()

        #Delays the screen
        time.sleep(1)
        
        #Print the window that the user choose the language from
        self.lang(self.screen)

        self.reset=False
        self.end = False
        
        self.input_text=''
        self.word = ''
        self.time_start = time.time()
        self.total_time = 0
        self.wpm = 0

        #Get random sentence from the chosen langauge
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()

        #Draw heading
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg, self.w/2, 80, 80,self.HEAD_C)  

        #Draw the sentence that need to be entered
        self.draw_text(self.screen, self.word, self.w/2, 200, 40,self.TEXT_C)
        
        pygame.display.update()

    


        



Game().run()

