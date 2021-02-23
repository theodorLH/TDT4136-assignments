#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import itertools

class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        # Deliverable 3.:
        # The number of times your BACKTRACK function was called, and the number of times your BACKTRACK
        # function returned failure, for each of the four boards shown above
        self.backtrack_calls = 0
        self.backtrack_fails = 0

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [ (i, j) for i in self.constraints for j in self.constraints[i] ]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [ (i, var) for i in self.constraints[var] ]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """
        # TODO: IMPLEMENT THIS
        # pseudokode s.215 i boken
        self.backtrack_calls += 1
        # hvis lengden til element eller hver variabel i assignment har lister av lengde 1,
        # så er assignment complete
        complete = True
        for i in assignment:
            if len(assignment[i]) > 1:
                complete = False
        if complete:
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in assignment[var]:
            new_assignment = copy.deepcopy(assignment)
            new_assignment[var] = [value]
            neighbouring_arcs = self.get_all_neighboring_arcs(var)
            if self.inference(new_assignment, neighbouring_arcs):
                # assignment.append(inferences)
                result = self.backtrack(new_assignment)
                if result:
                    return result
            # assignment.pop([value])    ikke nødvendig pga deepcopy
            # assignment.pop(self.inference(var, value))
        self.backtrack_fails += 1
        return False

# -----------------------------------------------------------------------------


    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """

        # ettersom vi kan få flere variabler som ikke er bestemte, så legges de i en liste
        undecided = []

        for x in assignment.keys(): # keys() When looping through dictionaries
            if len(assignment[x]) > 1:
                undecided.append(x)

        # velger å returnere den minste ubestemte variabelen fra listen, MRV
        # varibelen med færre "legal" values
        return min(undecided, key = lambda key: len(assignment[key]))

# -----------------------------------------------------------------------------

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """

        while len(queue) > 0: # queue[0] != ''
            x, y = queue.pop()
            if self.revise(assignment, x, y):
                if len(assignment[x]) == 0:
                    return False
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                for z1, z2 in self.get_all_neighboring_arcs(x): # det er nabo-Arkene vi ønsker
                    if z1 != y:
                        queue.append((z1, x)) # legger til tuppel
        return True

# -----------------------------------------------------------------------------

    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """

        revised = False
        not_satisfied = []
        for x in assignment[i]:  # her sjekker vi riktig arc fra assignment/current partial assignment
            satisfy = False
            for y in assignment[j]:
                # if not x in self.add_constraint_one_way(i,j,filter_function): #x fins innenfor i som ikke tilfredstiller constrainten mellom i og j
                # vil kanskje ikke adde en constraint, men bare sjekke at parene oppfyller denne constrainten:
                if (x, y) in self.constraints[i][j]:
                    satisfy = True
                    break
                    # vil fjerne denne verdien fra i sine legal_values
            if not satisfy:
                not_satisfied.append(x)
                revised = True

        for x in not_satisfied:
            assignment[i].remove(x)

        return revised


# -----------------------------------------------------------------------------

def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = [ 'WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T' ]
    edges = { 'SA': [ 'WA', 'NT', 'Q', 'NSW', 'V' ], 'NT': [ 'WA', 'Q' ], 'NSW': [ 'Q', 'V' ] }
    colors = [ 'red', 'green', 'blue' ]
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp

def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    board = map(lambda x: x.strip(), open(filename, 'r'))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), map(str, range(1, 10)))
            else:
                csp.add_variable('%d-%d' % (row, col), [ board[row][col] ])

    for row in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for col in range(9) ])
    for col in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for row in range(9) ])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp

def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print solution['%d-%d' % (row, col)][0],
            if col == 2 or col == 5:
                print'|',
        print
        if row == 2 or row == 5:
            print '------+-------+------'


# csp for hver av de 4 sudoku oppgavene
sudoku1 = create_sudoku_csp('easy.txt')
sudoku2 = create_sudoku_csp('medium.txt')
sudoku3 = create_sudoku_csp('hard.txt')
sudoku4 = create_sudoku_csp('veryhard.txt')

# søk for hver av brettene
search1 = sudoku1.backtracking_search()
search2 = sudoku2.backtracking_search()
search3 = sudoku3.backtracking_search()
search4 = sudoku4.backtracking_search()

# printe ut løsningen
print "Easy board solution:\n"
print_sudoku_solution(search1)
print "\n\nMedium board solution:\n"
print_sudoku_solution(search2)
print "\n\nHard board solution:\n"
print_sudoku_solution(search3)
print "\n\nVery hard board solution:\n"
print_sudoku_solution(search4)

# printe ut antall ganger BACKTRACK funksjonen ble kalt og feilet
print "\n\n"
print 'Antall Backtracks:'
print 'Easy board: ' + str(sudoku1.backtrack_calls) + ', medium board: ' + str(sudoku2.backtrack_calls) + ', hard board: ' + str(sudoku3.backtrack_calls) + ', very hard board: ' + str(sudoku4.backtrack_calls)
print 'Antall Failures:'
print 'Easy board: ' + str(sudoku1.backtrack_fails) + ', medium board: ' + str(sudoku2.backtrack_fails) + ', hard board: ' + str(sudoku3.backtrack_fails) + ', very hard board: ' + str(sudoku4.backtrack_fails)
