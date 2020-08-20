import random
import pygame
import time

pygame.init()

black_blue = (0, 0, 50)
white = (255, 240, 220)
red = (250, 100, 100)
dark_red = (200, 75, 75)

screen_width = 1000
screen_height = 550

font_size = 40
font_normal = pygame.font.SysFont('comicsansms', font_size)  # create font object

pygame.display.set_caption('Memory card')
game_display = pygame.display.set_mode((screen_width, screen_height))

fps = 45
clock = pygame.time.Clock()

card_state = 0

# array
characters = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']*2
card_objects = []
card_covers = []
revealed_covers = []
paired = []
random.shuffle(characters)


def restart_values():
    global card_objects, card_covers, revealed_covers, paired, characters, card_state
    card_objects = []
    card_covers = []
    revealed_covers = []
    paired = []
    random.shuffle(characters)
    card_state = 0


def replay():
    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    restart_values()
                    main()
                elif event.key == pygame.K_s:
                    game_exit = True
                    pygame.quit()
                    quit()
        game_display.fill(black_blue)
        screen_message('Game over. Press c to continue, s to stop.', red)
        pygame.display.update()


def screen_message(text, color, y_displace=0, font=font_normal):
    screen_text = font.render(text, True, color)  # creating the idea of the font
    text_rect = screen_text.get_rect()
    text_rect.center = [int(screen_width/2), int(screen_height/2 + y_displace)]
    game_display.blit(screen_text, text_rect)


class Cards:

    def __init__(self, character, cover, card_x, card_y):
        self.character = character
        self.name_character = self.character[-12]
        self.cover = cover
        self.image = pygame.image.load(character)
        self.cover_img = pygame.image.load(cover)
        self.rect = self.cover_img.get_rect()
        self.rect.x = card_x
        self.rect.y = card_y

    def draw_card(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def draw_cover(self, surface):
        surface.blit(self.cover_img, (self.rect.x, self.rect.y))


def initialize():
    global card_objects
    x = 0
    y = 0
    for i in characters[:int(len(characters)/3)]:  # first row
        images = 'C:/Users/Minh Phuong/PycharmProjects/working38/card_images/{}-spades.png'.format(i)
        cover_card = 'C:/Users/Minh Phuong/PycharmProjects/working38/card_images/card_back.png'
        card = Cards(images, cover_card, x, y)
        x += int(screen_width/16) + 60
        card_objects.append(card)
        card_covers.append(card)

    x = 0
    for i in characters[int(len(characters)/3):int(len(characters)/3)*2]:  # second row
        y = int(screen_height/3)
        images = 'C:/Users/Minh Phuong/PycharmProjects/working38/card_images/{}-spades.png'.format(i)
        cover_card = 'C:/Users/Minh Phuong/PycharmProjects/working38/card_images/card_back.png'
        card = Cards(images, cover_card, x, y)
        x += int(screen_width / 16) + 60
        card_objects.append(card)
        card_covers.append(card)

    x = 0
    for i in characters[int(len(characters) / 3) * 2:]:  # third row
        y = int(screen_height/3)*2
        images = 'C:/Users/Minh Phuong/PycharmProjects/working38/card_images/{}-spades.png'.format(i)
        cover_card = 'C:/Users/Minh Phuong/PycharmProjects/working38/card_images/card_back.png'
        card = Cards(images, cover_card, x, y)
        x += int(screen_width / 16) + 60
        card_objects.append(card)
        card_covers.append(card)


def draw_out():
    for card in card_objects:
        card.draw_card(game_display)
    for cover in card_covers:
        cover.draw_cover(game_display)


def main():
    global card_state, card_covers, revealed_covers
    game_over = False
    initialize()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                clicked_cards = [c for c in card_objects if c.rect.collidepoint(pos)]
                for i in clicked_cards:
                    revealed_covers.append(i)
                    card_covers.remove(i)
                    if card_state == 0:
                        card_state = 1
                    elif card_state == 1:
                        card_state = 2
                    elif card_state == 2:
                        card_state = 1
                        # if i.name_character != revealed_covers[0].name_character and i.name_character != revealed_covers[1].name_character:
                        if revealed_covers[0].name_character != revealed_covers[1].name_character:
                            card_covers.append(revealed_covers[0])
                            card_covers.append(revealed_covers[1])
                            del revealed_covers[:2]
                        else:
                            del revealed_covers[:2]
                        # elif i.name_character == revealed_covers[0].name_character and revealed_covers[0].name_character != revealed_covers[1].name_character:
                        #     card_covers.append(revealed_covers[1])
                        #     del revealed_covers[0]
                        #     del revealed_covers[revealed_covers.index(i)]
                        # elif i.name_character == revealed_covers[1].name_character and revealed_covers[0].name_character != revealed_covers[1].name_character:
                        #     card_covers.append(revealed_covers[0])
                        #     del revealed_covers[1]
                        #     del revealed_covers[revealed_covers.index(i)]

        if len(card_covers) == 0:
            game_over = True
        game_display.fill(black_blue)
        draw_out()
        pygame.display.update()
        clock.tick(fps)


main()
replay()