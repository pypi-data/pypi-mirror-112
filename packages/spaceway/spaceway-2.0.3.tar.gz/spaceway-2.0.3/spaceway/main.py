""" Root file with main entrypoint """

import os

import pygame

from . import scenes, collection, updater
from .config import ConfigManager


def main() -> None:
    # Set environment variable for centering window
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Initialization of pygame
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    # Get base directory to create absolute paths
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Initialization of configuration manager
    config = ConfigManager(base_dir)

    # Check software updates and view information dialog if update is available
    if config['user']['updates']:
        updater.check_software_updates(config['version'], base_dir)

    # Сreate screen with accounting for user settings
    if config['user']['full_screen']:
        screen = pygame.display.set_mode(config['mode'], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(config['mode'])

    # Configure screen
    pygame.display.set_caption(config['caption'])
    pygame.display.set_icon(pygame.image.load(f'{base_dir}/icon.ico'))

    # Get clock onject for the further use
    clock = pygame.time.Clock()

    # Initialize debug modules if configuration allows it
    if config['debug']:
        from . import debug
        debugger = debug.Debugger(config['FPS'])
        debugger.enable_module(debug.DebugStat, screen, base_dir, clock)
        debugger.enable_module(debug.DebugHitbox)

    # Set tick for calculating the past time in seconds
    tick = 0

    # Initialization of headpiece scene
    text = scenes.headpiece.init(screen, base_dir, config)

    # Initialization of lobby scene
    play_button, table_button, settings_button, caption = scenes.lobby.init(screen, base_dir, config)

    # Initialization of table scene
    table, table_back_button = scenes.table.init(screen, base_dir, config)

    # Initialization of settings scene
    effects_button, full_screen_button, updates_button, difficulty_button, settings_back_button, nick_input = scenes.settings.init(screen, base_dir, config)

    settings_buttons = collection.CenteredButtonsGroup(config['mode'])
    settings_buttons.add(effects_button, full_screen_button, updates_button, difficulty_button)

    # Initialization of game scene
    astrs = pygame.sprite.Group()
    boosts = collection.BoostsGroup()

    bg, plate, score, end, pause, resume_button, pause_lobby_button, again_button, end_lobby_button = scenes.game.init(screen, base_dir, config, astrs, boosts)

    pause_buttons = collection.CenteredButtonsGroup(config['mode'])
    pause_buttons.add(pause_lobby_button, resume_button)

    end_buttons = collection.CenteredButtonsGroup(config['mode'])
    end_buttons.add(end_lobby_button, again_button)

    # Scene buttons linking
    scene_buttons = collection.SceneButtonsGroup(config)
    scene_buttons.add(play_button, table_button, settings_button,
                      settings_back_button, table_back_button, resume_button,
                      pause_lobby_button, again_button, end_lobby_button)

    while True:
        # Update tick
        tick += 1

        # Showing a specific scene
        if config['scene'] == 'headpiece':
            scenes.headpiece.functions.check_events(config, base_dir)
            scenes.headpiece.functions.update(screen, config, text, tick)

        elif config['scene'] == 'lobby':
            scenes.lobby.functions.check_events(config, base_dir, scene_buttons, caption)
            scenes.lobby.functions.update(bg, scene_buttons, caption)

        elif config['scene'] == 'table':
            scenes.table.functions.check_events(config, scene_buttons)
            scenes.table.functions.update(base_dir, bg, table, scene_buttons)

        elif config['scene'] == 'settings':
            scenes.settings.functions.check_events(config, scene_buttons, settings_buttons, nick_input)
            scenes.settings.functions.update(bg, config, scene_buttons, settings_buttons, nick_input)

            # If fullscreen button was pressed, change screen to fullscreen and back again
            if full_screen_button.changed:
                screen = pygame.display.set_mode(config['mode'], pygame.FULLSCREEN * int(full_screen_button.state))
                full_screen_button.changed = False

        elif config['scene'] == 'game':
            scenes.game.functions.check_events(config, base_dir, plate, astrs, boosts, end, pause, scene_buttons)
            scenes.game.functions.update(screen, config, base_dir, bg, plate, astrs, boosts, score, end, pause, tick, pause_buttons, end_buttons, scene_buttons)

        # Zeroize tick from overflow
        if tick >= config['FPS'] * 10:
            tick = 0

        # Update debugger if debug mode enabled
        if config['debug']:
            debugger.update()

        # Update screen and adjust speed to FPS
        pygame.display.update()
        clock.tick(config['FPS'])
