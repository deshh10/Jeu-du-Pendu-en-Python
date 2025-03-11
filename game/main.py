import pygame, requests, os, random, sys

from GameProfile import GameProfile
from Game import Game

context = ""

options_selected = "Normal"
main_menu_options = ["Normal", "Time up", "While life", "Shop", "Lockers", "Quit"]
main_menu_info = ["Jouez au jeu en mode normal", "Trouvez les mots dans le temps imparti",
                  "Trouvez le plus de mots tant que vous n'avez pas perdu", "Achetez des nouveaux skins",
                  "Equipez vos skins", "Partir"]

temp_username = "anonyme"
profile = None
game = None

hangman_dir = os.path.dirname(os.path.realpath(__file__)) + '/'
assets_dir = hangman_dir + 'assets/'
images_dir = assets_dir + 'images/'
fonts_dir = assets_dir + 'fonts/'

i_icon = images_dir + "icon.png"


def reset():
    """
    Reset the game object and sending winned coin to the rest api
    """
    global profile, game
    profile.coins += game.coins_earned
    if profile.username != "anonyme":
        requests.put('http://134.209.25.34:8080/user/update/' + profile.username, json=game.coins_earned) #164.92.232.27 Ip of the DigitalOcean droplet
    game = None


def get_random_word():
    """
    Open the words file and get a random word on it
    """
    with open(assets_dir + "words.txt") as file:
        lines = file.readlines()
        index = random.randint(0, len(lines))
        return lines[index].strip('\n')


def draw_secret_word(background, word, correct_letters):
    """
    Draw the word to guess with finded letter and _
    :param background: Where draw
    :param word: the word to find
    :param correct_letters: the letter to show
    """
    global game
    drawable_word = ""
    for letter in word:
        if letter in correct_letters:
            drawable_word += letter
        else:
            drawable_word += "_"
    draw_text(' '.join(drawable_word),
              (255, 255, 255) if (game.over == False or game.gagné == True) else (255, 0, 0),
              (320, 220), background, font2)


def draw_text(text, color, position, surface, font, centered=None, highlight=None):
    """
    Draw text on the pygame windows
    :param text: Text to draw
    :param color: rgb color (r, g, b)
    :param position: duo (x, y) pos
    :param surface: Where draw
    :param font: the font used
    :param centered: if text is center on window
    :param highlight: if text is highlight
    """
    text_to_draw = font.render(text, 1, color)
    text_to_draw_position = text_to_draw.get_rect().move(position)

    if centered:
        text_to_draw_position.centerx = surface.get_rect().centerx
    if highlight:
        pygame.draw.rect(surface, (0, 0, 0), text_to_draw_position.inflate(10, 10), 0)

    surface.blit(text_to_draw, text_to_draw_position)

def draw_screen():
    """
    Methode used to the event loop to draw the windows in terms of context
    :return:
    """
    global context, window, monospace, options_selected, profile, game

    background = pygame.image.load(images_dir + 'bg.png').convert()

    if "playing" in context:
        background = pygame.image.load(images_dir + 'bg-game.png').convert()

    match context:
        case "login":
            draw_text("Veuillez vous connecter", (0, 0, 0), (0, 50), background, middst, True)
            current_user_edit = temp_username + " "
            draw_text(current_user_edit, (2, 0, 0), (0, 220), background, monospace, True)
            draw_text("Appuyez sur Entrée pour vous connecter,", (60, 60, 60), (0, 430),
                      background,
                      font2, True)
            draw_text("Laissez vide si vous ne souhaitez pas vous connecter", (60, 60, 60), (0, 450),
                      background,
                      font2, True)

        case "main-menu":
            draw_text("HangMan - Game", (0, 0, 0), (0, 20), background, middst, True)
            draw_text(profile.username + " (" + str(profile.id) + ")", (0, 0, 0), (500, 80), background, font2, False)
            draw_text(str(profile.coins) + " coins", (0, 0, 0), (500, 100), background, font2, False)
            draw_text(main_menu_info[main_menu_options.index(options_selected)], (255, 255, 255), (0, 135), background,
                      font2, True)
            option_pos_y = 170
            for option in main_menu_options:
                draw_text(option, (255, 255, 255), (50, option_pos_y), background, font2, True,
                          option == options_selected)

                option_pos_y += 40
        case "playing-normal":
            draw_secret_word(background, game.word[0], game.correct_letters)

            nn = "gagné" if game.gagné else "perdu"
            text = 'Choisissez une lettre...' if (
                not game.over) else "Tu a " + nn + " utilise retour"
            draw_text(text, (255, 255, 255), (320, 180), background, font2)

            draw_text(game.incorrect_letters, (0, 0, 0), (320, 260), background, font2)
            display_gallows(background, len(game.incorrect_letters) + 1)
        case "playing-while-life":
            draw_secret_word(background, game.word[len(game.word) - 1], game.correct_letters)

            nn = "gagné" if game.gagné else "perdu"
            text = 'Choisissez une lettre...' if (
                not game.over) else "Tu as " + nn + " utilise retour"
            draw_text(text, (255, 255, 255), (320, 180), background, font2)

            draw_text(game.incorrect_letters, (0, 0, 0), (320, 260), background, font2)
            draw_text(game.find_word, (0, 0, 0), (320, 300), background, font2)

            display_gallows(background, game.fail + 1)
        case "playing-time-up":
            draw_secret_word(background, game.word[len(game.word) - 1], game.correct_letters)

            draw_text(str(max(int(timer), 0)) + " seconde(s) restante ", (255, 255, 255), (320, 160), background, font2)

            nn = "gagné" if game.gagné else "perdu"
            text = 'Choisissez une lettre...' if (
                not game.over) else "Tu as " + nn + " utilise retour "
            draw_text(text, (255, 255, 255), (320, 180), background, font2)

            draw_text(game.incorrect_letters, (0, 0, 0), (320, 260), background, font2)
            draw_text(game.find_word, (0, 0, 0), (320, 300), background, font2)

            display_gallows(background, len(game.incorrect_letters) + 1)
        case "game-summary":
            background = pygame.image.load(images_dir + 'bg-game.png').convert()
            display_summary(background)

    window.blit(background, (0, 0))
    pygame.display.update()


