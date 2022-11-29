def read_lines(filepath):
    with open(filepath, 'r') as file:
        data = file.read()
    return data.split('\n')


def parse_country(line):
    args = line.split(' ')

    country = {
        "name": args[0],
        "ll": {
            "x": int(args[1]),
            "y": int(args[2])
        },
        "ur": {
            "x": int(args[3]),
            "y": int(args[4])
        }
    }
    return country

def parse_input():
    cases = []

    lines = read_lines('./data/input.txt')
    line_index = 0
    case = 0
    while line_index < len(lines):
        counties_len = int(lines[line_index])
        line_index += 1

        countries_list = []
        for j in range(counties_len):
            parsed = parse_country(lines[line_index])
            countries_list.append(parsed)
            line_index += 1
        case += 1
        cases.append(countries_list)

    return cases
