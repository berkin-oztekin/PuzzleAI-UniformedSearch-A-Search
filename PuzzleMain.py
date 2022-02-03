class Node:
    def __init__(self, data, level, fval):
        """ Initialize the node with the data, level of the node and the calculated fvalue """
        self.data = data
        self.level = level
        self.fval = fval

    def generate_child(self, tile_no):
        """ Generate child nodes from the given node by moving the blank space
            either in the four directions {up,down,left,right} """
        x_blanks, y_blanks = self.find_blanks(self.data, '_')
        """ val_list contains position values for moving the blank space in either of
            the 4 directions [up,down,left,right] respectively. 
        """
        children = []
        for (x, y) in zip(x_blanks, y_blanks):
            val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]

            for i in val_list:
                if i[0] >= 0 and i[0] < len(self.data) and i[1] >= 0 and i[1] < len(self.data):
                    if str(self.data[i[0]][i[1]]) == str(tile_no):
                        child = self.shuffle(self.data, x, y, i[0], i[1])
                        child_node = Node(child, self.level + 1, 0)
                        children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
        """ Move the blank space in the given direction and if the position value are out
            of limits the return None """
        temp_puz = []
        temp_puz = self.copy(puz)
        temp = temp_puz[x2][y2]
        temp_puz[x2][y2] = temp_puz[x1][y1]
        temp_puz[x1][y1] = temp
        return temp_puz

    def copy(self, root):
        """ Copy function to create a similar matrix of the given node"""
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp

    def find_blanks(self, puz, x):
        """ Specifically used to find the position of the blank space """
        x_blanks, y_blanks = [], []
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puz[i][j] == x:
                    x_blanks.append(i)
                    y_blanks.append(j)
        return x_blanks, y_blanks


class Puzzle:
    def __init__(self, size):
        """ Initialize the puzzle size by the specified size,open and closed lists to empty """
        self.n = size
        self.open = []
        self.closed = []

    def accept(self):
        """ Accepts the puzzle from the user """
        puz = []
        for i in range(0, self.n):
            temp = input().split(" ")
            puz.append(temp)
        return puz

    def f(self, start, goal, tile_id):
        """ Heuristic Function to calculate hueristic value f(x) = h(x) + g(x) """
        return self.h(start.data, goal, tile_id) + start.level

    def h(self, start, goal, tile_id):
        """ Calculates the different between the given puzzles """
        start_loc = []
        goal_loc = []
        for i in range(0, self.n):
            for j in range(0, self.n):
                if str(start[i][j]) == str(tile_id):
                    start_loc = [i, j]
                if str(goal[i][j]) == str(tile_id):
                    goal_loc = [i, j]

        x_diff = abs(goal_loc[0] - start_loc[0])
        y_diff = abs(goal_loc[1] - start_loc[1])
        if int(tile_id) == 1:
            h_val = x_diff * 2 + y_diff * 1
        if int(tile_id) == 2:
            h_val = x_diff * 1 + y_diff * 2
        if int(tile_id) == 3:
            h_val = x_diff * 3 + y_diff * 4
        return h_val

    def total_diff(self, start, goal):
        """ Calculates the different between the given puzzles """
        temp = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if start[i][j] != goal[i][j]:
                    temp += 1
        return temp

    def process(self):
        """ Accept Start and Goal Puzzle state"""
        print("Enter the start state matrix \n")
        start = self.accept()
        print("Enter the goal state matrix \n")
        goal = self.accept()

        choise = int(input("Press 1 for A* or press 2 for Uniform Cost Search"))

        if (choise == 1):

            start = Node(start, 0, 0)
            start.fval = self.f(start, goal, 1)
            """ Put the start node in the open list"""
            self.open.append(start)
            print("\n\n")
            counter = 0
            cur_level = start.level
            while cur_level <= 20:
                cur = self.open[0]
                cur_level = cur.level
                tile_id = (counter % 3) + 1

                print("")
                print("  | ")
                print("  | ")
                print(" \\\'/ \n")
                for i in cur.data:
                    for j in i:
                        print(j, end=" ")
                    print("")

                """ If the difference between current and goal node is 0 we have reached the goal node"""
                if (self.total_diff(cur.data, goal) == 0):
                    break

                children = cur.generate_child(tile_id)
                counter += 1

                if len(children) == 0:
                    continue

                for i in children:
                    i.fval = self.f(i, goal, tile_id)
                    self.open.append(i)
                self.closed.append(cur)
                del self.open[0]

                """ sort the opne list based on f value """
                self.open.sort(key=lambda x: x.fval, reverse=False)
        elif (choise == 2):
            start = Node(start, 0, 0)
            start.fval = self.f(start, goal, 1) - start.level
            """ Put the start node in the open list"""
            self.open.append(start)
            print("\n\n")
            counter = 0
            cur_level = start.level
            while cur_level <= 20:
                cur = self.open[0]
                cur_level = cur.level
                tile_id = (counter % 3) + 1

                print("")
                print("  | ")
                print("  | ")
                print(" \\\'/ \n")
                for i in cur.data:
                    for j in i:
                        print(j, end=" ")
                    print("")

                """ If the difference between current and goal node is 0 we have reached the goal node"""
                if (self.total_diff(cur.data, goal) == 0):
                    break

                children = cur.generate_child(tile_id)
                counter += 1

                if len(children) == 0:
                    continue

                for i in children:
                    i.fval = self.f(i, goal, tile_id) - start.level
                    self.open.append(i)
                self.closed.append(cur)
                del self.open[0]

                """ sort the open list based on f value """
                self.open.sort(key=lambda x: x.fval, reverse=False)
        else:
            print("Wrong input")


puz = Puzzle(3)
puz.process()  # _ _ _