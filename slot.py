import pygame
import sys
import random
import threading


# Initialize Pygame once
pygame.init()
pygame.font.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (20, 120, 20)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Slot Machine")

# Set up fonts
font_large = pygame.font.SysFont(None, 74)
font_medium = pygame.font.SysFont(None, 50)
FONT_LARGE = pygame.font.SysFont(None, 70)
FONT_MEDIUM = pygame.font.SysFont(None, 40)
FONT_SMALL = pygame.font.SysFont(None, 30)

# Button dimensions
button_width = 200
button_height = 80

# Button position (centered)
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = (SCREEN_HEIGHT - button_height) // 2
button_x2 = (SCREEN_WIDTH - button_width) // 2
button_y2 = (SCREEN_HEIGHT * 3 // 4) - (button_height // 2)

# Define button rectangle
start_button = pygame.Rect(button_x, button_y, button_width, button_height)
easy_button = pygame.Rect(button_x, button_y, button_width, button_height)
hard_button = pygame.Rect(button_x2, button_y2, button_width, button_height)

# FancyButton Class remains unchanged
class FancyButton:
    def __init__(
        self, x, y, width, height, text, font,
        color_normal=(200, 0, 0),
        color_hover=(255, 50, 50),
        color_pressed=(150, 0, 0),
        color_disabled=(0, 0, 0)
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_pressed = color_pressed
        self.color_disabled = color_disabled
        self.is_hovered = False
        self.is_pressed = False
        self.disabled = False

    def draw(self, surface):
        if self.disabled:
            color = self.color_disabled
        elif self.is_pressed:
            color = self.color_pressed
        elif self.is_hovered:
            color = self.color_hover
        else:
            color = self.color_normal

        # Draw rounded rectangle for the button
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        self._draw_gradient(surface, color)

        # Draw centered text
        text_surf = self.font.render(self.text, True, (255, 255, 255) if not self.disabled else (200, 200, 200))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def _draw_gradient(self, surface, base_color):
        """
        Optional top-to-bottom gradient for a glossy effect.
        """
        top_color = tuple(min(255, c+60) for c in base_color)
        bottom_color = tuple(max(0,  c-40) for c in base_color)

        for i in range(self.rect.height):
            blend_ratio = i / self.rect.height
            r = int(top_color[0]*(1 - blend_ratio) + bottom_color[0]*blend_ratio)
            g = int(top_color[1]*(1 - blend_ratio) + bottom_color[1]*blend_ratio)
            b = int(top_color[2]*(1 - blend_ratio) + bottom_color[2]*blend_ratio)

            pygame.draw.line(
                surface, (r, g, b),
                (self.rect.x,         self.rect.y + i),
                (self.rect.x + self.rect.width, self.rect.y + i)
            )

    def handle_event(self, event):
        """
        Returns True if the button is fully clicked (mouse down + up inside).
        """
        if self.disabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_pressed and self.rect.collidepoint(event.pos):
                    self.is_pressed = False
                    return True
                self.is_pressed = False

        return False

# Define Replay Button
replay_button = FancyButton(
    x=(SCREEN_WIDTH - 200) // 2,  # Centered horizontally
    y=(SCREEN_HEIGHT - 80) // 2 + 100,  # Positioned below the reels
    width=200,
    height=80,
    text="Replay",
    font=FONT_MEDIUM,
    color_normal=(0, 200, 0),
    color_hover=(50, 255, 50),
    color_pressed=(0, 150, 0),
    color_disabled=(100, 100, 100)
)

# Initialize Buttons (moved outside functions)
spin_button = FancyButton(
    x=SCREEN_WIDTH - 160,
    y=SCREEN_HEIGHT - 80,
    width=140,
    height=50,
    text="Spin",
    font=FONT_MEDIUM,
    color_normal=(200, 0, 0),
    color_hover=(255, 50, 50),
    color_pressed=(150, 0, 0),
    color_disabled=(0, 0, 255)
)

all_in_button = FancyButton(
    x=240,  # Start after the bet box
    y=SCREEN_HEIGHT - 70,
    width=90,
    height=40,
    text="All In",      # 100% of balance
    font=FONT_SMALL,
    color_normal=(255, 0, 0),
    color_hover=(0, 180, 0),
    color_pressed=(0, 120, 0)
)

half_button = FancyButton(
    x=340,
    y=SCREEN_HEIGHT - 70,
    width=90,
    height=40,
    text="50%",
    font=FONT_SMALL,
    color_normal=(255, 100, 0),
    color_hover=(0, 180, 0),
    color_pressed=(0, 120, 0)
)

quarter_button = FancyButton(
    x=440,
    y=SCREEN_HEIGHT - 70,
    width=90,
    height=40,
    text="25%",
    font=FONT_SMALL,
    color_normal=(255, 150, 0),
    color_hover=(0, 180, 0),
    color_pressed=(0, 120, 0)
)

ten_percent_button = FancyButton(
    x=540,
    y=SCREEN_HEIGHT - 70,
    width=90,
    height=40,
    text="10%",
    font=FONT_SMALL,
    color_normal=(255, 175, 50),
    color_hover=(0, 180, 0),
    color_pressed=(0, 120, 0)
)

bet_percent_buttons = [
    all_in_button, half_button, quarter_button, ten_percent_button
]

# Load Symbol Images with Error Handling
symbol_images = {}
symbol_names = ['Grape', 'Orange', 'Banana', 'Coin', 'Cherry', 'Seven', 'Diamond', 'Star', 'Bar']
symbol_names2 = ['Grape', 'Orange', 'Banana', 'Coin', 'Cherry', 'Seven']
symbol_data = {
    "Seven": {"value": "High", "probability": 7},
    "Cherry": {"value": "Low", "probability": 25}, 
    "Grape": {"value": "Medium", "probability": 15}, 
    "Orange": {"value": "Low", "probability": 25},
    "Coin": {"value": "Medium", "probability": 15},
    "Banana": {"value": "Low", "probability": 25},
    "Diamond": {"value": "High", "probability": 7},
    "Star": {"value": "Special", "probability": 3}
}
for name in symbol_names :
    try:
        img = pygame.image.load(f"/Volumes/CURTIS/term project/B13504034/symbols/{name.lower()}.png")
        symbol_images[name] = pygame.transform.scale(img, (100, 100))
    except pygame.error as e:
        print(f"Error loading image for {name}: {e}")
        # Create a placeholder surface if image fails to load
        symbol_images[name] = pygame.Surface((100, 100))
        symbol_images[name].fill(BLACK)
        text_surf = FONT_SMALL.render(name, True, WHITE)
        text_rect = text_surf.get_rect(center=(50, 50))
        symbol_images[name].blit(text_surf, text_rect)

for name in symbol_names2 :
    try:
        img = pygame.image.load(f"/Volumes/CURTIS/term project/B13504034/symbols/{name.lower()}.png")
        symbol_images[name] = pygame.transform.scale(img, (100, 100))
    except pygame.error as e:
        print(f"Error loading image for {name}: {e}")
        # Create a placeholder surface if image fails to load
        symbol_images[name] = pygame.Surface((100, 100))
        symbol_images[name].fill(BLACK)
        text_surf = FONT_SMALL.render(name, True, WHITE)
        text_rect = text_surf.get_rect(center=(50, 50))
        symbol_images[name].blit(text_surf, text_rect)

# Load Sounds with Error Handling
try:
    win_sound = pygame.mixer.Sound(f"/Volumes/CURTIS/term project/B13504034/sound effect/win.wav")
except pygame.error as e:
    print("Error loading win.wav:", e)
    win_sound = None

try:
    lose_sound = pygame.mixer.Sound(f"/Volumes/CURTIS/term project/B13504034/sound effect/lose.wav")
except pygame.error as e:
    print("Error loading lose.wav:", e)
    lose_sound = None

try:
    spin_sound = pygame.mixer.Sound(f"/Volumes/CURTIS/term project/B13504034/sound effect/spin.wav")
except pygame.error as e:
    print("Error loading spin.wav:", e)
    spin_sound = None

try:
    jackpot_sound = pygame.mixer.Sound(f"/Volumes/CURTIS/term project/B13504034/sound effect/jackpot.wav")
except pygame.error as e:
    print("Error loading jackpot.wav:", e)
    spin_sound = None

# Optional background image
'''try:
    background_img = pygame.image.load("slot_machine_background.jpg")
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print("Error loading background image:", e)'''
background_img = None

# Slot Machine Variables (Moved to Global Scope)
symbols = ['Grape', 'Orange', 'Cherry', 'Coin', 'Banana', 'Seven']  # seven = golden
own = 100               # Player's balance
bet = 0                 # Current integer bet
bet_text = ""           # What's typed in the bet box
final_reels = []        # Final spin result
win_message = ""
is_spinning = False
spin_frame = 0
max_spin_frames = 42    # Number of frames for the "placeholder" animation
placeholder_spins = []  # Each frame, a random set of symbols
a = 0                   # Tracks losing state for sound logic

def draw_start_screen():
    """Draws the start screen with a start button."""
    screen.fill(GREEN)  # Fill the background with white

    # Render the title
    title_text = font_large.render("Slot Machine", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)

    # Draw the start button
    pygame.draw.rect(screen, GRAY, easy_button)
    pygame.draw.rect(screen, BLACK, easy_button, 2)  # Button border
    pygame.draw.rect(screen, GRAY, hard_button)
    pygame.draw.rect(screen, BLACK, hard_button, 2)  # Button border

    # Render the button text
    button_text = font_medium.render("Easy", True, BLACK)
    button_text2 = font_medium.render("Hard", True, BLACK)
    button_rect = button_text.get_rect(center=easy_button.center)
    button_rect2 = button_text2.get_rect(center=hard_button.center)
    screen.blit(button_text, button_rect)
    screen.blit(button_text2, button_rect2)

    pygame.display.flip()

def reset_game_state():
    global own, bet, bet_text, is_spinning, spin_frame, final_reels, win_message, a

    # Reset all game-related variables
    own = 100
    bet = 0
    bet_text = ""
    is_spinning = False
    spin_frame = 0
    final_reels = []
    win_message = ""
    a = 0

    # Reset replay button state
    replay_button.disabled = False
    replay_button.is_pressed = False
    replay_button.is_hovered = False

'''def draw_start_screen():
    """Draws the start screen with a start button."""
    screen.fill(GREEN)  # Fill the background with white

    # Render the title
    title_text = font_large.render("Slot Machine", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)

    # Draw the start button
    pygame.draw.rect(screen, GRAY, start_button)
    pygame.draw.rect(screen, BLACK, start_button, 2)  # Button border

    # Render the button text
    button_text = font_medium.render("Start", True, BLACK)
    button_rect = button_text.get_rect(center=start_button.center)
    screen.blit(button_text, button_rect)

    pygame.display.flip()'''

def run_start_screen():
    """Runs the start screen loop."""
    while True:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if easy_button.collidepoint(event.pos):
                        # Start button clicked, proceed to main game
                        reset_game_state()
                        run_main_game()
                        return
                    if hard_button.collidepoint(event.pos):
                        reset_game_state()
                        run_main_game2()
                        return

def spin_reels():
    """Return a list of three symbols for a single spin."""
    return [random.choice(symbol_names2) for _ in range(3)]

def spin_reels2():
    """Return a list of three symbols for a single spin."""
    symbols = list(symbol_data.keys())
    probabilities = [symbol_data[symbol]['probability'] for symbol in symbols]
    return random.choices(symbols, weights = probabilities, k=3)

def check_win_condition(result):
    """
    Compare the final reels, update balance accordingly, and return a message.
    We assume we've already subtracted the bet from 'own'.
    """
    global own, bet, a

    symbol_count = {symbol: result.count(symbol) for symbol in result}
    unique_symbols = len(symbol_count)

    low_value_count = sum(1 for symbol in result if symbol_data[symbol]["value"] == "Low")
    medium_value_count = sum(1 for symbol in result if symbol_data[symbol]["value"] == "Medium")
    high_value_count = sum(1 for symbol in result if symbol_data[symbol]["value"] == "High")
    special_value_count = sum(1 for symbol in result if symbol_data[symbol]["value"] == "Special")


    if special_value_count == 3:
        own += bet * 20
        return "Super Jackpot! You Win 20*Bet!"
    
    if low_value_count == 3 and unique_symbols == 1:
        own += bet * 2
        return "Low Value Win! You Win 2*Bet!"
    elif low_value_count == 2 and special_value_count == 1 and unique_symbols == 2:
        own += bet * 3
        return "Low Value with Special! You Win 3*Bet!"
    if medium_value_count == 3 and unique_symbols == 1:
        own += bet * 5
        return "Medium Value Win! You Win 5*Bet!"
    elif medium_value_count == 2 and special_value_count == 1 and unique_symbols == 2:
        own += bet * 7
        return "Medium Value with Special! You Win 7*Bet!"
    if high_value_count == 3 and unique_symbols == 1:
        own += bet * 10
        return "High Value Win! You Win 10*Bet!"
    elif high_value_count == 2 and special_value_count == 1 and unique_symbols == 2:
        own += bet * 15
        return "High Value with Wild! You Win 15*Bet!"

    a = 1  
    return "Try Again!"

def start_spin():
    """
    Subtract the bet from 'own' (if valid), create placeholder frames,
    pick a final result, and set is_spinning to True.
    """
    global bet_text, bet, own, is_spinning, spin_frame
    global placeholder_spins, final_reels, win_message, a

    if is_spinning:
        return

    # Convert bet_text to int
    try:
        current_bet = int(bet_text)
    except ValueError:
        print("Invalid bet. Please enter a positive integer.")
        return

    # Check validity
    if current_bet <= 0 or current_bet > own:
        print("Invalid bet amount. Must be > 0 and <= your balance.")
        return

    bet = current_bet
    # Immediately subtract bet (so user sees updated balance)
    own -= bet

    # Prepare spin
    placeholder_spins.clear()
    for _ in range(max_spin_frames):
        placeholder_spins.append(spin_reels())

    final_reels.clear()
    final_reels.extend(spin_reels())

    spin_frame = 0
    is_spinning = True
    win_message = ""
    a = 0

    spin_button.disabled = True

    # Start spin sound (if loaded)
    if spin_sound:
        threading.Thread(target=lambda: spin_sound.play(), daemon=True).start()

def start_spin2():
    """
    Subtract the bet from 'own' (if valid), create placeholder frames,
    pick a final result, and set is_spinning to True.
    """
    global bet_text, bet, own, is_spinning, spin_frame
    global placeholder_spins, final_reels, win_message, a

    if is_spinning:
        return

    # Convert bet_text to int
    try:
        current_bet = int(bet_text)
    except ValueError:
        print("Invalid bet. Please enter a positive integer.")
        return

    # Check validity
    if current_bet <= 0 or current_bet > own:
        print("Invalid bet amount. Must be > 0 and <= your balance.")
        return

    bet = current_bet
    # Immediately subtract bet (so user sees updated balance)
    own -= bet

    # Prepare spin
    placeholder_spins.clear()
    for _ in range(max_spin_frames):
        placeholder_spins.append(spin_reels2())

    final_reels.clear()
    final_reels.extend(spin_reels2())

    spin_frame = 0
    is_spinning = True
    win_message = ""
    a = 0

    spin_button.disabled = True

    # Start spin sound (if loaded)
    if spin_sound:
        threading.Thread(target=lambda: spin_sound.play(), daemon=True).start()

def update_spin():
    """
    Advance the spin animation. If we reach the end, finalize the result
    by calling check_win_condition.
    """
    global is_spinning, spin_frame, win_message, a

    if not is_spinning:
        return

    spin_frame += 1
    if spin_frame >= max_spin_frames:
        # End of animation
        is_spinning = False
        # Stop spin sound if it’s still playing
        if spin_sound:
            spin_sound.stop()

        # Evaluate final result
        msg = check_win_condition(final_reels)
        win_message = msg
        if "Jackpot" in msg:
            if jackpot_sound:
                threading.Thread(target=lambda: jackpot_sound.play(), daemon=True).start()
        elif "Win" in msg:
            # Play win sound
            if win_sound:
                threading.Thread(target=lambda: win_sound.play(), daemon=True).start()
        elif a == 1:
            # Play lose sound
            if lose_sound:
                threading.Thread(target=lambda: lose_sound.play(), daemon=True).start()
            a = 0

        spin_button.disabled = False

def draw_slot_machine(fancy_spin_btn, bet_box_rect, bet_box_active):
    """
    Draw everything:
    - Background (if any)
    - Reels (either placeholder or final)
    - Win message
    - Balance
    - Fancy spin button
    - Bet box
    """
    # Background
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((20, 120, 20))

    # REELS
    if is_spinning and spin_frame < max_spin_frames:
        # Show placeholders
        current_symbols = placeholder_spins[spin_frame]
    else:
        # Show final reels
        current_symbols = final_reels

    # Positions for the reels
    reel_positions = [
        (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2),
        (SCREEN_WIDTH // 2,       SCREEN_HEIGHT // 2),
        (SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2)
    ]

    for pos, sym in zip(reel_positions, current_symbols):
        symbol_surf = symbol_images.get(sym, pygame.Surface((100, 100)))
        #text_surf = FONT_LARGE.render(sym, True, (0, 0, 0))
        rect = symbol_surf.get_rect(center=pos)
        screen.blit(symbol_surf, rect)

    # Win message
    color = (255, 0, 0) if "Try" in win_message else (0, 200, 0)
    msg_surf = FONT_MEDIUM.render(win_message, True, color)
    msg_rect = msg_surf.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    )
    screen.blit(msg_surf, msg_rect)

    if bet_text.isdigit():
        current_bet = int(bet_text)
        if 0 < current_bet <= own:
            remaining_balance = own - current_bet
            bal_text = f"Balance: {own} | Bet: {current_bet} | Remaining: {remaining_balance}"
            balance_color = (255, 255, 255)  # White for valid
        elif current_bet > own:
            bal_text = f"Balance: {own} | Bet: {current_bet} (Exceeds balance!)"
            balance_color = (255, 0, 0)  # Red for invalid
        else:
            bal_text = f"Balance: {own} | Bet: {current_bet}"
            balance_color = (255, 255, 255)  # White
    else:
        if bet_text == "":
            bal_text = f"Balance: {own}"
        else:
            bal_text = f"Balance: {own} | Bet: {bet_text} (Invalid)"
            balance_color = (255, 0, 0)  # Red for invalid or empty

    # Balance
    bal_surf = FONT_SMALL.render(bal_text, True, (255,255,255))
    screen.blit(bal_surf, (20, 20))

    if own > 0:
        for btn in bet_percent_buttons:
            btn.draw(screen)

    # Draw the fancy spin button
    if own > 0:
        fancy_spin_btn.draw(screen)

    if own <= 0 and is_spinning == False:
        replay_button.draw(screen)

    # BET BOX
    # If active, box is white; else gray
    if own > 0:
        box_color = (255, 255, 255) if bet_box_active else (180, 180, 180)
        pygame.draw.rect(screen, box_color, bet_box_rect, border_radius=5)

    # Draw bet text
        bet_surf = FONT_SMALL.render(bet_text, True, (0, 0, 0))
        screen.blit(bet_surf, (bet_box_rect.x + 10, bet_box_rect.y + 8))

def run_main_game():
    global bet_text, is_spinning, spin_frame, own, bet, win_message, a

    # Bet box variables
    bet_box_rect = pygame.Rect(20, SCREEN_HEIGHT - 70, 200, 40)
    bet_box_active = False

    clock = pygame.time.Clock()  # 初始化時鐘對象

    running = True
    while running:
        clock.tick(30)  # 設定每秒幀數 (FPS)

        # -- Handle Events --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if own > 0:
                # Fancy spin button events
                if spin_button.handle_event(event):
                    # Start the spin if the button was fully clicked
                    start_spin()

                # Bet box focus
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bet_box_rect.collidepoint(event.pos):
                        bet_box_active = True
                    else:
                        bet_box_active = False

                # Bet box typing
                if bet_box_active and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        bet_text = bet_text[:-1]
                    else:
                        # Only digits
                        if event.unicode.isdigit():
                            bet_text += event.unicode

                for btn in bet_percent_buttons:
                    if btn.handle_event(event):
                        # They clicked one of the percentage buttons
                        if btn == all_in_button:
                            # 100%: make bet_text = own
                            bet_text = str(own)
                        elif btn == half_button:
                            # 50%: half of own
                            half_val = own // 2
                            bet_text = str(half_val)
                        elif btn == quarter_button:
                            # 25%: quarter of own
                            quarter_val = own // 4
                            bet_text = str(quarter_val)
                        elif btn == ten_percent_button:
                            # 10%: 0.1 * own
                            ten_val = own // 10
                            bet_text = str(ten_val)
            else:
                # Handle Replay Button Events when balance is zero
                if replay_button.handle_event(event):
                    # Reset the game state
                    '''own = 100
                    bet = 0
                    bet_text = ""
                    final_reels.clear()
                    win_message = ""
                    is_spinning = False
                    spin_frame = 0
                    placeholder_spins.clear()
                    a = 0'''
                    running = False

        # -- Update Logic (Spin Animation) --
        update_spin()

        # -- Draw Everything --
        draw_slot_machine(spin_button, bet_box_rect, bet_box_active)
        pygame.display.flip()

    run_start_screen()

def run_main_game2():
    global bet_text, is_spinning, spin_frame, own, bet, win_message, a

    # Bet box variables
    bet_box_rect = pygame.Rect(20, SCREEN_HEIGHT - 70, 200, 40)
    bet_box_active = False

    clock = pygame.time.Clock()  # 初始化時鐘對象

    running = True
    while running:
        clock.tick(30)  # 設定每秒幀數 (FPS)

        # -- Handle Events --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if own > 0:
                # Fancy spin button events
                if spin_button.handle_event(event):
                    # Start the spin if the button was fully clicked
                    start_spin2()

                # Bet box focus
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bet_box_rect.collidepoint(event.pos):
                        bet_box_active = True
                    else:
                        bet_box_active = False

                # Bet box typing
                if bet_box_active and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        bet_text = bet_text[:-1]
                    else:
                        # Only digits
                        if event.unicode.isdigit():
                            bet_text += event.unicode

                for btn in bet_percent_buttons:
                    if btn.handle_event(event):
                        # They clicked one of the percentage buttons
                        if btn == all_in_button:
                            # 100%: make bet_text = own
                            bet_text = str(own)
                        elif btn == half_button:
                            # 50%: half of own
                            half_val = own // 2
                            bet_text = str(half_val)
                        elif btn == quarter_button:
                            # 25%: quarter of own
                            quarter_val = own // 4
                            bet_text = str(quarter_val)
                        elif btn == ten_percent_button:
                            # 10%: 0.1 * own
                            ten_val = own // 10
                            bet_text = str(ten_val)
            else:
                # Handle Replay Button Events when balance is zero
                if replay_button.handle_event(event):
                    # Reset the game state
                    '''own = 100
                    bet = 0
                    bet_text = ""
                    final_reels.clear()
                    win_message = ""
                    is_spinning = False
                    spin_frame = 0
                    placeholder_spins.clear()
                    a = 0'''
                    running = False

        # -- Update Logic (Spin Animation) --
        update_spin()

        # -- Draw Everything --
        draw_slot_machine(spin_button, bet_box_rect, bet_box_active)
        pygame.display.flip()

    run_start_screen()

def main():
    while True:
        run_start_screen()

if __name__ == "__main__":
    main()
