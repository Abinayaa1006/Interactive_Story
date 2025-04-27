import pygame
import sys
import random


# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Story Game")

# Timing constants (in milliseconds)
SHORT_DELAY = 800  # For brief pauses
MEDIUM_DELAY = 1200  # For moderate pauses
LONG_DELAY = 2000  # For important story moments

# Colors
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Font
font = pygame.font.SysFont("Arial", 32)
title_font = pygame.font.SysFont("Arial", 48)
stats_font = pygame.font.SysFont("Arial", 24)  # Smaller font for stats
def display_text(text, x=None, y=None, color=WHITE, font_obj=None, center=False, alpha=255):
    if not font_obj:
        font_obj = font
    text_surface = font_obj.render(text, True, color)
    text_surface.set_alpha(alpha)  # Add alpha support
    if center:
        text_rect = text_surface.get_rect(center=(WIDTH//2, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))
    pygame.draw.rect(screen, BLACK, text_rect.inflate(20, 10))
    screen.blit(text_surface, text_rect.topleft)
    return text_rect  # Return the rect for animation purposes



# Load images (fallback to colored surfaces if images not found)
try:
    neutral_background = pygame.image.load("welcome.png")
    neutral_background = pygame.transform.scale(neutral_background, (WIDTH, HEIGHT))
except:
    neutral_background = pygame.Surface((WIDTH, HEIGHT))
    neutral_background.fill((50, 50, 100))  # Dark blue background

try:
    jungle_background = pygame.image.load("jungle.png")
    jungle_background = pygame.transform.scale(jungle_background, (WIDTH, HEIGHT))
except:
    jungle_background = pygame.Surface((WIDTH, HEIGHT))
    jungle_background.fill((0, 100, 0))  # Dark green background

try:
    horror_background = pygame.image.load("horror.png")
    horror_background = pygame.transform.scale(horror_background, (WIDTH, HEIGHT))
except:
    horror_background = pygame.Surface((WIDTH, HEIGHT))
    horror_background.fill((20, 0, 20))  # Dark purple background

# Music and sounds
try:
    neutral_music = "background_music.mp3"
    horror_music = "Horror.mp3"
    jungle_music = "Jungle.mp3"
    click_sound = pygame.mixer.Sound("Click.mp3")
    has_sound = True
except:
    print("Sound files not found - continuing without sound")
    has_sound = False

# Game systems
score = 0
character_stats = {
    "health": 100,
    "courage": 50,
    "luck": 50,
    "sanity": 100,
    "inventory": []
}
jungle_stats = {
    "exploration": 0,
    "survival": 50,
    "animal_respect": 0
}
horror_stats = {
    "darkness_resistance": 0,
    "occult_knowledge": 0,
    "ghostly_favors": 0
}


def play_music(music_file):
    if has_sound and music_file:
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # Loop indefinitely
        except:
            pass


def play_click_sound():
    if has_sound and click_sound:
        try:
            click_sound.play()
        except:
            pass


def display_text(text, x=None, y=None, color=WHITE, font_obj=None, center=False, alpha=255):
    """Draw text with optional transparency"""
    if not font_obj:
        font_obj = font

    # Create text surface
    text_surface = font_obj.render(text, True, color)

    # Set transparency if alpha is provided
    if alpha < 255:
        text_surface = text_surface.copy()  # Create a copy to preserve original
        text_surface.set_alpha(alpha)

    # Position the text
    if center:
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))

    # Draw background (without alpha)
    pygame.draw.rect(screen, BLACK, text_rect.inflate(20, 10))

    # Draw the text
    screen.blit(text_surface, text_rect.topleft)

    return text_rect  # Return rect in case we need it
def get_choice(options):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and "start" in options:
                    play_click_sound()
                    return "start"
                for option in options:
                    if event.key == getattr(pygame, f"K_{option}"):
                        play_click_sound()
                        return option
        pygame.time.wait(100)


