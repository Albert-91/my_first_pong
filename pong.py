import pygame
import sys
from pygame.locals import *
import datetime

pygame.init()
WinWidth = 800
WinHeight = 400
WinColor = (230, 255, 255)
WinArea = pygame.display.set_mode((WinWidth, WinHeight), 0, 32)
pygame.display.set_caption("Simple Vertical Pong")

PlaWidth = 20
PlaHeight = 70
PlaColor = (25, 111, 255)
PlaStartPos = (20, 200)
Player1 = pygame.Surface([PlaWidth, PlaHeight])
Player1.fill(PlaColor)
Player1_rect = Player1.get_rect()
Player1_rect.x = PlaStartPos[0]
Player1_rect.y = PlaStartPos[1]

BallWidth = 20
BallHeight = 20
BallSpeed_x = 6
BallSpeed_y = 6
BallColor = (0, 255, 100)

ball = pygame.Surface([BallWidth, BallHeight], pygame.SRCALPHA, 32).convert_alpha(WinArea)
pygame.draw.ellipse(ball, BallColor, [0, 0, BallWidth, BallHeight])

BallRect = ball.get_rect()
BallRect.x = WinWidth / 2
BallRect.y = WinHeight / 2

FPS = 50
fpsClock = pygame.time.Clock()

k = 1.03
OpColor = (250, 122, 0)
OpStartPos = (760, 200)
Op = pygame.Surface([PlaWidth, PlaHeight])
Op.fill(OpColor)
OpRect = Op.get_rect()
OpRect.x = OpStartPos[0]
OpRect.y = OpStartPos[1]
OpSpeed = 5

JokColor = (255, 215, 0)
JokStartPos = (400, -70)
Joker = pygame.Surface([PlaWidth, PlaHeight])
Joker.fill(JokColor)
JokRect = Joker.get_rect()
JokRect.x = JokStartPos[0]
JokRect.y = JokStartPos[1]
JokSpeed = 3

PlayersPoint = '0'
OpPoint = '0'
fontObj = pygame.font.Font('freesansbold.ttf', 64)
pygame.key.set_repeat(50, 25)

def printPlayerPoint():
    textPlayer = fontObj.render(PlayersPoint, True, (0, 0, 0))
    TextRectPlayer = textPlayer.get_rect()
    TextRectPlayer.center = (WinWidth * 0.75, WinHeight / 2)
    WinArea.blit (textPlayer, TextRectPlayer)

def printOpPoint():
    textOp = fontObj.render(OpPoint, True, (0, 0, 0))
    TextRectOp = textOp.get_rect()
    TextRectOp.center = (WinWidth / 4, WinHeight / 2)
    WinArea.blit (textOp, TextRectOp)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                Player1_rect.y += 10
                if Player1_rect.y > WinHeight - PlaWidth:
                    Player1_rect.y = WinHeight - PlaWidth
            if event.key == pygame.K_UP:
                Player1_rect.y -= 10
                if Player1_rect.y < 0:
                    Player1_rect.y = 0

    BallRect.move_ip(BallSpeed_x, BallSpeed_y)
    if BallRect.right >= WinWidth:
        BallRect.x = WinWidth / 2
        BallRect.y = WinHeight / 2
        OpPoint = str(int(OpPoint) + 1)
    if BallRect.left <= 0:
        BallRect.x = WinWidth / 2
        BallRect.y = WinHeight / 2
        PlayersPoint = str(int(PlayersPoint) + 1)
    if BallRect.top <= 0:
        BallSpeed_y *= -1

    if BallRect.bottom >= WinHeight:
        BallSpeed_y *= -1

    if BallRect.centery > OpRect.centery:
        OpRect.y += OpSpeed * k
    elif BallRect.centery < OpRect.centery:
        OpRect.y -= OpSpeed

    if BallRect.colliderect(OpRect):
        BallSpeed_x *= -1
        BallRect.right = OpRect.left

    if BallRect.colliderect(Player1_rect):
        BallSpeed_x *= -1 * k
        BallRect.left = Player1_rect.right

    if BallSpeed_x > 0:
        if BallRect.colliderect(JokRect):
            BallSpeed_x *= -1
            BallRect.right = JokRect.left
    else:
        if BallRect.colliderect(JokRect):
            BallSpeed_x *= -1
            BallRect.left = JokRect.right

    if JokSpeed > 0:
        if WinHeight >= JokRect.y >= JokStartPos[1]:
            JokRect.y += JokSpeed
    if JokRect.y >= WinHeight:
        JokRect.y = JokStartPos[1]

    if event.type == MOUSEMOTION:
        mouseX, mouseY = event.pos
        Movement = mouseY - (PlaWidth / 2)
        if Movement > WinHeight - PlaWidth:
            Movement = WinHeight - PlaWidth
        if Movement < 0:
            Movement = 0
        Player1_rect.y = Movement

    WinArea.fill(WinColor)
    printPlayerPoint()
    printOpPoint()
    WinArea.blit(Player1, Player1_rect)
    WinArea.blit(Op, OpRect)
    WinArea.blit(Joker, JokRect)
    WinArea.blit(ball, BallRect)
    pygame.display.update()
    fpsClock.tick(FPS)
