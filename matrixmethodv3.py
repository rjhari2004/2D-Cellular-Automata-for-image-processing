import numpy as np
from raylib import *
from pyray import *

# Initialize Raylib window with resizable flag
def initialize_window(width, height, title):
    set_config_flags(FLAG_WINDOW_RESIZABLE)
    init_window(width, height, title)
    set_target_fps(60)

# Create T1 and T2 matrices for transformations
def create_matrices(image_shape):
    n = image_shape[0]
    T1 = np.zeros((n, n), dtype=int)
    T2 = np.zeros((n, n), dtype=int)
    
    for i in range(n - 1):
        T1[i, i + 1] = 1
    T2[1:n, 0:n-1] = np.eye(n - 1, dtype=int)
    return T1, T2

# Decompose rule number into powers of 2
def decompose_rule_number(rule_num):
    powers = []
    power = 1
    while rule_num > 0:
        if rule_num & 1:
            powers.append(power)
        rule_num >>= 1
        power <<= 1
    return powers

# Apply transformations based on decomposed rule
def apply_rule(rule_num, image):
    T1, T2 = create_matrices(image.shape)
    rule_transform = {
        1: lambda x: x,
        2: lambda x: np.dot(x, T2) % 2,
        4: lambda x: np.dot(T1, np.dot(x, T2)) % 2,
        8: lambda x: np.dot(T1, x) % 2,
        16: lambda x: np.dot(T1, np.dot(x, T1)) % 2,
        32: lambda x: np.dot(x, T1) % 2,
        64: lambda x: np.dot(T2, np.dot(x, T1)) % 2,
        128: lambda x: np.dot(T2, x) % 2,
        256: lambda x: np.dot(T2, np.dot(x, T2)) % 2
    }
    
    powers = decompose_rule_number(rule_num)
    result_image = np.zeros_like(image)

    for power in powers:
        if power in rule_transform:
            transformed_image = rule_transform[power](image)
            result_image = (result_image + transformed_image) % 2
    return result_image

# Input fields for rule, steps, rows, and columns
text_boxes = {
    "rule_num": {"label": "Rule Number:", "text": "", "position": (50, 50)},
    "steps": {"label": "Steps:", "text": "", "position": (50, 100)},
    "rows": {"label": "Rows:", "text": "", "position": (50, 150)},
    "columns": {"label": "Columns:", "text": "", "position": (50, 200)},
}
input_order = list(text_boxes.keys())
current_input = 0

# Button positions and sizes
start_button_pos = (50, 250)
next_button_pos = (160, 250)
undo_button_pos = (50, 300)
reset_button_pos = (160, 300)
toggle_boundaries_button_pos = (270, 300)
button_size = (100, 40)

# Page states and iteration control
on_first_page = True
on_input_page = False
show_boundaries = True
grid = np.zeros((10, 10), dtype=int)  # Default small grid
history = []
current_step = 0
rule_num, steps = 0, 0
used_grid = (0, 0)  # Used grid dimensions

# Zoom and pan control
zoom_level = 1.0
pan_offset = [0, 0]

# Draw input fields
def draw_text_boxes():
    global current_input
    for i, (key, box) in enumerate(text_boxes.items()):
        color = RED if i == current_input else DARKGRAY
        draw_text(box["label"], box["position"][0], box["position"][1] - 25, 20, BLACK)
        draw_rectangle(box["position"][0], box["position"][1], 200, 30, LIGHTGRAY)
        draw_text(box["text"], box["position"][0] + 5, box["position"][1] + 5, 20, color)

# Draw button
def draw_button(text, pos, size, active=False):
    color = LIGHTGRAY if active else GRAY
    draw_rectangle(pos[0], pos[1], size[0], size[1], color)
    draw_text(text, pos[0] + 15, pos[1] + 10, 20, BLACK)

# Draw the active part of the grid with zoom and pan
def draw_active_grid(grid):
    cell_size = int(20 * zoom_level)  # Ensure cell_size is an integer
    grid_origin_x = int(400 + pan_offset[0])  # Convert origin positions to integers
    grid_origin_y = int(50 + pan_offset[1])
    
    for i in range(used_grid[0]):
        for j in range(used_grid[1]):
            color = BLACK if grid[i, j] == 1 else RAYWHITE
            draw_rectangle(
                int(grid_origin_x + j * cell_size),  # Convert coordinates to integers
                int(grid_origin_y + i * cell_size),
                cell_size, cell_size, color
            )
            if show_boundaries:
                draw_rectangle_lines(
                    int(grid_origin_x + j * cell_size),
                    int(grid_origin_y + i * cell_size),
                    cell_size, cell_size, BLACK
                )

# Update used grid size dynamically
def update_used_grid(grid):
    non_zero_cells = np.nonzero(grid)
    if non_zero_cells[0].size > 0:
        return (np.max(non_zero_cells[0]) + 1, np.max(non_zero_cells[1]) + 1)
    return (10, 10)  # Default small grid if empty

# Initialize window
initialize_window(800, 600, "Interactive Cellular Automata")

