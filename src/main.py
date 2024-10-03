
###########################################################################
#   Goal is to collect more coins than the monster before time runs out!  #
#   Catch the coin and deliver it to you box, but don't let the monster   #
#   steal it from you!                                                    #
##########################################################################


import pygame
import random

class Hahmo:
    def __init__(self,hahmo,x,y,nopeus):
        self.x = x
        self.y = y
        self.nopeus = nopeus
        self.pisteet = 0
        self.carry = False
        self.hahmo = hahmo

    def kanna_kolikko(self):
        if self.carry == False:
            self.carry = True
        else:
            self.carry = False

    def lisaa_piste(self):
        self.pisteet +=1

    #def vaihda_suunta(x,y):
        #self.x = x
        #self.y = y



class Coingame:
    def __init__(self):

        pygame.init()
        self.loppu = False
        self.aika = pygame.time.Clock()
        
        self.lataa_kuvat()

        self.naytto = pygame.display.set_mode((1200, 700))
        self.ylos = False
        self.alas = False
        self.oikea = False
        self.vasen = False
        self.sekunnit = 30
        self.luo_hahmot()
        self.aseta_kolikko()
        self.silmukka()
        self.aika.tick(60)

    def ajastin(self):
        if pygame.time.get_ticks()%1000 == 0:           #get_ticks counts milliseconds
            self.sekunnit -= 1   
        if self.sekunnit == -1:
            self.loppu = True

    def lataa_kuvat(self):
        self.robo = pygame.image.load("src/robo.png")
        self.robo_arkku = pygame.image.load("src/robo.png")

        self.morko = pygame.image.load("src/hirvio.png")
        self.morko_arkku = pygame.image.load("src/hirvio.png")
        self.coin = pygame.image.load("src/kolikko.png")

        self.w_morko = self.morko.get_width()
        self.h_morko = self.morko.get_height()

        self.w_robo = self.robo.get_width()
        self.h_robo = self.robo.get_height()

        self.w_coin = self.coin.get_width()
        self.h_coin = self.coin.get_height() 

    def luo_hahmot(self):

        self.robotti = Hahmo(self.robo,0.75*1200,0.5*700,1)
        self.hirvio = Hahmo(self.morko,0.25*1200,0.5*700,0.5)

    def piirra(self):
        self.naytto.fill((255,255,255))
        fontti = pygame.font.SysFont("Arial", 50)
        pygame.draw.rect(self.naytto, (255,0, 0), (10, 10, 100, 100))
        pygame.draw.rect(self.naytto, (0,255, 0), (1090, 590, 100, 100))
        self.naytto.blit(self.morko_arkku,(10,10))
        self.naytto.blit(self.robo_arkku,(1090,590))
        
        
        self.teksti_morko = fontti.render(f'{self.hirvio.pisteet}', True, (255, 255, 255))
        self.teksti_robo = fontti.render(f'{self.robotti.pisteet}', True, (255, 255, 255))
        self.teksti_timer = fontti.render(f'{"{:02}".format(self.sekunnit)}',True,(0,255,0))
        self.naytto.blit(self.teksti_morko,(10+self.w_morko,10))
        self.naytto.blit(self.teksti_robo,(1090+self.w_robo,590))

        self.naytto.blit(self.teksti_timer,(600-0.5*self.teksti_timer.get_width(),0))
        
        self.naytto.blit(self.coin,(self.x,self.y))

        self.naytto.blit(self.hirvio.hahmo,(self.hirvio.x,self.hirvio.y))
        self.naytto.blit(self.robotti.hahmo,(self.robotti.x,self.robotti.y))

        pygame.display.flip()

    def piirra_loppu(self):
        while self.loppu:
            fontti = pygame.font.SysFont("Arial", 50)
            self.naytto.fill((255,255,255))
            self.teksti_morko = fontti.render(f'{self.hirvio.pisteet}', True, (255, 0, 0))
            self.teksti_robo = fontti.render(f'{self.robotti.pisteet}', True, (0, 255, 0))
            self.naytto.blit(self.morko_arkku,(200,350))
            self.naytto.blit(self.robo_arkku,(700,350))
            self.naytto.blit(self.teksti_morko,(400-self.w_morko*0.5,350))
            self.naytto.blit(self.teksti_robo,(800+self.w_robo,350))
            self.naytto.blit(fontti.render('Esc: Lopeta     Space: Uusi peli',True,(255,0,0)), (100,600))
            if self.robotti.pisteet > self.hirvio.pisteet:
                self.naytto.blit(fontti.render('Voitit pelin!',True,(0,255,0)), (100,100))
            elif self.robotti.pisteet < self.hirvio.pisteet:
                self.naytto.blit(fontti.render('Hävisit pelin!',True,(255,0,0)), (100,100))
            else:
                self.naytto.blit(fontti.render('Tasapeli!',True,(255,0,0)), (100,100))
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE:
                        exit()
                    if tapahtuma.key == pygame.K_SPACE:
                        self.luo_hahmot()
                        self.aseta_kolikko()
                        self.sekunnit = 30
                        self.loppu = False

            pygame.display.flip()
            


    def aseta_kolikko(self):
        self.nopeus_x = 0.5
        self.nopeus_y = 0.5
        self.keratty = False

        self.y = random.randint(0,700-self.h_coin)
        self.x = random.randint(0,1200-self.w_coin)


    def kolikon_liike(self):
        if self.hirvio.carry == False and self.robotti.carry == False:
            if  self.y+self.h_coin >=700:
                self.nopeus_y = -self.nopeus_y
            if self.x+self.w_coin >= 1200:
                self.nopeus_x = -self.nopeus_x
            if  self.y == 0:
                self.nopeus_y = -self.nopeus_y
            if self.x == 0:
                self.nopeus_x = -self.nopeus_x
            self.y += self.nopeus_y
            self.x += self.nopeus_x

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = True
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasen = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikea = True
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasen = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikea = False
            if tapahtuma.type == pygame.QUIT:
                exit()

    
    def liikuta_robottia(self):
        if self.vasen:
            if self.robotti.x > 0:
                self.robotti.x -= self.robotti.nopeus
        if self.oikea:
            if self.robotti.x < 1200-self.w_robo:
                self.robotti.x += self.robotti.nopeus
        if self.ylos:
            if self.robotti.y > 0:
                self.robotti.y -= self.robotti.nopeus
        if self.alas:
            if self.robotti.y < 700-self.h_robo:
                self.robotti.y += self.robotti.nopeus

    def nappaa_kolikko(self):
        
        if (self.robotti.x < self.x + self.w_coin and
            self.robotti.x + self.w_robo > self.x and
            self.robotti.y < self.y + self.h_coin and
            self.robotti.y + self.h_robo > self.y and self.robotti.carry == False and self.keratty ==False):
            self.y = self.robotti.y
            self.x = self.robotti.x
            self.robotti.carry = True
            self.hirvio.carry = False
            self.keratty = True
        
        if self.robotti.carry:
            self.y = self.robotti.y
            self.x = self.robotti.x
        

    def jata_kolikko(self):
        if (self.robotti.x > 1090 and
            self.robotti.y > 590
            and  self.robotti.carry == True):

            self.robotti.lisaa_piste()
            self.keratty = True
            self.aseta_kolikko()
            self.robotti.carry = False
            self.hirvio.carry = False
    

    def morko_nappaa_kolikon(self):

        if (self.hirvio.x < self.x + self.w_coin and
            self.hirvio.x + self.w_morko > self.x and
            self.hirvio.y < self.y + self.h_coin and
            self.hirvio.y + self.h_morko > self.y and self.hirvio.carry == False and self.keratty == False):
            self.y = self.hirvio.y
            self.x = self.hirvio.x
            self.hirvio.carry = True
            self.robotti.carry = False
            self.keratty = True
        
        if self.hirvio.carry:
            self.y = self.hirvio.y
            self.x = self.hirvio.x

    
    def morko_jattaa_kolikon(self):
        if (self.hirvio.x < 110 and
            self.hirvio.y < 110
            and  self.hirvio.carry == True):

            self.hirvio.lisaa_piste()
            self.keratty = True
            self.aseta_kolikko()
            self.robotti.carry = False
            self.hirvio.carry = False

    def hirvion_liike(self):
        if self.hirvio.carry == False:
            if self.hirvio.x > self.x and self.hirvio.x > 0:
                self.hirvio.x -= self.hirvio.nopeus
            if self.hirvio.x < self.x and self.hirvio.x <1200-self.w_morko:
                self.hirvio.x += self.hirvio.nopeus
            if self.hirvio.y > self.y and self.hirvio.y > 0:
                self.hirvio.y -= self.hirvio.nopeus
            if self.hirvio.y < self.y and self.hirvio.y < 700-self.h_morko:
                self.hirvio.y += self.hirvio.nopeus

        else:
            if self.hirvio.x > 50:
                self.hirvio.x -= self.hirvio.nopeus
            if self.hirvio.y > 50:
                self.hirvio.y -= self.hirvio.nopeus
    
    def kaikki_tormaa(self):

        if (self.hirvio.x < self.robotti.x + self.w_robo and
            self.hirvio.x + self.w_morko > self.robotti.x and
            self.hirvio.y < self.robotti.y + self.h_robo and
            self.hirvio.y + self.h_morko > self.robotti.y):
            if self.robotti.carry:
                self.robotti.kanna_kolikko()
                self.hirvio.kanna_kolikko()
            elif self.hirvio.carry:
                self.hirvio.kanna_kolikko()
                self.robotti.kanna_kolikko()

    
    def silmukka(self):
        while True:
            self.ajastin()
            self.kolikon_liike()
            self.tutki_tapahtumat()
            self.liikuta_robottia()
            self.nappaa_kolikko()
            self.jata_kolikko()
            self.hirvion_liike()
            self.morko_nappaa_kolikon()
            self.morko_jattaa_kolikon()
            self.kaikki_tormaa()
            self.piirra()
            if self.loppu:
                self.piirra_loppu()




#####################################################################################################
play = Coingame()

