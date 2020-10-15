import pygame
import random
import csv
from pygame import mixer

pygame.init()

# Displaying Screen
width = 800
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minecraft Clicker")

# Game States/Scenes
main_menu = True
display_game_menu = False
shop_menu = False
upgrade_menu = False
setting_menu = False

# Mouse Position
mouse_pos = pygame.mouse.get_pos()

# Call and uncall Events for objects
grass_click_events_call = []
grass_click_events_uncall = []

start_gameB_events_call = []
start_gameB_events_uncall = []

shopB_events_call = []
shopB_events_uncall = []

upgradeB_events_call = []
upgradeB_events_uncall = []

Shop_scroll_barB_events_call = []
Shop_scroll_barB_events_uncall = []

Upgrade_scroll_barB_events_call = []
Upgrade_scroll_barB_events_uncall = []

settingB_events_call = []
settingB_events_uncall = []

settings_Buttons_call = []
settings_Buttons_uncall = []

lucky_block_call = []
lucky_block_uncall = []

# List of types of objects
Clickables = []
Buttons = []
Buy_Boxes = []
Texts = []
Upgrade_Boxes = []
Buy_Box_Price_Icons = []
Icons = []
Glow_Effects = []

# Lists of Objects
Main_Menu_Objects = []

Game_Menu_Objects_Back = []
Game_Menu_Objects = []
Game_Menu_Objects_Front = []
Overlay_Objects = []

Shop_Menu_Objects_Far_Back = []
Shop_Menu_Objects_Back = []
Shop_Menu_Objects_Front = []
Shop_Menu_Objects_Very_Front = []

Upgrade_Menu_Objects_Far_Back = []
Upgrade_Menu_Objects_Back = []
Upgrade_Menu_Objects_Front = []
Upgrade_Menu_Objects_Very_Front = []

Settings_Menu_Objects = []

# Lists of buy_box icons
Pickaxe_Icon_Objects = []
Axe_Icon_Objects = []
Shovel_Icon_Objects = []
Sword_Icon_Objects = []
Hoe_Icon_Objects = []
Shears_Icon_Objects = []
Firecharge_Icon_Objects = []
Bow_Icon_Objects = []
Rod_Icon_Objects = []
Fns_Icon_Objects = []
Tnt_Icon_Objects = []
Beacon_Icon_Objects = []
Creeper_Icon_Objects = []
Fireball_Icon_Objects = []
Crystal_Icon_Objects = []
Dragon_Icon_Objects = []
Wither_Icon_Objects = []

Clickables_Icon_Objects = []

Block_Multi_Objects = []

Price_Reduction_Icon_Objects = []
# Fonts
font_buy_box_name = pygame.font.Font('Fonts/Varela.otf', 27)
header = pygame.font.Font('Fonts/brandon.otf', 30)
font_buy_box_price = pygame.font.Font('Fonts/Varela.otf', 12)
font_upgrade_box_name = pygame.font.Font('Fonts/Varela.otf', 20)
font_click_amount = pygame.font.Font('Fonts/AmericanCaptain.otf', 20)

# Variables
blocks = 0
blocks_per_second = 0
total_blocks = 0
click_multiplier = 1
block_multiplier = 1
non_click_multiplier = 0
times_divided = 0
shopB_toggle = False
upgradeB_toggle = False
soundB_toggle = False
musicB_toggle = False
from_main_menu = False
from_game_menu = False
block_pressed = False
sound_effects_on = True
float_values = []

# Use this to change the number of upgrade boxes blited
upgrade_boxes_active = []

clickables_to_initialize = []
buy_boxes_to_initialize = []
upgrade_boxes_to_initialize = []

icons_to_buy_box_initialize = []
icons_to_upgrade_box_initialize = []
current_clickable_completed = []

upgrade_boxes_beginning_cor = {
    1: 56,
    2: 112,
    3: 168,
    4: 224,
    5: 280,
    6: 336,
    7: 392,
    8: 448,
    9: 504,
    10: 560,
    11: 616,
    12: 672,
    13: 728,
    14: 784,
    15: 840,
    16: 896,
    17: 952,
    18: 1008,
    19: 1064,
    20: 1120,
    21: 1176,
}

# Sounds
pygame.mixer.music.load('Sound and Music/background_music.wav')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

click_effect = mixer.Sound("Sound and Music/click_effect.wav")
menu_click = mixer.Sound("Sound and Music/menu_click.wav")
buy_sound = mixer.Sound("Sound and Music/buy_sound.wav")