while not window_should_close():
    begin_drawing()
    clear_background(RAYWHITE)
    
    # Handle zoom with mouse wheel
    zoom_level += get_mouse_wheel_move() * 0.1
    zoom_level = max(0.5, min(zoom_level, 3.0))  # Limit zoom between 0.5x and 3x

    # Handle panning with mouse drag
    if is_mouse_button_down(MOUSE_RIGHT_BUTTON):
        pan_offset[0] += get_mouse_delta().x
        pan_offset[1] += get_mouse_delta().y

    if on_first_page:
        draw_text_boxes()
        draw_button("Start", start_button_pos, button_size, True)

        active_key = input_order[current_input]
        if is_key_pressed(KEY_TAB):
            current_input = (current_input + 1) % len(input_order)

        # Text input handling
        key = get_key_pressed()
        if key == KEY_BACKSPACE:
            text_boxes[active_key]["text"] = text_boxes[active_key]["text"][:-1]
        elif key >= 32 and key <= 126:  # Handle standard characters
            text_boxes[active_key]["text"] += chr(key)

        # Start button action
        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON) and \
           start_button_pos[0] <= get_mouse_position().x <= start_button_pos[0] + button_size[0] and \
           start_button_pos[1] <= get_mouse_position().y <= start_button_pos[1] + button_size[1]:
            try:
                rule_num = int(text_boxes["rule_num"]["text"])
                steps = int(text_boxes["steps"]["text"])
                rows = int(text_boxes["rows"]["text"])
                columns = int(text_boxes["columns"]["text"])
                grid = np.zeros((rows, columns), dtype=int)  # Resize the grid based on input
                history.append(grid.copy())
                on_first_page = False
                on_input_page = True  # Go to input phase for initial state
                used_grid = (rows, columns)  # Set used grid size
            except ValueError:
                pass

    elif on_input_page:
        draw_active_grid(grid)

        # Click on grid cells to set initial pattern
        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
            mouse_position = get_mouse_position()
            mouse_x = mouse_position.x - 400 - pan_offset[0]
            mouse_y = mouse_position.y - 50 - pan_offset[1]

            # Calculate cell indices, adjusting for zoom and ensuring integers
            cell_x = int(mouse_x // (20 * zoom_level))
            cell_y = int(mouse_y // (20 * zoom_level))

            # Check bounds before toggling the cell state
            if 0 <= cell_x < grid.shape[1] and 0 <= cell_y < grid.shape[0]:
                grid[cell_y, cell_x] ^= 1  # Toggle cell state (on/off)

        # Draw "Start Simulation" button to begin iterations
        draw_button("Start Simulation", start_button_pos, button_size, True)

        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON) and \
           start_button_pos[0] <= get_mouse_position().x <= start_button_pos[0] + button_size[0] and \
           start_button_pos[1] <= get_mouse_position().y <= start_button_pos[1] + button_size[1]:
            if current_step < steps:  # Check if steps not exceeded
                print(f"Iteration: {current_step + 1}")  # Print the current iteration number
                grid = apply_rule(rule_num, grid)
                history.append(grid.copy())
                current_step += 1  # Increment step counter

        # Draw "Next" button
        draw_button("Next", next_button_pos, button_size, True)

        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON) and \
           next_button_pos[0] <= get_mouse_position().x <= next_button_pos[0] + button_size[0] and \
           next_button_pos[1] <= get_mouse_position().y <= next_button_pos[1] + button_size[1]:
            if current_step < steps:  # Check if steps not exceeded
                print(f"Iteration: {current_step + 1}")  # Print the current iteration number
                grid = apply_rule(rule_num, grid)
                history.append(grid.copy())
                current_step += 1  # Increment step counter

        # Draw "Undo" button
        draw_button("Undo", undo_button_pos, button_size, True)

        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON) and \
           undo_button_pos[0] <= get_mouse_position().x <= undo_button_pos[0] + button_size[0] and \
           undo_button_pos[1] <= get_mouse_position().y <= undo_button_pos[1] + button_size[1]:
            if len(history) > 1:  # Check if history has more than one entry
                history.pop()  # Remove last state
                grid = history[-1].copy()  # Restore previous state
                current_step -= 1  # Decrement step counter

        # Draw "Reset" button
        draw_button("Reset", reset_button_pos, button_size, True)

        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON) and \
           reset_button_pos[0] <= get_mouse_position().x <= reset_button_pos[0] + button_size[0] and \
           reset_button_pos[1] <= get_mouse_position().y <= reset_button_pos[1] + button_size[1]:
            # Reset to first page and print iteration number
            current_step = 0  # Reset step counter
            grid = np.zeros((used_grid[0], used_grid[1]), dtype=int)  # Clear grid
            history.clear()  # Clear history
            print("Reset to first page.")
            on_first_page = True  # Go back to input page

        # Draw "Toggle Boundaries" button
        draw_button("Toggle Boundaries", toggle_boundaries_button_pos, button_size, True)

        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON) and \
           toggle_boundaries_button_pos[0] <= get_mouse_position().x <= toggle_boundaries_button_pos[0] + button_size[0] and \
           toggle_boundaries_button_pos[1] <= get_mouse_position().y <= toggle_boundaries_button_pos[1] + button_size[1]:
            show_boundaries = not show_boundaries

        # Draw the iteration number on the screen
        draw_text(f"Iteration: {current_step}", 50, 350, 20, BLACK)

    end_drawing()

# Close the window
close_window()
