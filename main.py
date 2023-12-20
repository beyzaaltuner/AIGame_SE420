import heapq
import itertools
import tkinter as tk
from tkinter import ttk
import time

#from PIL import Image, ImageDraw


class Node:
        _ids = itertools.count()
        _labels = itertools.cycle('ABCDEFGHIJKLMNOPQRSTUVWXYZ')  # Labels for nodes A, B, C, ...

        def __init__(self, app, row, col, value='_'):
            self.row = row
            self.col = col
            self.value = value
            self.neighbors = []
            self.id = next(self._ids)
            self.app = app  # Reference to the GridApp instance

        def add_neighbor(self, neighbor, cost):
            self.neighbors.append((neighbor, cost))

        def remove_neighbor(self, neighbor):
            self.neighbors = [(n, cost) for n, cost in self.neighbors if n != neighbor]

        def draw(self):
            x = self.col * 100 + 50  # x-coordinate for text (center of the cell)
            y = self.row * 100 + 50  # y-coordinate for text (center of the cell)
            self.app.canvas.create_text(x, y, text=self.value, font=("Arial", 20))

            
            
class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.config(bg="white")


    


        self.path_label = tk.Label(self.root, text="Path: ")
        self.path_label.pack(side=tk.BOTTOM, pady=5)

        self.cost_label = tk.Label(self.root, text="Cost: ")
        self.cost_label.pack(side=tk.BOTTOM, pady=5)


        self.horizontal_line_ids = []  # Store IDs of horizontal lines for removal later
        self.vertical_line_ids = []  # Store IDs of vertical lines for removal later
        self.robot_image = None  # Store ID of the robot image
        self.robot_text_image = None
        self.setup_gui()

    def update_path_label(self, path):
        self.path_label.config(text=f"Path: {path}")

    def update_cost_label(self, cost):
        self.cost_label.config(text=f"Cost: {cost}")

    def move_robot_along_path_button(self):
        source_label = self.source_room.get()
        goal_label = self.goal_room.get()

        if source_label in self.label_to_node and goal_label in self.label_to_node:
            source_node = self.label_to_node[source_label]
            goal_node = self.label_to_node[goal_label]

            algorithm_choice = self.search_algorithm_choice.get()

            if algorithm_choice == 'Uniform Cost Search':
                _, _, _, _, final_path = self.uniform_cost_search(source_node, goal_node)
            elif algorithm_choice == 'A* Search':
                _, _, _, _, final_path = self.a_star_search(source_node, goal_node)
            else:
                print("Invalid algorithm choice")
                return

            self.move_robot_along_path(final_path)







    def setup_gui(self):
        self.root.title("Wolly The Room Founder")
        self.root.geometry("800x800")
        self.root.resizable(False, False)
        

        robot_text_path = "wolly_text.png"  
        robot_text_image = tk.PhotoImage(file=robot_text_path)
        scaled_robot_text_image = robot_text_image.subsample(2, 2)
        robot_text_image_label = tk.Label(self.root, image=scaled_robot_text_image)
        robot_text_image_label.image = scaled_robot_text_image  # To prevent garbage collection
        robot_text_image_label.pack(side=tk.TOP, padx=0, pady=40)

        self.frame1 = tk.Frame(self.root, width=600, height=400, borderwidth=1, relief="solid")
        self.frame1.pack(side=tk.LEFT, padx=30, pady=30)

        self.canvas = tk.Canvas(self.frame1, width=300, height=300)
        self.canvas.pack()

 

        self.frame2 = tk.Frame(self.root, borderwidth=1, relief="solid")
        self.frame2.pack(side=tk.LEFT, padx=30, pady=30)
        # Draw vertical lines for columns
        for i in range(1, 3):
            for j in range(3):
                # Draw dashed vertical lines in gray
                line_id = self.canvas.create_line(i * 100, j * 100, i * 100, (j + 1) * 100, width=2, dash=(4, 4), fill="gray")
                self.vertical_line_ids.append(line_id)

        # Draw horizontal lines for rows
        for i in range(1, 3):
            for j in range(3):
                # Draw dashed horizontal lines in gray
                line_id = self.canvas.create_line(j * 100, i * 100, (j + 1) * 100, i * 100, width=2, dash=(4, 4), fill="gray")
                self.horizontal_line_ids.append(line_id)

        # Add text in each cell
        self.cell_text = [
            ['A', 'B', 'C'],
            ['D', 'E', 'F'],
            ['G', 'H', 'I']
        ]

        move_robot_button = tk.Button(self.root, text="Move Robot Along Path", command=self.move_robot_along_path_button)
        move_robot_button.pack(side=tk.TOP, pady=5)

        for i in range(3):
            for j in range(3):
                x = j * 100 + 50  # x-coordinate for text (center of the cell)
                y = i * 100 + 50  # y-coordinate for text (center of the cell)
                self.canvas.create_text(x, y, text=self.cell_text[i][j], font=("Arial", 20))


                

        # Dictionary to map labels to nodes
        self.label_to_node = {}
        self.create_nodes()
        for row in range(3):
            for col in range(3):
                self.label_to_node[self.cell_text[row][col]] = self.grid[row][col] 

        self.wall_labels_to_nodes = {}  # New dictionary for wall labels to nodes
        self.create_wall_mapping()  # Create mapping for wall labels to nodes         

        self.setup_widgets()

    def create_nodes(self):
        self.grid = [[Node(self, row, col) for col in range(3)] for row in range(3)]

        # Connect neighbors for each node
        for row in range(3):
            for col in range(3):
                current_node = self.grid[row][col]

                # Connect with right neighbor
                if col < 2:
                    current_node.add_neighbor(self.grid[row][col + 1], 2)

                # Connect with left neighbor
                if col > 0:
                    current_node.add_neighbor(self.grid[row][col - 1], 2)

                # Connect with bottom neighbor
                if row < 2:
                    current_node.add_neighbor(self.grid[row + 1][col], 1)

                # Connect with top neighbor
                if row > 0:
                    current_node.add_neighbor(self.grid[row - 1][col], 1)

    def create_wall_mapping(self):
        walls = ['AB', 'AD', 'BC', 'BE', 'CF', 'DE', 'DG', 'EH', 'EF', 'FI', 'GH', 'HI']

        for wall_label in walls:
            node1, node2 = self.get_nodes_from_wall_label(wall_label)
            if node1 and node2:
                self.wall_labels_to_nodes[wall_label] = (node1, node2)

    def get_nodes_from_wall_label(self, wall_label):
        if wall_label[0] in self.label_to_node and wall_label[1] in self.label_to_node:
            return self.label_to_node[wall_label[0]], self.label_to_node[wall_label[1]]
        else:
            return None, None                            

    def draw_nodes(self):
        for row in self.grid:
            for node in row:
                node.draw()              

    def setup_widgets(self):
        source_label = tk.Label(self.frame2, text="Please choose your source room:")
        source_label.grid(row=0, column=0, padx=5, pady=5)

        rooms = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

        self.source_room = tk.StringVar()
        source_room_dropdown = ttk.Combobox(self.frame2, textvariable=self.source_room, values=rooms)
        source_room_dropdown.grid(row=0, column=1, padx=5, pady=5)

        goal_label = tk.Label(self.frame2, text="Please choose your goal room:")
        goal_label.grid(row=1, column=0, padx=5, pady=5)

        self.goal_room = tk.StringVar()
        goal_room_dropdown = ttk.Combobox(self.frame2, textvariable=self.goal_room, values=rooms)
        goal_room_dropdown.grid(row=1, column=1, padx=5, pady=5)

        wall_label = tk.Label(self.frame2, text="Please select your wall choices:")
        wall_label.grid(row=2, columnspan=2, padx=5, pady=5)

        check_buttons_frame = tk.Frame(self.frame2, borderwidth=1, relief="solid")
        check_buttons_frame.grid(row=3, columnspan=2, padx=5, pady=5)

        walls = ['AB', 'AD', 'BC', 'BE', 'CF', 'DE', 'DG', 'EH', 'EF', 'FI', 'GH', 'HI']

        # Store line IDs for walls
        self.wall_line_ids = {
            'AB': 1,
            'AD': 7,
            'BC': 4,
            'BE': 8,
            'CF': 9,
            'DE': 2,
            'DG': 10,
            'EH': 11,
            'EF': 5,
            'FI': 12,
            'GH': 3,
            'HI': 6
        }

        #Create Checkbuttons using grid layout inside the check_buttons_frame
        for i, value in enumerate(walls):
            row_val = i // 4
            col_val = i % 4
            v = tk.IntVar()
            check = tk.Checkbutton(check_buttons_frame, text=value, variable=v,
                                   command=lambda val=value: self.get_wall_from_user(val))
            check.grid(row=row_val, column=col_val, padx=5, pady=5)

        search_algorithm_label = tk.Label(self.frame2, text="Please choose a searching algorithm:")
        search_algorithm_label.grid(row=4, column=0, padx=5, pady=5)

        search_algorithms = ['Uniform Cost Search', 'A* Search']
        self.search_algorithm_choice = tk.StringVar()
        search_algorithm_dropdown = ttk.Combobox(self.frame2, textvariable=self.search_algorithm_choice,
                                              values=search_algorithms)
        search_algorithm_dropdown.grid(row=4, column=1, padx=5, pady=5)

        # Button to start searching
        button = tk.Button(self.frame2, text="Start Searching", command=self.start_searching)
        button.grid(row=5, columnspan=2, pady=5)

        robot_image_path = "wolly.png"    # Replace with the actual path to your robot image
 
        original_robot_image = tk.PhotoImage(file=robot_image_path)
        
        # Adjust the subsample factor to control the size of the image
        subsample_factor = 6  # Change this value to adjust the size
        smaller_robot_image = original_robot_image.subsample(subsample_factor, subsample_factor)

        self.robot_image = smaller_robot_image
        self.robot_image_id = self.canvas.create_image(0, 0, anchor=tk.CENTER, image=self.robot_image)
        # Hide the robot image initially
        self.canvas.itemconfigure(self.robot_image_id, state=tk.HIDDEN)

    def move_robot(self, row, col, show=True):
        # Move the robot image to the specified row and column
        x = col * 100 + 50
        y = row * 100 + 50

        if self.robot_image:
            self.canvas.coords(self.robot_image_id, x, y)
            if show:
                self.canvas.itemconfigure(self.robot_image_id, state=tk.NORMAL)
            else:
                self.canvas.itemconfigure(self.robot_image_id, state=tk.HIDDEN)

            # Update the window to make the movement visible
            self.root.update()
            # Introduce a delay (you can adjust the time in milliseconds)
            self.root.after(500)  # Adjust the time delay as needed




    def move_robot_along_path(self, path):
        # Move the robot along the final path
        for row, col in path:
            self.move_robot(row, col, show=True)

        time.sleep(5)

        self.move_robot(row, col, show=False)


    def get_wall_from_user(self, wall_label):
        # Check if the wall is selected or deselected
        if wall_label in self.wall_line_ids:
            line_id = self.wall_line_ids[wall_label]

            # Convert the corresponding line to a solid black line
            self.convert_to_solid_black(line_id)

            # Add the wall to the dictionary
            node1, node2 = self.wall_labels_to_nodes.get(wall_label, (None, None))
            if node1 and node2:
                self.add_wall_between_nodes(node1, node2)

        else:
            print(f"Invalid wall label: {wall_label}")

    def add_wall_between_nodes(self, node1, node2):
        # Remove neighbors to create a wall
        node1.remove_neighbor(node2)
        node2.remove_neighbor(node1)
        print("Wall added successfully!")        

    def convert_to_solid_black(self, line_id):
        if 1 <= line_id <= 6:  # Vertical lines
            self.convert_to_solid_black_vertical(line_id)
        elif 7 <= line_id <= 12:  # Horizontal lines
            self.convert_to_solid_black_horizontal(line_id)
        else:
            print("Invalid line_id.")


    def convert_to_solid_black_horizontal(self, line_id):
        self.canvas.itemconfigure(line_id, dash=(), fill="black")    

    def convert_to_solid_black_vertical(self, line_id):
        self.canvas.itemconfigure(line_id, dash=(), fill="black")


    def uniform_cost_search(self, start, goal, max_expanded_nodes=10):
        heap = [(0, start.id, start, [])]  # Priority queue to store (cost, id, node, path) tuples
        visited = set()

        while heap and len(visited) < max_expanded_nodes:
            current_cost, _, current_node, current_path = heapq.heappop(heap)

            if current_node in visited:
                continue

            visited.add(current_node)

            current_path = current_path + [(current_node.row, current_node.col)]

            print(f"Expanded Node: ({current_node.row}, {current_node.col}), Cost: {current_cost}")

            # Move the robot for all expanded nodes
            self.move_robot(current_node.row, current_node.col, show=True)

            if current_node == goal:
                self.root.after(5000)
                print(f"Goal reached! Final Path: {current_path}, Cost: {current_cost}")
                self.move_robot_along_path(current_path)
                return

            for neighbor, cost in current_node.neighbors:
                heapq.heappush(heap, (current_cost + cost, neighbor.id, neighbor, current_path))


            self.update_path_label(current_path)
            self.update_cost_label(current_cost)


    # Calculate Manhattan distance heuristic
    def manhattan_distance(self,node, goal):
        return abs(node.row - goal.row) + abs(node.col - goal.col)

    # A* Search Algorithm
    def a_star_search(self, start, goal, max_expanded_nodes=10):
        heap = [(0, 0, start.id, start, [])]  # Priority queue to store (f, g, id, node, path) tuples
        visited = set()

        # Set to store walls
        walls = set()

        while heap and len(visited) < max_expanded_nodes:
            _, g, _, current_node, current_path = heapq.heappop(heap)

            if current_node in visited:
                continue

            visited.add(current_node)

            current_path = current_path + [(current_node.row, current_node.col)]

            h = self.manhattan_distance(current_node, goal)
            print(f"Expanded Node: ({current_node.row}, {current_node.col}), Cost: {g}, Heuristic: {h}")

            # Move the robot for all expanded nodes
            self.move_robot(current_node.row, current_node.col, show=True)

            if current_node == goal:
                self.root.after(5000)
                print(f"Goal reached! Final Path: {current_path}, Cost: {g}")
                self.move_robot_along_path(current_path)
                return

            for neighbor, cost in current_node.neighbors:
                # Check if there is a wall between the current_node and neighbor
                if (current_node.id, neighbor.id) in walls or (neighbor.id, current_node.id) in walls:
                    continue

                h_neighbor = self.manhattan_distance(neighbor, goal)
                f = g + cost + h_neighbor
                heapq.heappush(heap, (f, g + cost, neighbor.id, neighbor, current_path))

            self.update_path_label(current_path)
            self.update_cost_label(f)
          
    


    def reset_labels(self):
        self.update_path_label("")
        self.update_cost_label("")


    def start_searching(self):
        source_label = self.source_room.get()
        goal_label = self.goal_room.get()

        self.reset_labels()


        source_label = self.source_room.get()
        goal_label = self.goal_room.get()




        if source_label in self.label_to_node and goal_label in self.label_to_node:
            source_node = self.label_to_node[source_label]
            goal_node = self.label_to_node[goal_label]

            algorithm_choice = self.search_algorithm_choice.get()

            if algorithm_choice == 'Uniform Cost Search':
                self.uniform_cost_search(source_node, goal_node)
            elif algorithm_choice == 'A* Search':
                self.a_star_search(source_node, goal_node)
            else:
                print("Invalid algorithm choice")
        else:
            print("Invalid source or goal labels. Please choose valid labels.")


    # ... (other methods and definitions)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")
    root.resizable(False, False)
    app = GridApp(root)
    app.draw_nodes() 
    root.mainloop()
       