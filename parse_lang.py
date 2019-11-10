def parse_lang(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.readlines()
        for line in content:
            result = line.find(",en,English")
            if result != -1:
                return parse_line(line)
    return '0'

def parse_line(line):
    result = ""
    for i in range(len(line)):
        if line[i] != ',':
            result += line[i]
        else:
            return result