class Clickable:
    # The current Clickable object
    global current_Clickable

    def __init__(self, image, name, is_default=False):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = pygame.Rect(0, 0, 200, 200)
        self.center = (width // 2, height // 2)
        self.rect = pygame.Rect(self.center[0] - (self.rect[2] // 2), self.center[1] - (self.rect[3] // 2),
                                self.rect[2], self.rect[3])
        self.name = name
        self.angle = 0
        # Making copies of itself for falling animation
        self.copies = []
        # Adding itself to list of Clickables
        Clickables.append(self)
        self.icon_image = pygame.transform.scale(self.image, (45, 45))
        self.icon = Icon(self.icon_image, (200, 100), Clickables_Icon_Objects, upgrade_box=click_upgrade_box,
                         is_clickable=True, name=self.name + ".icon")

        # Making a hover over version of itself (lighter and slightly bigger)
        self.image_lighter = self.image.copy()
        self.image_lighter = brighten_image(self.image_lighter, 50)
        self.image_lighter = pygame.transform.scale(self.image_lighter,
                                                    (int(self.rect[2] * 1.05), int(self.rect[3] * 1.05)))
        # Making a press down version of itself (darker)
        self.image_darker = self.image.copy()
        self.image_darker = darken_image(self.image_darker, 50)

        # Start by displaying default version of itself
        self.image_to_display = self.image

        # Stating Variables
        self.is_hovering = False
        self.is_pressed_down = False
        self.is_pressed_up = False
        self.initialized = False
        self.called_on = False
        self.completed = False
        self.is_default = is_default
        # Use this for when switching between clickables

        # Adding number of "small_Block" objects to copies list
        for i in range(70):
            self.copies.append(small_Block(self.image, (0, 0, 300, 300), (random.randint(0, width), 10)))

    def __repr__(self):
        return self.name

    # Get the coordinates depending on different state of object (Used for blits)
    def get_center_cor(self):
        if self.is_hovering and not self.is_pressed_down:
            return self.center[0] - ((self.rect[2] * 1.05) // 2), self.center[1] - ((self.rect[3] * 1.05) // 2)
        elif not self.is_hovering or self.is_pressed_down:
            return self.center[0] - (self.rect[2] // 2), self.center[1] - (self.rect[3] // 2)

    # Called upon each tick, calls transform function on each object in copies list
    def descend(self):
        for copy in self.copies:
            self.transform(copy)

    # Called upon each tick, moves the small_Block and rotates them
    def transform(self, copy):
        copy.image_copy = pygame.transform.rotate(copy.image, self.angle)
        self.angle += 0.15
        x, y = copy.rect.center
        copy.rect = copy.image_copy.get_rect()
        # If the object reaches the end of the screen, it comes back up
        if y > height or copy.is_first:
            copy.rect.center = (random.randint(0, width), random.randint(-1000, 10))
            copy.is_first = False
        else:
            copy.rect.center = (x, y + 7)

    # Called upon once per tick
    def state_check(self):
        global mouse_pos
        global current_Clickable
        mouse_pos = pygame.mouse.get_pos()

        # Checks if mouse position is hovering and changes image depending on object state
        if self.initialized and not self.completed:
            if self.rect[0] + self.rect[2] > mouse_pos[0] > self.rect[0] and self.rect[1] + self.rect[3] > mouse_pos[
                1] > \
                    self.rect[1] and not self.is_hovering:
                self.is_hovering = True
            elif not self.rect[0] + self.rect[2] > mouse_pos[0] > self.rect[0] and self.is_hovering or not \
                    self.rect[1] + self.rect[3] > mouse_pos[1] > self.rect[1] and self.is_hovering:
                self.is_hovering = False
            if self.is_pressed_up:
                # Calls upon block click function once
                block_click()
                self.is_pressed_up = False
            if self.is_hovering and not self.is_pressed_down:
                self.image_to_display = self.image_lighter
            elif self.is_pressed_down and self.is_hovering:
                self.image_to_display = self.image_darker
            else:
                self.image_to_display = self.image
        if not self.initialized and self.is_default or not self.initialized and self.called_on:
            self.initialized = True
            clickables_to_initialize.append(self)
            self.called_on = False
            Game_Menu_Objects.append(self)
            Game_Menu_Objects.remove(current_Clickable)
            current_Clickable = self


def block_click():
    global blocks
    global total_blocks
    global block_pressed
    block_pressed = True
    total_amount_bought = 0
    if sound_effects_on:
        click_effect.play()

    for item in Buy_Boxes:
        total_amount_bought += item.amount_bought

    blocks += (1 * click_multiplier) + (non_click_multiplier * total_amount_bought)
    total_blocks += (1 * click_multiplier) + (non_click_multiplier * total_amount_bought)

    print("Block has been pressed")


class Button:

    def __init__(self, image, rect, center, call, uncall, scene, button_press_command, is_menu_button=True,
                 buy_box=None, scene_list=None, is_back_button=False, is_setting_button=False, is_scroll_bar=False,
                 amount_per_buy=0, initialized=True, upgrade_box=None, name="Button", is_lucky_block=False,
                 info_text=None, is_toggle_button=False):
        self.image = pygame.image.load(image).convert_alpha()
        self.center = center
        self.rect = pygame.Rect(self.center[0] - (rect[2] // 2), self.center[1] - (rect[3] // 2), rect[2], rect[3])
        self.name = name
        self.info = info_text

        # Making a hover over version of itself (lighter and slightly bigger)
        self.image_lighter = self.image.copy()
        self.image_lighter = brighten_image(self.image_lighter, 20)
        if is_menu_button:
            self.image_lighter = pygame.transform.scale(self.image_lighter, (int(rect[2] * 1.2), int(rect[3] * 1.2)))

        # Making a press down version of itself (darker)
        self.image_darker = self.image.copy()
        self.image_darker = darken_image(self.image_darker, 50)

        # Start by displaying default version of itself
        self.image_to_display = self.image

        self.is_lucky_block = is_lucky_block

        # Stating Variables
        self.is_hovering = False
        self.is_pressed_down = False
        self.is_pressed_up = False
        self.active = False
        if self.is_lucky_block:
            self.initialized = True
            self.active = True
            self.runs = 0
        self.initialized = initialized
        self.is_menu_button = is_menu_button
        self.buy_box = buy_box
        self.is_back_button = is_back_button
        self.is_setting_button = is_setting_button
        self.is_scroll_bar = is_scroll_bar
        self.upgrade_box = upgrade_box
        self.call_events = call
        self.uncall_events = uncall
        self.scene_list = scene_list
        self.amount_per_buy = amount_per_buy
        self.scene = scene
        self.info_text = ""
        self.is_toggle_button = is_toggle_button

        if self.buy_box is not None:
            self.rect = (self.buy_box.cor[0], self.buy_box.cor[1], 267, 57)

        if self.upgrade_box is not None:
            self.rect = (self.upgrade_box.cor[0], self.upgrade_box.cor[1], 267, 57)

        # Adding itself to Buttons list
        Buttons.append(self)
        if self.scene_list is not None and buy_box is None:
            for obj in self.scene_list:
                obj.append(self)
        elif self.scene_list is None and buy_box is None and upgrade_box is None and not self.is_toggle_button:
            self.scene.append(self)

        # The command that will be call upon once button has been clicked
        self.button_press_command = button_press_command

    def __repr__(self):
        return self.name

    # Get the coordinates depending on different state of object (Used for blits)
    def get_center_cor(self):
        if self.is_menu_button:
            if self.is_hovering and not self.is_pressed_down:
                return self.center[0] - ((self.rect[2] * 1.2) // 2), self.center[1] - ((self.rect[3] * 1.2) // 2)
            elif not self.is_hovering or self.is_pressed_down:
                return self.center[0] - (self.rect[2] // 2), self.center[1] - (self.rect[3] // 2)
        if self.buy_box is not None:
            return self.buy_box.cor[0], self.buy_box.cor[1]
        if self.upgrade_box is not None:
            return self.upgrade_box.cor[0], self.upgrade_box.cor[1]
        return self.center[0] - (self.rect[2] // 2), self.center[1] - (self.rect[3] // 2)

    # Called upon once per tick
    def state_check(self):
        global mouse_pos
        global block_multiplier
        # Checks if mouse position is hovering and changes image depending on object state
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovering:
            self.is_hovering = False
            if self.upgrade_box is not None:
                Upgrade_Menu_Objects_Very_Front.remove(self.info_text)
            if self.buy_box is not None:
                Shop_Menu_Objects_Very_Front.remove(self.info_text)
        if self.buy_box is not None:
            if self.buy_box == pickaxe_buy_box and not self.initialized:
                self.scene.append(self)
                self.initialized = True
            if not self.initialized and total_blocks >= self.buy_box.start_price:
                self.scene.append(self)
                self.initialized = True

        if self.upgrade_box is not None:
            if self.upgrade_box.is_block_multi is not None:
                if self.upgrade_box.initialized and not self.initialized:
                    self.initialized = True
                    Upgrade_Menu_Objects_Back.append(self)
            if self.upgrade_box.tiered_building is not None:
                if self.upgrade_box.initialized and not self.initialized:
                    self.initialized = True
                    Upgrade_Menu_Objects_Back.append(self)
            if self.upgrade_box.is_clickable:
                if self.upgrade_box.initialized and not self.initialized:
                    self.initialized = True
                    Upgrade_Menu_Objects_Back.append(self)

        if self.active and self.initialized:
            if self.rect[0] + self.rect[2] > mouse_pos[0] > self.rect[0] and self.rect[1] + self.rect[3] > mouse_pos[
                1] > \
                    self.rect[1] and not self.is_hovering:
                self.is_hovering = True
                if self.upgrade_box is not None:
                    self.info_text = Text(font_click_amount, self.info,
                                          (self.upgrade_box.cor[0] + 267, self.upgrade_box.cor[1]),
                                          Upgrade_Menu_Objects_Very_Front, is_info_text=True,
                                          upgrade_box=self.upgrade_box)
                    Upgrade_Menu_Objects_Very_Front.append(self.info_text)
                if self.buy_box is not None:
                    single_bps_text = ""
                    if 1000 > self.buy_box.amount_per_buy * self.buy_box.bps_multiplier * block_multiplier >= 0:
                        single_bps_text = str(
                            round(self.buy_box.amount_per_buy * self.buy_box.bps_multiplier * block_multiplier, 1))
                    if self.buy_box.amount_per_buy * self.buy_box.bps_multiplier * block_multiplier >= 1000:
                        single_bps_text = divide_by_1000(
                            self.buy_box.amount_per_buy * self.buy_box.bps_multiplier * block_multiplier, is_price=True)

                    total_bps_text = ""
                    if 1000 > self.buy_box.amount_per_buy * self.buy_box.bps_multiplier * self.buy_box.amount_bought * block_multiplier >= 0:
                        total_bps_text = str(round(
                            self.buy_box.amount_per_buy * self.buy_box.bps_multiplier * self.buy_box.amount_bought * block_multiplier,
                            1))
                    if self.buy_box.amount_per_buy * self.buy_box.bps_multiplier * self.buy_box.amount_bought * block_multiplier >= 1000:
                        total_bps_text = divide_by_1000(
                            self.buy_box.amount_per_buy * self.buy_box.bps_multiplier * self.buy_box.amount_bought * block_multiplier,
                            is_price=True)

                    self.info_text = Text(font_click_amount,
                                          "Each " + str(self.buy_box.text) + " produces " + single_bps_text +
                                          " bps. Total of " + total_bps_text + " bps.",
                                          (self.buy_box.cor[0] + 267, self.buy_box.cor[1]),
                                          Shop_Menu_Objects_Very_Front, is_info_text=True, buy_box=self.buy_box)
                    Shop_Menu_Objects_Very_Front.append(self.info_text)
            if self.is_pressed_up:
                if not self.is_scroll_bar and sound_effects_on and self.upgrade_box is None and self.buy_box is None:
                    menu_click.play()
                # Calls upon button press command once
                if self.is_setting_button and main_menu:
                    self.button_press_command(1)
                elif self.is_setting_button and display_game_menu:
                    self.button_press_command(2)
                elif self.is_back_button and from_main_menu:
                    self.button_press_command(1)
                elif self.is_back_button and from_game_menu:
                    self.button_press_command(2)
                if self.is_lucky_block:
                    self.button_press_command(self.center)
                    Overlay_Objects.remove(self)
                    self.active = False
                    self.initialized = False
                    Buttons.remove(self)

                elif self.buy_box is not None:
                    self.button_press_command(self.buy_box, self.amount_per_buy)
                    self.buy_box.current_price = round(self.buy_box.start_price * (1.15 ** self.buy_box.amount_bought))

                elif self.upgrade_box is not None:
                    if self.upgrade_box.is_block_multi:
                        self.button_press_command(self.upgrade_box)
                    if self.upgrade_box.tiered_building is not None:
                        self.button_press_command(self.upgrade_box)
                    if self.upgrade_box.is_clickable:
                        self.button_press_command(self.upgrade_box)
                    if self.upgrade_box.is_price_reduction:
                        self.button_press_command(self.upgrade_box)

                elif self.buy_box is None:
                    self.button_press_command()
                self.is_pressed_up = False

            if self.is_pressed_down and self.is_scroll_bar:
                self.center = (self.center[0], pygame.mouse.get_pos()[1])
                self.rect = (self.rect[0], pygame.mouse.get_pos()[1] - 20, self.rect[2], self.rect[3])
            if self.is_scroll_bar and self.center[1] <= 8:
                self.center = self.center[0], 26
                self.rect = (self.rect[0], self.center[1] - 20, self.rect[2], self.rect[3])
                self.is_pressed_down = False
            if self.is_scroll_bar and self.center[1] >= 580:
                self.center = self.center[0], 560
                self.rect = (self.rect[0], self.center[1] - 20, self.rect[2], self.rect[3])
                self.is_pressed_down = False

            if self.is_hovering and not self.is_pressed_down:
                self.image_to_display = self.image_lighter
            elif self.is_pressed_down and self.is_hovering:
                self.image_to_display = self.image_darker
            else:
                self.image_to_display = self.image
            if self.buy_box is not None:
                self.rect = (self.buy_box.cor[0], self.buy_box.cor[1], 267, 57)
            if self.upgrade_box is not None:
                self.rect = (self.upgrade_box.cor[0], self.upgrade_box.cor[1], 267, 57)
        if self.is_lucky_block:
            self.runs += 1
            if self.runs > 325:
                self.active = False
                Buttons.remove(self)
                self.scene.remove(self)
        for event in self.uncall_events:
            if event:
                self.active = False
        for event in self.call_events:
            if event:
                self.active = True


# Function for when the start button is pressed
def start_button_pressed():
    global display_game_menu
    global main_menu
    global shop_menu
    print("Start Button Pressed")
    # Calls upon an event
    display_game_menu = True
    main_menu = False
    shop_menu = False
    startB.is_hovering = False
    # Updates the state of events
    update_game_events()


def shop_menu_pressed():
    global shop_menu
    global main_menu
    global shopB_toggle

    print("shop menu pressed")
    if not shopB_toggle:
        shopB.center = (511, 300)
        shopB.rect = (501, 266, 20, 68)
        shopB_toggle = True
    elif shopB_toggle:
        shopB.center = (790, 300)
        shopB.rect = (780, 266, 20, 68)
        shopB_toggle = False
    main_menu = False
    shop_menu = not shop_menu
    update_game_events()


def upgrade_menu_pressed():
    global upgrade_menu
    global main_menu
    global upgradeB_toggle

    print("upgrade menu pressed")
    if not upgradeB_toggle:
        upgradeB.center = (290, 300)
        upgradeB.rect = (280, 244, 20, 112)
        upgradeB_toggle = True
    elif upgradeB_toggle:
        upgradeB.center = (10, 300)
        upgradeB.rect = (0, 244, 20, 112)
        upgradeB_toggle = False
    main_menu = False
    upgrade_menu = not upgrade_menu
    update_game_events()


def buy_box_pressed(buy_box, amount_per_buy=0):
    global blocks
    global blocks_per_second
    print(str(buy_box.text) + " buy box has been pressed")
    main_box = buy_box
    if blocks >= main_box.current_price:
        if sound_effects_on:
            buy_sound.play()
        main_box.amount_bought = main_box.amount_bought + 1
        buy_box.bps += amount_per_buy
        blocks -= main_box.current_price


def upgrade_box_pressed(upgrade_box):
    global blocks
    global current_Clickable
    global click_multiplier
    global non_click_multiplier
    global block_multiplier
    upgrade_box = upgrade_box
    if blocks >= upgrade_box.current_price:
        if sound_effects_on:
            buy_sound.play()
        blocks -= upgrade_box.current_price
        if upgrade_box.tiered_building is not None:
            upgrade_box.tiered_building.bps_multiplier = upgrade_box.tiered_building.bps_multiplier * 2
            if upgrade_box.times_bought == 0:
                upgrade_box.current_price = upgrade_box.current_price * 5
            elif upgrade_box.times_bought == 1:
                upgrade_box.current_price = upgrade_box.current_price * 10
            elif upgrade_box.times_bought == 2:
                upgrade_box.current_price = upgrade_box.current_price * 100
            elif upgrade_box.times_bought == 3:
                upgrade_box.current_price = upgrade_box.current_price * 100
            elif upgrade_box.times_bought == 4:
                upgrade_box.current_price = upgrade_box.current_price * 100
            elif upgrade_box.times_bought == 5:
                upgrade_box.current_price = upgrade_box.current_price * 1000
            elif upgrade_box.times_bought == 6:
                upgrade_box.current_price = upgrade_box.current_price * 1000
            elif upgrade_box.times_bought == 7:
                upgrade_box.current_price = upgrade_box.current_price * 1000
            elif upgrade_box.times_bought == 8:
                upgrade_box.current_price = upgrade_box.current_price * 1000
            elif upgrade_box.times_bought == 9:
                upgrade_box.current_price = upgrade_box.current_price * 10000
            elif upgrade_box.times_bought == 10:
                upgrade_box.current_price = upgrade_box.current_price * 0
        elif upgrade_box.is_clickable:
            current_Clickable.completed = True
            current_clickable_completed.append(current_Clickable)
            Game_Menu_Objects.remove(current_Clickable)
            if upgrade_box.times_bought == 0:
                current_Clickable = sand_click
                click_multiplier = 2
                upgrade_box.current_price = 500
            elif upgrade_box.times_bought == 1:
                current_Clickable = oak_click
                click_multiplier = 4
                upgrade_box.current_price = 10000
            elif upgrade_box.times_bought == 2:
                current_Clickable = stone_click
                click_multiplier = 8
                upgrade_box.current_price = 100000
            elif upgrade_box.times_bought == 3:
                current_Clickable = iron_click
                non_click_multiplier += 0.1
                upgrade_box.current_price = 10000000
            elif upgrade_box.times_bought == 4:
                current_Clickable = ice_click
                non_click_multiplier += 0.5
                upgrade_box.current_price = 100000000
            elif upgrade_box.times_bought == 5:
                current_Clickable = glowstone_click
                non_click_multiplier += 5
                upgrade_box.current_price = 1000000000
            elif upgrade_box.times_bought == 6:
                current_Clickable = diamondore_click
                non_click_multiplier += 50
                upgrade_box.current_price = 10000000000
            elif upgrade_box.times_bought == 7:
                current_Clickable = slimeblock_click
                non_click_multiplier += 500
                upgrade_box.current_price = 10000000000000
            elif upgrade_box.times_bought == 8:
                current_Clickable = obsidian_click
                non_click_multiplier += 5000
                upgrade_box.current_price = 10000000000000000
            elif upgrade_box.times_bought == 9:
                current_Clickable = diamondblock_click
                non_click_multiplier += 50000
                upgrade_box.current_price = 10000000000000000000
            elif upgrade_box.times_bought == 10:
                current_Clickable = dragonegg_click
                non_click_multiplier += 500000
                upgrade_box.current_price = 10000000000000000000000
            elif upgrade_box.times_bought == 11:
                current_Clickable = bedrock_click
                non_click_multiplier += 5000000
                upgrade_box.current_price = 10000000000000000000000000
        elif upgrade_box.is_block_multi:
            if upgrade_box.times_bought % 2 == 0 and upgrade_box.times_bought <= 4:
                block_multiplier += 0.10
                upgrade_box.current_price = upgrade_box.current_price * 5
                upgrade_box.multi_required = upgrade_box.multi_required * 2
            elif upgrade_box.times_bought % 2 == 1 and upgrade_box.times_bought <= 4:
                block_multiplier += 0.10
                upgrade_box.current_price = upgrade_box.current_price * 2
                upgrade_box.multi_required = upgrade_box.multi_required * 5
            if upgrade_box.times_bought == 4:
                upgrade_box.info_box_text = "Block production multiplier +20%"
            elif upgrade_box.times_bought % 2 == 0 and 4 < upgrade_box.times_bought <= 20:
                block_multiplier += 0.20
                upgrade_box.current_price = upgrade_box.current_price * 5
                upgrade_box.multi_required = upgrade_box.multi_required * 2
            elif upgrade_box.times_bought % 2 == 1 and 4 < upgrade_box.times_bought <= 20:
                block_multiplier += 0.20
                upgrade_box.current_price = upgrade_box.current_price * 2
                upgrade_box.multi_required = upgrade_box.multi_required * 5
            if upgrade_box.times_bought == 20:
                upgrade_box.info_box_text = "Block production multiplier +25%"
            elif upgrade_box.times_bought % 2 == 0 and 20 < upgrade_box.times_bought <= 50:
                block_multiplier += 0.25
                upgrade_box.current_price = upgrade_box.current_price * 5
                upgrade_box.multi_required = upgrade_box.multi_required * 2
            elif upgrade_box.times_bought % 2 == 1 and 20 < upgrade_box.times_bought <= 50:
                block_multiplier += 0.25
                upgrade_box.current_price = upgrade_box.current_price * 2
                upgrade_box.multi_required = upgrade_box.multi_required * 5
            if upgrade_box.times_bought == 50:
                upgrade_box.info_box_text = "Block production multiplier +30%"
            elif upgrade_box.times_bought % 2 == 0 and 50 < upgrade_box.times_bought <= 70:
                block_multiplier += 0.30
                upgrade_box.current_price = upgrade_box.current_price * 5
                upgrade_box.multi_required = upgrade_box.multi_required * 2
            elif upgrade_box.times_bought % 2 == 1 and 50 < upgrade_box.times_bought <= 70:
                block_multiplier += 0.30
                upgrade_box.current_price = upgrade_box.current_price * 2
                upgrade_box.multi_required = upgrade_box.multi_required * 5
            if upgrade_box.times_bought == 70:
                upgrade_box.info_box_text = "Block production multiplier +35%"
            elif upgrade_box.times_bought % 2 == 0 and 70 < upgrade_box.times_bought <= 100:
                block_multiplier += 0.35
                upgrade_box.current_price = upgrade_box.current_price * 5
                upgrade_box.multi_required = upgrade_box.multi_required * 2
            elif upgrade_box.times_bought % 2 == 1 and 70 < upgrade_box.times_bought <= 100:
                block_multiplier += 0.35
                upgrade_box.current_price = upgrade_box.current_price * 2
                upgrade_box.multi_required = upgrade_box.multi_required * 5
        elif upgrade_box.is_price_reduction:
            if upgrade_box.times_bought <= 5:
                for buy_box in Buy_Boxes:
                    buy_box.current_price -= buy_box.current_price * 0.05
                upgrade_box.current_price = upgrade_box.current_price * 10
                upgrade_box.multi_required = upgrade_box.multi_required * 5
            elif 5 < upgrade_box.times_bought <= 20:
                for buy_box in Buy_Boxes:
                    buy_box.current_price -= buy_box.current_price * 0.05
                upgrade_box.current_price = upgrade_box.current_price * 100
                upgrade_box.multi_required = upgrade_box.multi_required * 50
            elif 20 < upgrade_box.times_bought <= 50:
                for buy_box in Buy_Boxes:
                    buy_box.current_price -= buy_box.current_price * 0.05
                upgrade_box.current_price = upgrade_box.current_price * 150
                upgrade_box.multi_required = upgrade_box.multi_required * 100
            elif 50 < upgrade_box.times_bought <= 100:
                for buy_box in Buy_Boxes:
                    buy_box.current_price -= buy_box.current_price * 0.05
                upgrade_box.current_price = upgrade_box.current_price * 200
                upgrade_box.multi_required = upgrade_box.multi_required * 100

        upgrade_box.initialized = False
        upgrade_boxes_to_initialize.remove(upgrade_box)
        upgrade_box.times_bought += 1

        i = upgrade_box.icon_list.pop(0)

        if upgrade_box.tiered_building is not None:
            Shop_Menu_Objects_Front.remove(i)
            Shop_Menu_Objects_Front.append(upgrade_box.icon_list[0])
            Upgrade_Menu_Objects_Front.remove(upgrade_box.icon_list[0])
            upgrade_box.icon_list[0].upgrade_box_initialized = False
            icons_to_upgrade_box_initialize.remove(upgrade_box.icon_list[0])

        if upgrade_box.is_clickable:
            Upgrade_Menu_Objects_Front.remove(upgrade_box.icon_list[0])
            Game_Menu_Objects.append(current_Clickable)
            current_Clickable.initialized = True
            clickables_to_initialize.append(current_Clickable)

        if upgrade_box.is_block_multi:
            Upgrade_Menu_Objects_Front.remove(upgrade_box.icon_list[0])
            upgrade_box.icon_list[0].upgrade_box_initialized = False
            icons_to_upgrade_box_initialize.remove(upgrade_box.icon_list[0])

        upgrade_box.icon_list.append(i)

        upgrade_box.upgrade_box_text.initialized = False

        upgrade_box.price_icon.initialized = False

        upgrade_box.current_price_text.initialized = False

        upgrade_box.background.initialized = False

        upgrade_boxes_active.remove(upgrade_box)
        check_upgrade_box_cor()

        Upgrade_Menu_Objects_Front.remove(upgrade_box.upgrade_box_text)
        Upgrade_Menu_Objects_Front.remove(upgrade_box.price_icon)
        Upgrade_Menu_Objects_Front.remove(upgrade_box.current_price_text)
        Upgrade_Menu_Objects_Back.remove(upgrade_box.background)


def scroll_bar_pressed():
    pass


def setting_menu_pressed(from_where=0):
    global setting_menu
    global display_game_menu
    global main_menu
    global shop_menu
    global upgrade_menu
    global from_game_menu
    global from_main_menu
    global shopB_toggle
    global upgradeB_toggle
    print("Settings Button pressed")
    if from_where == 1:
        from_main_menu = True
    if from_where == 2:
        from_game_menu = True
    settingsB.is_hovering = False
    setting_menu = True
    display_game_menu = False
    main_menu = False
    shop_menu = False
    upgrade_menu = False

    shopB_toggle = False
    shopB.center = (790, 300)
    shopB.rect = (780, 266, 20, 68)

    upgradeB_toggle = False
    upgradeB.center = (10, 300)
    upgradeB.rect = (0, 244, 20, 112)

    upgradeB_toggle = False
    update_game_events()


def music_on_pressed():
    global musicB_toggle
    if not musicB_toggle:
        print("test")
        Settings_Menu_Objects.remove(MusicOnB)
        MusicOnB.initialized = False
        Settings_Menu_Objects.append(MusicOffB)
        MusicOffB.initialized = True
        musicB_toggle = True
        pygame.mixer.music.set_volume(0.01)
    elif musicB_toggle:
        Settings_Menu_Objects.remove(MusicOffB)
        MusicOffB.initialized = False
        Settings_Menu_Objects.append(MusicOnB)
        MusicOnB.initialized = True
        musicB_toggle = False
        pygame.mixer.music.set_volume(0.05)
    check_events()
    print("Music On Pressed")


def sound_on_pressed():
    global blocks
    global soundB_toggle
    global sound_effects_on
    if not soundB_toggle:
        print("test")
        Settings_Menu_Objects.remove(SoundOnB)
        SoundOnB.initialized = False
        Settings_Menu_Objects.append(SoundOffB)
        SoundOffB.initialized = True
        soundB_toggle = True
        sound_effects_on = False
    elif soundB_toggle:
        Settings_Menu_Objects.remove(SoundOffB)
        SoundOffB.initialized = False
        Settings_Menu_Objects.append(SoundOnB)
        SoundOnB.initialized = True
        soundB_toggle = False
        sound_effects_on = True
    check_events()
    print("Sound and Music On Pressed")


def stats_pressed():
    global total_blocks
    print("Stats pressed")


def credits_pressed():
    global total_blocks
    global blocks
    blocks = (blocks + 1) * 2
    total_blocks = (total_blocks + 1) * 2
    print("Credits pressed")


def save_button_pressed():
    print("Save Button pressed")
    save_game()


def main_menu_pressed():
    print("Main Menu pressed")
    global setting_menu
    global display_game_menu
    global main_menu
    global shop_menu
    global upgrade_menu

    setting_menu = False
    shop_menu = False
    upgrade_menu = False
    main_menu = True
    display_game_menu = False

    update_game_events()


def back_button_pressed(from_where=0):
    global setting_menu
    global display_game_menu
    global main_menu
    global shop_menu
    global upgrade_menu
    global from_game_menu
    global from_main_menu
    print("Back Button Pressed")
    from_game_menu = False
    from_main_menu = False
    setting_menu = False
    shop_menu = False
    upgrade_menu = False
    if from_where == 1:
        main_menu = True
        display_game_menu = False
    if from_where == 2:
        main_menu = False
        display_game_menu = True
    update_game_events()


def lucky_block_pressed(center):
    global total_blocks
    global blocks
    blocks_to_display = "+" + str(blocks)
    if 1000 > blocks >= 0:
        blocks_to_display = "+" + str(round(blocks))
    if blocks >= 1000:
        blocks_to_display = "+" + divide_by_1000(blocks, is_blocks=True)
    blocks += blocks
    total_blocks += blocks
    Text(font_click_amount, blocks_to_display, center, Overlay_Objects, is_click_text=True)


class Uninteractable:

    # Requires rect because it is not the same each instance
    def __init__(self, image, rect, center, scene, buy_box=None, is_buy_box_background=False, is_glow_effect=False,
                 start_angle=0, left=False):
        self.image = pygame.image.load(image).convert_alpha()
        self.image_to_display = self.image
        self.image_copy = self.image
        self.center = center
        self.left = left
        self.is_glow_effect = is_glow_effect
        self.rect = pygame.Rect(self.center[0] - (rect[2] // 2), self.center[1] - (rect[3] // 2), rect[2], rect[3])
        if not self.is_glow_effect:
            scene.append(self)
        self.buy_box = buy_box
        self.is_buy_box_background = is_buy_box_background
        self.angle = start_angle
        if self.is_glow_effect:
            Glow_Effects.append(self)

    # Get coordinates (Used for blits)
    def get_center_cor(self):
        if self.is_buy_box_background:
            return self.buy_box.cor[0] + 1, self.buy_box.cor[1]
        return self.center[0] - (self.rect[2] // 2), self.center[1] - (self.rect[3] // 2)

    def transform(self):
        self.image_copy = pygame.transform.rotate(self.image, self.angle)
        if self.left:
            self.angle -= 0.90
        if not self.left:
            self.angle += 1.50
        x, y = self.rect.center
        self.rect = self.image_copy.get_rect()
        self.rect.center = (x, y)


class small_Block:

    # Takes original image, re-sizes and also creates new Rect
    def __init__(self, image, rect, center):
        self.image_orig = image
        self.image = pygame.transform.scale(self.image_orig, (30, 30))
        self.image_copy = self.image
        self.center = center
        self.rect = pygame.Rect(self.center[0] - (rect[2] // 2), self.center[1] - (rect[3] // 2), rect[2], rect[3])
        self.is_first = True
        self.start_pressed_first = False


class Text:

    def __init__(self, font, text, center, scene, colour=(255, 255, 255), buy_box=None, is_price_text=False,
                 is_amount_bought_text=False, is_amount_blocks_text=False, is_per_second_text=False, upgrade_box=None,
                 is_click_text=False, is_info_text=False):
        self.text = text
        self.center = center
        self.buy_box = buy_box
        self.colour = colour
        self.image_to_display = font.render(self.text, True, self.colour, None)
        self.is_price_text = is_price_text
        self.is_amount_bought_text = is_amount_bought_text
        self.is_per_second_text = is_per_second_text
        self.is_blocks_text = is_amount_blocks_text
        self.initialized = False
        self.upgrade_box = upgrade_box
        self.price_to_display = ""
        self.is_click_text = is_click_text
        self.scene = scene
        self.is_info_text = is_info_text
        if self.is_amount_bought_text:
            self.amount_bought_display_text = self.buy_box.amount_bought
        if self.is_blocks_text:
            self.blocks_to_display = blocks
        if self.is_per_second_text:
            self.per_second_to_display = blocks_per_second
        if self.buy_box is None and self.upgrade_box is None and not self.is_info_text:
            self.scene.append(self)
        Texts.append(self)
        if self.is_click_text:
            self.runs = 0

    def get_center_cor(self):
        global blocks
        global mouse_pos
        if self.buy_box is not None and not self.is_info_text:
            if self.is_price_text:
                return self.buy_box.cor[0] + 80, self.buy_box.cor[1] + 36
            elif self.is_amount_bought_text:
                if self.buy_box.amount_bought <= 1000000:
                    return (self.buy_box.cor[0] + 232) - (len(str(self.buy_box.amount_bought)) * 12), self.buy_box.cor[
                        1] + 13
                elif self.buy_box.amount_bought >= 1000000:
                    return (self.buy_box.cor[0] + 232) - (
                            len(str(round(self.buy_box.amount_bought / 1000000, 1))) * 14), self.buy_box.cor[
                               1] + 13
            elif not self.is_price_text and not self.is_amount_bought_text:
                return self.buy_box.cor[0] + 60, self.buy_box.cor[1] + 5
        if self.upgrade_box is not None and not self.is_info_text:
            if self.is_price_text:
                return self.upgrade_box.cor[0] + 80, self.upgrade_box.cor[1] + 36
            elif not self.is_price_text:
                return self.upgrade_box.cor[0] + 60, self.upgrade_box.cor[1] + 10
        elif self.is_blocks_text:
            return self.center[0] - (len(str(self.blocks_to_display)) * 4), self.center[1]
        elif self.is_per_second_text:
            return amount_of_blocks_text.get_center_cor()[0] + 2 + (
                    len(str(amount_of_blocks_text.blocks_to_display)) * 4) - (
                           len(str(self.per_second_to_display)) * 2), amount_of_blocks_text.get_center_cor()[1] + 35
        elif self.is_info_text and self.upgrade_box is not None:
            return mouse_pos[0] + 10, mouse_pos[1] - 10
        elif self.is_info_text and self.buy_box is not None:
            return mouse_pos[0] - 325, mouse_pos[1] - 20
        return self.center

    # noinspection PyTypeChecker
    def state_check(self):
        global blocks
        global times_divided

        if self.is_click_text:
            self.runs += 1
            self.center = (self.center[0], self.center[1] - 2)
            if self.runs > 20:
                self.scene.remove(self)
                Texts.remove(self)
        if self.buy_box is not None and not self.is_info_text:
            if self.buy_box == pickaxe_buy_box and not self.initialized:
                Shop_Menu_Objects_Front.append(self)
                self.initialized = True
            if self.buy_box.initialized and not self.initialized:
                Shop_Menu_Objects_Front.append(self)
                self.initialized = True

        if self.upgrade_box is not None and not self.is_info_text:
            if self.upgrade_box.is_block_multi or self.upgrade_box.tiered_building is not None or self.upgrade_box.is_clickable or self.upgrade_box.is_price_reduction:
                if self.upgrade_box.initialized and not self.initialized:
                    self.initialized = True
                    Upgrade_Menu_Objects_Front.append(self)

        if self.is_price_text and self.initialized:
            if self.buy_box is not None:
                Shop_Menu_Objects_Front.remove(self)
                if 1000 > self.buy_box.current_price >= 0:
                    self.price_to_display = str(round(self.buy_box.current_price))
                if self.buy_box.current_price >= 1000:
                    self.price_to_display = divide_by_1000(self.buy_box.current_price, is_price=True)
                self.image_to_display = font_buy_box_price.render(str(self.price_to_display), True, self.colour, None)
                Shop_Menu_Objects_Front.append(self)

            if self.upgrade_box is not None:
                Upgrade_Menu_Objects_Front.remove(self)
                if 0 <= self.upgrade_box.current_price < 1000:
                    self.price_to_display = self.upgrade_box.current_price
                if 1000 > self.upgrade_box.current_price >= 0:
                    self.price_to_display = str(round(self.upgrade_box.current_price))
                if self.upgrade_box.current_price >= 1000:
                    self.price_to_display = divide_by_1000(self.upgrade_box.current_price, is_price=True)
                self.image_to_display = font_buy_box_price.render(str(self.price_to_display), True, self.colour, None)
                Upgrade_Menu_Objects_Front.append(self)

        if self.is_amount_bought_text and self.initialized:
            Shop_Menu_Objects_Front.remove(self)
            if 1000 > self.buy_box.amount_bought >= 0:
                self.price_to_display = str(round(self.buy_box.amount_bought))
            if self.buy_box.amount_bought >= 1000:
                self.price_to_display = divide_by_1000(self.buy_box.amount_bought, is_price=True)
            self.image_to_display = font_buy_box_name.render(str(self.price_to_display), True, self.colour, None)
            Shop_Menu_Objects_Front.append(self)

        elif self.is_blocks_text:
            self.blocks_to_display = str(blocks) + " blocks"
            Game_Menu_Objects.remove(self)
            if 1000 > blocks >= 0:
                self.blocks_to_display = str(round(blocks)) + " blocks"
            if blocks >= 1000:
                self.blocks_to_display = divide_by_1000(blocks, is_blocks=True)
            self.image_to_display = header.render(str(self.blocks_to_display), True, self.colour, None)
            Game_Menu_Objects.append(self)

        elif self.is_per_second_text:
            global blocks_per_second
            self.per_second_to_display = str(blocks_per_second) + " per second"
            Game_Menu_Objects.remove(self)

            if 1000 > blocks_per_second >= 0:
                self.per_second_to_display = str(round(blocks_per_second, 1)) + " per second"
            if blocks_per_second >= 1000:
                self.per_second_to_display = divide_by_1000(blocks_per_second, is_per_second=True)

            self.image_to_display = font_buy_box_price.render(str(self.per_second_to_display), True, self.colour, None)
            Game_Menu_Objects.append(self)


class Icon:

    def __init__(self, image, center, buy_box_list, name, buy_box=None, upgrade_box=None, is_clickable=False,
                 is_block_multi=False, is_price_reduction=False):
        self.is_clickable = is_clickable
        self.buy_box_list = buy_box_list
        self.is_block_multi = is_block_multi
        self.buy_box_list.append(self)
        self.name = name
        if self.is_clickable:
            self.image_to_display = image
        if not self.is_clickable:
            self.image_to_display = pygame.image.load(image).convert_alpha()
        self.center = center
        self.rect = pygame.Rect(self.center[0] - (50 // 2), self.center[1] - (50 // 2), 50, 50)
        self.buy_box = buy_box
        self.buy_box_initialized = False
        self.upgrade_box_initialized = False
        self.buy_box_first = True
        self.upgrade_box_first = True
        self.first_icon = None
        self.default_upgrade_box_icon = None
        self.upgrade_box = upgrade_box
        self.is_upgrade_box_icon = False
        self.first = True
        self.is_price_reduction = is_price_reduction
        Icons.append(self)

    def __repr__(self):
        return self.name

    # Gets the coordinates (Used for blits)
    def get_center_cor(self):
        if self.is_block_multi or self.is_upgrade_box_icon or self.is_price_reduction:
            return self.upgrade_box.cor[0], self.upgrade_box.cor[1] + 2
        if self.is_clickable:
            return self.upgrade_box.cor[0] + 5, self.upgrade_box.cor[1] + 5
        if not self.is_upgrade_box_icon:
            return self.buy_box.cor[0], self.buy_box.cor[1] + 2

    def state_check(self):
        if self.buy_box is not None:
            if self.buy_box.initialized and not self.buy_box_initialized or not self.buy_box_initialized and self.buy_box == pickaxe_buy_box:
                self.buy_box_initialized = True
                icons_to_buy_box_initialize.append(self)
                if self.buy_box_list[0] == self:
                    Shop_Menu_Objects_Front.append(self.buy_box_list[0])
                self.buy_box.icon = self
                self.first_icon = self.buy_box_list[0]
        if self.upgrade_box is not None and not self.is_block_multi and not self.is_price_reduction:
            if self.upgrade_box.initialized and not self.upgrade_box_initialized:
                if not self.first:
                    if self.buy_box_list[1] == self:
                        self.upgrade_box_initialized = True
                        icons_to_upgrade_box_initialize.append(self)
                        Upgrade_Menu_Objects_Front.append(self)
                self.first = False

            if self.buy_box_initialized:
                if self.buy_box_list[0] == self:
                    Shop_Menu_Objects_Front.remove(self.buy_box_list[0])
                    self.is_upgrade_box_icon = False
                    Shop_Menu_Objects_Front.append(self.buy_box_list[0])

        if self.upgrade_box is not None and not self.is_block_multi and not self.is_price_reduction:
            if self.upgrade_box_initialized:
                if self.buy_box_list[1] == self:
                    Upgrade_Menu_Objects_Front.remove(self.buy_box_list[1])
                    self.buy_box_list[1].is_upgrade_box_icon = True
                    Upgrade_Menu_Objects_Front.append(self.buy_box_list[1])
        if self.is_block_multi:
            if self.upgrade_box.initialized and not self.upgrade_box_initialized:
                if self.buy_box_list[1] == self:
                    self.upgrade_box_initialized = True
                    icons_to_upgrade_box_initialize.append(self)
                    Upgrade_Menu_Objects_Front.append(self)

        if self.is_price_reduction:
            if self.upgrade_box.initialized and not self.upgrade_box_initialized:
                self.upgrade_box_initialized = True
                icons_to_upgrade_box_initialize.append(self)
                Upgrade_Menu_Objects_Front.append(self)


class buy_Box:
    def __init__(self, name, start_price, cor, amount_per_buy, name_obj):
        self.icon = None
        self.text = name
        self.start_price = start_price
        self.current_price = start_price
        self.amount_bought = 0
        self.beginning_cor = cor
        self.cor = self.beginning_cor
        self.bps = 0
        self.name = name_obj
        self.overlay_events_call = [shop_menu]
        self.overlay_events_uncall = [not shop_menu]
        self.amount_per_buy = amount_per_buy
        self.bps_multiplier = 1
        self.first = True
        self.initialized = False

        self.current_price_text = Text(font_buy_box_price, str(self.current_price), (0, 0), Shop_Menu_Objects_Front,
                                       buy_box=self, is_price_text=True)
        self.amount_bought_text = Text(font_buy_box_name, str(self.amount_bought), (0, 0), Shop_Menu_Objects_Front,
                                       buy_box=self, is_amount_bought_text=True, colour=(18, 106, 250))
        self.background = Button('Minecraft Clicker Images/buy_box_background.png', (0, 0, 267, 57), (0, 0),
                                 self.overlay_events_call, self.overlay_events_uncall, Shop_Menu_Objects_Back,
                                 buy_box_pressed, is_menu_button=False, buy_box=self,
                                 amount_per_buy=self.amount_per_buy, initialized=False)
        self.price_icon = box_price_icon(current_Clickable.image, self)
        self.buy_box_text = Text(font_buy_box_name, self.text, self.cor, Shop_Menu_Objects_Front,
                                 buy_box=self)
        Buy_Boxes.append(self)

    def __repr__(self):
        return self.name

    # Called on once per tick
    def state_check(self):
        global total_blocks
        if pickaxe_buy_box == self and not self.initialized:
            self.initialized = True
            buy_boxes_to_initialize.append(self)
        if total_blocks >= self.start_price and not self.initialized:
            self.initialized = True
            buy_boxes_to_initialize.append(self)
        self.cor = self.cor[0], self.beginning_cor[1] - Shop_scroll_barB.get_center_cor()[1] + 3

        # Add functions to make these change depending on events


class box_price_icon:
    def __init__(self, image, use_box, is_upgrade_box=False):
        self.image_to_display = image
        self.box = use_box
        self.initialized = False
        self.is_upgrade_box = is_upgrade_box
        self.image_to_display = pygame.transform.scale(image, (15, 15))
        Buy_Box_Price_Icons.append(self)

    def get_center_cor(self):
        return self.box.cor[0] + 60, self.box.cor[1] + 36

    def state_check(self):
        if self.box == pickaxe_buy_box and not self.initialized:
            Shop_Menu_Objects_Front.append(self)
            self.initialized = True
        if not self.is_upgrade_box:
            if self.box.initialized and not self.initialized:
                Shop_Menu_Objects_Front.append(self)
                self.initialized = True
            if self.initialized:
                Shop_Menu_Objects_Front.remove(self)
                self.image_to_display = pygame.transform.scale(current_Clickable.image, (15, 15))
                Shop_Menu_Objects_Front.append(self)
        if self.is_upgrade_box:
            if self.box.initialized and not self.initialized:
                Upgrade_Menu_Objects_Front.append(self)
                self.initialized = True
            if self.initialized:
                Upgrade_Menu_Objects_Front.remove(self)
                self.image_to_display = pygame.transform.scale(current_Clickable.image, (15, 15))
                Upgrade_Menu_Objects_Front.append(self)


class upgrade_Box:
    def __init__(self, text, base_price, icon_list, name, info_box_text="", tiered_building=None, is_clickable=False,
                 is_block_multi=False, is_price_reduction=False):
        Upgrade_Boxes.append(self)
        self.text = text
        self.name = name
        self.info_box_text = info_box_text
        self.price = base_price
        self.current_price = base_price
        self.icon_list = icon_list
        self.events_call = [upgrade_menu]
        self.events_uncall = [not upgrade_menu]
        self.tiered_building = tiered_building
        self.beginning_cor = (50, 56)
        self.cor = (0, 56)
        self.times_bought = 0
        self.price_icon = None
        self.is_clickable = is_clickable
        self.multi_required = 50000
        self.is_block_multi = is_block_multi
        self.is_price_reduction = is_price_reduction
        if self.tiered_building is not None:
            self.info_box_text = "Doubles " + str(self.tiered_building.text) + " production"
        self.current_price_text = Text(font_buy_box_price, str(self.current_price), (0, 0), Upgrade_Menu_Objects_Front,
                                       upgrade_box=self, is_price_text=True)
        self.background = Button('Minecraft Clicker Images/buy_box_background.png', (0, 0, 267, 57), (0, 0),
                                 self.events_call, self.events_uncall, Upgrade_Menu_Objects_Back,
                                 upgrade_box_pressed, is_menu_button=False, upgrade_box=self,
                                 initialized=False, info_text=self.info_box_text)
        self.upgrade_box_text = Text(font_upgrade_box_name, self.text, self.cor, Upgrade_Menu_Objects_Front,
                                     upgrade_box=self)
        self.initialized = False

        self.first = True

    def __repr__(self):
        return self.name

    def state_check(self):
        global total_blocks
        if self.tiered_building == pickaxe_buy_box:
            self.icon_list = Pickaxe_Icon_Objects
        elif self.tiered_building == axe_buy_box:
            self.icon_list = Axe_Icon_Objects
        elif self.tiered_building == shovel_buy_box:
            self.icon_list = Shovel_Icon_Objects
        elif self.tiered_building == sword_buy_box:
            self.icon_list = Sword_Icon_Objects
        elif self.tiered_building == hoe_buy_box:
            self.icon_list = Hoe_Icon_Objects
        elif self.tiered_building == shears_buy_box:
            self.icon_list = Shears_Icon_Objects
        elif self.tiered_building == firecharge_buy_box:
            self.icon_list = Firecharge_Icon_Objects
        elif self.tiered_building == bow_buy_box:
            self.icon_list = Bow_Icon_Objects
        elif self.tiered_building == rod_buy_box:
            self.icon_list = Rod_Icon_Objects
        elif self.tiered_building == fns_buy_box:
            self.icon_list = Fns_Icon_Objects
        elif self.tiered_building == tnt_buy_box:
            self.icon_list = Tnt_Icon_Objects
        elif self.tiered_building == beacon_buy_box:
            self.icon_list = Beacon_Icon_Objects
        elif self.tiered_building == creeper_buy_box:
            self.icon_list = Creeper_Icon_Objects
        elif self.tiered_building == fireball_buy_box:
            self.icon_list = Fireball_Icon_Objects
        elif self.tiered_building == crystal_buy_box:
            self.icon_list = Crystal_Icon_Objects
        elif self.tiered_building == dragon_buy_box:
            self.icon_list = Dragon_Icon_Objects
        elif self.tiered_building == wither_buy_box:
            self.icon_list = Wither_Icon_Objects

        # if self.tiered_building == pickaxe_buy_box:
        if self.first:
            self.price_icon = box_price_icon(current_Clickable.image, self, is_upgrade_box=True)
        elif self.tiered_building is not None:
            if self.times_bought == 0 and self.tiered_building.amount_bought >= 1 and not self.initialized or \
                    self.times_bought == 1 and self.tiered_building.amount_bought >= 5 and not self.initialized or \
                    self.times_bought == 2 and self.tiered_building.amount_bought >= 25 and not self.initialized or \
                    self.times_bought == 3 and self.tiered_building.amount_bought >= 50 and not self.initialized or \
                    self.times_bought == 4 and self.tiered_building.amount_bought >= 100 and not self.initialized or \
                    self.times_bought == 5 and self.tiered_building.amount_bought >= 150 and not self.initialized or \
                    self.times_bought == 6 and self.tiered_building.amount_bought >= 200 and not self.initialized or \
                    self.times_bought == 7 and self.tiered_building.amount_bought >= 250 and not self.initialized or \
                    self.times_bought == 8 and self.tiered_building.amount_bought >= 300 and not self.initialized or \
                    self.times_bought == 9 and self.tiered_building.amount_bought >= 350 and not self.initialized:
                self.initialized = True
                upgrade_boxes_active.append(self)
                upgrade_boxes_to_initialize.append(self)
                check_upgrade_box_cor()

        elif self.is_clickable:
            if self.times_bought == 0 and pickaxe_buy_box.amount_bought >= 1 and not self.initialized or \
                    self.times_bought == 1 and pickaxe_buy_box.amount_bought >= 5 and not self.initialized or \
                    self.times_bought == 2 and pickaxe_buy_box.amount_bought >= 10 and not self.initialized or \
                    self.times_bought == 3 and pickaxe_buy_box.amount_bought >= 25 and not self.initialized or \
                    self.times_bought == 4 and pickaxe_buy_box.amount_bought >= 50 and not self.initialized or \
                    self.times_bought == 5 and pickaxe_buy_box.amount_bought >= 100 and not self.initialized or \
                    self.times_bought == 6 and pickaxe_buy_box.amount_bought >= 150 and not self.initialized or \
                    self.times_bought == 7 and pickaxe_buy_box.amount_bought >= 200 and not self.initialized or \
                    self.times_bought == 8 and pickaxe_buy_box.amount_bought >= 250 and not self.initialized or \
                    self.times_bought == 9 and pickaxe_buy_box.amount_bought >= 300 and not self.initialized or \
                    self.times_bought == 10 and pickaxe_buy_box.amount_bought >= 350 and not self.initialized or \
                    self.times_bought == 11 and pickaxe_buy_box.amount_bought >= 400 and not self.initialized:
                self.initialized = True
                upgrade_boxes_active.append(self)
                upgrade_boxes_to_initialize.append(self)
                check_upgrade_box_cor()

        elif self.is_block_multi:
            if total_blocks >= self.multi_required and not self.initialized:
                self.initialized = True
                upgrade_boxes_active.append(self)
                upgrade_boxes_to_initialize.append(self)
                check_upgrade_box_cor()
        elif self.is_price_reduction:
            if total_blocks >= self.multi_required and not self.initialized:
                self.initialized = True
                upgrade_boxes_active.append(self)
                upgrade_boxes_to_initialize.append(self)
                check_upgrade_box_cor()

        self.cor = self.cor[0], self.beginning_cor[1] - Upgrade_scroll_barB.get_center_cor()[1] + 3
        self.first = False


def check_upgrade_box_cor():
    for num, use_box in enumerate(upgrade_boxes_active, 1):
        use_box.beginning_cor = use_box.beginning_cor[0], upgrade_boxes_beginning_cor.get(num)


# Function that brightens image by certain amount
def brighten_image(image, brighten):
    image.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
    return image


# Function that darkens image by certain amount
def darken_image(image, darken):
    image.fill((darken, darken, darken), special_flags=pygame.BLEND_RGB_SUB)
    return image


def make_price_icon(clickable_image):
    return pygame.transform.scale(clickable_image, (100, 100))


def check_events():
    global run
    global blocks
    global total_blocks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Stops Program
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Checks event to object and Changes object state
            for obj in Buttons:
                if obj.is_hovering:
                    obj.is_pressed_down = True
            for obj in Clickables:
                if obj.is_hovering:
                    obj.is_pressed_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # Checks event to object and Changes object state
            for obj in Buttons:
                if obj.is_scroll_bar:
                    obj.is_pressed_down = False
                    obj.is_pressed_up = True
                elif obj.is_hovering:
                    obj.is_pressed_down = False
                    obj.is_pressed_up = True
            for obj in Clickables:
                if obj.is_hovering:
                    obj.is_pressed_down = False
                    obj.is_pressed_up = True
    current_Clickable.descend()
    for glow in Glow_Effects:
        glow.transform()
    # Update object states every frame
    check_bps()
    blocks += blocks_per_second / 25
    total_blocks += blocks_per_second / 25
    for obj in Upgrade_Boxes:
        obj.state_check()
    for obj in Buy_Box_Price_Icons:
        obj.state_check()
    for obj in Buttons:
        obj.state_check()
    for obj in Clickables:
        obj.state_check()
    for obj in Icons:
        obj.state_check()
    for obj in Buy_Boxes:
        obj.state_check()
    for obj in Texts:
        if obj.buy_box is not None or obj.is_blocks_text or obj.is_per_second_text or obj.upgrade_box is not None or obj.is_click_text:
            obj.state_check()


def check_bps():
    global blocks_per_second
    blocks_per_second = 0
    for obj in Buy_Boxes:
        blocks_per_second += round(obj.bps, 1) * obj.bps_multiplier
    blocks_per_second = round(blocks_per_second * block_multiplier, 1)


# Called upon once per tick
def redraw():
    global display_game_menu
    global block_pressed
    # Displays Background
    win.blit(background, (0, 0))
    for copy in current_Clickable.copies:
        win.blit(copy.image_copy, copy.rect)
    # Checks game state
    if main_menu:
        # displays certain objects
        for obj in Main_Menu_Objects:
            win.blit(obj.image_to_display, obj.get_center_cor())
    if display_game_menu:
        for glow in Glow_Effects:
            win.blit(glow.image_copy, glow.rect)
        for obj in Game_Menu_Objects_Back:
            win.blit(obj.image_to_display, obj.get_center_cor())
        for obj in Game_Menu_Objects:
            win.blit(obj.image_to_display, obj.get_center_cor())
        for obj in Game_Menu_Objects_Front:
            win.blit(obj.image_to_display, obj.get_center_cor())
    if block_pressed:
        total_amount_bought = 0
        for item in Buy_Boxes:
            total_amount_bought += item.amount_bought

        temp_text = ""
        if 1000 > (1 * click_multiplier) + (non_click_multiplier * total_amount_bought) >= 0:
            temp_text = "+" + str(round((1 * click_multiplier) + (non_click_multiplier * total_amount_bought)))
        if (1 * click_multiplier) + (non_click_multiplier * total_amount_bought) >= 1000:
            temp_text = "+" + str(divide_by_1000((1 * click_multiplier) + (non_click_multiplier * total_amount_bought), is_price=True))

        Text(font_click_amount, temp_text, (random.randint(300, 500), random.randint(200, 400)),
             Game_Menu_Objects_Front, is_click_text=True)
        block_pressed = False

    i = random.randint(0, 21000)
    if i == 1:
        Button('Minecraft Clicker Images/Buttons/Lucky_Blocks.png', (0, 0, 75, 75),
               (random.randint(100, 700), random.randint(100, 500)), lucky_block_call, lucky_block_uncall,
               Overlay_Objects, lucky_block_pressed, is_lucky_block=True)

    if shop_menu:
        for obj in Shop_Menu_Objects_Far_Back:
            win.blit(obj.image_to_display, obj.get_center_cor())
        for obj in Shop_Menu_Objects_Back:
            win.blit(obj.image_to_display, obj.get_center_cor())
        for obj in Shop_Menu_Objects_Front:
            win.blit(obj.image_to_display, obj.get_center_cor())
        for obj in Shop_Menu_Objects_Very_Front:
            win.blit(obj.image_to_display, obj.get_center_cor())
    if upgrade_menu:
        for obj in Upgrade_Menu_Objects_Far_Back:
            win.blit(obj.image_to_display, obj.get_center_cor())
        for obj in Upgrade_Menu_Objects_Back:
            win.blit(obj.image_to_display, obj.get_center_cor())
        for obj in Upgrade_Menu_Objects_Front:
            win.blit(obj.image_to_display, obj.get_center_cor())
        for obj in Upgrade_Menu_Objects_Very_Front:
            win.blit(obj.image_to_display, obj.get_center_cor())
    if display_game_menu:
        for obj in Overlay_Objects:
            win.blit(obj.image_to_display, obj.get_center_cor())
    if setting_menu:
        for obj in Settings_Menu_Objects:
            win.blit(obj.image_to_display, obj.get_center_cor())
    pygame.display.update()


def update_game_events():
    # Updates event states
    grass_click_events_call.clear()
    grass_click_events_call.append(display_game_menu)
    grass_click_events_uncall.clear()
    grass_click_events_uncall.append(not display_game_menu)

    start_gameB_events_call.clear()
    start_gameB_events_call.append(main_menu)
    start_gameB_events_uncall.clear()
    start_gameB_events_uncall.append(not main_menu)

    shopB_events_call.clear()
    shopB_events_call.append(display_game_menu)
    shopB_events_uncall.clear()
    shopB_events_uncall.append(not display_game_menu)

    upgradeB_events_call.clear()
    upgradeB_events_call.append(display_game_menu)
    upgradeB_events_uncall.clear()
    upgradeB_events_uncall.append(not display_game_menu)

    for button in Buttons:
        if button.buy_box is not None:
            button.buy_box.overlay_events_call.clear()
            button.buy_box.overlay_events_call.append(shop_menu)
            button.buy_box.overlay_events_uncall.clear()
            button.buy_box.overlay_events_uncall.append(not shop_menu)
        if button.upgrade_box is not None:
            button.upgrade_box.events_call.clear()
            button.upgrade_box.events_call.append(upgrade_menu)
            button.upgrade_box.events_uncall.clear()
            button.upgrade_box.events_uncall.append(not upgrade_menu)

    settingB_events_call.clear()
    settingB_events_call.append(display_game_menu)
    settingB_events_call.append(main_menu)
    settingB_events_uncall.clear()
    settingB_events_uncall.append(not main_menu)
    settingB_events_uncall.append(not display_game_menu)

    settings_Buttons_call.clear()
    settings_Buttons_call.append(setting_menu)
    settings_Buttons_uncall.clear()
    settings_Buttons_uncall.append(not setting_menu)

    Shop_scroll_barB_events_call.clear()
    Shop_scroll_barB_events_call.append(shop_menu)
    Shop_scroll_barB_events_uncall.clear()
    Shop_scroll_barB_events_uncall.append(not shop_menu)

    Upgrade_scroll_barB_events_call.clear()
    Upgrade_scroll_barB_events_call.append(upgrade_menu)
    Upgrade_scroll_barB_events_uncall.clear()
    Upgrade_scroll_barB_events_uncall.append(not upgrade_menu)


def divide_by_1000(num, is_blocks=False, is_price=False, is_per_second=False, is_amount_bought=False):
    global times_divided
    temp_text = ""
    rem = num / 1000
    if rem < 1000:
        if times_divided == 0:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "K"
        if times_divided == 1:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Mil"
        if times_divided == 2:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Bil"
        if times_divided == 3:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Tril"
        if times_divided == 4:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Quad"
        if times_divided == 5:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Quin"
        if times_divided == 6:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Sex"
        if times_divided == 7:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Sep"
        if times_divided == 8:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Oct"
        if times_divided == 9:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Non"
        if times_divided == 10:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Dec"
        if times_divided == 11:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Undec"
        if times_divided == 12:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Duodec"
        if times_divided == 13:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Tredec"
        if times_divided == 14:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Quattuordec"
        if times_divided == 15:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Quindec"
        if times_divided == 16:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Sexdec"
        if times_divided == 17:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Septdec"
        if times_divided == 18:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Octodec"
        if times_divided == 19:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Novemdec"
        if times_divided == 20:
            times_divided = 0
            temp_text = str(round(rem * (1000 ** times_divided), 1)) + "Vigin"
        if is_blocks:
            return temp_text + " blocks"
        if is_per_second:
            return temp_text + " per second"
        if is_amount_bought or is_price:
            return temp_text
    if rem >= 1000:
        times_divided += 1
        return divide_by_1000(rem, is_blocks=is_blocks, is_per_second=is_per_second, is_amount_bought=is_amount_bought,
                              is_price=is_price)


def save_game():
    global float_values
    temp_bps = []
    temp_bps_multiplier = []
    temp_amount_bought = []
    temp_times_bought = []
    temp_upgrade_current_price = []
    temp_buy_current_price = []

    for obj in Buy_Boxes:
        temp_bps.append(obj.bps)
        temp_bps_multiplier.append(obj.bps_multiplier)
        temp_amount_bought.append(obj.amount_bought)
        temp_buy_current_price.append(obj.current_price)
    for obj in Upgrade_Boxes:
        temp_times_bought.append(obj.times_bought)
        temp_upgrade_current_price.append(obj.current_price)

    float_values.clear()
    float_values.append(blocks)
    float_values.append(total_blocks)
    float_values.append(click_multiplier)
    float_values.append(block_multiplier)
    float_values.append(non_click_multiplier)
    current_temp_clickable = [current_Clickable.name]

    with open('save_game.txt', mode='w') as save:
        csv_writer = csv.writer(save)
        csv_writer.writerow(float_values)  # 1
        csv_writer.writerow(upgrade_boxes_active)  # 2
        csv_writer.writerow(buy_boxes_to_initialize)  # 3
        csv_writer.writerow(upgrade_boxes_to_initialize)  # 4
        csv_writer.writerow(clickables_to_initialize)  # 5
        csv_writer.writerow(current_clickable_completed)  # 6
        csv_writer.writerow(current_temp_clickable)  # 7
        csv_writer.writerow(temp_bps)  # 8
        csv_writer.writerow(temp_bps_multiplier)  # 9
        csv_writer.writerow(temp_amount_bought)  # 10
        csv_writer.writerow(temp_times_bought)  # 11
        csv_writer.writerow(temp_buy_current_price)  # 12
        csv_writer.writerow(temp_upgrade_current_price)  # 13
        csv_writer.writerow(Clickables_Icon_Objects)  # 14
        csv_writer.writerow(Block_Multi_Objects)  # 15
        csv_writer.writerow(Pickaxe_Icon_Objects)  # 16
        csv_writer.writerow(Axe_Icon_Objects)  # 17
        csv_writer.writerow(Shovel_Icon_Objects)  # 18
        csv_writer.writerow(Sword_Icon_Objects)  # 19
        csv_writer.writerow(Hoe_Icon_Objects)  # 20
        csv_writer.writerow(Shears_Icon_Objects)  # 21
        csv_writer.writerow(Firecharge_Icon_Objects)  # 22
        csv_writer.writerow(Bow_Icon_Objects)  # 23
        csv_writer.writerow(Rod_Icon_Objects)  # 24
        csv_writer.writerow(Fns_Icon_Objects)  # 25
        csv_writer.writerow(Tnt_Icon_Objects)  # 26
        csv_writer.writerow(Beacon_Icon_Objects)  # 27
        csv_writer.writerow(Creeper_Icon_Objects)  # 28
        csv_writer.writerow(Fireball_Icon_Objects)  # 29
        csv_writer.writerow(Crystal_Icon_Objects)  # 30
        csv_writer.writerow(Dragon_Icon_Objects)  # 31
        csv_writer.writerow(Wither_Icon_Objects)  # 32


def open_save():
    global blocks
    global total_blocks
    global click_multiplier
    global block_multiplier
    global float_values
    global non_click_multiplier
    global current_Clickable
    with open('save_game.txt') as save_game_1:
        csv_reader = csv.reader(save_game_1)
        line_count = 1
        for row in csv_reader:
            if line_count == 1:
                line_count += 1
                float_values = row
                blocks = eval(float_values[0])
                total_blocks = eval(float_values[1])
                click_multiplier = eval(float_values[2])
                block_multiplier = eval(float_values[3])
                non_click_multiplier = eval(float_values[4])
            elif line_count == 2:
                line_count += 1
                for box in row:
                    upgrade_boxes_active.append(eval(box))
                check_upgrade_box_cor()
            elif line_count == 3:
                line_count += 1
                for buybox in row:
                    eval(buybox).initialized = True
                    buy_boxes_to_initialize.append(eval(buybox))
            elif line_count == 4:
                line_count += 1
                for upgradebox in row:
                    eval(upgradebox).initialized = True
                    upgrade_boxes_to_initialize.append(eval(upgradebox))
            elif line_count == 5:
                line_count += 1
                for clickable in row:
                    eval(clickable).initialized = True
                    clickables_to_initialize.append(eval(clickable))
            elif line_count == 6:
                line_count += 1
                for clickable in row:
                    eval(clickable).completed = True
                    current_clickable_completed.append(eval(clickable))
            elif line_count == 7:
                line_count += 1
                Game_Menu_Objects.append(eval(row[0]))
                current_Clickable = eval(row[0])
            elif line_count == 8:
                line_count += 1
                for pair in enumerate(Buy_Boxes, 0):
                    pair[1].bps = eval(row[pair[0]])
            elif line_count == 9:
                line_count += 1
                for pair in enumerate(Buy_Boxes, 0):
                    pair[1].bps_multiplier = eval(row[pair[0]])
            elif line_count == 10:
                line_count += 1
                for pair in enumerate(Buy_Boxes, 0):
                    pair[1].amount_bought = eval(row[pair[0]])
            elif line_count == 11:
                line_count += 1
                for pair in enumerate(Upgrade_Boxes, 0):
                    pair[1].times_bought = eval(row[pair[0]])
            elif line_count == 12:
                line_count += 1
                for pair in enumerate(Buy_Boxes, 0):
                    pair[1].current_price = eval(row[pair[0]])
            elif line_count == 13:
                line_count += 1
                for pair in enumerate(Upgrade_Boxes, 0):
                    pair[1].current_price = eval(row[pair[0]])
            elif line_count == 14:
                line_count += 1
                Clickables_Icon_Objects.clear()
                for clickable_icon in row:
                    Clickables_Icon_Objects.append(eval(clickable_icon))
            elif line_count == 15:
                line_count += 1
                Block_Multi_Objects.clear()
                for block_icon in row:
                    Block_Multi_Objects.append(eval(block_icon))
            elif line_count == 16:
                line_count += 1
                Pickaxe_Icon_Objects.clear()
                for icon in row:
                    Pickaxe_Icon_Objects.append(eval(icon))
            elif line_count == 17:
                line_count += 1
                Axe_Icon_Objects.clear()
                for icon in row:
                    Axe_Icon_Objects.append(eval(icon))
            elif line_count == 18:
                line_count += 1
                Shovel_Icon_Objects.clear()
                for icon in row:
                    Shovel_Icon_Objects.append(eval(icon))
            elif line_count == 19:
                line_count += 1
                Sword_Icon_Objects.clear()
                for icon in row:
                    Sword_Icon_Objects.append(eval(icon))
            elif line_count == 20:
                line_count += 1
                Hoe_Icon_Objects.clear()
                for icon in row:
                    Hoe_Icon_Objects.append(eval(icon))
            elif line_count == 21:
                line_count += 1
                Shears_Icon_Objects.clear()
                for icon in row:
                    Shears_Icon_Objects.append(eval(icon))
            elif line_count == 22:
                line_count += 1
                Firecharge_Icon_Objects.clear()
                for icon in row:
                    Firecharge_Icon_Objects.append(eval(icon))
            elif line_count == 23:
                line_count += 1
                Bow_Icon_Objects.clear()
                for icon in row:
                    Bow_Icon_Objects.append(eval(icon))
            elif line_count == 24:
                line_count += 1
                Rod_Icon_Objects.clear()
                for icon in row:
                    Rod_Icon_Objects.append(eval(icon))
            elif line_count == 25:
                line_count += 1
                Fns_Icon_Objects.clear()
                for icon in row:
                    Fns_Icon_Objects.append(eval(icon))
            elif line_count == 26:
                line_count += 1
                Tnt_Icon_Objects.clear()
                for icon in row:
                    Tnt_Icon_Objects.append(eval(icon))
            elif line_count == 27:
                line_count += 1
                Beacon_Icon_Objects.clear()
                for icon in row:
                    Beacon_Icon_Objects.append(eval(icon))
            elif line_count == 28:
                line_count += 1
                Creeper_Icon_Objects.clear()
                for icon in row:
                    Creeper_Icon_Objects.append(eval(icon))
            elif line_count == 29:
                line_count += 1
                Fireball_Icon_Objects.clear()
                for icon in row:
                    Fireball_Icon_Objects.append(eval(icon))
            elif line_count == 30:
                line_count += 1
                Crystal_Icon_Objects.clear()
                for icon in row:
                    Crystal_Icon_Objects.append(eval(icon))
            elif line_count == 31:
                line_count += 1
                Dragon_Icon_Objects.clear()
                for icon in row:
                    Dragon_Icon_Objects.append(eval(icon))
            elif line_count == 32:
                line_count += 1
                Wither_Icon_Objects.clear()
                for icon in row:
                    Wither_Icon_Objects.append(eval(icon))


# Instantiating all objects
instances = True
if instances:
    click_upgrade_box = upgrade_Box("Better Blocks", 100, Clickables_Icon_Objects, is_clickable=True,
                                    name="click_upgrade_box", info_box_text="Doubles blocks per click")

    grass_click = Clickable('Minecraft Clicker Images/Clickables/grassblock_click.png', "grass_click", is_default=True)
    sand_click = Clickable('Minecraft Clicker Images/Clickables/sandblock_click.png', "sand_click")
    oak_click = Clickable('Minecraft Clicker Images/Clickables/oakwoodblock_click.png', "oak_click")
    stone_click = Clickable('Minecraft Clicker Images/Clickables/stoneblock_click.png', "stone_click")
    iron_click = Clickable('Minecraft Clicker Images/Clickables/ironoreblock_click.png', "iron_click")
    ice_click = Clickable('Minecraft Clicker Images/Clickables/iceblock_click.png', "ice_click")
    glowstone_click = Clickable('Minecraft Clicker Images/Clickables/glowstoneblock_click.png', "glowstone_click")
    diamondore_click = Clickable('Minecraft Clicker Images/Clickables/diamondoreblock_click.png', "diamondore_click")
    slimeblock_click = Clickable('Minecraft Clicker Images/Clickables/slimeblock_click.png', "slimeblock_click")
    obsidian_click = Clickable('Minecraft Clicker Images/Clickables/obsidianblock_click.png', "obsidian_click")
    diamondblock_click = Clickable('Minecraft Clicker Images/Clickables/diamondblock_click.png', "diamondblock_click")
    dragonegg_click = Clickable('Minecraft Clicker Images/Clickables/dragoneggblock_click.png', "dragonegg_click")
    bedrock_click = Clickable('Minecraft Clicker Images/Clickables/bedrockblock_click.png', "bedrock_click")

    current_Clickable = grass_click

    # Buy Boxes
    pickaxe_buy_box = buy_Box("Pickaxe", 15, (535, 56), 0.1, name_obj="pickaxe_buy_box")
    axe_buy_box = buy_Box("Axe", 100, (535, 112), 1, name_obj="axe_buy_box")
    shovel_buy_box = buy_Box("Shovel", 1100, (535, 168), 8, name_obj="shovel_buy_box")
    sword_buy_box = buy_Box("Sword", 12000, (535, 224), 47, name_obj="sword_buy_box")
    hoe_buy_box = buy_Box("Hoe", 130000, (535, 280), 260, name_obj="hoe_buy_box")
    shears_buy_box = buy_Box("Shears", 1400000, (535, 336), 1400, name_obj="shears_buy_box")
    firecharge_buy_box = buy_Box("Fire Charge", 20000000, (535, 392), 7800, name_obj="firecharge_buy_box")
    bow_buy_box = buy_Box("Bow", 330000000, (535, 448), 44000, name_obj="bow_buy_box")
    rod_buy_box = buy_Box("Fishing Rod", 5100000000, (535, 504), 260000, name_obj="rod_buy_box")
    fns_buy_box = buy_Box("Flint & Steel", 75000000000, (535, 560), 1600000, name_obj="fns_buy_box")
    tnt_buy_box = buy_Box("Tnt", 1000000000000, (535, 616), 10000000, name_obj="tnt_buy_box")
    beacon_buy_box = buy_Box("Beacon", 14000000000000, (535, 672), 65000000, name_obj="beacon_buy_box")
    creeper_buy_box = buy_Box("Creeper", 170000000000000, (535, 728), 430000000, name_obj="creeper_buy_box")
    fireball_buy_box = buy_Box("Fireball", 2100000000000000, (535, 784), 2900000000, name_obj="fireball_buy_box")
    crystal_buy_box = buy_Box("End Crystal", 26000000000000000, (535, 840), 21000000000, name_obj="crystal_buy_box")
    dragon_buy_box = buy_Box("Dragon", 310000000000000000, (535, 896), 150000000000, name_obj="dragon_buy_box")
    wither_buy_box = buy_Box("Wither", 71000000000000000000, (535, 952), 1100000000000, name_obj="wither_buy_box")

    # Upgrade Boxes
    pickaxe_upgrade_box = upgrade_Box("Better Pickaxes", 100, Pickaxe_Icon_Objects, tiered_building=pickaxe_buy_box,
                                      name="pickaxe_upgrade_box")
    axe_upgrade_box = upgrade_Box("Better Axes", 1000, Axe_Icon_Objects, tiered_building=axe_buy_box,
                                  name="axe_upgrade_box")
    shovel_upgrade_box = upgrade_Box("Better Shovels", 11000, Shovel_Icon_Objects, tiered_building=shovel_buy_box,
                                     name="shovel_upgrade_box")
    sword_upgrade_box = upgrade_Box("Better Swords", 120000, Sword_Icon_Objects, tiered_building=sword_buy_box,
                                    name="sword_upgrade_box")
    hoe_upgrade_box = upgrade_Box("Better Hoes", 1300000, Hoe_Icon_Objects, tiered_building=hoe_buy_box,
                                  name="hoe_upgrade_box")
    shears_upgrade_box = upgrade_Box("Better Shears", 14000000, Shears_Icon_Objects, tiered_building=shears_buy_box,
                                     name="shears_upgrade_box")
    firecharge_upgrade_box = upgrade_Box("Better Fire Charges", 200000000, Firecharge_Icon_Objects,
                                         tiered_building=firecharge_buy_box,
                                         name="firecharge_upgrade_box")
    bow_upgrade_box = upgrade_Box("Better Bows", 3300000000, Bow_Icon_Objects, tiered_building=bow_buy_box,
                                  name="bow_upgrade_box")
    rod_upgrade_box = upgrade_Box("Better Fishing Rods", 51000000000, Rod_Icon_Objects, tiered_building=rod_buy_box,
                                  name="rod_upgrade_box")
    fns_upgrade_box = upgrade_Box("Better Flint & Steels", 750000000000, Fns_Icon_Objects, tiered_building=fns_buy_box,
                                  name="fns_upgrade_box")
    tnt_upgrade_box = upgrade_Box("Better Tnts", 10000000000000, Tnt_Icon_Objects, tiered_building=tnt_buy_box,
                                  name="tnt_upgrade_box")
    beacon_upgrade_box = upgrade_Box("Better Beacons", 140000000000000, Beacon_Icon_Objects,
                                     tiered_building=beacon_buy_box,
                                     name="tnt_upgrade_box")
    creeper_upgrade_box = upgrade_Box("Better Creepers", 1700000000000000, Creeper_Icon_Objects,
                                      tiered_building=creeper_buy_box,
                                      name="creeper_upgrade_box")
    fireball_upgrade_box = upgrade_Box("Better Fireballs", 21000000000000000, Fireball_Icon_Objects,
                                       tiered_building=fireball_buy_box,
                                       name="fireball_upgrade_box")
    crystal_upgrade_box = upgrade_Box("Better Crystals", 260000000000000000, Crystal_Icon_Objects,
                                      tiered_building=crystal_buy_box,
                                      name="crystal_upgrade_box")
    dragon_upgrade_box = upgrade_Box("Better Dragons", 3100000000000000000, Dragon_Icon_Objects,
                                     tiered_building=dragon_buy_box,
                                     name="dragon_upgrade_box")
    wither_upgrade_box = upgrade_Box("Better Withers", 710000000000000000000, Wither_Icon_Objects,
                                     tiered_building=wither_buy_box,
                                     name="wither_upgrade_box")

    enhancement_upgrade_box = upgrade_Box("Enhancements", 1000000, Block_Multi_Objects, is_block_multi=True,
                                          name="enhancement_upgrade_box",
                                          info_box_text="Block production multiplier +10%")

    price_reduction_upgrade_box = upgrade_Box("Cheaper Prices", 1000000, Price_Reduction_Icon_Objects,
                                              name="price_reduction_upgrade_box",
                                              info_box_text="5% cheaper shop prices",
                                              is_price_reduction=True)

    icons = True
    if icons:
        # Icons
        wood_pick = Icon('Minecraft Clicker Images/Icons/Pickaxes/woodpick_icon.png', (200, 100), Pickaxe_Icon_Objects,
                         buy_box=pickaxe_buy_box, upgrade_box=pickaxe_upgrade_box, name="wood_pick")
        stone_pick = Icon('Minecraft Clicker Images/Icons/Pickaxes/stonepick_icon.png', (200, 100),
                          Pickaxe_Icon_Objects,
                          buy_box=pickaxe_buy_box, upgrade_box=pickaxe_upgrade_box, name="stone_pick")
        gold_pick = Icon('Minecraft Clicker Images/Icons/Pickaxes/goldpick_icon.png', (200, 100), Pickaxe_Icon_Objects,
                         buy_box=pickaxe_buy_box, upgrade_box=pickaxe_upgrade_box, name="gold_pick")
        iron_pick = Icon('Minecraft Clicker Images/Icons/Pickaxes/ironpick_icon.png', (200, 100), Pickaxe_Icon_Objects,
                         buy_box=pickaxe_buy_box, upgrade_box=pickaxe_upgrade_box, name="iron_pick")
        diamond_pick = Icon('Minecraft Clicker Images/Icons/Pickaxes/diamondpick_icon.png', (200, 100),
                            Pickaxe_Icon_Objects,
                            buy_box=pickaxe_buy_box, upgrade_box=pickaxe_upgrade_box, name="diamond_pick")
        netherite_pick = Icon('Minecraft Clicker Images/Icons/Pickaxes/netheritepick_icon.png', (200, 100),
                              Pickaxe_Icon_Objects, buy_box=pickaxe_buy_box, upgrade_box=pickaxe_upgrade_box,
                              name="netherite_pick")
        purple_pick = Icon('Minecraft Clicker Images/Icons/Pickaxes/purple_pick_icon.png', (200, 100),
                           Pickaxe_Icon_Objects,
                           buy_box=pickaxe_buy_box, upgrade_box=pickaxe_upgrade_box, name="purple_pick")
        green_pick = Icon('Minecraft Clicker Images/Icons/Pickaxes/green_pick_icon.png', (200, 100),
                          Pickaxe_Icon_Objects,
                          buy_box=pickaxe_buy_box, upgrade_box=pickaxe_upgrade_box, name="green_pick")
        orange_pick = Icon('Minecraft Clicker Images/Icons/Pickaxes/orange_pick_icon.png', (200, 100),
                           Pickaxe_Icon_Objects,
                           buy_box=pickaxe_buy_box, upgrade_box=pickaxe_upgrade_box, name="orange_pick")
        pink_pick = Icon('Minecraft Clicker Images/Icons/Pickaxes/pink_pick_icon.png', (200, 100), Pickaxe_Icon_Objects,
                         buy_box=pickaxe_buy_box, upgrade_box=pickaxe_upgrade_box, name="pink_pick")
        rainbow_pick = Icon('Minecraft Clicker Images/Icons/Pickaxes/rainbow_pick_icon.png', (200, 100),
                            Pickaxe_Icon_Objects,
                            buy_box=pickaxe_buy_box, upgrade_box=pickaxe_upgrade_box, name="rainbow_pick")

        wood_axe = Icon('Minecraft Clicker Images/Icons/Axes/woodaxe_icon.png', (200, 100),
                        buy_box_list=Axe_Icon_Objects,
                        buy_box=axe_buy_box, upgrade_box=axe_upgrade_box, name="wood_axe")
        stone_axe = Icon('Minecraft Clicker Images/Icons/Axes/stoneaxe_icon.png', (200, 100),
                         buy_box_list=Axe_Icon_Objects,
                         buy_box=axe_buy_box, upgrade_box=axe_upgrade_box, name="stone_axe")
        gold_axe = Icon('Minecraft Clicker Images/Icons/Axes/goldaxe_icon.png', (200, 100),
                        buy_box_list=Axe_Icon_Objects,
                        buy_box=axe_buy_box, upgrade_box=axe_upgrade_box, name="gold_axe")
        iron_axe = Icon('Minecraft Clicker Images/Icons/Axes/ironaxe_icon.png', (200, 100),
                        buy_box_list=Axe_Icon_Objects,
                        buy_box=axe_buy_box, upgrade_box=axe_upgrade_box, name="iron_axe")
        diamond_axe = Icon('Minecraft Clicker Images/Icons/Axes/diamondaxe_icon.png', (200, 100),
                           buy_box_list=Axe_Icon_Objects,
                           buy_box=axe_buy_box, upgrade_box=axe_upgrade_box, name="diamond_axe")
        netherite_axe = Icon('Minecraft Clicker Images/Icons/Axes/netheriteaxe_icon.png', (200, 100),
                             buy_box_list=Axe_Icon_Objects, buy_box=axe_buy_box, upgrade_box=axe_upgrade_box,
                             name="netherite_axe")
        purple_axe = Icon('Minecraft Clicker Images/Icons/Axes/purple_axe_icon.png', (200, 100),
                          buy_box_list=Axe_Icon_Objects,
                          buy_box=axe_buy_box, upgrade_box=axe_upgrade_box, name="purple_axe")
        green_axe = Icon('Minecraft Clicker Images/Icons/Axes/green_axe_icon.png', (200, 100),
                         buy_box_list=Axe_Icon_Objects,
                         buy_box=axe_buy_box, upgrade_box=axe_upgrade_box, name="green_axe")
        orange_axe = Icon('Minecraft Clicker Images/Icons/Axes/orange_axe_icon.png', (200, 100),
                          buy_box_list=Axe_Icon_Objects,
                          buy_box=axe_buy_box, upgrade_box=axe_upgrade_box, name="orange_axe")
        pink_axe = Icon('Minecraft Clicker Images/Icons/Axes/pink_axe_icon.png', (200, 100),
                        buy_box_list=Axe_Icon_Objects,
                        buy_box=axe_buy_box, upgrade_box=axe_upgrade_box, name="pink_axe")
        rainbow_axe = Icon('Minecraft Clicker Images/Icons/Axes/rainbow_axe_icon.png', (200, 100),
                           buy_box_list=Axe_Icon_Objects, buy_box=axe_buy_box, upgrade_box=axe_upgrade_box,
                           name="rainbow_axe")

        wood_shovel = Icon('Minecraft Clicker Images/Icons/Shovels/woodshovel_icon.png', (200, 100),
                           buy_box_list=Shovel_Icon_Objects, buy_box=shovel_buy_box, upgrade_box=shovel_upgrade_box,
                           name="wood_shovel")
        stone_shovel = Icon('Minecraft Clicker Images/Icons/Shovels/stoneshovel_icon.png', (200, 100),
                            buy_box_list=Shovel_Icon_Objects, buy_box=shovel_buy_box, upgrade_box=shovel_upgrade_box,
                            name="stone_shovel")
        gold_shovel = Icon('Minecraft Clicker Images/Icons/Shovels/goldshovel_icon.png', (200, 100),
                           buy_box_list=Shovel_Icon_Objects, buy_box=shovel_buy_box, upgrade_box=shovel_upgrade_box,
                           name="gold_shovel")
        iron_shovel = Icon('Minecraft Clicker Images/Icons/Shovels/ironshovel_icon.png', (200, 100),
                           buy_box_list=Shovel_Icon_Objects, buy_box=shovel_buy_box, upgrade_box=shovel_upgrade_box,
                           name="iron_shovel")
        diamond_shovel = Icon('Minecraft Clicker Images/Icons/Shovels/diamondshovel_icon.png', (200, 100),
                              buy_box_list=Shovel_Icon_Objects, buy_box=shovel_buy_box, upgrade_box=shovel_upgrade_box,
                              name="diamond_shovel")
        netherite_shovel = Icon('Minecraft Clicker Images/Icons/Shovels/netheriteshovel_icon.png', (200, 100),
                                buy_box_list=Shovel_Icon_Objects, buy_box=shovel_buy_box,
                                upgrade_box=shovel_upgrade_box,
                                name="netherite_shovel")
        purple_shovel = Icon('Minecraft Clicker Images/Icons/Shovels/purple_shovel_icon.png', (200, 100),
                             buy_box_list=Shovel_Icon_Objects, buy_box=shovel_buy_box, upgrade_box=shovel_upgrade_box,
                             name="purple_shovel")
        green_shovel = Icon('Minecraft Clicker Images/Icons/Shovels/green_shovel_icon.png', (200, 100),
                            buy_box_list=Shovel_Icon_Objects, buy_box=shovel_buy_box, upgrade_box=shovel_upgrade_box,
                            name="green_shovel")
        orange_shovel = Icon('Minecraft Clicker Images/Icons/Shovels/orange_shovel_icon.png', (200, 100),
                             buy_box_list=Shovel_Icon_Objects, buy_box=shovel_buy_box, upgrade_box=shovel_upgrade_box,
                             name="orange_shovel")
        pink_shovel = Icon('Minecraft Clicker Images/Icons/Shovels/pink_shovel_icon.png', (200, 100),
                           buy_box_list=Shovel_Icon_Objects, buy_box=shovel_buy_box, upgrade_box=shovel_upgrade_box,
                           name="pink_shovel")
        rainbow_shovel = Icon('Minecraft Clicker Images/Icons/Shovels/rainbow_shovel_icon.png', (200, 100),
                              buy_box_list=Shovel_Icon_Objects, buy_box=shovel_buy_box, upgrade_box=shovel_upgrade_box,
                              name="rainbow_shovel")

        wood_sword = Icon('Minecraft Clicker Images/Icons/Swords/woodsword_icon.png', (200, 100),
                          buy_box_list=Sword_Icon_Objects, buy_box=sword_buy_box, upgrade_box=sword_upgrade_box,
                          name="wood_sword")
        stone_sword = Icon('Minecraft Clicker Images/Icons/Swords/stonesword_icon.png', (200, 100),
                           buy_box_list=Sword_Icon_Objects, buy_box=sword_buy_box, upgrade_box=sword_upgrade_box,
                           name="stone_sword")
        gold_sword = Icon('Minecraft Clicker Images/Icons/Swords/goldsword_icon.png', (200, 100),
                          buy_box_list=Sword_Icon_Objects, buy_box=sword_buy_box, upgrade_box=sword_upgrade_box,
                          name="gold_sword")
        iron_sword = Icon('Minecraft Clicker Images/Icons/Swords/ironsword_icon.png', (200, 100),
                          buy_box_list=Sword_Icon_Objects, buy_box=sword_buy_box, upgrade_box=sword_upgrade_box,
                          name="iron_sword")
        diamond_sword = Icon('Minecraft Clicker Images/Icons/Swords/diamondsword_icon.png', (200, 100),
                             buy_box_list=Sword_Icon_Objects, buy_box=sword_buy_box, upgrade_box=sword_upgrade_box,
                             name="diamond_sword")
        netherite_sword = Icon('Minecraft Clicker Images/Icons/Swords/netheritesword_icon.png', (200, 100),
                               buy_box_list=Sword_Icon_Objects, buy_box=sword_buy_box, upgrade_box=sword_upgrade_box,
                               name="netherite_sword")
        purple_sword = Icon('Minecraft Clicker Images/Icons/Swords/purple_sword_icon.png', (200, 100),
                            buy_box_list=Sword_Icon_Objects, buy_box=sword_buy_box, upgrade_box=sword_upgrade_box,
                            name="purple_sword")
        green_sword = Icon('Minecraft Clicker Images/Icons/Swords/green_sword_icon.png', (200, 100),
                           buy_box_list=Sword_Icon_Objects, buy_box=sword_buy_box, upgrade_box=sword_upgrade_box,
                           name="green_sword")
        orange_sword = Icon('Minecraft Clicker Images/Icons/Swords/orange_sword_icon.png', (200, 100),
                            buy_box_list=Sword_Icon_Objects, buy_box=sword_buy_box, upgrade_box=sword_upgrade_box,
                            name="orange_sword")
        pink_sword = Icon('Minecraft Clicker Images/Icons/Swords/pink_sword_icon.png', (200, 100),
                          buy_box_list=Sword_Icon_Objects, buy_box=sword_buy_box, upgrade_box=sword_upgrade_box,
                          name="pink_sword")
        rainbow_sword = Icon('Minecraft Clicker Images/Icons/Swords/rainbow_sword_icon.png', (200, 100),
                             buy_box_list=Sword_Icon_Objects, buy_box=sword_buy_box, upgrade_box=sword_upgrade_box,
                             name="rainbow_sword")

        wood_hoe = Icon('Minecraft Clicker Images/Icons/Hoes/wood_hoe_icon.png', (200, 100),
                        buy_box_list=Hoe_Icon_Objects, buy_box=hoe_buy_box, upgrade_box=hoe_upgrade_box,
                        name="wood_hoe")
        stone_hoe = Icon('Minecraft Clicker Images/Icons/Hoes/stone_hoe_icon.png', (200, 100),
                         buy_box_list=Hoe_Icon_Objects, buy_box=hoe_buy_box, upgrade_box=hoe_upgrade_box,
                         name="stone_hoe")
        gold_hoe = Icon('Minecraft Clicker Images/Icons/Hoes/gold_hoe_icon.png', (200, 100),
                        buy_box_list=Hoe_Icon_Objects, buy_box=hoe_buy_box, upgrade_box=hoe_upgrade_box,
                        name="gold_hoe")
        iron_hoe = Icon('Minecraft Clicker Images/Icons/Hoes/iron_hoe_icon.png', (200, 100),
                        buy_box_list=Hoe_Icon_Objects, buy_box=hoe_buy_box, upgrade_box=hoe_upgrade_box,
                        name="iron_hoe")
        diamond_hoe = Icon('Minecraft Clicker Images/Icons/Hoes/diamond_hoe_icon.png', (200, 100),
                           buy_box_list=Hoe_Icon_Objects, buy_box=hoe_buy_box, upgrade_box=hoe_upgrade_box,
                           name="diamond_hoe")
        netherite_hoe = Icon('Minecraft Clicker Images/Icons/Hoes/netherite_hoe_icon.png', (200, 100),
                             buy_box_list=Hoe_Icon_Objects, buy_box=hoe_buy_box, upgrade_box=hoe_upgrade_box,
                             name="netherite_hoe")
        purple_hoe = Icon('Minecraft Clicker Images/Icons/Hoes/purple_hoe_icon.png', (200, 100),
                          buy_box_list=Hoe_Icon_Objects, buy_box=hoe_buy_box, upgrade_box=hoe_upgrade_box,
                          name="purple_hoe")
        green_hoe = Icon('Minecraft Clicker Images/Icons/Hoes/green_hoe_icon.png', (200, 100),
                         buy_box_list=Hoe_Icon_Objects, buy_box=hoe_buy_box, upgrade_box=hoe_upgrade_box,
                         name="green_hoe")
        orange_hoe = Icon('Minecraft Clicker Images/Icons/Hoes/orange_hoe_icon.png', (200, 100),
                          buy_box_list=Hoe_Icon_Objects, buy_box=hoe_buy_box, upgrade_box=hoe_upgrade_box,
                          name="orange_hoe")
        pink_hoe = Icon('Minecraft Clicker Images/Icons/Hoes/pink_hoe_icon.png', (200, 100),
                        buy_box_list=Hoe_Icon_Objects, buy_box=hoe_buy_box, upgrade_box=hoe_upgrade_box,
                        name="pink_hoe")
        rainbow_hoe = Icon('Minecraft Clicker Images/Icons/Hoes/rainbow_hoe_icon.png', (200, 100),
                           buy_box_list=Hoe_Icon_Objects, buy_box=hoe_buy_box, upgrade_box=hoe_upgrade_box,
                           name="rainbow_hoe")

        cream_shears = Icon('Minecraft Clicker Images/Icons/Shears/cream_shears_icon.png', (200, 100),
                            buy_box_list=Shears_Icon_Objects, buy_box=shears_buy_box, upgrade_box=shears_upgrade_box,
                            name="cream_shears")
        greyscale_shears = Icon('Minecraft Clicker Images/Icons/Shears/greyscale_shears_icon.png', (200, 100),
                                buy_box_list=Shears_Icon_Objects, buy_box=shears_buy_box,
                                upgrade_box=shears_upgrade_box,
                                name="greyscale_shears")
        yellow_shears = Icon('Minecraft Clicker Images/Icons/Shears/yellow_shears_icon.png', (200, 100),
                             buy_box_list=Shears_Icon_Objects, buy_box=shears_buy_box, upgrade_box=shears_upgrade_box,
                             name="yellow_shears")
        blue_shears = Icon('Minecraft Clicker Images/Icons/Shears/blue_shears_icon.png', (200, 100),
                           buy_box_list=Shears_Icon_Objects, buy_box=shears_buy_box, upgrade_box=shears_upgrade_box,
                           name="blue_shears")
        cyan_shears = Icon('Minecraft Clicker Images/Icons/Shears/cyan_shears_icon.png', (200, 100),
                           buy_box_list=Shears_Icon_Objects, buy_box=shears_buy_box, upgrade_box=shears_upgrade_box,
                           name="cyan_shears")
        red_shears = Icon('Minecraft Clicker Images/Icons/Shears/red_shears_icon.png', (200, 100),
                          buy_box_list=Shears_Icon_Objects, buy_box=shears_buy_box, upgrade_box=shears_upgrade_box,
                          name="red_shears")
        purple_shears = Icon('Minecraft Clicker Images/Icons/Shears/purple_shears_icon.png', (200, 100),
                             buy_box_list=Shears_Icon_Objects, buy_box=shears_buy_box, upgrade_box=shears_upgrade_box,
                             name="purple_shears")
        green_shears = Icon('Minecraft Clicker Images/Icons/Shears/green_shears_icon.png', (200, 100),
                            buy_box_list=Shears_Icon_Objects, buy_box=shears_buy_box, upgrade_box=shears_upgrade_box,
                            name="green_shears")
        orange_shears = Icon('Minecraft Clicker Images/Icons/Shears/orange_shears_icon.png', (200, 100),
                             buy_box_list=Shears_Icon_Objects, buy_box=shears_buy_box, upgrade_box=shears_upgrade_box,
                             name="orange_shears")
        pink_shears = Icon('Minecraft Clicker Images/Icons/Shears/pink_shears_icon.png', (200, 100),
                           buy_box_list=Shears_Icon_Objects, buy_box=shears_buy_box, upgrade_box=shears_upgrade_box,
                           name="pink_shears")
        rainbow_shears = Icon('Minecraft Clicker Images/Icons/Shears/rainbow_shears_icon.png', (200, 100),
                              buy_box_list=Shears_Icon_Objects, buy_box=shears_buy_box, upgrade_box=shears_upgrade_box,
                              name="rainbow_shears")

        cream_firecharge = Icon('Minecraft Clicker Images/Icons/Firecharges/cream_firecharge_icon.png', (200, 100),
                                buy_box_list=Firecharge_Icon_Objects, buy_box=firecharge_buy_box,
                                upgrade_box=firecharge_upgrade_box,
                                name="cream_firecharge")
        greyscale_firecharge = Icon('Minecraft Clicker Images/Icons/Firecharges/greyscale_firecharge_icon.png',
                                    (200, 100),
                                    buy_box_list=Firecharge_Icon_Objects, buy_box=firecharge_buy_box,
                                    upgrade_box=firecharge_upgrade_box,
                                    name="greyscale_firecharge")
        yellow_firecharge = Icon('Minecraft Clicker Images/Icons/Firecharges/yellow_firecharge_icon.png', (200, 100),
                                 buy_box_list=Firecharge_Icon_Objects, buy_box=firecharge_buy_box,
                                 upgrade_box=firecharge_upgrade_box,
                                 name="yellow_firecharge")
        blue_firecharge = Icon('Minecraft Clicker Images/Icons/Firecharges/blue_firecharge_icon.png', (200, 100),
                               buy_box_list=Firecharge_Icon_Objects, buy_box=firecharge_buy_box,
                               upgrade_box=firecharge_upgrade_box,
                               name="blue_firecharge")
        cyan_firecharge = Icon('Minecraft Clicker Images/Icons/Firecharges/cyan_firecharge_icon.png', (200, 100),
                               buy_box_list=Firecharge_Icon_Objects, buy_box=firecharge_buy_box,
                               upgrade_box=firecharge_upgrade_box,
                               name="cyan_firecharge")
        red_firecharge = Icon('Minecraft Clicker Images/Icons/Firecharges/red_firecharge_icon.png', (200, 100),
                              buy_box_list=Firecharge_Icon_Objects, buy_box=firecharge_buy_box,
                              upgrade_box=firecharge_upgrade_box,
                              name="red_firecharge")
        purple_firecharge = Icon('Minecraft Clicker Images/Icons/Firecharges/purple_firecharge_icon.png', (200, 100),
                                 buy_box_list=Firecharge_Icon_Objects, buy_box=firecharge_buy_box,
                                 upgrade_box=firecharge_upgrade_box,
                                 name="purple_firecharge")
        green_firecharge = Icon('Minecraft Clicker Images/Icons/Firecharges/green_firecharge_icon.png', (200, 100),
                                buy_box_list=Firecharge_Icon_Objects, buy_box=firecharge_buy_box,
                                upgrade_box=firecharge_upgrade_box,
                                name="green_firecharge")
        orange_firecharge = Icon('Minecraft Clicker Images/Icons/Firecharges/orange_firecharge_icon.png', (200, 100),
                                 buy_box_list=Firecharge_Icon_Objects, buy_box=firecharge_buy_box,
                                 upgrade_box=firecharge_upgrade_box,
                                 name="orange_firecharge")
        pink_firecharge = Icon('Minecraft Clicker Images/Icons/Firecharges/pink_firecharge_icon.png', (200, 100),
                               buy_box_list=Firecharge_Icon_Objects, buy_box=firecharge_buy_box,
                               upgrade_box=firecharge_upgrade_box,
                               name="pink_firecharge")
        rainbow_firecharge = Icon('Minecraft Clicker Images/Icons/Firecharges/rainbow_firecharge_icon.png', (200, 100),
                                  buy_box_list=Firecharge_Icon_Objects, buy_box=firecharge_buy_box,
                                  upgrade_box=firecharge_upgrade_box,
                                  name="rainbow_firecharge")

        cream_bow = Icon('Minecraft Clicker Images/Icons/Bows/cream_bow_icon.png', (200, 100),
                         buy_box_list=Bow_Icon_Objects, buy_box=bow_buy_box, upgrade_box=bow_upgrade_box,
                         name="cream_bow")
        greyscale_bow = Icon('Minecraft Clicker Images/Icons/Bows/greyscale_bow_icon.png', (200, 100),
                             buy_box_list=Bow_Icon_Objects, buy_box=bow_buy_box, upgrade_box=bow_upgrade_box,
                             name="greyscale_bow")
        yellow_bow = Icon('Minecraft Clicker Images/Icons/Bows/yellow_bow_icon.png', (200, 100),
                          buy_box_list=Bow_Icon_Objects, buy_box=bow_buy_box, upgrade_box=bow_upgrade_box,
                          name="yellow_bow")
        blue_bow = Icon('Minecraft Clicker Images/Icons/Bows/blue_bow_icon.png', (200, 100),
                        buy_box_list=Bow_Icon_Objects, buy_box=bow_buy_box, upgrade_box=bow_upgrade_box,
                        name="blue_bow")
        cyan_bow = Icon('Minecraft Clicker Images/Icons/Bows/cyan_bow_icon.png', (200, 100),
                        buy_box_list=Bow_Icon_Objects, buy_box=bow_buy_box, upgrade_box=bow_upgrade_box,
                        name="cyan_bow")
        red_bow = Icon('Minecraft Clicker Images/Icons/Bows/red_bow_icon.png', (200, 100),
                       buy_box_list=Bow_Icon_Objects, buy_box=bow_buy_box, upgrade_box=bow_upgrade_box, name="red_bow")
        purple_bow = Icon('Minecraft Clicker Images/Icons/Bows/purple_bow_icon.png', (200, 100),
                          buy_box_list=Bow_Icon_Objects, buy_box=bow_buy_box, upgrade_box=bow_upgrade_box,
                          name="purple_bow")
        green_bow = Icon('Minecraft Clicker Images/Icons/Bows/green_bow_icon.png', (200, 100),
                         buy_box_list=Bow_Icon_Objects, buy_box=bow_buy_box, upgrade_box=bow_upgrade_box,
                         name="green_bow")
        orange_bow = Icon('Minecraft Clicker Images/Icons/Bows/orange_bow_icon.png', (200, 100),
                          buy_box_list=Bow_Icon_Objects, buy_box=bow_buy_box, upgrade_box=bow_upgrade_box,
                          name="orange_bow")
        pink_bow = Icon('Minecraft Clicker Images/Icons/Bows/pink_bow_icon.png', (200, 100),
                        buy_box_list=Bow_Icon_Objects, buy_box=bow_buy_box, upgrade_box=bow_upgrade_box,
                        name="pink_bow")
        rainbow_bow = Icon('Minecraft Clicker Images/Icons/Bows/rainbow_bow_icon.png', (200, 100),
                           buy_box_list=Bow_Icon_Objects, buy_box=bow_buy_box, upgrade_box=bow_upgrade_box,
                           name="rainbow_bow")

        cream_rod = Icon('Minecraft Clicker Images/Icons/Rods/cream_rod_icon.png', (200, 100),
                         buy_box_list=Rod_Icon_Objects, buy_box=rod_buy_box, upgrade_box=rod_upgrade_box,
                         name="cream_rod")
        greyscale_rod = Icon('Minecraft Clicker Images/Icons/Rods/greyscale_rod_icon.png', (200, 100),
                             buy_box_list=Rod_Icon_Objects, buy_box=rod_buy_box, upgrade_box=rod_upgrade_box,
                             name="greyscale_rod")
        yellow_rod = Icon('Minecraft Clicker Images/Icons/Rods/yellow_rod_icon.png', (200, 100),
                          buy_box_list=Rod_Icon_Objects, buy_box=rod_buy_box, upgrade_box=rod_upgrade_box,
                          name="yellow_rod")
        blue_rod = Icon('Minecraft Clicker Images/Icons/Rods/blue_rod_icon.png', (200, 100),
                        buy_box_list=Rod_Icon_Objects, buy_box=rod_buy_box, upgrade_box=rod_upgrade_box,
                        name="blue_rod")
        cyan_rod = Icon('Minecraft Clicker Images/Icons/Rods/cyan_rod_icon.png', (200, 100),
                        buy_box_list=Rod_Icon_Objects, buy_box=rod_buy_box, upgrade_box=rod_upgrade_box,
                        name="cyan_rod")
        red_rod = Icon('Minecraft Clicker Images/Icons/Rods/red_rod_icon.png', (200, 100),
                       buy_box_list=Rod_Icon_Objects, buy_box=rod_buy_box, upgrade_box=rod_upgrade_box, name="red_rod")
        purple_rod = Icon('Minecraft Clicker Images/Icons/Rods/purple_rod_icon.png', (200, 100),
                          buy_box_list=Rod_Icon_Objects, buy_box=rod_buy_box, upgrade_box=rod_upgrade_box,
                          name="purple_rod")
        green_rod = Icon('Minecraft Clicker Images/Icons/Rods/green_rod_icon.png', (200, 100),
                         buy_box_list=Rod_Icon_Objects, buy_box=rod_buy_box, upgrade_box=rod_upgrade_box,
                         name="green_rod")
        orange_rod = Icon('Minecraft Clicker Images/Icons/Rods/orange_rod_icon.png', (200, 100),
                          buy_box_list=Rod_Icon_Objects, buy_box=rod_buy_box, upgrade_box=rod_upgrade_box,
                          name="orange_rod")
        pink_rod = Icon('Minecraft Clicker Images/Icons/Rods/pink_rod_icon.png', (200, 100),
                        buy_box_list=Rod_Icon_Objects, buy_box=rod_buy_box, upgrade_box=rod_upgrade_box,
                        name="pink_rod")
        rainbow_rod = Icon('Minecraft Clicker Images/Icons/Rods/rainbow_rod_icon.png', (200, 100),
                           buy_box_list=Rod_Icon_Objects, buy_box=rod_buy_box, upgrade_box=rod_upgrade_box,
                           name="rainbow_rod")

        cream_fns = Icon('Minecraft Clicker Images/Icons/Fns/cream_fns_icon.png', (200, 100),
                         buy_box_list=Fns_Icon_Objects, buy_box=fns_buy_box, upgrade_box=fns_upgrade_box,
                         name="cream_fns")
        greyscale_fns = Icon('Minecraft Clicker Images/Icons/Fns/greyscale_fns_icon.png', (200, 100),
                             buy_box_list=Fns_Icon_Objects, buy_box=fns_buy_box, upgrade_box=fns_upgrade_box,
                             name="greyscale_fns")
        yellow_fns = Icon('Minecraft Clicker Images/Icons/Fns/yellow_fns_icon.png', (200, 100),
                          buy_box_list=Fns_Icon_Objects, buy_box=fns_buy_box, upgrade_box=fns_upgrade_box,
                          name="yellow_fns")
        blue_fns = Icon('Minecraft Clicker Images/Icons/Fns/blue_fns_icon.png', (200, 100),
                        buy_box_list=Fns_Icon_Objects, buy_box=fns_buy_box, upgrade_box=fns_upgrade_box,
                        name="blue_fns")
        cyan_fns = Icon('Minecraft Clicker Images/Icons/Fns/cyan_fns_icon.png', (200, 100),
                        buy_box_list=Fns_Icon_Objects, buy_box=fns_buy_box, upgrade_box=fns_upgrade_box,
                        name="cyan_fns")
        red_fns = Icon('Minecraft Clicker Images/Icons/Fns/red_fns_icon.png', (200, 100),
                       buy_box_list=Fns_Icon_Objects, buy_box=fns_buy_box, upgrade_box=fns_upgrade_box, name="red_fns")
        purple_fns = Icon('Minecraft Clicker Images/Icons/Fns/purple_fns_icon.png', (200, 100),
                          buy_box_list=Fns_Icon_Objects, buy_box=fns_buy_box, upgrade_box=fns_upgrade_box,
                          name="purple_fns")
        green_fns = Icon('Minecraft Clicker Images/Icons/Fns/green_fns_icon.png', (200, 100),
                         buy_box_list=Fns_Icon_Objects, buy_box=fns_buy_box, upgrade_box=fns_upgrade_box,
                         name="green_fns")
        orange_fns = Icon('Minecraft Clicker Images/Icons/Fns/orange_fns_icon.png', (200, 100),
                          buy_box_list=Fns_Icon_Objects, buy_box=fns_buy_box, upgrade_box=fns_upgrade_box,
                          name="orange_fns")
        pink_fns = Icon('Minecraft Clicker Images/Icons/Fns/pink_fns_icon.png', (200, 100),
                        buy_box_list=Fns_Icon_Objects, buy_box=fns_buy_box, upgrade_box=fns_upgrade_box,
                        name="pink_fns")
        rainbow_fns = Icon('Minecraft Clicker Images/Icons/Fns/rainbow_fns_icon.png', (200, 100),
                           buy_box_list=Fns_Icon_Objects, buy_box=fns_buy_box, upgrade_box=fns_upgrade_box,
                           name="rainbow_fns")

        cream_tnt = Icon('Minecraft Clicker Images/Icons/Tnt/cream_tnt_icon.png', (200, 100),
                         buy_box_list=Tnt_Icon_Objects, buy_box=tnt_buy_box, upgrade_box=tnt_upgrade_box,
                         name="cream_tnt")
        greyscale_tnt = Icon('Minecraft Clicker Images/Icons/Tnt/greyscale_tnt_icon.png', (200, 100),
                             buy_box_list=Tnt_Icon_Objects, buy_box=tnt_buy_box, upgrade_box=tnt_upgrade_box,
                             name="greyscale_tnt")
        yellow_tnt = Icon('Minecraft Clicker Images/Icons/Tnt/yellow_tnt_icon.png', (200, 100),
                          buy_box_list=Tnt_Icon_Objects, buy_box=tnt_buy_box, upgrade_box=tnt_upgrade_box,
                          name="yellow_tnt")
        blue_tnt = Icon('Minecraft Clicker Images/Icons/Tnt/blue_tnt_icon.png', (200, 100),
                        buy_box_list=Tnt_Icon_Objects, buy_box=tnt_buy_box, upgrade_box=tnt_upgrade_box,
                        name="blue_tnt")
        cyan_tnt = Icon('Minecraft Clicker Images/Icons/Tnt/cyan_tnt_icon.png', (200, 100),
                        buy_box_list=Tnt_Icon_Objects, buy_box=tnt_buy_box, upgrade_box=tnt_upgrade_box,
                        name="cyan_tnt")
        red_tnt = Icon('Minecraft Clicker Images/Icons/Tnt/red_tnt_icon.png', (200, 100),
                       buy_box_list=Tnt_Icon_Objects, buy_box=tnt_buy_box, upgrade_box=tnt_upgrade_box, name="red_tnt")
        purple_tnt = Icon('Minecraft Clicker Images/Icons/Tnt/purple_tnt_icon.png', (200, 100),
                          buy_box_list=Tnt_Icon_Objects, buy_box=tnt_buy_box, upgrade_box=tnt_upgrade_box,
                          name="purple_tnt")
        green_tnt = Icon('Minecraft Clicker Images/Icons/Tnt/green_tnt_icon.png', (200, 100),
                         buy_box_list=Tnt_Icon_Objects, buy_box=tnt_buy_box, upgrade_box=tnt_upgrade_box,
                         name="green_tnt")
        orange_tnt = Icon('Minecraft Clicker Images/Icons/Tnt/orange_tnt_icon.png', (200, 100),
                          buy_box_list=Tnt_Icon_Objects, buy_box=tnt_buy_box, upgrade_box=tnt_upgrade_box,
                          name="orange_tnt")
        pink_tnt = Icon('Minecraft Clicker Images/Icons/Tnt/pink_tnt_icon.png', (200, 100),
                        buy_box_list=Tnt_Icon_Objects, buy_box=tnt_buy_box, upgrade_box=tnt_upgrade_box,
                        name="pink_tnt")
        rainbow_tnt = Icon('Minecraft Clicker Images/Icons/Tnt/rainbow_tnt_icon.png', (200, 100),
                           buy_box_list=Tnt_Icon_Objects, buy_box=tnt_buy_box, upgrade_box=tnt_upgrade_box,
                           name="rainbow_tnt")

        cream_beacon = Icon('Minecraft Clicker Images/Icons/Beacons/cream_beacon_icon.png', (200, 100),
                            buy_box_list=Beacon_Icon_Objects, buy_box=beacon_buy_box, upgrade_box=beacon_upgrade_box,
                            name="cream_beacon")
        greyscale_beacon = Icon('Minecraft Clicker Images/Icons/Beacons/greyscale_beacon_icon.png', (200, 100),
                                buy_box_list=Beacon_Icon_Objects, buy_box=beacon_buy_box,
                                upgrade_box=beacon_upgrade_box,
                                name="greyscale_beacon")
        yellow_beacon = Icon('Minecraft Clicker Images/Icons/Beacons/yellow_beacon_icon.png', (200, 100),
                             buy_box_list=Beacon_Icon_Objects, buy_box=beacon_buy_box, upgrade_box=beacon_upgrade_box,
                             name="yellow_beacon")
        blue_beacon = Icon('Minecraft Clicker Images/Icons/Beacons/blue_beacon_icon.png', (200, 100),
                           buy_box_list=Beacon_Icon_Objects, buy_box=beacon_buy_box, upgrade_box=beacon_upgrade_box,
                           name="blue_beacon")
        cyan_beacon = Icon('Minecraft Clicker Images/Icons/Beacons/cyan_beacon_icon.png', (200, 100),
                           buy_box_list=Beacon_Icon_Objects, buy_box=beacon_buy_box, upgrade_box=beacon_upgrade_box,
                           name="cyan_beacon")
        red_beacon = Icon('Minecraft Clicker Images/Icons/Beacons/red_beacon_icon.png', (200, 100),
                          buy_box_list=Beacon_Icon_Objects, buy_box=beacon_buy_box, upgrade_box=beacon_upgrade_box,
                          name="red_beacon")
        purple_beacon = Icon('Minecraft Clicker Images/Icons/Beacons/purple_beacon_icon.png', (200, 100),
                             buy_box_list=Beacon_Icon_Objects, buy_box=beacon_buy_box, upgrade_box=beacon_upgrade_box,
                             name="purple_beacon")
        green_beacon = Icon('Minecraft Clicker Images/Icons/Beacons/green_beacon_icon.png', (200, 100),
                            buy_box_list=Beacon_Icon_Objects, buy_box=beacon_buy_box, upgrade_box=beacon_upgrade_box,
                            name="green_beacon")
        orange_beacon = Icon('Minecraft Clicker Images/Icons/Beacons/orange_beacon_icon.png', (200, 100),
                             buy_box_list=Beacon_Icon_Objects, buy_box=beacon_buy_box, upgrade_box=beacon_upgrade_box,
                             name="orange_beacon")
        pink_beacon = Icon('Minecraft Clicker Images/Icons/Beacons/pink_beacon_icon.png', (200, 100),
                           buy_box_list=Beacon_Icon_Objects, buy_box=beacon_buy_box, upgrade_box=beacon_upgrade_box,
                           name="pink_beacon")
        rainbow_beacon = Icon('Minecraft Clicker Images/Icons/Beacons/rainbow_beacon_icon.png', (200, 100),
                              buy_box_list=Beacon_Icon_Objects, buy_box=beacon_buy_box, upgrade_box=beacon_upgrade_box,
                              name="rainbow_beacon")

        cream_creeper = Icon('Minecraft Clicker Images/Icons/Creepers/cream_creeper_icon.png', (200, 100),
                             buy_box_list=Creeper_Icon_Objects, buy_box=creeper_buy_box,
                             upgrade_box=creeper_upgrade_box,
                             name="cream_creeper")
        greyscale_creeper = Icon('Minecraft Clicker Images/Icons/Creepers/greyscale_creeper_icon.png', (200, 100),
                                 buy_box_list=Creeper_Icon_Objects, buy_box=creeper_buy_box,
                                 upgrade_box=creeper_upgrade_box,
                                 name="greyscale_creeper")
        yellow_creeper = Icon('Minecraft Clicker Images/Icons/Creepers/yellow_creeper_icon.png', (200, 100),
                              buy_box_list=Creeper_Icon_Objects, buy_box=creeper_buy_box,
                              upgrade_box=creeper_upgrade_box,
                              name="yellow_creeper")
        blue_creeper = Icon('Minecraft Clicker Images/Icons/Creepers/blue_creeper_icon.png', (200, 100),
                            buy_box_list=Creeper_Icon_Objects, buy_box=creeper_buy_box, upgrade_box=creeper_upgrade_box,
                            name="blue_creeper")
        cyan_creeper = Icon('Minecraft Clicker Images/Icons/Creepers/cyan_creeper_icon.png', (200, 100),
                            buy_box_list=Creeper_Icon_Objects, buy_box=creeper_buy_box, upgrade_box=creeper_upgrade_box,
                            name="cyan_creeper")
        red_creeper = Icon('Minecraft Clicker Images/Icons/Creepers/red_creeper_icon.png', (200, 100),
                           buy_box_list=Creeper_Icon_Objects, buy_box=creeper_buy_box, upgrade_box=creeper_upgrade_box,
                           name="red_creeper")
        purple_creeper = Icon('Minecraft Clicker Images/Icons/Creepers/purple_creeper_icon.png', (200, 100),
                              buy_box_list=Creeper_Icon_Objects, buy_box=creeper_buy_box,
                              upgrade_box=creeper_upgrade_box,
                              name="purple_creeper")
        green_creeper = Icon('Minecraft Clicker Images/Icons/Creepers/green_creeper_icon.png', (200, 100),
                             buy_box_list=Creeper_Icon_Objects, buy_box=creeper_buy_box,
                             upgrade_box=creeper_upgrade_box,
                             name="green_creeper")
        orange_creeper = Icon('Minecraft Clicker Images/Icons/Creepers/orange_creeper_icon.png', (200, 100),
                              buy_box_list=Creeper_Icon_Objects, buy_box=creeper_buy_box,
                              upgrade_box=creeper_upgrade_box,
                              name="orange_creeper")
        pink_creeper = Icon('Minecraft Clicker Images/Icons/Creepers/pink_creeper_icon.png', (200, 100),
                            buy_box_list=Creeper_Icon_Objects, buy_box=creeper_buy_box, upgrade_box=creeper_upgrade_box,
                            name="pink_creeper")
        rainbow_creeper = Icon('Minecraft Clicker Images/Icons/Creepers/rainbow_creeper_icon.png', (200, 100),
                               buy_box_list=Creeper_Icon_Objects, buy_box=creeper_buy_box,
                               upgrade_box=creeper_upgrade_box,
                               name="rainbow_creeper")

        cream_fireball = Icon('Minecraft Clicker Images/Icons/Fireballs/cream_fireball_icon.png', (200, 100),
                              buy_box_list=Fireball_Icon_Objects, buy_box=fireball_buy_box,
                              upgrade_box=fireball_upgrade_box,
                              name="cream_fireball")
        greyscale_fireball = Icon('Minecraft Clicker Images/Icons/Fireballs/greyscale_fireball_icon.png', (200, 100),
                                  buy_box_list=Fireball_Icon_Objects, buy_box=fireball_buy_box,
                                  upgrade_box=fireball_upgrade_box,
                                  name="greyscale_fireball")
        yellow_fireball = Icon('Minecraft Clicker Images/Icons/Fireballs/yellow_fireball_icon.png', (200, 100),
                               buy_box_list=Fireball_Icon_Objects, buy_box=fireball_buy_box,
                               upgrade_box=fireball_upgrade_box,
                               name="yellow_fireball")
        blue_fireball = Icon('Minecraft Clicker Images/Icons/Fireballs/blue_fireball_icon.png', (200, 100),
                             buy_box_list=Fireball_Icon_Objects, buy_box=fireball_buy_box,
                             upgrade_box=fireball_upgrade_box,
                             name="blue_fireball")
        cyan_fireball = Icon('Minecraft Clicker Images/Icons/Fireballs/cyan_fireball_icon.png', (200, 100),
                             buy_box_list=Fireball_Icon_Objects, buy_box=fireball_buy_box,
                             upgrade_box=fireball_upgrade_box,
                             name="cyan_fireball")
        red_fireball = Icon('Minecraft Clicker Images/Icons/Fireballs/red_fireball_icon.png', (200, 100),
                            buy_box_list=Fireball_Icon_Objects, buy_box=fireball_buy_box,
                            upgrade_box=fireball_upgrade_box,
                            name="red_fireball")
        purple_fireball = Icon('Minecraft Clicker Images/Icons/Fireballs/purple_fireball_icon.png', (200, 100),
                               buy_box_list=Fireball_Icon_Objects, buy_box=fireball_buy_box,
                               upgrade_box=fireball_upgrade_box,
                               name="purple_fireball")
        green_fireball = Icon('Minecraft Clicker Images/Icons/Fireballs/green_fireball_icon.png', (200, 100),
                              buy_box_list=Fireball_Icon_Objects, buy_box=fireball_buy_box,
                              upgrade_box=fireball_upgrade_box,
                              name="green_fireball")
        orange_fireball = Icon('Minecraft Clicker Images/Icons/Fireballs/orange_fireball_icon.png', (200, 100),
                               buy_box_list=Fireball_Icon_Objects, buy_box=fireball_buy_box,
                               upgrade_box=fireball_upgrade_box,
                               name="orange_fireball")
        pink_fireball = Icon('Minecraft Clicker Images/Icons/Fireballs/pink_fireball_icon.png', (200, 100),
                             buy_box_list=Fireball_Icon_Objects, buy_box=fireball_buy_box,
                             upgrade_box=fireball_upgrade_box,
                             name="pink_fireball")
        rainbow_fireball = Icon('Minecraft Clicker Images/Icons/Fireballs/rainbow_fireball_icon.png', (200, 100),
                                buy_box_list=Fireball_Icon_Objects, buy_box=fireball_buy_box,
                                upgrade_box=fireball_upgrade_box,
                                name="rainbow_fireball")

        cream_crystal = Icon('Minecraft Clicker Images/Icons/Crystals/cream_crystal_icon.png', (200, 100),
                             buy_box_list=Crystal_Icon_Objects, buy_box=crystal_buy_box,
                             upgrade_box=crystal_upgrade_box,
                             name="cream_crystal")
        greyscale_crystal = Icon('Minecraft Clicker Images/Icons/Crystals/greyscale_crystal_icon.png', (200, 100),
                                 buy_box_list=Crystal_Icon_Objects, buy_box=crystal_buy_box,
                                 upgrade_box=crystal_upgrade_box,
                                 name="greyscale_crystal")
        yellow_crystal = Icon('Minecraft Clicker Images/Icons/Crystals/yellow_crystal_icon.png', (200, 100),
                              buy_box_list=Crystal_Icon_Objects, buy_box=crystal_buy_box,
                              upgrade_box=crystal_upgrade_box,
                              name="yellow_crystal")
        blue_crystal = Icon('Minecraft Clicker Images/Icons/Crystals/blue_crystal_icon.png', (200, 100),
                            buy_box_list=Crystal_Icon_Objects, buy_box=crystal_buy_box,
                            upgrade_box=crystal_upgrade_box,
                            name="blue_crystal")
        cyan_crystal = Icon('Minecraft Clicker Images/Icons/Crystals/cyan_crystal_icon.png', (200, 100),
                            buy_box_list=Crystal_Icon_Objects, buy_box=crystal_buy_box,
                            upgrade_box=crystal_upgrade_box,
                            name="cyan_crystal")
        red_crystal = Icon('Minecraft Clicker Images/Icons/Crystals/red_crystal_icon.png', (200, 100),
                           buy_box_list=Crystal_Icon_Objects, buy_box=crystal_buy_box,
                           upgrade_box=crystal_upgrade_box,
                           name="red_crystal")
        purple_crystal = Icon('Minecraft Clicker Images/Icons/Crystals/purple_crystal_icon.png', (200, 100),
                              buy_box_list=Crystal_Icon_Objects, buy_box=crystal_buy_box,
                              upgrade_box=crystal_upgrade_box,
                              name="purple_crystal")
        green_crystal = Icon('Minecraft Clicker Images/Icons/Crystals/green_crystal_icon.png', (200, 100),
                             buy_box_list=Crystal_Icon_Objects, buy_box=crystal_buy_box,
                             upgrade_box=crystal_upgrade_box,
                             name="green_crystal")
        orange_crystal = Icon('Minecraft Clicker Images/Icons/Crystals/orange_crystal_icon.png', (200, 100),
                              buy_box_list=Crystal_Icon_Objects, buy_box=crystal_buy_box,
                              upgrade_box=crystal_upgrade_box,
                              name="orange_crystal")
        pink_crystal = Icon('Minecraft Clicker Images/Icons/Crystals/pink_crystal_icon.png', (200, 100),
                            buy_box_list=Crystal_Icon_Objects, buy_box=crystal_buy_box,
                            upgrade_box=crystal_upgrade_box,
                            name="pink_crystal")
        rainbow_crystal = Icon('Minecraft Clicker Images/Icons/Crystals/rainbow_crystal_icon.png', (200, 100),
                               buy_box_list=Crystal_Icon_Objects, buy_box=crystal_buy_box,
                               upgrade_box=crystal_upgrade_box,
                               name="rainbow_crystal")

        cream_dragon = Icon('Minecraft Clicker Images/Icons/Dragons/cream_dragon_icon.png', (200, 100),
                            buy_box_list=Dragon_Icon_Objects, buy_box=dragon_buy_box,
                            upgrade_box=dragon_upgrade_box,
                            name="cream_dragon")
        greyscale_dragon = Icon('Minecraft Clicker Images/Icons/Dragons/greyscale_dragon_icon.png', (200, 100),
                                buy_box_list=Dragon_Icon_Objects, buy_box=dragon_buy_box,
                                upgrade_box=dragon_upgrade_box,
                                name="greyscale_dragon")
        yellow_dragon = Icon('Minecraft Clicker Images/Icons/Dragons/yellow_dragon_icon.png', (200, 100),
                             buy_box_list=Dragon_Icon_Objects, buy_box=dragon_buy_box,
                             upgrade_box=dragon_upgrade_box,
                             name="yellow_dragon")
        blue_dragon = Icon('Minecraft Clicker Images/Icons/Dragons/blue_dragon_icon.png', (200, 100),
                           buy_box_list=Dragon_Icon_Objects, buy_box=dragon_buy_box,
                           upgrade_box=dragon_upgrade_box,
                           name="blue_dragon")
        cyan_dragon = Icon('Minecraft Clicker Images/Icons/Dragons/cyan_dragon_icon.png', (200, 100),
                           buy_box_list=Dragon_Icon_Objects, buy_box=dragon_buy_box,
                           upgrade_box=dragon_upgrade_box,
                           name="cyan_dragon")
        red_dragon = Icon('Minecraft Clicker Images/Icons/Dragons/red_dragon_icon.png', (200, 100),
                          buy_box_list=Dragon_Icon_Objects, buy_box=dragon_buy_box,
                          upgrade_box=dragon_upgrade_box,
                          name="red_dragon")
        purple_dragon = Icon('Minecraft Clicker Images/Icons/Dragons/purple_dragon_icon.png', (200, 100),
                             buy_box_list=Dragon_Icon_Objects, buy_box=dragon_buy_box,
                             upgrade_box=dragon_upgrade_box,
                             name="purple_dragon")
        green_dragon = Icon('Minecraft Clicker Images/Icons/Dragons/green_dragon_icon.png', (200, 100),
                            buy_box_list=Dragon_Icon_Objects, buy_box=dragon_buy_box,
                            upgrade_box=dragon_upgrade_box,
                            name="green_dragon")
        orange_dragon = Icon('Minecraft Clicker Images/Icons/Dragons/orange_dragon_icon.png', (200, 100),
                             buy_box_list=Dragon_Icon_Objects, buy_box=dragon_buy_box,
                             upgrade_box=dragon_upgrade_box,
                             name="orange_dragon")
        pink_dragon = Icon('Minecraft Clicker Images/Icons/Dragons/pink_dragon_icon.png', (200, 100),
                           buy_box_list=Dragon_Icon_Objects, buy_box=dragon_buy_box,
                           upgrade_box=dragon_upgrade_box,
                           name="pink_dragon")
        rainbow_dragon = Icon('Minecraft Clicker Images/Icons/Dragons/rainbow_dragon_icon.png', (200, 100),
                              buy_box_list=Dragon_Icon_Objects, buy_box=dragon_buy_box,
                              upgrade_box=dragon_upgrade_box,
                              name="rainbow_dragon")

        cream_wither = Icon('Minecraft Clicker Images/Icons/Withers/cream_wither_icon.png', (200, 100),
                            buy_box_list=Wither_Icon_Objects, buy_box=wither_buy_box,
                            upgrade_box=wither_upgrade_box,
                            name="cream_wither")
        greyscale_wither = Icon('Minecraft Clicker Images/Icons/Withers/greyscale_wither_icon.png', (200, 100),
                                buy_box_list=Wither_Icon_Objects, buy_box=wither_buy_box,
                                upgrade_box=wither_upgrade_box,
                                name="greyscale_wither")
        yellow_wither = Icon('Minecraft Clicker Images/Icons/Withers/yellow_wither_icon.png', (200, 100),
                             buy_box_list=Wither_Icon_Objects, buy_box=wither_buy_box,
                             upgrade_box=wither_upgrade_box,
                             name="yellow_wither")
        blue_wither = Icon('Minecraft Clicker Images/Icons/Withers/blue_wither_icon.png', (200, 100),
                           buy_box_list=Wither_Icon_Objects, buy_box=wither_buy_box,
                           upgrade_box=wither_upgrade_box,
                           name="blue_wither")
        cyan_wither = Icon('Minecraft Clicker Images/Icons/Withers/cyan_wither_icon.png', (200, 100),
                           buy_box_list=Wither_Icon_Objects, buy_box=wither_buy_box,
                           upgrade_box=wither_upgrade_box,
                           name="cyan_wither")
        red_wither = Icon('Minecraft Clicker Images/Icons/Withers/red_wither_icon.png', (200, 100),
                          buy_box_list=Wither_Icon_Objects, buy_box=wither_buy_box,
                          upgrade_box=wither_upgrade_box,
                          name="red_wither")
        purple_wither = Icon('Minecraft Clicker Images/Icons/Withers/purple_wither_icon.png', (200, 100),
                             buy_box_list=Wither_Icon_Objects, buy_box=wither_buy_box,
                             upgrade_box=wither_upgrade_box,
                             name="purple_wither")
        green_wither = Icon('Minecraft Clicker Images/Icons/Withers/green_wither_icon.png', (200, 100),
                            buy_box_list=Wither_Icon_Objects, buy_box=wither_buy_box,
                            upgrade_box=wither_upgrade_box,
                            name="green_wither")
        orange_wither = Icon('Minecraft Clicker Images/Icons/Withers/orange_wither_icon.png', (200, 100),
                             buy_box_list=Wither_Icon_Objects, buy_box=wither_buy_box,
                             upgrade_box=wither_upgrade_box,
                             name="orange_wither")
        pink_wither = Icon('Minecraft Clicker Images/Icons/Withers/pink_wither_icon.png', (200, 100),
                           buy_box_list=Wither_Icon_Objects, buy_box=wither_buy_box,
                           upgrade_box=wither_upgrade_box,
                           name="pink_wither")
        rainbow_wither = Icon('Minecraft Clicker Images/Icons/Withers/rainbow_wither_icon.png', (200, 100),
                              buy_box_list=Wither_Icon_Objects, buy_box=wither_buy_box,
                              upgrade_box=wither_upgrade_box,
                              name="rainbow_wither")

        potion1_Icon = Icon('Minecraft Clicker Images/Icons/Potions/1potion_icon.png', (200, 100),
                            upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                            name="potion1_Icon")
        potion2_Icon = Icon('Minecraft Clicker Images/Icons/Potions/2potion_icon.png', (200, 100),
                            upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                            name="potion2_Icon")
        potion3_Icon = Icon('Minecraft Clicker Images/Icons/Potions/3potion_icon.png', (200, 100),
                            upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                            name="potion3_Icon")
        potion4_Icon = Icon('Minecraft Clicker Images/Icons/Potions/4potion_icon.png', (200, 100),
                            upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                            name="potion4_Icon")
        potion5_Icon = Icon('Minecraft Clicker Images/Icons/Potions/5potion_icon.png', (200, 100),
                            upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                            name="potion5_Icon")
        potion6_Icon = Icon('Minecraft Clicker Images/Icons/Potions/6potion_icon.png', (200, 100),
                            upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                            name="potion6_Icon")
        potion7_Icon = Icon('Minecraft Clicker Images/Icons/Potions/7potion_icon.png', (200, 100),
                            upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                            name="potion7_Icon")
        potion8_Icon = Icon('Minecraft Clicker Images/Icons/Potions/8potion_icon.png', (200, 100),
                            upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                            name="potion8_Icon")
        potion9_Icon = Icon('Minecraft Clicker Images/Icons/Potions/9potion_icon.png', (200, 100),
                            upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                            name="potion9_Icon")
        potion10_Icon = Icon('Minecraft Clicker Images/Icons/Potions/10potion_icon.png', (200, 100),
                             upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                             name="potion10_Icon")
        potion11_Icon = Icon('Minecraft Clicker Images/Icons/Potions/11potion_icon.png', (200, 100),
                             upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                             name="potion11_Icon")
        potion12_Icon = Icon('Minecraft Clicker Images/Icons/Potions/12potion_icon.png', (200, 100),
                             upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                             name="potion12_Icon")
        potion13_Icon = Icon('Minecraft Clicker Images/Icons/Potions/13potion_icon.png', (200, 100),
                             upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                             name="potion13_Icon")
        potion14_Icon = Icon('Minecraft Clicker Images/Icons/Potions/14potion_icon.png', (200, 100),
                             upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                             name="potion14_Icon")
        potion15_Icon = Icon('Minecraft Clicker Images/Icons/Potions/15potion_icon.png', (200, 100),
                             upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                             name="potion15_Icon")
        potion16_Icon = Icon('Minecraft Clicker Images/Icons/Potions/16potion_icon.png', (200, 100),
                             upgrade_box=enhancement_upgrade_box, buy_box_list=Block_Multi_Objects, is_block_multi=True,
                             name="potion16_Icon")

        price_reduction_icon = Icon('Minecraft Clicker Images/Icons/price_reduction_icon.png', (200, 100),
                                    upgrade_box=price_reduction_upgrade_box, buy_box_list=Price_Reduction_Icon_Objects,
                                    is_price_reduction=True,
                                    name="price_reduction_icon")

    Game_Menu_Objects.append(current_Clickable)

    buttons = True
    if buttons:
        # Buttons
        startB = Button('Minecraft Clicker Images/Buttons/start_gameB.png', (0, 0, 230, 65), (400, 500),
                        start_gameB_events_call, start_gameB_events_uncall, Main_Menu_Objects, start_button_pressed)
        shopB = Button('Minecraft Clicker Images/Buttons/shopB.png', (0, 0, 20, 68), (790, 300), shopB_events_call,
                       shopB_events_uncall, Game_Menu_Objects, shop_menu_pressed, is_menu_button=False)
        upgradeB = Button('Minecraft Clicker Images/Buttons/upgradesB.png', (0, 0, 20, 112), (10, 300),
                          upgradeB_events_call,
                          upgradeB_events_uncall, Game_Menu_Objects, upgrade_menu_pressed, is_menu_button=False)
        settingsB = Button('Minecraft Clicker Images/Buttons/settingsB.png', (0, 0, 50, 50), (760, 40),
                           settingB_events_call,
                           settingB_events_uncall, Main_Menu_Objects, setting_menu_pressed,
                           scene_list=[Game_Menu_Objects, Main_Menu_Objects], is_setting_button=True)
        MusicOnB = Button('Minecraft Clicker Images/Buttons/MusicOnB.png', (0, 0, 230, 65), (400, 225),
                          settings_Buttons_call,
                          settingB_events_uncall, Settings_Menu_Objects, music_on_pressed)
        MusicOffB = Button('Minecraft Clicker Images/Buttons/MusicOffB.png', (0, 0, 230, 65), (400, 225),
                           settings_Buttons_call,
                           settingB_events_uncall, Settings_Menu_Objects, music_on_pressed, is_toggle_button=True,
                           initialized=False)
        SoundOnB = Button('Minecraft Clicker Images/Buttons/SoundOnB.png', (0, 0, 230, 65), (400, 300),
                          settings_Buttons_call,
                          settingB_events_uncall, Settings_Menu_Objects, sound_on_pressed)
        SoundOffB = Button('Minecraft Clicker Images/Buttons/SoundOffB.png', (0, 0, 230, 65), (400, 300),
                           settings_Buttons_call,
                           settingB_events_uncall, Settings_Menu_Objects, sound_on_pressed, is_toggle_button=True,
                           initialized=False)
        StatsB = Button('Minecraft Clicker Images/Buttons/StatsB.png', (0, 0, 230, 65), (400, 375),
                        settings_Buttons_call,
                        settingB_events_uncall, Settings_Menu_Objects, stats_pressed)
        CreditsB = Button('Minecraft Clicker Images/Buttons/CreditsB.png', (0, 0, 230, 65), (400, 450),
                          settings_Buttons_call,
                          settingB_events_uncall, Settings_Menu_Objects, credits_pressed)
        BackB = Button('Minecraft Clicker Images/Buttons/BackB.png', (0, 0, 230, 65), (650, 525), settings_Buttons_call,
                       settings_Buttons_uncall, Settings_Menu_Objects, back_button_pressed, is_back_button=True)
        Main_MenuB = Button('Minecraft Clicker Images/Buttons/main_menuB.png', (0, 0, 230, 65), (150, 525),
                            settings_Buttons_call, settings_Buttons_uncall, Settings_Menu_Objects, main_menu_pressed)
        SaveB = Button('Minecraft Clicker Images/Buttons/SaveB.png', (0, 0, 50, 50), (50, 50), settings_Buttons_call,
                       settingB_events_uncall, Settings_Menu_Objects, save_button_pressed)
        Shop_scroll_barB = Button('Minecraft Clicker Images/Buttons/scroll_barB.png', (0, 0, 12, 45), (528, 25),
                                  Shop_scroll_barB_events_call, Shop_scroll_barB_events_uncall, Shop_Menu_Objects_Front,
                                  scroll_bar_pressed, is_scroll_bar=True, is_menu_button=False)
        Upgrade_scroll_barB = Button('Minecraft Clicker Images/Buttons/scroll_barB.png', (0, 0, 12, 45), (273, 25),
                                     Upgrade_scroll_barB_events_call, Upgrade_scroll_barB_events_uncall,
                                     Upgrade_Menu_Objects_Front, scroll_bar_pressed, is_scroll_bar=True,
                                     is_menu_button=False)

    uninteractables = True
    if uninteractables:
        # Uninteractables
        title = Uninteractable('Minecraft Clicker Images/Uninteractables/title.png', (0, 0, 700, 66), (400, 100),
                               Main_Menu_Objects)
        settings_title = Uninteractable('Minecraft Clicker Images/Uninteractables/settings_title.png', (0, 0, 421, 78),
                                        (400, 100), Settings_Menu_Objects)
        glow_effect1 = Uninteractable('Minecraft Clicker Images/Uninteractables/glow_effect_1.png', (0, 0, 350, 350),
                                      (400, 300), Game_Menu_Objects_Back, is_glow_effect=True, start_angle=0)
        glow_effect2 = Uninteractable('Minecraft Clicker Images/Uninteractables/glow_effect_2.png', (0, 0, 312, 312),
                                      (400, 300), Game_Menu_Objects_Back, is_glow_effect=True, start_angle=120,
                                      left=True)
        glow_effect3 = Uninteractable('Minecraft Clicker Images/Uninteractables/glow_effect_3.png', (0, 0, 275, 275),
                                      (400, 300), Game_Menu_Objects_Back, is_glow_effect=True, start_angle=120)
        background = pygame.image.load('Minecraft Clicker Images/Uninteractables/background.png').convert_alpha()
        grass_block_image = Uninteractable("Minecraft Clicker Images/Uninteractables/grass_blockimage.png",
                                           (0, 0, 300, 300),
                                           (400, 300), Main_Menu_Objects)

    # Shop Items
    background_dark_right = Uninteractable('Minecraft Clicker Images/Uninteractables/background_dark.png',
                                           (0, 0, 267, 600),
                                           (668, 300), Shop_Menu_Objects_Far_Back)
    background_bar_right = Uninteractable('Minecraft Clicker Images/Uninteractables/background_bar.png',
                                          (0, 0, 16, 600),
                                          (528, 300), Shop_Menu_Objects_Far_Back)
    background_box_right = Uninteractable('Minecraft Clicker Images/buy_box_background.png', (0, 0, 267, 57), (668, 28),
                                          Shop_Menu_Objects_Very_Front)
    background_dark_left = Uninteractable('Minecraft Clicker Images/Uninteractables/background_dark.png',
                                          (0, 0, 267, 600),
                                          (133, 300), Upgrade_Menu_Objects_Far_Back)
    background_bar_left = Uninteractable('Minecraft Clicker Images/Uninteractables/background_bar.png', (0, 0, 14, 600),
                                         (272, 300), Upgrade_Menu_Objects_Far_Back)
    background_box_left = Uninteractable('Minecraft Clicker Images/buy_box_background.png', (0, 0, 267, 57), (133, 28),
                                         Upgrade_Menu_Objects_Very_Front)

    # Texts
    upgrade_header_text = Text(header, "UPGRADES", (55, 7), Upgrade_Menu_Objects_Very_Front)
    shop_header_text = Text(header, "SHOP", (625, 7), Shop_Menu_Objects_Very_Front)
    amount_of_blocks_text = Text(header, str(blocks) + " blocks", (390, 7), Game_Menu_Objects,
                                 is_amount_blocks_text=True)
    blocks_per_second_text = Text(font_buy_box_price, str(blocks_per_second) + " per second", (365, 40),
                                  Game_Menu_Objects,
                                  is_per_second_text=True)

clock = pygame.time.Clock()
open_save()
run = True
update_game_events()


# Mainloop, calls upon number of times per second (order of functions matter)
def main():
    global run
    while run:
        clock.tick(25)
        check_events()
        redraw()
        # print(clock.get_fps())
    save_game()
    pygame.quit()


if __name__ == "__main__":
    main()
