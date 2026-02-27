from search import *

class MissCannibalsVariant(Problem):
    def __init__(self, N1=4, N2=4, goal=(0, 0, False)):
        """Define goal state and initialize a problem"""
        initial = (N1, N2, True)
        self.N1 = N1
        self.N2 = N2
        super().__init__(initial, goal)

    def goal_test(self, state):
        return state == self.goal

    def result(self, state, action):
        m, c, onLeft = state
        num_m = action.count('M')
        num_c = action.count('C')

        if onLeft:
            # Boat moves right: people leave the left bank
            return (m - num_m, c - num_c, False)
        else:
            # Boat moves left: people return to the left bank
            return (m + num_m, c + num_c, True)

    def actions(self, state):
        m, c, onLeft = state
        possible_actions = ['M', 'C', 'MM', 'MC', 'CC', 'MMM', 'MMC', 'MCC', 'CCC']
        valid = []

        for action in possible_actions:
            num_m = action.count('M')
            num_c = action.count('C')

            if onLeft:
                # Taking people from left bank to right
                new_m_left  = m - num_m
                new_c_left  = c - num_c
            else:
                # Bringing people from right bank to left
                new_m_left  = m + num_m
                new_c_left  = c + num_c

            new_m_right = self.N1 - new_m_left
            new_c_right = self.N2 - new_c_left

            # Check bounds — no negative values, no exceeding totals
            if new_m_left < 0 or new_c_left < 0:
                continue
            if new_m_left > self.N1 or new_c_left > self.N2:
                continue

            # Check missionary safety on LEFT bank
            # Missionaries outnumbered only matters if there are missionaries present
            if new_m_left > 0 and new_c_left > new_m_left:
                continue

            # Check missionary safety on RIGHT bank
            if new_m_right > 0 and new_c_right > new_m_right:
                continue

            valid.append(action)

        return valid


if __name__ == '__main__':
    mc = MissCannibalsVariant(4, 4)

    # Test example while developing:
    # print(mc.actions((3, 3, True)))

    path = depth_first_graph_search(mc).solution()
    print(path)

    path = breadth_first_graph_search(mc).solution()
    print(path)