#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    progress-tracker.py add_skill <skill>..
    progress-tracker.py view_skills
    progress-tracker.py studied <skill>
    progress-tracker.py not_studied <skill>
    progress-tracker.py view_studied
    progress-tracker.py view_notstudied
    progress-tracker.py (-i | --interactive)
    progress-tracker.py (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.

"""

import sys
import cmd
from docopt import docopt, DocoptExit

All_skills = []
skills = {'Not studied': [], 'Studied': []}


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive(cmd.Cmd):
    intro = 'Welcome to Progress Tracker!' \
            + ' (type help for a list of commands.)'
    prompt = '(Progress Tracker) '
    file = None

    @docopt_cmd
    def do_add_skill(self, arg):
        """Usage: add_skill <skill>..."""
        skill = " ".join(arg['<skill>'])
        skills=skill.split("|")
        for skill_item in skills:
            if isinstance(skill_item, str):
                All_skills.append(skill_item)
                print('{} added'.format(skill_item))

    @docopt_cmd
    def do_view_skills(self, arg):
        """Usage: view_skills"""
        print(All_skills)

    @docopt_cmd
    def do_studied(self, arg):
        """Usage: studied <skill>"""
        skill = arg['<skill>']
        if skill not in All_skills:
            print('Add skill first')
        else:
            skills['Studied'].append(skill)
            print('Added to studied list')

    @docopt_cmd
    def do_not_studied(self, arg):
        """Usage: not_studied <skill>"""
        skill = arg['<skill>']
        if skill not in All_skills:
            print('Add skill first')
        else:
            skills['Not studied'].append(skill)

    @docopt_cmd
    def do_view_studied(self, arg):
        """Usage: view_studied"""
        print(skills['Studied'])

    @docopt_cmd
    def do_view_notstudied(self, arg):
        """Usage: view_studied"""
        print(skills['Not studied'])

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

    def do_view_study_progess(self, arg):
        """Usage: view_study_progress"""
        total_skills = All_skills
        unfinished = skills.get('Not studied')
        finished = skills.get('Studied')
        print(
            'Total Skills: {}\nFinished Skills: {}\nUnfinished Skills: {}'.format(  # NOQA
                len(total_skills), len(finished), len(unfinished)
        ))


opt = docopt(__doc__, sys.argv[1:])


if opt['--interactive']:
    MyInteractive().cmdloop()

print(opt)
