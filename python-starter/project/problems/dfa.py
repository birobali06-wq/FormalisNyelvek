from project.problem import Problem
import argparse

class DFAProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--check',
            help='The word or words to check'
        )

    def is_chosen_problem(self, args):
        return args.check is not None

    def run(self, args):
        input_file = args.input
        output_file = args.output
        words = args.check.split(',')

        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        states = lines[0].split()

        alphabet = lines[1].split()

        initial_state = lines[2]

        final_states = set(lines[3].split())

        transitions = {}

        for line in lines[4:]:
            parts = line.split()

            from_state = parts[0]
            symbol = parts[1]
            to_state = parts[2]

            transitions[(from_state, symbol)] = to_state

        results = []

        #Check every word
        for word in words:
            current_state = initial_state

            for symbol in word:
                current_state = transitions[(current_state, symbol)]

            if current_state in final_states:
                results.append("IGEN")
            else:
                results.append("NEM")

        #Write results
        with open(output_file, 'w') as f:
            f.write('\n'.join(results))