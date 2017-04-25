### UTILITY STUFF

from copy import deepcopy

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
diag_units = [[rows[i] + cols[i] for i in range(9)], [rows[i] + cols[8-i] for i in range(9)]]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    # print(box + ':' + values[box] + '-->' + value)
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(a, b):
    return [s+t for s in a for t in b]

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    grid_dict = dict()
    # use the row and col indices to find the right key for the right value
    for ri in range(9):
        for ci in range(9):
            cell_val = grid[(9 * ri) + ci] if grid[(9 * ri) + ci] != '.' else '123456789'
            grid_dict[rows[ri] + cols[ci]] = cell_val
    assignments.append(grid_dict)
    return grid_dict

#Some testing STUFF
before_naked_twins_1 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
                        'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
                        'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
                        'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
                        'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
                        'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
                        'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
                        'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
                        'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
                        'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
                        'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}

## ACTUAL SOLVING STUFF
def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    single_val_boxes = [key for key in values if len(values[key]) == 1]
    for box in single_val_boxes:
        peer_list = peers[box]
        for peer in peer_list:
            new_peer_val = values[peer].replace(values[box], '')
            values = assign_value(values, peer, new_peer_val)
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        possibilities = []
        for box in unit:
            possibilities += values[box]
        choices = [val for val in possibilities if possibilities.count(val) == 1]
        for box in unit:
            for value in values[box]:
                if value in choices:
                    values = assign_value(values, box, value)
    return values

def naked_twins(values):
    """
    Identify any naked twins (boxes in the same unit which contain the same two
    values) and remove the values from peer boxes.

    Input: Sudoku in directory form
    Output: Resulting Sudoku in directory form.
    """
    # Get the twins on the board
    all_twins = []
    for unit in unitlist:
        box_values = [values[box] for box in unit]
        twins = []
        for box in unit:
            if len(values[box]) == 2 and box_values.count(values[box]) == 2:
                twins.append(box)
            # else:
            #     print("not a twin: " + str(unit) + "..." + box + "..." + values[box])
        if twins != []:
            all_twins.append([unit,twins])
            # print("all twins: "+str(all_twins))

    # Eliminate values from other boxes as needed
    for twin_unit_pair in all_twins:
        unit = twin_unit_pair[0]
        twin_val = values[twin_unit_pair[1][0]]

        # make sure that a twin
        if len(twin_val) != 2:
            continue
        twin_pair = twin_unit_pair[1]
        for box in unit:
            if box in twin_pair:
                continue
            new_val = values[box].replace(twin_val[0],'').replace(twin_val[1],'')
            # if values[box] != new_val:
            #     print(str(box)+":"+str(values[box])+"-->"+str(new_val))
            values = assign_value(values, box, new_val)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        elim_values = eliminate(values)
        if len([box for box in values.keys() if len(values[box]) == 0]):
            print("Reduction error at elim stage")
            display(assignments[-1])
            display(values)
            return False

        chosen_values = only_choice(elim_values)
        if len([box for box in values.keys() if len(values[box]) == 0]):
            print("Reduction error at choice stage")
            display(values)
            return False

        no_twins = naked_twins(chosen_values)
        if len([box for box in values.keys() if len(values[box]) == 0]):
            print("Reduction error at twins stage")
            display(values)
            return False

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    reduced = reduce_puzzle(values)
    if not reduced:
        print("Reduction error?")
        return False  # Something went wrong

    # Check to see if it's solved
    solved = True
    for box in reduced:
        if len(reduced[box]) != 1:
            solved = False
    if solved:
        return reduced

    try:
        min_box = smallest_boxes(reduced)[0]
    except IndexError as e:
        # print(display(reduced))
        raise
    for value in reduced[min_box]:  # Branch the search for each value in the smallest box
        split_sudoku = deepcopy(reduced)  # Create a new board to search
        split_sudoku[min_box] = value  # alter it to reflect the choice we're making
        success = search(split_sudoku)
        if success:
            return success

def smallest_boxes(values):
    """
    Returns a list of boxes which have the fewest possibilities.
    """
    min_poss_count = min([len(poss) for poss in values.values() if len(poss) > 1])
    min_boxes = []
    for box in values:
        if len(values[box]) == min_poss_count:
            min_boxes.append(box)
    return min_boxes

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    result = search(grid_values(grid))
    # result = eliminate(grid_values(grid))
    return result

if __name__ == '__main__':
    test_sudoku_grid = '1......2.....9.5...............8...4.........9..7123...........3....4.....936.4..'
    # test_res = solve(test_sudoku_grid)
    test_res = solve(test_sudoku_grid)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
