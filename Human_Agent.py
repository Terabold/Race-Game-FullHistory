import pygame
class Human_Agent:
    def __init__(self):
        self.action = 0  

    def get_Action(self,keys):
            
            if keys[pygame.K_w]:
                self.action = 1  

            elif keys[pygame.K_s]:
                self.action = 2 

            elif keys[pygame.K_a]:
                self.action = 3  

            elif keys[pygame.K_d]:
                self.action = 4  
            else:
                self.action = 0  

            return self.action
    
     

   