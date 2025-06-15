from sounds import SoundManager
import pygame as pg
import sys, time
from bird import Bird
from pipe import Pipe
pg.init()

class Game :
    def __init__(self) :
        # Setting Window Configuration
        self.width = 600
        self.height = 768
        self.scale_factor = 1.0012
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.move_speed = 500
        self.start_monitoring = False
        self.score = 0
        self.font = pg.font.Font("images/font.ttf", 24)
        self.score_text = self.font.render("Score : 0", True, (0, 0, 0))
        self.score_text_rect = self.score_text.get_rect(center = (100, 30))
        self.restart_text = self.font.render("Restart", True, (0, 0, 0))
        self.restart_text_rect = self.restart_text.get_rect(center = (300, 700))
        self.bird = Bird(self.scale_factor)
        self.is_enter_pressed = False
        self.is_game_started = True
        self.pipes = []
        self.pipe_generate_counter = 0
        self.setUpBackgroundAndGround()
        self.sound_manager = SoundManager()
        self.high_score = self.loadHighScore()
        self.has_hit_played = False
        self.gameLoop()

    def gameLoop(self) :
        last_time = time.time()
        while True :
            # Calculating Delta Time
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get() :
                if event.type == pg.QUIT :
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and self.is_game_started :
                    if event.key == pg.K_RETURN :
                        self.is_enter_pressed = True
                        self.bird.update_on = True
                    if event.key == pg.K_SPACE and self.is_enter_pressed :
                        self.bird.flap(dt)
                if event.type == pg.MOUSEBUTTONUP :
                    if self.restart_text_rect.collidepoint(pg.mouse.get_pos()) :
                        self.restartGame()             

            self.updateEverything(dt)
            self.checkCollisions()
            self.checkScore()
            self.drawEverything()        
            pg.display.update()
            self.clock.tick(60)

    def restartGame(self) :
        self.score = 0
        self.score_text = self.font.render("Score : 0", True, (0, 0, 0))
        self.is_enter_pressed = False
        self.is_game_started = True
        self.bird.resetPosition()
        self.pipes.clear()
        self.pipe_generate_counter = 71
        self.bird.update_on = False
        self.has_hit_played = False
            
    def checkScore(self) :
        if len(self.pipes) > 0 :
            if (self.bird.rect.left > self.pipes[0].rect_down.left and 
            self.bird.rect.right < self.pipes[0].rect_down.right and not self.start_monitoring) :
                self.start_monitoring = True 
            if self.bird.rect.left > self.pipes[0].rect_down.right and self.start_monitoring :
                self.start_monitoring = False
                self.score += 1
                self.score_text = self.font.render(f"Score : {self.score}", True, (0, 0, 0))  
                self.sound_manager.play_point()        

    def checkCollisions(self):
        if len(self.pipes):
            collision_happened = False
            if self.bird.rect.bottom > 540 :
                collision_happened = True
            if(self.bird.rect.colliderect(self.pipes[0].rect_down) or
            self.bird.rect.colliderect(self.pipes[0].rect_up)) : 
                collision_happened = True
            if collision_happened :     
                if not self.has_hit_played:
                    self.sound_manager.play_hit()
                    self.has_hit_played = True
                    self.is_enter_pressed = False
                    self.is_game_started = False
                    self.bird.update_on = False

                    if self.score > self.high_score : self.high_score = self.score
                    with open("highscore.txt", "w") as file :
                        file.write(str(self.high_score))

    def gameOver(self) :
        game_over_font = pg.font.Font("images/font.ttf", 48)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(300, 300))                
        self.win.blit(game_over_text, game_over_rect)

    def loadHighScore(self) :
        try :
            with open("highscore.txt", "r") as file :
                return int(file.read())
        except :
            return 0    

    def updateEverything(self, dt) :
        if self.is_enter_pressed :
            # Moving The Ground
            self.ground1_rect.x -= int(self.move_speed*dt)
            self.ground2_rect.x -= int(self.move_speed*dt)

            if self.ground1_rect.right < 0 :
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right < 0 :
                self.ground2_rect.x = self.ground1_rect.right
            
            # Generating Pipes
            if self.pipe_generate_counter > 70 :
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0
            self.pipe_generate_counter += 1
            print("Pipe Created")

            # Moving The Pipes
            for pipe in self.pipes :
                pipe.update(dt)
            # Removing Pipes If Out Of Screen
            if len(self.pipes) != 0 :
                if self.pipes[0].rect_up.right < 0 :
                    self.pipes.pop(0)
                    print("Pipe Removed")
            # Moving The Bird    
        self.bird.update(dt)      


    def drawEverything(self) :
        self.win.blit(self.bg_img, (0, -150))
        for pipe in self.pipes :
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)
        self.win.blit(self.score_text, self.score_text_rect)
        if not self.is_game_started :
            self.gameOver()
            self.win.blit(self.restart_text, self.restart_text_rect)
        high_score_text = self.font.render(f"High Score : {self.high_score}", True, (0, 0, 0))
        self.win.blit(high_score_text, (290, 20))    


    def setUpBackgroundAndGround(self) :
        # For Background and Ground
        self.bg_img = pg.transform.scale_by(pg.image.load("images/background.png").convert(), self.scale_factor)
        self.ground1_img = pg.transform.scale_by(pg.image.load("images/ground.png").convert(), self.scale_factor)
        self.ground2_img = pg.transform.scale_by(pg.image.load("images/ground.png").convert(), self.scale_factor)

        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 540
        self.ground2_rect.y = 540


game = Game()