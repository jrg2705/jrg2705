import random
# import os # No longer needed for os.system('cls')
import time
import curses

class Player:
    def __init__(self, x, y, representation='^'):
        self.x = x
        self.y = y
        self.representation = representation

    def move(self, dx, dy, max_x): # Added max_x for boundary check
        new_x = self.x + dx
        if 0 <= new_x < max_x: # Check against game width
            self.x = new_x
        # self.y += dy # Vertical movement not used for player in this game

    def shoot(self, game_bullets_list):
        game_bullets_list.append(Bullet(self.x, self.y - 1))

class Target:
    def __init__(self, x, y, representation='T', speed=1.0): # speed can be float
        self.x = x
        self.y = float(y) # Y position can be float for smoother movement
        self.representation = representation
        self.speed = speed

    def move(self, game_height, game_width):
        self.y += self.speed
        if int(self.y) >= game_height: # Compare int(self.y) with game_height
            self.y = 0.0
            self.x = random.randint(0, game_width - 1)

class Bullet:
    def __init__(self, x, y, representation='|', speed=1.0): # speed can be float
        self.x = x
        self.y = float(y) # Y position can be float
        self.representation = representation
        self.speed = speed

    def move(self):
        self.y -= self.speed

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Adjust player starting y to be within typical curses screen
        self.player = Player(width // 2, height - 2)
        self.targets = []
        self.bullets = []
        self.score = 0
        self.level = 1
        self.level_up_score_threshold = 100
        self.game_over = False
        self.level_up_message_timer = 0 # Timer to display "Level Up!" message
        self.level_up_message_duration = 30 # Frames to display message (e.g., 3 seconds at 0.1s per frame)

        self._configure_level_parameters()

    def _configure_level_parameters(self):
        base_target_spawn_interval = 25 # Adjusted for curses timing
        base_target_speed = 0.2 # Adjusted for curses timing (targets move 0.2 units per frame)

        self.current_target_speed = base_target_speed + (self.level - 1) * 0.05
        self.target_spawn_interval = max(10, base_target_spawn_interval - (self.level - 1) * 2)
        self.target_spawn_timer = 0

    def display_game(self, stdscr):
        # stdscr.clear() is called in the main loop before this

        # Display game boundaries (optional, for visual debugging)
        for y_coord in range(self.height):
            try:
                stdscr.addch(y_coord, 0, '|')
                stdscr.addch(y_coord, self.width -1 , '|')
            except curses.error: pass # Ignore errors if drawing exactly at COLS-1/LINES-1 edges
        for x_coord in range(self.width):
            try:
                stdscr.addch(0, x_coord, '-')
                stdscr.addch(self.height -1, x_coord, '-')
            except curses.error: pass


        # Player
        if 0 <= self.player.y < self.height and 0 <= self.player.x < self.width:
            try:
                stdscr.addstr(int(self.player.y), int(self.player.x), self.player.representation)
            except curses.error: pass

        # Targets
        for target in self.targets:
            if 0 <= int(target.y) < self.height and 0 <= target.x < self.width:
                try:
                    stdscr.addstr(int(target.y), target.x, target.representation)
                except curses.error: pass

        # Bullets
        for bullet in self.bullets:
            if 0 <= int(bullet.y) < self.height and 0 <= bullet.x < self.width:
                try:
                    stdscr.addstr(int(bullet.y), bullet.x, bullet.representation)
                except curses.error: pass

        # Score and Level
        score_level_text = f"Score: {self.score}  Level: {self.level}"
        try:
            stdscr.addstr(self.height, 0, score_level_text) # Display below game area
        except curses.error: # If height is exactly curses.LINES-1, try last line
             try: stdscr.addstr(self.height-1, 0, score_level_text)
             except curses.error: pass


        if self.level_up_message_timer > 0:
            level_up_text = f"*** Level Up! Reached Level {self.level}! ***"
            try:
                # Display centered, or at a fixed position
                msg_y = self.height // 2
                msg_x = (self.width - len(level_up_text)) // 2
                stdscr.addstr(msg_y, msg_x, level_up_text)
            except curses.error: pass
            self.level_up_message_timer -= 1


        if self.game_over:
            game_over_text = "Game Over!"
            try:
                stdscr.addstr(self.height // 2, (self.width - len(game_over_text)) // 2, game_over_text)
            except curses.error: pass


    def update(self):
        if self.game_over:
            return

        if self.level_up_message_timer == 0: # Only update game logic if not showing level up message pause
            self.check_level_up()

            self.target_spawn_timer +=1
            if self.target_spawn_timer >= self.target_spawn_interval:
                self.spawn_target()
                self.target_spawn_timer = 0

            for target in self.targets:
                target.move(self.height, self.width)

            for bullet in self.bullets:
                bullet.move()

            self.check_collisions()

    def handle_input(self, key_code):
        if self.game_over:
            return

        if key_code == curses.KEY_LEFT or key_code == ord('a'):
            self.player.move(-1, 0, self.width)
        elif key_code == curses.KEY_RIGHT or key_code == ord('d'):
            self.player.move(1, 0, self.width)
        elif key_code == ord('s'): # Using 's' for shoot
            self.player.shoot(self.bullets)
        # 'q' is handled in main_loop

    def check_collisions(self):
        bullets_to_remove_indices = []
        targets_to_remove_indices = []

        for i, bullet in enumerate(self.bullets):
            # Check collision with targets
            for j, target in enumerate(self.targets):
                if int(bullet.y) == int(target.y) and bullet.x == target.x:
                    if i not in bullets_to_remove_indices: bullets_to_remove_indices.append(i)
                    if j not in targets_to_remove_indices: targets_to_remove_indices.append(j)
                    self.score += 10

        for index in sorted(list(set(bullets_to_remove_indices)), reverse=True):
            del self.bullets[index]
        for index in sorted(list(set(targets_to_remove_indices)), reverse=True):
            del self.targets[index]

        for target in self.targets:
            if int(target.y) == self.player.y and target.x == self.player.x:
                self.game_over = True
                return

        # Remove bullets that go off the top screen
        self.bullets = [bullet for bullet in self.bullets if int(bullet.y) >= 0]

    def spawn_target(self):
        new_target_x = random.randint(1, self.width - 2) # Spawn away from side borders
        new_target = Target(new_target_x, 0, speed=self.current_target_speed)
        self.targets.append(new_target)

    def check_level_up(self):
        # Check if score reached the threshold for the *next* level
        if self.score >= self.level * self.level_up_score_threshold:
            self.level += 1
            self._configure_level_parameters()
            self.level_up_message_timer = self.level_up_message_duration # Start timer for message


def curses_main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True) # Non-blocking getch
    stdscr.keypad(True)  # Enable special keys (like arrow keys)

    # Game dimensions - should be less than curses.LINES and curses.COLS
    # Ensure game area is smaller than screen to display score below
    game_height = curses.LINES - 2  # Reserve a line for score/status
    game_width = curses.COLS -1   # Use full available width, -1 for safety

    if game_height < 10 or game_width < 20:
        # Restore terminal state before printing
        curses.curs_set(1)
        curses.endwin()
        print("Terminal window too small. Please resize and try again.")
        print(f"Minimum required: 20x10. Current: {curses.COLS}x{curses.LINES}")
        return


    game = Game(game_width, game_height)

    # Level up message right at the start if level 1 (for testing or initial message)
    # game.level_up_message_timer = game.level_up_message_duration # remove this if not needed

    last_frame_time = time.time()

    while not game.game_over:
        current_time = time.time()
        delta_time = current_time - last_frame_time

        # Target frame rate (e.g., 10 FPS -> 0.1s per frame)
        # This loop will run faster, game logic speed is controlled by entity speeds and spawn rates
        frame_delay = 0.05 # Reduced for smoother input, was 0.1

        if delta_time < frame_delay:
            time.sleep(frame_delay - delta_time)
        last_frame_time = time.time() # Reset last_frame_time more accurately


        key_code = stdscr.getch()

        if key_code == ord('q'):
            break

        if key_code != -1: # Check if a key was pressed (curses.ERR is -1)
             game.handle_input(key_code)

        game.update()

        stdscr.clear()
        game.display_game(stdscr) # Pass stdscr
        stdscr.refresh()

    # Game Over sequence
    curses.curs_set(1) # Show cursor again
    stdscr.nodelay(False) # Make getch blocking for final message

    final_score_text = f"Game Over! Final Score: {game.score} (Reached Level {game.level})"
    info_text = "Press any key to exit."

    stdscr.clear()
    try:
        stdscr.addstr(game_height // 2 -1, (game_width - len(final_score_text)) // 2, final_score_text)
        stdscr.addstr(game_height // 2 +1, (game_width - len(info_text)) // 2, info_text)
    except curses.error: # Fallback if text is too long or screen too small
        try:
            stdscr.addstr(0,0, final_score_text)
            stdscr.addstr(1,0, info_text)
        except curses.error: pass # Give up if still erroring
    stdscr.refresh()
    stdscr.getch() # Wait for user to press a key


if __name__ == "__main__":
    # Check if on Windows and install windows-curses if needed (already handled by prior step)
    # No need to run the pip install again here as it was a separate step
    try:
        curses.wrapper(curses_main)
    except curses.error as e:
        # This might happen if the terminal doesn't support curses, or during cleanup
        print(f"Curses error: {e}")
        print("If on Windows, ensure 'windows-curses' is installed: pip install windows-curses")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # It's good practice to ensure curses state is reset if an error occurs within wrapper
        # but wrapper usually handles this. If not, manual curses.endwin() might be needed.
        # For now, just print the error.
    finally:
        # curses.endwin() # wrapper should handle this
        pass
