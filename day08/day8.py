with open('input.txt') as file:
    program = {i: (cmd, int(value)) for i, line in enumerate(file.readlines()) for cmd, value in [line.strip().split()]}


def execute_program(program_input: dict):
    visited = set()
    program_length = len(program)

    def execute_cmd(cmd_key: int = 0, score_input: int = 0):
        # condition for next cmd after last init command
        if cmd_key == program_length:
            return (True, cmd_key, score_input)
        elif cmd_key > program_length or cmd_key < 0 or cmd_key in visited:
            return (False, cmd_key, score_input)

        visited.add(cmd_key)
        cmd, value = program_input[cmd_key]
        if cmd == 'nop':
            return execute_cmd(cmd_key + 1, score_input)
        elif cmd == 'acc':
            return execute_cmd(cmd_key + 1, score_input + value)
        elif cmd == 'jmp':
            return execute_cmd(cmd_key + value, score_input)

    return execute_cmd()


if __name__ == '__main__':
    print(execute_program(program_input=program))
    for i, (cmd, value) in program.items():
        if cmd in ['nop', 'jmp']:
            new_cmd = 'jmp' if cmd == 'nop' else 'nop'
            program_test = program.copy()
            program_test[i] = (new_cmd, value)
            result, _, score = execute_program(program_input=program_test)
            if result:
                print(score)
                break
