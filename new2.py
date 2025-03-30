import pygame
import sys

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
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 32)

# Load images and sounds
neutral_background = pygame.image.load("welcome.png")
neutral_background = pygame.transform.scale(neutral_background, (WIDTH, HEIGHT))
jungle_background = pygame.image.load("jungle.png")
jungle_background = pygame.transform.scale(jungle_background, (WIDTH, HEIGHT))
horror_background = pygame.image.load("horror.png")
horror_background = pygame.transform.scale(horror_background, (WIDTH, HEIGHT))

# Music and sounds
neutral_music = "background_music.mp3"
horror_music = "Horror.mp3"
jungle_music = "Jungle.mp3"
click_sound = pygame.mixer.Sound("Click.mp3")

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
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)


def play_click_sound():
    click_sound.play()


def display_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x, y))
    pygame.draw.rect(screen, BLACK, text_rect.inflate(10, 5))
    screen.blit(text_surface, text_rect.topleft)


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
                if event.key == pygame.K_1 and "1" in options:
                    play_click_sound()
                    return "1"
                if event.key == pygame.K_2 and "2" in options:
                    play_click_sound()
                    return "2"
                if event.key == pygame.K_3 and "3" in options:
                    play_click_sound()
                    return "3"


def get_character_name():
    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play_click_sound()
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.blit(neutral_background, (0, 0))
        display_text("Enter your character's name:", 50, 50, WHITE)
        display_text(name, 50, 100, WHITE)
        pygame.display.flip()
    return name


def welcome_page(character_name):
    screen.blit(neutral_background, (0, 0))
    display_text(f"Welcome, {character_name}!", 200, 200, WHITE)
    display_text("Choose your adventure:", 50, 250, WHITE)
    display_text("1. Horror", 50, 300, WHITE)
    display_text("2. Jungle", 50, 350, WHITE)
    pygame.display.flip()
    return get_choice(["1", "2"])