def display_gallows(background, state):
    """
    Show the gallow on the game windows using image assets
    :param background: windows to draw gallows
    :param state: the state of hangman
    """
    global profile, game
    img = pygame.image.load(images_dir + "gallows/" + profile.gallows_equipped + "/" + str(
        state) + ".png").convert_alpha()
    background.blit(img, (10, 10))


def display_summary(background):
    """
    Show the summary of the game in the windows
    :param background: where to draw
    """
    draw_text("Résumé du jeu", (0, 0, 0), (0, 20), background, middst, True)

    nn = "gagné" if game.gagné else "perdu"
    title_text = 'Tu ' + nn + '!'
    draw_text(title_text, (0, 0, 0), (0, 100), background, font2, True)

    pygame.draw.line(background, (0, 0, 0), (25, 150), (625, 150), 4)
    pygame.draw.line(background, (0, 0, 0), (25, 300), (625, 300), 4)
    pygame.draw.line(background, (0, 0, 0), (25, 430), (625, 430), 4)

    if game.mode == "normal":
        draw_text("Mauvaise lettre utilisée : " + str(len(game.incorrect_letters)), (0, 0, 0), (25, 160),
                  background,
                  font2, True)
        draw_text("Bonne lettre : " + str(len(game.word[0])), (0, 0, 0), (25, 260), background, font2, True)
        draw_text("Le mot est : " + game.word[0], (0, 0, 0), (0, 400), background, font2, True)
    elif game.mode == "while-life":
        draw_text("Vous avez trouvé : " + str(len(game.word) - 1) + " mot(s)", (0, 0, 0), (25, 160), background, font2,
                  True)
        draw_text("Vous avez trouvé les mots : " + game.find_word, (0, 0, 0), (0, 200), background, font2, True)
        draw_text("Vous n'avez pas trouvé le mot : " + game.word[len(game.word) - 1], (0, 0, 0), (0, 240), background,
                  font2, True)
    elif game.mode == "time-up":
        draw_text("Mauvaise lettre utilisée : " + str(len(game.incorrect_letters)), (0, 0, 0), (25, 160),
                  background,
                  font2, True)
        draw_text("Temps utilisé pour trouver : " + str(max(60 - int(timer), 0)), (0, 0, 0), (25, 180), background,
                  font2, True)
        draw_text("Le mot est : " + game.word[0], (0, 0, 0), (0, 200), background, font2, True)

    draw_text("SCORE    :          " + str(game.score), (0, 0, 0), (25, 340), background, font2, True)
    draw_text("PIÈCES    :          " + str(game.coins_earned), (0, 0, 0), (25, 360), background, font2, True)
    draw_text("Si vous voulez rejouer tapez Y sinon N", (0, 0, 0), (0, 450), background, font2, True)


def previous_option_main():
    """
    Set the previous option of the main menu
    """
    global options_selected
    current_index = main_menu_options.index(options_selected)
    if current_index > 0:
        options_selected = main_menu_options[current_index - 1]
    else:
        options_selected = main_menu_options[len(main_menu_options) - 1]


def next_option_main():
    """
    Set the next option of the main menu
    """
    global options_selected
    current_index = main_menu_options.index(options_selected)
    if current_index < len(main_menu_options) - 1:
        options_selected = main_menu_options[current_index + 1]
    else:
        options_selected = main_menu_options[0]


def load_profile(username):
    """
    Laod the user profile if anonyme set default value, get from rest api if login
    :param username: Player user name
    """
    global profile
    if username == "anonyme":
        profile = GameProfile()
        profile.id = 0
        profile.username = username
        profile.coins = 0

        profile.purchased_avatars = []
        profile.purchased_gallows = []

        profile.avatar_equipped = "default"
        profile.gallows_equipped = "default"
    else:
        profile = GameProfile()
        response = requests.get("http://134.209.25.34:8080/user/get/" + username); #164.92.232.27 the ip of the DigitalOcean Droplet

        json = response.json()

        profile.id = json["id"]
        profile.username = json["username"]
        profile.coins = json["coins"]

        profile.purchased_avatars = json["purchased_avatars"]
        profile.purchased_gallows = json["purchased_gallows"]

        profile.avatar_equipped = json["avatar_equipped"]
        profile.gallows_equipped = json["gallows_equipped"]


