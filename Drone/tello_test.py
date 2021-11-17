from easytello import tello
import pygame
from math import sin, cos, radians
import cv2
import threading
import numpy
import time
import asyncio
from tello_asyncio import Tello

async def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)


    drone = tello.Tello()
    print(drone.tello_ip)

    timer = 0

    battery = drone.get_battery()
    height = drone.get_height()
    temp = drone.get_temp()

    #drone.streamon()
    drone.set_speed(100)

        
    while True:

        try:
            #drone.set_speed(0)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        drone.forward(40)
                    elif event.key == pygame.K_s:
                        drone.back(40)
                    elif event.key == pygame.K_d:
                        drone.cw(30)
                    elif event.key == pygame.K_a:
                        drone.ccw(30)
                    elif event.key == pygame.K_e:
                        drone.up(40)
                    elif event.key == pygame.K_q:
                        drone.down(40)
                    elif event.key == pygame.K_z:
                        drone.flip("l")
                    elif event.key == pygame.K_x:
                        drone.flip("r")
                    elif event.key == pygame.K_t:
                        drone.takeoff()
                    elif event.key == pygame.K_m:
                        drone.up(120)
                        drone.cw(int(input("How many degrees clockwise till target? ")))
                        drone.forward(200)
                        drone.cww(270)
                        drone.forward(200)
                        drone.ccw(270)
                        drone.forward(200)
                        drone.ccw(270)
                        drone.forward(230)
                    elif event.key == pygame.K_r:
                         drone.land()

        except:
            drone.land()

       
        timer = timer + 1

        if timer % 80 == 0:
            battery = drone.get_battery()
            height = drone.get_height()
            temp = drone.get_temp()

        screen.fill((0, 0, 0))
        battery_text = font.render("Battery: " + str(battery) + "%", False, (255, 255, 255))
        screen.blit(battery_text, (WIDTH/2 - battery_text.get_size()[0]/2, HEIGHT/7))

        height_text = font.render("Height: " + str(height), False, (255, 255, 255))
        screen.blit(height_text, (WIDTH/2 - height_text.get_size()[0]/2, 3*HEIGHT/7))

        temp_text = font.render("Temperature: " + str(temp) + "F", False, (255, 255, 255))
        screen.blit(temp_text, (WIDTH/2 - temp_text.get_size()[0]/2, 5*HEIGHT/7))

        pygame.display.update()
        clock.tick(2)
asyncio.run(main())