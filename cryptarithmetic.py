import streamlit as st
from simpleai.search import CspProblem, backtrack

# Define the app title and layout
st.title('Cryptarithmetic Solver')
st.sidebar.header('User Input')

# Get user input
expression = st.sidebar.text_input('Enter the cryptarithmetic expression:', 'TO + GO = OUT')

# Extract letters from the input expression
def extract_unique_letters(expression):
    return set(filter(str.isalpha, expression))

# Convert word to number using a given assignment
def word_to_number(word, assignment):
    return int(''.join(str(assignment[letter]) for letter in word))

# Constraint function
def cryptarithmetic_constraint(variables, values):
    assignment = dict(zip(variables, values))
    left_sum = sum(word_to_number(word, assignment) for word in left_words)
    return left_sum == word_to_number(right_word, assignment)

# Solver Function
def solve_cryptarithmetic(expression):
    global left_words, right_word
    expression = expression.replace(" ", "")  # Remove any whitespace
    left, right = expression.split('=')
    left_words = left.split('+')
    right_word = right.strip()
    letters = list(extract_unique_letters(expression))

    domains = {letter: list(range(10)) for letter in letters}
    for word in left_words + [right_word]:
        domains[word[0]] = list(range(1, 10))

    constraints = [(letters, cryptarithmetic_constraint)]
    problem = CspProblem(letters, domains, constraints)
    solution = backtrack(problem)

    return solution

# Validate input and solve
if expression:
    try:
        # Validate input format
        if '=' not in expression or '+' not in expression:
            st.error('Invalid expression format! Please enter in the format: WORD + WORD = WORD')
        else:
            # Solve and display result
            solution = solve_cryptarithmetic(expression)
            if solution:
                st.success('Solution found!')
                st.write(solution)
                st.write('---')
                st.write('Here’s how the equation looks with the found solution:')
                left_expression = ' + '.join([f"{word_to_number(word, solution)}" for word in left_words])
                right_expression = f"{word_to_number(right_word, solution)}"
                st.write(f"{left_expression} = {right_expression}")
            else:
                st.error('No solution found!')
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Add some styling
st.markdown(
    """
    <style>
        .reportview-container {
            background-color: #f0f0f5;
        }
        .big-font {
            font-size:20px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