def setup_game(mode):
    """
    Setup the game object for mode
    :param mode: The mode of the game (Normal, WHileLife, TimeUp)
    """
    global game
    game = Game()
    game.mode = mode
    game.word = []
    game.word.append(get_random_word())
    game.find_word = ""
    game.incorrect_letters = ""
    game.correct_letters = ""
    game.score = 0
    game.fail = 0
    game.coins_earned = 0
    game.over = False
    game.gagné = False


def calculate_score(mode):
    """
    Calculate the score of game when game is finish
    :param mode: Game mode
    """
    global game
    if mode == "playing-normal":
        game.score = max(len(game.word[0]) - len(game.incorrect_letters), 0)
        game.coins_earned = max((game.score * 10), 0)
    elif mode == "playing-while-life":
        game.score = max((len(game.word) * 2) - game.fail, 0)
        game.coins_earned = max((game.score * 10), 0)
    elif mode == "playing-time-up":
        if game.gagné == True:
            game.score = max((len(game.word[0]) - len(game.incorrect_letters) * timer), 0)
            game.coins_earned = max((game.score * 10), 0)


def handle_event_on_game(event):
    """
    Use the event to game
    :param event: the pygame event fired
    """
    global context, timer
    key_pressed = chr(event.key)
    if not game.over:
        if key_pressed in "abcdefghijklmnopqrstuvwxyz0123456789":
            secret_word = game.word[len(game.word) - 1]
            correct_letters = game.correct_letters
            incorrect_letters = game.incorrect_letters

            if key_pressed in secret_word:
                if key_pressed not in correct_letters:
                    game.correct_letters = correct_letters + key_pressed
                    found_all_letters = True
                    for i in range(len(secret_word)):
                        if secret_word[i] not in game.correct_letters:
                            found_all_letters = False
                    if found_all_letters:
                        if not context == "playing-while-life":
                            game.gagné = True
                            game.over = True
                        else:
                            game.find_word = game.find_word + " " + secret_word
                            game.word.append(get_random_word())
                            game.correct_letters = ""
                            game.incorrect_letters = ""
                            game.gagné = True
            elif key_pressed not in incorrect_letters:
                game.incorrect_letters = incorrect_letters + key_pressed
                game.fail = game.fail + 1
                if game.fail == 9:
                    game.over = True
                    game.gagné = False
                    timer = 0
    else:
        if event.key == pygame.K_RETURN:
            calculate_score(context)
            context = "game-summary"

#Init pygame the library to make window
pygame.init()
pygame_icon = pygame.image.load(i_icon)
pygame.display.set_icon(pygame_icon)

#Init the pygame clock for the TimeUp game
clock = pygame.time.Clock()
timer = 120
dt = 0

#Load font
middst = pygame.font.Font(fonts_dir + 'middst.ttf', 56)
font2 = pygame.font.Font(None, 24)
monospace = pygame.font.SysFont("monospace", 60)

#The contexte of the game
context = "login"

#Window where all informations are draw
window = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)

while True:
    draw_screen()

    if context == "playing-time-up":
        if not game.over:
            timer -= dt
        if timer <= 0:
            game.over = True
            game.gagné = False
        dt = clock.tick(30) / 1000

    #When a key or anythings is fired he is add on event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:

            match context:
                case "login":
                    if event.key < 256:
                        key_pressed = chr(event.key)
                        if event.key == pygame.K_BACKSPACE:
                            temp_username = temp_username[:-1]
                        elif event.key == pygame.K_RETURN:
                            load_profile(temp_username)
                            context = "main-menu"
                        elif key_pressed in 'abcdefghijklmnopqrstuvwxyz0123456789':
                            temp_username += key_pressed
                        else:
                            print("Invalid character")
                case "main-menu":
                    if event.key == pygame.K_DOWN:
                        next_option_main()
                    elif event.key == pygame.K_UP:
                        previous_option_main()
                    elif event.key == pygame.K_RETURN:
                        match options_selected:
                            case "Normal":
                                setup_game("normal")
                                context = "playing-normal"
                            case "Time up":
                                setup_game("time-up")
                                context = "playing-time-up"
                                timer = 60
                            case "While life":
                                setup_game("while-life")
                                context = "playing-while-life"
                            case "Quit":
                                sys.exit(0)
                    else:
                        print("Invalid key")
                case "playing-normal":
                    if event.key < 256:
                        handle_event_on_game(event)
                case "playing-time-up":
                    if event.key < 256:
                        handle_event_on_game(event)
                case "playing-while-life":
                    if event.key < 256:
                        handle_event_on_game(event)
                case "game-summary":
                    if event.key < 256:
                        key_pressed = chr(event.key)

                        if key_pressed == "y":
                            reset()
                            context = "main-menu"
                        elif key_pressed == "n":
                            sys.exit(0)
                        else:
                            print("Invalid key")
