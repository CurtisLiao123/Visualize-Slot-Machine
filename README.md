# Slot Machine Game
## How to Use
    1.Install Dependencies:
        Ensure Python and Pygame are installed.
        Install Pygame using the command:
            pip install pygame
    2.Setup:
        Remember to see if the directory of loading image and souneffect is right
        img = pygame.image.load(image_path)
        xxx_sound = pygame.mixer.Sound(f"sound effect path/xxx.wav")
    3.Run the Game:
        Execute the script using Python:
        python slot_machine.py
    4.Gameplay Instructions:
        Use the on-screen buttons to set your bet and spin the reels.
        Choose between Easy or Hard modes on the start screen.
        Monitor your balance and adjust bets accordingly.
    5.Replay:
        If your balance reaches zero, click the replay button to restart the game.

# Functions
    1.Interactive Slot Machine Game:
    2.Multiple Game Modes:
        Easy Mode: Simple gameplay with equal probability.
        Hard Mode: Weighted probabilities based on symbol values.
    3.Betting Options:
        Players can input their desired bet amount.
        Predefined percentage-based betting options:
            All In (100% of balance).
            Half (50% of balance).
            Quarter (25% of balance).
            Ten Percent (10% of balance).
    4.Symbol and Reel Display:
        Visual display of reels with symbols like Grape, Orange, Cherry, Banana, and others.Each have different values and probabilities based on mode.
    5.Win/Loss Evaluation:
        Automatically evaluates the result of a spin and displays the win or lose message.
        Different payouts based on matching symbols:
            Low, Medium, and High value matches.
            Special jackpot when matching special combination.
    6.Dynamic Balances:
        Tracks player balance and updates after each spin based on results.
        Prevents invalid bets
    7.Sounds and Feedback:
        Sound effects for spinning, winning, and losing:
        win.wav for wins.
        lose.wav for losses.
        jackpot.wav for jackpot wins.   
    8.Replay Functionality:
        Allows players to restart the game if the balance reaches zero.
    9.Interactive buttons and Responsive UI Components for:
        Includes button for:
            Starting the game.
            Spinning the reels.
            Mannual Betting input box
            Bet input box for manual betting amounts
        Dynamic messages and balance display.
        Responsive hover and click effects on buttons.
    10.Animation:
        Smooth spinning animation of the reels
    11.others
        Easily extendable for new symbols, sounds, or gameplay rules.

# Development Process
    Initial version generated with the help of ChatGPT using Matplotlib
    
    # Subsequent Improvements
    1.I add a simple determination of winning or losing
    2.I added a bet and balance system(visualized)
    3.Added sound effects for different payouts.
    4.Upgraded user interface for better interaction.
   
    Transition to Pygame:
    Pygame was selected for better event-driven programming capabilities, color options, and UI flexibility.
    Converted the Matplotlib version to Pygame with enhancements:
        Structural Improvements:
            1.Modularized Functions: Organized the code by putting related functionalities into modular functions, making it more readable and maintainable compared to earlier versions.
            2. Global Variables: Made the settings like screen dimensions, font sizes, and symbols global, simplifying adjustments and improving clarity.
            3. UI Consolidation: Moved all UI-related features into dedicated functions to enhance reusability.
            4. Event Handling: Adding an event handling mechanism to efficiently manage user inputs and interactions.
            5. Function Separation: Split 'update_spin' and 'check_win' functions for better logic and modularity.
            6. Reset Game State: Added a 'reset_game_state' function for restarting the game after a session ends.

            With ChatGPT’s help:
            - Introduced threaded sound play for smooth integration of sound effects.
            - Improved code organization and concise logic flow.

        Functional Enhancements:
            1. Game Modes: Added Easy and Hard modes with distinct win conditions for varied gameplays.
            2. Betting Options: Implemented predefined percentage-based betting buttons for convenience.
            3. Symbols and Sounds: Expanded symbol variety and added corresponding sound effects for immersive gameplay.
            4. Dynamic Balance: Integrated real-time balance tracking and updates to enhance player interaction.
            5. Replay Functionality: Enabled players to restart the game when the balance reaches zero.

            With ChatGPT’s suggestions:
            - Converted 'spin_reels' into a Pygame-compatible format for animation.
            - Used dictionaries to efficiently implement weighted probabilities for Hard mode.

# Code Structure：
        A[main function] --> B[run_start_screen]
        B -->|Easy Button Clicked| C[reset_game_state]
        C --> D[run_main_game]
        B -->|Hard Button Clicked| E[reset_game_state]
        E --> F[run_main_game2]

        D -->|Spin Button Clicked| G[start_spin]
        F -->|Spin Button Clicked| H[start_spin2]

        G --> I[update_spin]
        H --> I[update_spin]

        I -->|Spinning Ends| J[check_win_condition]
        J -->|Jackpot or Win| K[Play Win or Jackpot Sound]
        J -->|Lose| L[Play Lose Sound]

        J --> M[Enable Spin Button]

        D -->|Own <= 0| N[Replay Button]
        F -->|Own <= 0| N

        N -->|Replay Clicked| C

    functions:
        'draw_start_screen': Renders the start screen with game mode options.
        'reset_game_state': Resets all variables for a new game.
        'spin_reels': Simulates the spinning of reels.
        'check_win_conditions': Evaluates reels for win/lose conditions.
        'start_spin': Handles spin animations and sound effects.
        'update_spin': Updates spinning animation frame-by-frame.
        'run_main_game': Runs the main game loop with user interactions.


## References
  ChatGPT for code suggestions and improvements and text modifications of md writing.
  Freesound for sound effects.
  Pygame official documentation for game development guidance.
    



    





