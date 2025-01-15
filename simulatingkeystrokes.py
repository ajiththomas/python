import os
import datetime
import subprocess
import time
import turtle

def get_current_datetime():
    """
    Get the current date and time in the format: 'ddmmyy_HHMMSS'
    """
    return datetime.datetime.now().strftime("%d%m%y_%H%M%S")


def create_temp_directory(folder_path="C:\\temp"):
    """
    Create a temporary directory if it doesn't exist.
    """
    try:
        os.makedirs(folder_path, exist_ok=True)
        print("Folder created successfully or already exists.")
    except Exception as e:
        print(f"Error creating folder: {e}")


def open_paint():
    """
    Open Microsoft Paint application.
    """
    subprocess.Popen(["mspaint.exe"])
    time.sleep(3)  # Wait for Paint to open


def save_as_option(file_name):
    """
    Simulate the process of saving the file in Paint.
    In a real scenario, you might need to use an automation tool like PyAutoGUI.
    """
    print(f"Simulating typing the file name: {file_name}")




def draw_circle():
    # Set up the turtle environment
    turtle.speed(1)  # Set the drawing speed
    turtle.penup()   # Don't draw when moving to the starting position
    turtle.goto(0, -200)  # Move to starting position
    turtle.pendown()  # Start drawing

    # Draw multiple circles with increasing radius
    for radius in range(50, 300, 50):  # Draw circles with radius 50, 100, 150, 200, 250
        turtle.circle(radius)  # Draw a circle with the specified radius
        turtle.penup()  # Lift the pen to move without drawing
        turtle.goto(0, -200)  # Return to the starting position
        turtle.pendown()  # Start drawing again

    turtle.done()  # Finish the drawing



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


