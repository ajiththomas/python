//pip install pyautogui


import pyautogui

def draw_circle(radius=50, center_x=400, center_y=300):
    """
    Draw a circle in Paint using pyautogui.
    
    Parameters:
    - radius: Radius of the circle to be drawn.
    - center_x: X-coordinate of the circle's center.
    - center_y: Y-coordinate of the circle's center.
    """
    pyautogui.moveTo(center_x + radius, center_y)
    pyautogui.mouseDown()

    for i in range(361):
        x = center_x + radius * math.cos(math.radians(i))
        y = center_y + radius * math.sin(math.radians(i))
        pyautogui.moveTo(x, y)
    
    pyautogui.mouseUp()

# Import necessary library
import math

def main():
    file_name = os.path.join("C:\\temp", f"mspaint_{get_current_datetime()}.png")
    create_temp_directory()
    open_paint()
    draw_circle()
    time.sleep(10)  # Wait for drawing to complete
    save_as_option(file_name)
    time.sleep(2)

if __name__ == "__main__":
    main()
