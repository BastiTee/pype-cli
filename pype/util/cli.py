# -*- coding: utf-8 -*-
"""CLI-functions for better user experience and consistency."""


def ask_yes_or_no(question, default='yes'):
    """Ask user a yes/no question and return their answer."""
    valid = {'yes': True, 'y': True, 'ye': True,
             'no': False, 'n': False}
    if default is None:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError('invalid default answer: {}'.format(default))

    while True:
        print(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print('Please respond with "yes" or "no" (or "y" or "n").')


def ask_for_text(question):
    """Ask user for free text input and return their answer."""
    print(question)
    return input('> ')
