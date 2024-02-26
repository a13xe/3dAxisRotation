import numpy as np
import tkinter as tk
from tkinter import ttk

###############################################################
# ImportError: No module named 'Tkinter' [duplicate] - on LINUX
###############################################################
# import sys
# if sys.version_info[0] == 3:
#     import tkinter as tk
#     from tkinter import ttk
# else:
#     import Tkinter as tk
#     from tkinter import ttk

# Pyramid vertices
def generate_pyramid_points(base_center, base_size, height):
    half_size = base_size / 2
    points = [
        np.array([base_center[0] - half_size, base_center[1] - half_size, base_center[2]]),
        np.array([base_center[0] + half_size, base_center[1] - half_size, base_center[2]]),
        np.array([base_center[0] + half_size, base_center[1] + half_size, base_center[2]]),
        np.array([base_center[0] - half_size, base_center[1] + half_size, base_center[2]])
    ]
    points.append(np.array([base_center[0], base_center[1], base_center[2] + height]))
    return points


# Rotate points around an axis
def rotate_points(points, axis_p1, axis_p2, angle):
    axis = np.array(axis_p2) - np.array(axis_p1)
    axis = axis / np.linalg.norm(axis)
    angle = np.radians(angle)
    # Matrix shenanigans
    rotation_matrix = np.array([
        [np.cos(angle) + axis[0]**2 * (1 - np.cos(angle)), axis[0] * axis[1] * (1 - np.cos(angle)) - axis[2] * np.sin(angle), axis[0] * axis[2] * (1 - np.cos(angle)) + axis[1] * np.sin(angle)],
        [axis[1] * axis[0] * (1 - np.cos(angle)) + axis[2] * np.sin(angle), np.cos(angle) + axis[1]**2 * (1 - np.cos(angle)), axis[1] * axis[2] * (1 - np.cos(angle)) - axis[0] * np.sin(angle)],
        [axis[2] * axis[0] * (1 - np.cos(angle)) - axis[1] * np.sin(angle), axis[2] * axis[1] * (1 - np.cos(angle)) + axis[0] * np.sin(angle), np.cos(angle) + axis[2]**2 * (1 - np.cos(angle))]
    ])
    rotated_points = [np.dot(rotation_matrix, point - axis_p1) + axis_p1 for point in points]
    return rotated_points


# Draw pyramid
def draw_pyramid(canvas, points):
    canvas.delete("all")
    base_points = points[:4]
    for i in range(len(base_points)):
        next_i = (i + 1) % len(base_points)
        canvas.create_line(base_points[i][0], base_points[i][1], base_points[next_i][0], base_points[next_i][1], fill='black')
    top_point = points[-1]
    for base_point in base_points:
        canvas.create_line(base_point[0], base_point[1], top_point[0], top_point[1], fill='black')


def main():
    root = tk.Tk()
    root.title("3D Object Rotation with Custom Axis")
    # Entry fields for axis coordinates
    axis_entries = []
    for i, label in enumerate(["X1", "Y1", "Z1", "X2", "Y2", "Z2"]):
        ttk.Label(root, text=label).grid(row=i, column=0)
        entry = ttk.Entry(root)
        entry.grid(row=i, column=1)
        axis_entries.append(entry)
    # Default values for axis points
    default_values = [-100, -100, 0, 50, 200, 0]
    for entry, value in zip(axis_entries, default_values):
        entry.insert(0, str(value))
    # Slider
    angle_slider = ttk.Scale(root, from_=0, to=360, orient='horizontal')
    angle_slider.grid(row=6, columnspan=2, sticky='ew')
    # Canvas
    canvas_width=400
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_width, bg="white")
    canvas.grid(row=0, column=2, rowspan=7)

    base_2d_center = canvas_width/2
    base_center = [base_2d_center, base_2d_center, 0]
    base_size = 100
    height = 120
    points = generate_pyramid_points(base_center, base_size, height)
    
    def update_canvas(event=None):
        try:
            base_2d_center = 200
            # Reading the rotation axis coordinates with an offset to center the pyramid base
            axis_p1 = np.array([float(axis_entries[0].get()) + base_2d_center, float(axis_entries[1].get()) + base_2d_center, float(axis_entries[2].get())])
            axis_p2 = np.array([float(axis_entries[3].get()) + base_2d_center, float(axis_entries[4].get()) + base_2d_center, float(axis_entries[5].get())])
            angle = angle_slider.get()
            # Rotating the pyramid vertices
            rotated_points = rotate_points(points, axis_p1, axis_p2, angle)
            draw_pyramid(canvas, rotated_points)
            # Simple perspective: decreasing visibility with increasing Z
            z_factor = 1 - 0.1 * abs(axis_p1[2] + axis_p2[2])
            z_factor = max(min(z_factor, 1), 0)
            canvas.create_line(axis_p1[0], axis_p1[1], axis_p2[0], axis_p2[1], fill='red', dash=(4, 2), width=z_factor)
        except ValueError:
            pass
            
    # Binding canvas update to slider changes and input fields
    angle_slider.bind("<Motion>", update_canvas)
    angle_slider.bind("<ButtonRelease-1>", update_canvas)
    for entry in axis_entries:
        entry.bind("<KeyRelease>", update_canvas)
    update_canvas()
    root.mainloop()


if __name__ == "__main__":
    main()
