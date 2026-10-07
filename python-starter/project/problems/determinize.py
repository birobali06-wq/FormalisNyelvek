from project.problem import Problem
import argparse


class DeterminizeProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--det',
            action='store_true',
            help='Determinizálja az automatát'
        )

    def is_chosen_problem(self, args):
        return args.det

    def run(self, args):
        input_file = args.input
        output_file = args.output

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

            if from_state not in states:
                raise ValueError(
                    f"Invalid state in transition: {from_state}"
                )

            if to_state not in states:
                raise ValueError(
                    f"Invalid state in transition: {to_state}"
                )

            if symbol not in alphabet:
                raise ValueError(
                    f"Invalid symbol in transition: {symbol}"
                )

            if (from_state, symbol) not in transitions:
                transitions[(from_state, symbol)] = set()

            transitions[(from_state, symbol)].add(to_state)

        start_subset = frozenset([initial_state])

        subsets = [start_subset]
        subset_to_name = {
            start_subset: 's0'
        }

        deterministic_transitions = {}
        index = 0

        while index < len(subsets):
            current_subset = subsets[index]
            current_name = subset_to_name[current_subset]

            for symbol in alphabet:
                next_subset = set()

                for state in current_subset:
                    if (state, symbol) in transitions:
                        next_subset.update(
                            transitions[(state, symbol)]
                        )

                if not next_subset:
                    continue

                next_subset = frozenset(next_subset)

                if next_subset not in subset_to_name:
                    new_name = f's{len(subsets)}'
                    subset_to_name[next_subset] = new_name
                    subsets.append(next_subset)

                deterministic_transitions[
                    (current_name, symbol)
                ] = subset_to_name[next_subset]

            index += 1

        deterministic_final_states = set()

        for subset in subsets:
            for state in subset:
                if state in final_states:
                    deterministic_final_states.add(
                        subset_to_name[subset]
                    )
                    break

        with open(output_file, 'w') as f:
            f.write(
                ' '.join(
                    f's{i}' for i in range(len(subsets))
                )
                + '\n'
            )

            f.write(' '.join(alphabet) + '\n')

            f.write('s0\n')

            final_names = [
                f's{i}'
                for i in range(len(subsets))
                if f's{i}' in deterministic_final_states
            ]

            f.write(' '.join(final_names) + '\n')

            for i in range(len(subsets)):
                current_name = f's{i}'

                for symbol in alphabet:
                    key = (current_name, symbol)

                    if key in deterministic_transitions:
                        target = deterministic_transitions[key]
                        f.write(
                            f'{current_name} {symbol} {target}\n'
                        )