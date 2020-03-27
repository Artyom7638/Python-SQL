import os
import re
import tokenize
from collections import namedtuple

Query = namedtuple('Query', 'start end')


def process_folder():
    pass


def process_file(path, cursor_name, save_as_copy=True):
    queries = find_SQL_queries(path)
    with open(path, 'r') as r:
        lines = r.readlines()
    filename = generate_processed_file_name(path, ' - copy')
    with open(filename, 'w') as w:
        i = 0
        for query in queries:
            while i < query.start - 1:  # т.к. номера строк начинаются с единицы
                i = write_line(w, lines, i)
            q, i = normalize_query(query, lines, i)  # если несколько строк - преобразовать в одну и т.д.
            w.write(process_query(q, cursor_name))
        while i < len(lines):
            i = write_line(w, lines, i)


def find_SQL_queries(path):
    with tokenize.open(path) as f:
        tokens = tokenize.generate_tokens(f.readline)
        tokens = list(tokens)
    i = 0
    res = []
    while i < len(tokens):
        token = tokens[i]
        # print(tokenize.tok_name[token.type], '---', token.string, '---', token.line)
        if token.type == tokenize.ERRORTOKEN and token.string == '$':
            # строку кода можно переносить на следующую строку несколько раз, надо найти начало и конец SQL-запроса
            t = i - 1
            while tokens[t].type != tokenize.NEWLINE and tokens[t].type != tokenize.NL:  # в начале файла NL
                t -= 1
            start = tokens[t].start[0] + 1  # символ переноса строки находится в конце предыдущей строки
            i += 1
            while tokens[i].type != tokenize.NEWLINE and tokens[t].type != tokenize.NL:
                i += 1
            end = tokens[i].end[0]
            query = Query(start, end)
            res.append(query)
        i += 1
    return res


def generate_processed_file_name(path, postfix):
    filename = os.path.basename(path)
    split = filename.rsplit('.', 1)
    name = split[0]
    extension = split[1]
    return os.path.join(os.path.dirname(path), name + postfix + '.' + extension)


def write_line(file, lines, index):
    file.write(lines[index])
    return index + 1


def normalize_query(query, lines, i):
    # первый indent нужно будет сохранять отдельно все остальные убирать
    res = ''
    while i <= query.end - 1:
        line = lines[i]
        if line[len(line) - 1] == '\n':  # в последней строке файла этого символа нет
            line = line[:-1]
        if line[len(line) - 1] == '\\':  # символ переноса строки
            line = line[:-1]
        res += line
        i += 1
    return res, i


def process_query(query, connection_name):
    insert_variables = []
    into_encountered = False
    call_start = query.find('$')
    while call_start != -1:
        if query[call_start + 1] == '(' and query[len(query) - 1] == ')':
            # hard-coded запрос без каких-либо переменных
            query = query[call_start + 2:len(query) - 1]
            break
        pos = read_word(query, call_start + 1)
        directive = query[call_start + 1:pos]
        if directive.casefold() == 'into'.casefold():
            pos = skip_whitespaces(query, pos)
            t = pos
            pos = read_word(query, pos)
            result_var = query[t:pos]
            t = pos
            t = skip_whitespaces(query, t)
            q = ''
            while t < len(query) and is_part_of_name(query[t]):
                q += query[t]
                t += 1
            bulk = False
            if q.casefold() == 'bulk'.casefold():
                bulk = True
                pos = t
            into_encountered = True
            query = query[0:call_start] + query[pos:len(query)]
        else:  # название переменной
            insert_variables.append(directive)
            query = query[0:call_start] + '?' + query[pos:len(query)]
        call_start = query.find('$')
    result = connection_name + '.execute("' + query + '"'
    if insert_variables:
        result += ', ('
        for variable in insert_variables:
            result += variable + ', '
        result += ')'
    result += ')'
    if into_encountered:
        result = result_var + ' = ' + result
        if bulk:
            result += '.fetchall()'
    result += '\n'
    return result


def read_word(query, pos):
    while pos < len(query) and is_part_of_name(query[pos]):
        pos += 1
    return pos


def is_part_of_name(char):
    return char != ' ' and char != ')' and char != ';' and char != ','  # Скобка, запятая - values()


def skip_whitespaces(query, pos):
    while pos < len(query) and query[pos] == ' ':
        pos += 1
    return pos