def jungle_adventure(character_name):
    global score
    score = 0
    jungle_stats.update({
        "exploration": 0,
        "survival": 50,
        "animal_respect": 0
    })

    background = jungle_background
    play_music(jungle_music)

    def display_jungle_stats():
        char_stats = f"Health: {character_stats['health']} | Courage: {character_stats['courage']}"
        jungle_stats_text = f"Exploration: {jungle_stats['exploration']} | Survival: {jungle_stats['survival']} | Animal Respect: {jungle_stats['animal_respect']}"
        inv_text = "Inventory: " + ", ".join(character_stats['inventory']) if character_stats[
            'inventory'] else "Inventory: Empty"

        display_text(char_stats, 50, HEIGHT - 80, (200, 200, 255))
        display_text(jungle_stats_text, 50, HEIGHT - 50, (200, 255, 200))
        display_text(inv_text, 50, HEIGHT - 20, (255, 255, 200))

    # River Crossing
    screen.blit(background, (0, 0))
    display_text(f"{character_name}, you stand before a raging river.", 50, 50, WHITE)
    display_text("How will you cross?", 50, 100, WHITE)
    display_text("1. Build a raft (requires survival skill)", 50, 150, WHITE)
    display_text("2. Search for a bridge", 50, 200, WHITE)
    display_text("3. Swim across (dangerous!)", 50, 250, WHITE)
    display_jungle_stats()
    pygame.display.flip()

    choice = get_choice(["1", "2", "3"])

    if choice == "1":
        if jungle_stats['survival'] > 40:
            display_text("You build a sturdy raft and cross safely!", 50, 300, WHITE)
            jungle_stats['survival'] += 5
            character_stats['inventory'].append("raft")
        else:
            display_text("Your raft falls apart! (-15 health)", 50, 300, WHITE)
            character_stats['health'] -= 15
    elif choice == "2":
        jungle_stats['exploration'] += 10
        display_text("You find an ancient vine bridge.", 50, 300, WHITE)
        display_text("1. Cross carefully", 50, 350, WHITE)
        display_text("2. Investigate the bridge first", 50, 400, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2"])
        if choice == "1":
            display_text("You make it across safely.", 50, 450, WHITE)
        else:
            display_text("You find carvings that reveal a secret path!", 50, 450, WHITE)
            character_stats['inventory'].append("ancient map")
    else:
        if character_stats['luck'] > 70:
            display_text("Against all odds, you make it across!", 50, 300, WHITE)
            jungle_stats['animal_respect'] += 5
        else:
            display_text("The current nearly drowns you! (-25 health)", 50, 300, WHITE)
            character_stats['health'] -= 25

    pygame.time.wait(SHORT_DELAY)

    # Temple Ruins
    screen.blit(jungle_background, (0, 0))
    display_text("You discover ancient temple ruins.", 50, 50, WHITE)

    options = ["1. Enter main temple", "2. Explore surroundings"]
    if "ancient map" in character_stats['inventory']:
        options.append("3. Follow map to hidden chambers")

    for i, option in enumerate(options):
        display_text(option, 50, 150 + i * 50, WHITE)
    display_jungle_stats()
    pygame.display.flip()

    choice = get_choice(["1", "2", "3"][:len(options)])

    # Temple branches
    if choice == "1":
        display_text("A stone guardian blocks your path!", 50, 300, WHITE)
        display_text("1. Fight it", 50, 350, WHITE)
        display_text("2. Reason with it", 50, 400, WHITE)
        display_text("3. Find another way", 50, 450, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2", "3"])
        if choice == "1":
            if character_stats['health'] > 80:
                display_text("You defeat the guardian but are wounded!", 50, 500, WHITE)
                character_stats['health'] -= 30
                character_stats['inventory'].append("amulet")
            else:
                display_text("The guardian overpowers you! (-40 health)", 50, 500, WHITE)
                character_stats['health'] -= 40
        elif choice == "2":
            if jungle_stats['animal_respect'] > 20:
                display_text("The guardian lets you pass.", 50, 500, WHITE)
                jungle_stats['animal_respect'] += 10
            else:
                display_text("The guardian doesn't trust you.", 50, 500, WHITE)
        else:
            jungle_stats['exploration'] += 15
            display_text("You find a hidden tunnel.", 50, 500, WHITE)
    elif choice == "2":
        jungle_stats['exploration'] += 20
        display_text("You find rare medicinal plants.", 50, 300, WHITE)
        display_text("1. Harvest them", 50, 350, WHITE)
        display_text("2. Leave them", 50, 400, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2"])
        if choice == "1":
            if jungle_stats['survival'] > 50:
                display_text("You collect valuable herbs!", 50, 450, WHITE)
                jungle_stats['survival'] += 15
                character_stats['inventory'].append("herbs")
            else:
                display_text("You poison yourself! (-20 health)", 50, 450, WHITE)
                character_stats['health'] -= 20
        else:
            display_text("A spirit blesses you.", 50, 450, WHITE)
            jungle_stats['animal_respect'] += 10
    else:
        display_text("The map leads to a treasure room!", 50, 300, WHITE)
        display_text("1. Take golden idol", 50, 350, WHITE)
        display_text("2. Study writings", 50, 400, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2"])
        if choice == "1":
            display_text("You take the idol! Temple collapses!", 50, 450, WHITE)
            character_stats['inventory'].append("golden idol")
            score += 100
        else:
            display_text("You learn jungle secrets.", 50, 450, WHITE)
            jungle_stats['survival'] += 25

    pygame.time.wait(SHORT_DELAY)

    # Tribal Encounter (optimized)
    screen.blit(jungle_background, (0, 0))
    display_text("You encounter a native tribe.", 50, 50, WHITE)

    options = []
    if "amulet" in character_stats['inventory']:
        options.append("1. Show amulet")
    if "herbs" in character_stats['inventory'] or "golden idol" in character_stats['inventory']:
        options.append("2. Offer gifts")
    options.append("1. Sneak around")
    options.append("2. Approach peacefully")

    for i, option in enumerate(options):
        display_text(option, 50, 150 + i * 50, WHITE)
    display_jungle_stats()
    pygame.display.flip()

    choice = get_choice([str(i + 1) for i in range(len(options))])

    # Immediate response
    screen.blit(jungle_background, (0, 0))
    if choice == "1" and "amulet" in character_stats['inventory']:
        display_text("The tribe welcomes you!", 50, 300, WHITE)
        jungle_stats['animal_respect'] += 30
        score += 50
    elif choice == "2":
        if "herbs" in character_stats['inventory']:
            display_text("They accept your herbs.", 50, 300, WHITE)
            jungle_stats['survival'] += 20
            character_stats['inventory'].remove("herbs")
        elif "golden idol" in character_stats['inventory']:
            display_text("They demand the idol!", 50, 300, WHITE)
            display_text("1. Return it", 50, 350, WHITE)
            display_text("2. Refuse", 50, 400, WHITE)
            pygame.display.flip()

            choice = get_choice(["1", "2"])
            if choice == "1":
                display_text("They share wisdom.", 50, 450, WHITE)
                character_stats['inventory'].remove("golden idol")
                jungle_stats['survival'] += 30
            else:
                display_text("They attack! (-50 health)", 50, 450, WHITE)
                character_stats['health'] -= 50
    elif choice == "3":
        if jungle_stats['exploration'] > 50:
            display_text("You slip by unseen.", 50, 300, WHITE)
        else:
            display_text("You're caught!", 50, 300, WHITE)
            character_stats['health'] -= 30
    else:
        if jungle_stats['animal_respect'] > 30:
            display_text("They respect you.", 50, 300, WHITE)
            jungle_stats['survival'] += 40
        else:
            display_text("They're suspicious.", 50, 300, WHITE)

    pygame.display.flip()
    pygame.time.wait(SHORT_DELAY)

    # Finale (optimized)
    screen.blit(jungle_background, (0, 0))
    display_text("You reach the jungle's heart!", 50, 50, WHITE)
    pygame.display.flip()
    pygame.time.wait(SHORT_DELAY)

    endings = []
    if jungle_stats['animal_respect'] > 50:
        endings.append("1. Become protector")
    if "golden idol" in character_stats['inventory']:
        endings.append("2. Escape with treasure")
    endings.append("1. Find white jaguar")
    endings.append("2. Find civilization")

    for i, ending in enumerate(endings):
        display_text(ending, 50, 150 + i * 50, WHITE)
    display_jungle_stats()
    pygame.display.flip()

    choice = get_choice([str(i + 1) for i in range(len(endings))])

    # Immediate outcome
    screen.blit(jungle_background, (0, 0))
    if choice == "1" and jungle_stats['animal_respect'] > 50:
        outcome = "You become the jungle's guardian!"
        score += 200
    elif choice == "2" and "golden idol" in character_stats['inventory']:
        outcome = "You escape with the idol (but cursed)!"
        score += 150
    elif choice == "3":
        outcome = "You found the jaguar!" if jungle_stats['exploration'] > 70 else "You never find it..."
        score += 300 if jungle_stats['exploration'] > 70 else 50
    else:
        outcome = "You find civilization!" if jungle_stats['survival'] > 80 else "You're lost forever"
        score += 180 if jungle_stats['survival'] > 80 else 0

    display_text(outcome, 50, 150, WHITE)
    display_text(f"Final Score: {score}", 50, 200, WHITE)
    display_text("1. Play Again", 50, 300, WHITE)
    display_text("2. Quit", 50, 350, WHITE)
    pygame.display.flip()

    choice = get_choice(["1", "2"])
    if choice == "1":
        main()
    else:
        pygame.quit()
        sys.exit()

# Function to handle the horror story
def horror_story(character_name):
    global score
    score = 0

    # Reset horror stats
    horror_stats.update({
        "darkness_resistance": 0,
        "occult_knowledge": 0,
        "ghostly_favors": 0
    })

    # Setup
    background = horror_background
    play_music(horror_music)

    def display_horror_stats():
        char_stats = f"Health: {character_stats['health']} | Courage: {character_stats['courage']} | Sanity: {character_stats['sanity']}"
        horror_stats_text = f"Dark Resist: {horror_stats['darkness_resistance']} | Occult: {horror_stats['occult_knowledge']} | Ghost Favors: {horror_stats['ghostly_favors']}"
        inv_text = "Inventory: " + ", ".join(character_stats['inventory']) if character_stats[
            'inventory'] else "Inventory: Empty"

        display_text(char_stats, 50, HEIGHT - 80, (200, 200, 255))
        display_text(horror_stats_text, 50, HEIGHT - 50, (255, 200, 200))
        display_text(inv_text, 50, HEIGHT - 20, (255, 255, 200))

    # Haunted House Approach
    screen.blit(background, (0, 0))
    display_text(f"{character_name}, you stand before Blackwood Manor.", 50, 50, WHITE)
    display_text("How will you enter?", 50, 100, WHITE)
    display_text("1. Kick down the door (Courage)", 50, 150, WHITE)
    display_text("2. Find hidden entrance (Luck)", 50, 200, WHITE)
    display_text("3. Perform ritual (Occult)", 50, 250, WHITE)
    display_horror_stats()
    pygame.display.flip()

    choice = get_choice(["1", "2", "3"])

    # Immediate consequences
    screen.blit(background, (0, 0))
    if choice == "1":
        if character_stats['courage'] > 60:
            display_text("You burst in defiantly!", 50, 300, WHITE)
            horror_stats['darkness_resistance'] += 10
        else:
            display_text("You panic! (-15 Sanity)", 50, 300, WHITE)
            character_stats['sanity'] -= 15
    elif choice == "2":
        if character_stats['luck'] > 55:
            display_text("You find a hidden entrance.", 50, 300, WHITE)
            character_stats['inventory'].append("house layout")
        else:
            display_text("You trigger an alarm!", 50, 300, WHITE)
            horror_stats['ghostly_favors'] -= 5
    else:
        if "occult tome" in character_stats['inventory']:
            display_text("Your ritual creates protection!", 50, 300, WHITE)
            horror_stats['darkness_resistance'] += 20
        else:
            display_text("You anger the spirits! (-25 Sanity)", 50, 300, WHITE)
            character_stats['sanity'] -= 25

    pygame.display.flip()
    pygame.time.wait(SHORT_DELAY)

    # Haunted Halls
    screen.blit(background, (0, 0))
    display_text("Inside, the manor's halls stretch endlessly.", 50, 50, WHITE)

    options = []
    if character_stats['sanity'] > 70:
        options.append("1. Explore grand hall")
    options.append("2. Investigate kitchen")
    if horror_stats['darkness_resistance'] > 15:
        options.append("3. Descend to cellar")

    for i, option in enumerate(options):
        display_text(option, 50, 150 + i * 50, WHITE)
    display_horror_stats()
    pygame.display.flip()

    choice = get_choice([str(i + 1) for i in range(len(options))])

    # Immediate results
    screen.blit(background, (0, 0))
    if choice == "1":
        display_text("Portraits whisper warnings...", 50, 300, WHITE)
        display_text("1. Listen", 50, 350, WHITE)
        display_text("2. Ignore", 50, 400, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2"])
        if choice == "1":
            horror_stats['occult_knowledge'] += 10
            display_text("You learn dark secrets.", 50, 450, WHITE)
        else:
            character_stats['sanity'] -= 10
            display_text("The whispers grow angry.", 50, 450, WHITE)
    elif choice == "2":
        display_text("Ghostly servants reenact murders!", 50, 300, WHITE)
        display_text("1. Help them", 50, 350, WHITE)
        display_text("2. Take knife", 50, 400, WHITE)
        pygame.display.flip()

        choice = get_choice(["1", "2"])
        if choice == "1":
            horror_stats['ghostly_favors'] += 15
            display_text("They gift you a spectral key.", 50, 450, WHITE)
            character_stats['inventory'].append("spectral key")
        else:
            character_stats['sanity'] -= 20
            display_text("The knife burns your hand!", 50, 450, WHITE)
    else:
        display_text("Something ancient stirs below...", 50, 300, WHITE)
        if horror_stats['occult_knowledge'] > 30:
            display_text("Your knowledge protects you.", 50, 350, WHITE)
            score += 50
        else:
            character_stats['sanity'] -= 40
            display_text("You glimpse something horrific!", 50, 350, WHITE)

    pygame.display.flip()
    pygame.time.wait(SHORT_DELAY)

    # Final Confrontation (optimized)
    screen.blit(background, (0, 0))
    display_text("A shadowy figure appears!", 50, 50, WHITE)
    display_text("1. Fight", 50, 150, WHITE)
    display_text("2. Sneak past", 50, 200, WHITE)
    if horror_stats['ghostly_favors'] > 20:
        display_text("3. Call for ghostly aid", 50, 250, WHITE)
    display_horror_stats()
    pygame.display.flip()

    options = ["1", "2", "3"] if horror_stats['ghostly_favors'] > 20 else ["1", "2"]
    choice = get_choice(options)

    # Immediate outcome
    screen.blit(background, (0, 0))
    if choice == "1":
        if character_stats['courage'] > 70:
            display_text("You fight valiantly but lose!", 50, 300, WHITE)
            character_stats['health'] -= 30
            score += 20
        else:
            display_text("The figure overwhelms you!", 50, 300, WHITE)
            character_stats['health'] -= 50
    elif choice == "2":
        if character_stats['luck'] > 60:
            display_text("You sneak past and find treasure!", 50, 300, WHITE)
            score += 80
        else:
            display_text("You're caught!", 50, 300, WHITE)
            character_stats['sanity'] -= 30
    else:
        display_text("Ghosts aid your escape!", 50, 300, WHITE)
        score += 100

    pygame.display.flip()
    pygame.time.wait(MEDIUM_DELAY)

    # Ending
    screen.blit(background, (0, 0))
    display_text(f"{character_name}, your final score: {score}", 50, 50, WHITE)
    display_text("1. Play Again", 50, 150, WHITE)
    display_text("2. Quit", 50, 200, WHITE)
    pygame.display.flip()

    choice = get_choice(["1", "2"])
    if choice == "1":
        main()
    else:
        pygame.quit()
        sys.exit()
# Main game loop
def main():
    play_music(neutral_music)  # Play neutral music on the welcome page
    character_name = get_character_name()  # Get the player's character name
    choice = welcome_page(character_name)  # Show the welcome page and get the player's choice

    if choice == "1":
        horror_story(character_name)  # Start the horror story
    elif choice == "2":
        jungle_adventure(character_name)  # Start the jungle adventure

if __name__ == "__main__":
    main()