"""Optimize Grapper"""
import argparse

import os
import sys


from classes.bootstrap import Bootstrap


class Optimizo:
    def __init__(self):
        self.process_commands()
        
    def process_commands(self):
        # Create the parser
        my_parser = argparse.ArgumentParser(prog="optimizo", 
                                            description='Optimizo its an tool that allows to set up instructions and run them later. In the mean you will have to run them manually',
                                            epilog='Happy Automating and Optimizing!')

        # Add the arguments
        my_parser.add_argument('-c',
                            '--generate',
                            action='store_true',
                            help='Generate optimizo config file. If you dont specify directory(using -w) it will generate in the current directory.')


        my_parser.add_argument('-g',
                            '--group',
                            metavar='group',
                            type=str,
                            help='Group to work with. If group doesnt exist it will be created.')

        my_parser.add_argument('-r',
                            '--run',
                            metavar='run',
                            type=str,
                            help='Run instructions under a specific group.')

        my_parser.add_argument('-a',
                            '--add',
                            action='store_true',
                            help='Add an instruction')


        my_parser.add_argument('-w',
                            '--directory',
                            action='store',
                            help='Working directory. Directory with your project')


        # Execute the parse_args() method
        args = my_parser.parse_args()
        bootstrap = Bootstrap() 


        try:
            if (args.generate):
                bootstrap.generate(args.directory)
            
            if (args.group and args.add):
                bootstrap.add_instruction_interactive(args.group, args.directory)
                
            if (args.run):
                bootstrap.run_instruction(args.run, args.directory)

        except KeyboardInterrupt:
            print("\n\n[0] Goodbye, Exiting!")
    



if __name__ == '__main__':
    optimizo = Optimizo()