def get_character_name():
    name = ""
    input_active = True

    # Pre-render title
    title1 = title_font.render("Chronicles of Fate:", True, PURPLE)
    title2 = title_font.render("Paths Untold", True, PURPLE)
    title1_rect = title1.get_rect(center=(WIDTH // 2, 100))
    title2_rect = title2.get_rect(center=(WIDTH // 2, 160))

    # Initial fade-in
    for alpha in range(0, 256, 5):
        screen.blit(neutral_background, (0, 0))
        title1.set_alpha(alpha)
        title2.set_alpha(alpha)
        screen.blit(title1, title1_rect)
        screen.blit(title2, title2_rect)

        # Static elements
        display_text("Enter your character's name:", center=True, y=250, color=WHITE)
        display_text("Press Enter when done", center=True, y=350, color=YELLOW)

        pygame.display.flip()
        pygame.time.wait(30)

    # Main input loop
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    play_click_sound()
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isalnum() or event.unicode == " ":
                    if len(name) < 15:
                        name += event.unicode

        # Keep drawing the titles at full alpha
        screen.blit(neutral_background, (0, 0))
        screen.blit(title1, title1_rect)
        screen.blit(title2, title2_rect)
        display_text("Chronicles of Fate:", center=True, y=100, color=PURPLE, font_obj=title_font)
        display_text("Paths Untold", center=True, y=160, color=YELLOW, font_obj=title_font)

        display_text("Enter your character's name:", center=True, y=250, color=WHITE)
        display_text(name, center=True, y=300, color=GREEN, font_obj=font)
        display_text("Press Enter when done", center=True, y=350, color=YELLOW)
        pygame.display.flip()


    return name.strip()


def welcome_page(character_name):
    options = ["1", "2", "3"]  # Define available options

    # Fade in the entire welcome screen
    for alpha in range(0, 256, 5):  # From 0 to 255 in steps of 5
        screen.blit(neutral_background, (0, 0))

        # Draw all elements with increasing alpha
        display_text("Chronicles of Fate:", center=True, y=50, color=PURPLE,
                     font_obj=title_font, alpha=alpha)
        display_text("Paths Untold", center=True, y=110, color=YELLOW,
                     font_obj=title_font, alpha=alpha)
        display_text(f"Welcome, {character_name}!", center=True, y=180,
                     color=WHITE, alpha=alpha)
        display_text("Choose your adventure:", center=True, y=250,
                     color=WHITE, alpha=alpha)
        display_text("1. Horror Adventure", center=True, y=300,
                     color=RED, alpha=alpha)
        display_text("2. Jungle Expedition", center=True, y=350,
                     color=GREEN, alpha=alpha)
        display_text("3. View Character Stats", center=True, y=400,
                     color=BLUE, alpha=alpha)

        pygame.display.flip()
        pygame.time.wait(30)  # Control fade speed

    # After fade-in, proceed with normal interaction
    return get_choice(options)

def show_character_stats(character_name):
    screen.blit(neutral_background, (0, 0))
    display_text(f"{character_name}'s Stats", center=True, y=50, color=WHITE, font_obj=title_font)

    y_pos = 150
    for stat, value in character_stats.items():
        if stat != "inventory":
            display_text(f"{stat.capitalize()}: {value}", 100, y_pos, WHITE)
            y_pos += 50

    display_text("Inventory:", 100, y_pos, WHITE)
    y_pos += 50
    if character_stats['inventory']:
        for item in character_stats['inventory']:
            display_text(f"- {item}", 150, y_pos, YELLOW)
            y_pos += 40
    else:
        display_text("Empty", 150, y_pos, YELLOW)
        y_pos += 40

    display_text("Press any key to continue", center=True, y=y_pos + 50, color=BLUE)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                play_click_sound()


def jungle_adventure(character_name):
    global score
    score = 0
    jungle_stats.update({
        "exploration": 0,
        "survival": 50,
        "animal_respect": 0
    })

    play_music(jungle_music)
    def display_jungle_stats():
        # Single line condensed stats display positioned higher
        stats_y = HEIGHT - 70  # 70px from bottom

        # Compact stats format
        stats_text = (
            f"Health: {character_stats['health']} | "
            f"Courage: {character_stats['courage']} | "
            f"Expl: {jungle_stats['exploration']} | "
            f"Survival: {jungle_stats['survival']} | "
            f"Animals: {jungle_stats['animal_respect']} | "
            f"Inventory: {', '.join(character_stats['inventory']) if character_stats['inventory'] else 'Empty'}"
        )

        # Display single line of stats with smaller font
        display_text(stats_text, 10, stats_y, (220, 220, 220), stats_font)


    # Introduction
    screen.blit(jungle_background, (0, 0))
    display_text(f"Jungle Expedition: {character_name}", center=True, y=50, color=GREEN, font_obj=title_font)
    display_text("You've been hired to explore the uncharted", center=True, y=150, color=WHITE)
    display_text("Amazon rainforest and discover its secrets.", center=True, y=200, color=WHITE)
    display_text("Press 1 to begin your adventure", center=True, y=300, color=YELLOW)
    pygame.display.flip()
    get_choice(["1"])

    # River Crossing
    screen.blit(jungle_background, (0, 0))
    display_text("Your first challenge: A raging river blocks your path.", 50, 50, WHITE)
    display_text("How will you cross?", 50, 100, WHITE)
    display_text("1. Build a raft (requires survival skill)", 50, 150, WHITE)
    display_text("2. Search for a bridge", 50, 200, WHITE)
    display_text("3. Swim across (dangerous!)", 50, 250, WHITE)
    display_jungle_stats()
    pygame.display.flip()

    choice = get_choice(["1", "2", "3"])

    if choice == "1":
        if jungle_stats['survival'] > 40:
            display_text("You build a sturdy raft and cross safely!", 50, 300, GREEN)
            jungle_stats['survival'] += 5
            character_stats['inventory'].append("raft")
            score += 20
        else:
            display_text("Your raft falls apart! (-15 health)", 50, 300, RED)
            character_stats['health'] -= 15
            score -= 10
    elif choice == "2":
        jungle_stats['exploration'] += 10
        display_text("You find an ancient vine bridge.", 50, 300, WHITE)
        display_text("1. Cross carefully", 50, 350, WHITE)
        display_text("2. Investigate the bridge first", 50, 400, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2"])
        if choice == "1":
            display_text("You make it across safely.", 50, 450, GREEN)
            score += 15
        else:
            display_text("You find carvings that reveal a secret path!", 50, 450, YELLOW)
            character_stats['inventory'].append("ancient map")
            score += 30
    else:
        if character_stats['luck'] > 70:
            display_text("Against all odds, you make it across!", 50, 300, GREEN)
            jungle_stats['animal_respect'] += 5
            score += 25
        else:
            display_text("The current nearly drowns you! (-25 health)", 50, 300, RED)
            character_stats['health'] -= 25
            score -= 15

    pygame.time.wait(SHORT_DELAY)

    # Temple Ruins
    screen.blit(jungle_background, (0, 0))
    display_text("After days of travel, you discover ancient temple ruins.", 50, 50, WHITE)
    display_text("The stones are covered in strange carvings.", 50, 100, WHITE)

    options = ["1", "2"]
    option_texts = ["1. Enter main temple", "2. Explore surroundings"]
    if "ancient map" in character_stats['inventory']:
        options.append("3")
        option_texts.append("3. Follow map to hidden chambers")

    for i, option in enumerate(option_texts):
        display_text(option, 50, 200 + i * 50, WHITE)
    display_jungle_stats()
    pygame.display.flip()

    choice = get_choice(options)

    # Temple branches
    if choice == "1":
        display_text("A stone guardian blocks your path!", 50, 350, RED)
        display_text("1. Fight it", 50, 400, WHITE)
        display_text("2. Reason with it", 50, 450, WHITE)
        display_text("3. Find another way", 50, 500, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2", "3"])
        if choice == "1":
            if character_stats['health'] > 80:
                display_text("You defeat the guardian but are wounded!", 50, 550, YELLOW)
                character_stats['health'] -= 30
                character_stats['inventory'].append("guardian's amulet")
                score += 50
            else:
                display_text("The guardian overpowers you! (-40 health)", 50, 550, RED)
                character_stats['health'] -= 40
                score -= 20
        elif choice == "2":
            if jungle_stats['animal_respect'] > 20:
                display_text("The guardian lets you pass.", 50, 550, GREEN)
                jungle_stats['animal_respect'] += 10
                score += 30
            else:
                display_text("The guardian doesn't trust you.", 50, 550, YELLOW)
                score += 10
        else:
            jungle_stats['exploration'] += 15
            display_text("You find a hidden tunnel.", 50, 550, GREEN)
            score += 20
    elif choice == "2":
        jungle_stats['exploration'] += 20
        display_text("You find rare medicinal plants.", 50, 350, GREEN)
        display_text("1. Harvest them", 50, 400, WHITE)
        display_text("2. Leave them", 50, 450, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2"])
        if choice == "1":
            if jungle_stats['survival'] > 50:
                display_text("You collect valuable herbs!", 50, 500, GREEN)
                jungle_stats['survival'] += 15
                character_stats['inventory'].append("medicinal herbs")
                score += 30
            else:
                display_text("You poison yourself! (-20 health)", 50, 500, RED)
                character_stats['health'] -= 20
                score -= 15
        else:
            display_text("A spirit blesses you.", 50, 500, YELLOW)
            jungle_stats['animal_respect'] += 10
            score += 20
    else:
        display_text("The map leads to a treasure room!", 50, 350, YELLOW)
        display_text("1. Take golden idol", 50, 400, WHITE)
        display_text("2. Study writings", 50, 450, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2"])
        if choice == "1":
            display_text("You take the idol! The temple rumbles...", 50, 500, YELLOW)
            character_stats['inventory'].append("golden idol")
            score += 100
        else:
            display_text("You learn ancient jungle secrets.", 50, 500, GREEN)
            jungle_stats['survival'] += 25
            score += 50

    pygame.time.wait(SHORT_DELAY)

    # Tribal Encounter
    screen.blit(jungle_background, (0, 0))
    display_text("As you leave the ruins, you encounter a native tribe.", 50, 50, WHITE)
    display_text("They seem wary of outsiders.", 50, 100, WHITE)

    options = []
    option_texts = []
    if "guardian's amulet" in character_stats['inventory']:
        options.append("1")
        option_texts.append("1. Show amulet")
    if "medicinal herbs" in character_stats['inventory']:
        options.append("2")
        option_texts.append("2. Offer herbs")
    if "golden idol" in character_stats['inventory']:
        options.append("3")
        option_texts.append("3. Show idol")
    options.append("4")
    option_texts.append("4. Sneak around")
    options.append("5")
    option_texts.append("5. Approach peacefully")

    for i, option in enumerate(option_texts):
        display_text(option, 50, 200 + i * 50, WHITE)
    display_jungle_stats()
    pygame.display.flip()

    choice = get_choice(options)

    # Immediate response
    screen.blit(jungle_background, (0, 0))
    if choice == "1" and "guardian's amulet" in character_stats['inventory']:
        display_text("The tribe welcomes you as a guardian!", 50, 300, GREEN)
        jungle_stats['animal_respect'] += 30
        score += 50
    elif choice == "2" and "medicinal herbs" in character_stats['inventory']:
        display_text("They accept your herbs and share knowledge.", 50, 300, GREEN)
        jungle_stats['survival'] += 20
        character_stats['inventory'].remove("medicinal herbs")
        score += 40
    elif choice == "3" and "golden idol" in character_stats['inventory']:
        display_text("They recognize the idol and kneel before you!", 50, 300, YELLOW)
        display_text("1. Return it to them", 50, 350, WHITE)
        display_text("2. Keep it as a trophy", 50, 400, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2"])
        if choice == "1":
            display_text("They share ancient wisdom with you.", 50, 450, GREEN)
            character_stats['inventory'].remove("golden idol")
            jungle_stats['survival'] += 30
            score += 80
        else:
            display_text("They reluctantly accept your decision.", 50, 450, YELLOW)
            score += 60
    elif choice == "4":
        if jungle_stats['exploration'] > 50:
            display_text("You slip by unseen.", 50, 300, GREEN)
            score += 30
        else:
            display_text("You're caught! They take some supplies.", 50, 300, RED)
            character_stats['health'] -= 30
            if "medicinal herbs" in character_stats['inventory']:
                character_stats['inventory'].remove("medicinal herbs")
            score -= 20
    else:
        if jungle_stats['animal_respect'] > 30:
            display_text("They respect your peaceful approach.", 50, 300, GREEN)
            jungle_stats['survival'] += 40
            score += 50
        else:
            display_text("They're suspicious but let you pass.", 50, 300, YELLOW)
            score += 20

    pygame.display.flip()
    pygame.time.wait(SHORT_DELAY)

    # Finale - Heart of the Jungle
    screen.blit(jungle_background, (0, 0))
    display_text("After weeks of travel, you reach the jungle's heart!", 50, 50, GREEN)
    display_text("Before you lies the legendary White Jaguar's shrine.", 50, 100, WHITE)
    pygame.display.flip()
    pygame.time.wait(MEDIUM_DELAY)

    options = []
    option_texts = []
    if jungle_stats['animal_respect'] > 50:
        options.append("1")
        option_texts.append("1. Become the jungle's protector")
    if "golden idol" in character_stats['inventory']:
        options.append("2")
        option_texts.append("2. Claim the treasure for yourself")
    options.append("3")
    option_texts.append("3. Seek the White Jaguar")
    options.append("4")
    option_texts.append("4. Find your way back to civilization")

    for i, option in enumerate(option_texts):
        display_text(option, 50, 200 + i * 50, WHITE)
    display_jungle_stats()
    pygame.display.flip()

    choice = get_choice(options)

    # Final outcomes
    screen.blit(jungle_background, (0, 0))

    # Calculate base score based on achievements
    base_score = (
            jungle_stats['exploration'] * 2 +
            jungle_stats['survival'] * 2 +
            jungle_stats['animal_respect'] * 3 +
            len(character_stats['inventory']) * 15 +
            character_stats['health'] +
            character_stats['courage']
    )

    # Ensure minimum score of 100
    score = max(base_score, 100)

    # Ending messages based on performance
    if choice == "1" and jungle_stats['animal_respect'] > 50:
        display_text("Congratulations!", center=True, y=150, color=GREEN, font_obj=title_font)
        display_text("You've become the jungle's eternal guardian.", center=True, y=220, color=WHITE)
        display_text("The spirits bless you with wisdom and longevity", center=True, y=270, color=WHITE)
        score += 100  # Bonus for best ending
    elif choice == "2" and "golden idol" in character_stats['inventory']:
        display_text("Success!", center=True, y=150, color=YELLOW, font_obj=title_font)
        display_text("You return with priceless treasures.", center=True, y=220, color=WHITE)
        display_text("Though part of you misses the jungle's call...", center=True, y=270, color=WHITE)
        score += 80
    elif choice == "3":
        if jungle_stats['exploration'] > 70 and jungle_stats['animal_respect'] > 40:
            display_text("Triumph!", center=True, y=150, color=GREEN, font_obj=title_font)
            display_text("The White Jaguar shares ancient secrets with you.", center=True, y=220, color=WHITE)
            display_text("You gain wisdom beyond measure.", center=True, y=270, color=WHITE)
            score += 120
        else:
            display_text("A Good Journey", center=True, y=150, color=YELLOW, font_obj=title_font)
            display_text("Though you didn't find the Jaguar,", center=True, y=220, color=WHITE)
            display_text("you gained valuable experience.", center=True, y=270, color=WHITE)
            score = max(score, 150)  # Ensure decent score
    else:
            if jungle_stats['survival'] > 80:
               display_text("Well Done!", center=True, y=150, color=GREEN, font_obj=title_font)
               display_text("You return with incredible stories", center=True, y=270, color=WHITE)
               score += 70
            else:
               display_text("A New Beginning", center=True, y=150, color=YELLOW, font_obj=title_font)
               display_text("Though you got lost, you discover", center=True, y=220, color=WHITE)
               display_text("a beautiful hidden valley to call home.", center=True, y=270, color=WHITE)
    pygame.time.wait(MEDIUM_DELAY)
    screen.blit(jungle_background, (0, 0))
    display_text("Your Adventure Concludes", center=True, y=100, color=WHITE, font_obj=title_font)
    display_text(f"Final Score: {score}", center=True, y=200, color=YELLOW, font_obj=title_font)

# Personalized closing based on score
    if score >= 300:
     display_text("Legendary Explorer!", center=True, y=300, color=GREEN)
    elif score >= 200:
      display_text("Master Adventurer!", center=True, y=300, color=YELLOW)
    else:
       display_text("Brave Wanderer!", center=True, y=300, color=WHITE)

    display_text("1. Play Again", 100, 500, WHITE)
    display_text("2. Quit", 600, 500, WHITE)
    pygame.display.flip()

    choice = get_choice(["1", "2"])
    if choice == "1":
        main()
    else:
        pygame.quit()
        sys.exit()

def horror_story(character_name):
    global score
    score = 0
    horror_stats.update({
        "darkness_resistance": 0,
        "occult_knowledge": 0,
        "ghostly_favors": 0
    })

    play_music(horror_music)

    def display_horror_stats():
     stats_y = HEIGHT - 70  # 70px from bottom

    # Compact stats format
     stats_text = (
        f"Health: {character_stats['health']} | "
        f"Courage: {character_stats['courage']} | "
        f"Sanity: {character_stats['sanity']} | "
        f"Dark: {horror_stats['darkness_resistance']} | "
        f"Occult: {horror_stats['occult_knowledge']} | "
        f"Ghosts: {horror_stats['ghostly_favors']} | "
        f"Inventory: {', '.join(character_stats['inventory']) if character_stats['inventory'] else 'Empty'}"
      )

    # Display single line of stats with smaller font
     display_text(stats_text, 10, stats_y, (220, 220, 220), stats_font)


    # Introduction
    screen.blit(horror_background, (0, 0))
    display_text(f"Haunting of Blackwood Manor", center=True, y=50, color=RED, font_obj=title_font)
    display_text(f"{character_name}, you've inherited Blackwood Manor", center=True, y=150, color=WHITE)
    display_text("from your mysterious uncle. Locals say it's haunted.", center=True, y=200, color=WHITE)
    display_text("You arrive at midnight during a storm...", center=True, y=250, color=WHITE)
    display_text("Press 1 to enter the manor", center=True, y=350, color=YELLOW)
    pygame.display.flip()
    get_choice(["1"])

    # Haunted House Approach
    screen.blit(horror_background, (0, 0))
    display_text("The massive oak doors loom before you.", 50, 50, WHITE)
    display_text("How will you enter?", 50, 100, WHITE)
    display_text("1. Kick down the door (Courage)", 50, 150, WHITE)
    display_text("2. Find hidden entrance (Luck)", 50, 200, WHITE)
    display_text("3. Perform protection ritual (Occult)", 50, 250, WHITE)
    display_horror_stats()
    pygame.display.flip()

    choice = get_choice(["1", "2", "3"])

    # Immediate consequences
    screen.blit(horror_background, (0, 0))
    if choice == "1":
        if character_stats['courage'] > 60:
            display_text("You burst in defiantly! The darkness recoils.", 50, 300, GREEN)
            horror_stats['darkness_resistance'] += 10
            score += 20
        else:
            display_text("You panic at the last moment! (-15 Sanity)", 50, 300, RED)
            character_stats['sanity'] -= 15
            score -= 10
    elif choice == "2":
        if character_stats['luck'] > 55:
            display_text("You find a hidden servants' entrance.", 50, 300, GREEN)
            character_stats['inventory'].append("house blueprint")
            score += 30
        else:
            display_text("You trigger an ancient alarm! Spirits awaken.", 50, 300, RED)
            horror_stats['ghostly_favors'] -= 5
            score -= 15
    else:
        if "occult tome" in character_stats['inventory']:
            display_text("Your ritual creates a protective aura!", 50, 300, GREEN)
            horror_stats['darkness_resistance'] += 20
            score += 40
        else:
            display_text("You anger the spirits with your poor ritual! (-25 Sanity)", 50, 300, RED)
            character_stats['sanity'] -= 25
            score -= 20

    pygame.display.flip()
    pygame.time.wait(SHORT_DELAY)

    # Main Hall
    screen.blit(horror_background, (0, 0))
    display_text("Inside, the grand hall stretches before you.", 50, 50, WHITE)
    display_text("Dust covers everything. The air feels heavy.", 50, 100, WHITE)

    options = []
    option_texts = []
    if character_stats['sanity'] > 70:
        options.append("1")
        option_texts.append("1. Explore the grand hall")
    options.append("2")
    option_texts.append("2. Investigate the dining room")
    if horror_stats['darkness_resistance'] > 15:
        options.append("3")
        option_texts.append("3. Descend to the cellar")
    if "house blueprint" in character_stats['inventory']:
        options.append("4")
        option_texts.append("4. Find the study")

    for i, option in enumerate(option_texts):
        display_text(option, 50, 200 + i * 50, WHITE)
    display_horror_stats()
    pygame.display.flip()

    choice = get_choice(options)

    # Immediate results
    screen.blit(horror_background, (0, 0))
    if choice == "1":
        display_text("Portraits whisper warnings as you pass...", 50, 300, WHITE)
        display_text("1. Listen to their warnings", 50, 350, WHITE)
        display_text("2. Ignore them", 50, 400, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2"])
        if choice == "1":
            horror_stats['occult_knowledge'] += 10
            display_text("You learn of the manor's dark history.", 50, 450, GREEN)
            score += 30
        else:
            character_stats['sanity'] -= 10
            display_text("The whispers grow angry and louder.", 50, 450, RED)
            score -= 10
    elif choice == "2":
        display_text("Ghostly servants reenact their final meal!", 50, 300, WHITE)
        display_text("1. Join their feast", 50, 350, WHITE)
        display_text("2. Take a silver knife", 50, 400, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2"])
        if choice == "1":
            horror_stats['ghostly_favors'] += 15
            display_text("They gift you a spectral key.", 50, 450, GREEN)
            character_stats['inventory'].append("spectral key")
            score += 50
        else:
            character_stats['sanity'] -= 20
            display_text("The knife burns your hand! It's cursed.", 50, 450, RED)
            score -= 20
    elif choice == "3":
        display_text("Something ancient stirs in the darkness below...", 50, 300, RED)
        if horror_stats['occult_knowledge'] > 30:
            display_text("Your knowledge protects you from its gaze.", 50, 350, GREEN)
            display_text("You find an ancient tome!", 50, 400, YELLOW)
            character_stats['inventory'].append("occult tome")
            score += 70
        else:
            character_stats['sanity'] -= 40
            display_text("You glimpse something unspeakable!", 50, 350, RED)
            score -= 30
    else:
        display_text("The study contains your uncle's research.", 50, 300, GREEN)
        display_text("You learn he was trying to banish a demon.", 50, 350, WHITE)
        horror_stats['occult_knowledge'] += 25
        character_stats['inventory'].append("uncle's notes")
        score += 60

    pygame.display.flip()
    pygame.time.wait(SHORT_DELAY)

    # Upstairs Investigation
    screen.blit(horror_background, (0, 0))
    display_text("A grand staircase leads to the upper floors.", 50, 50, WHITE)
    display_text("The air grows colder as you ascend...", 50, 100, WHITE)

    options = []
    option_texts = []
    if horror_stats['ghostly_favors'] > 10:
        options.append("1")
        option_texts.append("1. Follow the friendly spirit")
    options.append("2")
    option_texts.append("2. Search the master bedroom")
    if "spectral key" in character_stats['inventory']:
        options.append("3")
        option_texts.append("3. Unlock the forbidden room")
    options.append("4")
    option_texts.append("4. Investigate the nursery")

    for i, option in enumerate(option_texts):
        display_text(option, 50, 200 + i * 50, WHITE)
    display_horror_stats()
    pygame.display.flip()

    choice = get_choice(options)

    # Immediate results
    screen.blit(horror_background, (0, 0))
    if choice == "1" and horror_stats['ghostly_favors'] > 10:
        display_text("The spirit leads you to a hidden safe.", 50, 300, GREEN)
        display_text("Inside is your uncle's will and a holy symbol.", 50, 350, WHITE)
        character_stats['inventory'].append("holy symbol")
        horror_stats['darkness_resistance'] += 30
        score += 80
    elif choice == "2":
        display_text("The bedroom is frozen in time.", 50, 300, WHITE)
        display_text("A diary reveals the family's tragic fate.", 50, 350, WHITE)
        horror_stats['occult_knowledge'] += 15
        score += 40

        if random.randint(1, 100) > character_stats['luck']:
            display_text("A ghost attacks you! (-20 Health)", 50, 400, RED)
            character_stats['health'] -= 20
            score -= 20
    elif choice == "3" and "spectral key" in character_stats['inventory']:
        display_text("The key unlocks a hidden occult library.", 50, 300, YELLOW)
        display_text("Ancient knowledge floods your mind!", 50, 350, WHITE)
        horror_stats['occult_knowledge'] += 40
        character_stats['sanity'] -= 30
        score += 100
    else:
        display_text("A child's ghost plays with a music box.", 50, 300, WHITE)
        display_text("1. Take the music box", 50, 350, WHITE)
        display_text("2. Play with the ghost", 50, 400, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2"])
        if choice == "1":
            display_text("The ghost wails! (-30 Sanity)", 50, 450, RED)
            character_stats['sanity'] -= 30
            character_stats['inventory'].append("cursed music box")
            score -= 20
        else:
            display_text("The ghost leads you to a hidden passage.", 50, 450, GREEN)
            horror_stats['ghostly_favors'] += 20
            score += 50

    pygame.display.flip()
    pygame.time.wait(SHORT_DELAY)
    # Final Confrontation
    screen.blit(horror_background, (0, 0))
    display_text("A blood-curdling scream echoes through the manor!", 50, 50, RED)
    display_text("The walls bleed as the true horror reveals itself...", 50, 100, WHITE)
    display_text("Your uncle's failed ritual unleashed a demon!", 50, 150, WHITE)
    pygame.display.flip()
    pygame.time.wait(LONG_DELAY)

    options = []
    option_texts = []
    if horror_stats['occult_knowledge'] > 50:
        options.append("1")
        option_texts.append("1. Perform banishment ritual")
    if "holy symbol" in character_stats['inventory']:
        options.append("2")
        option_texts.append("2. Use holy symbol")
    options.append("3")
    option_texts.append("3. Fight with courage")
    if horror_stats['ghostly_favors'] > 30:
        options.append("4")
        option_texts.append("4. Call for ghostly aid")

    for i, option in enumerate(option_texts):
        display_text(option, 50, 250 + i * 50, WHITE)
    display_horror_stats()
    pygame.display.flip()

    choice = get_choice(options)

    # Final outcomes
    screen.blit(horror_background, (0, 0))

    # Calculate base score based on achievements
    base_score = (
            horror_stats['darkness_resistance'] * 2 +
            horror_stats['occult_knowledge'] * 3 +
            horror_stats['ghostly_favors'] * 2 +
            len(character_stats['inventory']) * 20 +
            character_stats['health'] +
            character_stats['courage'] +
            character_stats['sanity']
    )

    # Ensure minimum score of 100
    score = max(base_score, 100)

    # Ending messages based on performance
    if choice == "1" and horror_stats['occult_knowledge'] > 50:
        display_text("Victory!", center=True, y=150, color=GREEN, font_obj=title_font)
        display_text("You've banished the demon forever.", center=True, y=220, color=WHITE)
        display_text("The manor is at peace thanks to you.", center=True, y=270, color=WHITE)
        score += 150
    elif choice == "2" and "holy symbol" in character_stats['inventory']:
        display_text("Success!", center=True, y=150, color=YELLOW, font_obj=title_font)
        display_text("The holy symbol protects you and the manor.", center=True, y=220, color=WHITE)
        display_text("Though evil may return one day...", center=True, y=270, color=WHITE)
        score += 120
    elif choice == "3":
        if character_stats['courage'] > 80:
            display_text("Heroic!", center=True, y=150, color=GREEN, font_obj=title_font)
            display_text("Your bravery inspired the ghosts", center=True, y=220, color=WHITE)
            display_text("to finally defeat the demon.", center=True, y=270, color=WHITE)
            score += 100
        else:
            display_text("A Second Chance", center=True, y=150, color=YELLOW, font_obj=title_font)
            display_text("Though wounded, you escape to tell", center=True, y=220, color=WHITE)
            display_text("the tale and prepare for another attempt.", center=True, y=270, color=WHITE)
            score = max(score, 150)
    elif choice == "4" and horror_stats['ghostly_favors'] > 30:
        display_text("Triumph!", center=True, y=150, color=GREEN, font_obj=title_font)
        display_text("Together with the spirits,", center=True, y=220, color=WHITE)
        display_text("you've cleansed the manor forever.", center=True, y=270, color=WHITE)
        score += 180
    else:
        display_text("Survivor!", center=True, y=150, color=YELLOW, font_obj=title_font)
        display_text("You barely escaped with your life,", center=True, y=220, color=WHITE)
        display_text("but gained valuable knowledge.", center=True, y=270, color=WHITE)
        score = max(score, 120)

    pygame.time.wait(MEDIUM_DELAY)

    # Final score display
    screen.blit(horror_background, (0, 0))
    display_text("The Haunting Ends", center=True, y=100, color=WHITE, font_obj=title_font)
    display_text(f"Final Score: {score}", center=True, y=200, color=YELLOW, font_obj=title_font)

    # Personalized closing based on score
    if score >= 400:
        display_text("Master of the Occult!", center=True, y=300, color=GREEN)
    elif score >= 250:
        display_text("Skilled Ghost Hunter!", center=True, y=300, color=YELLOW)
    else:
        display_text("Brave Investigator!", center=True, y=300, color=WHITE)

    display_text("1. Play Again", 100, 500, WHITE)
    display_text("2. Quit", 600, 500, WHITE)
    pygame.display.flip()

    choice = get_choice(["1", "2"])
    if choice == "1":
        main()
    else:
        pygame.quit()
        sys.exit()
def main():
        play_music(neutral_music)
        while True:
            character_name = get_character_name()
            choice = welcome_page(character_name)

            if choice == "1":
                horror_story(character_name)
            elif choice == "2":
                jungle_adventure(character_name)

if __name__ == "__main__":
        main()