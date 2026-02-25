"""
Utility functions for UI formatting
"""
import os


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Print a formatted header"""
    width = 50
    print("\n" + "="*width)
    print(title.center(width))
    print("="*width)


def print_separator():
    """Print a separator line"""
    print("-"*50)
