import lexical_Analyzer

tokens = lexical_Analyzer.lexical_analyzer('program.c')
list = []
express_n = ""
print("\n\n")


def parma(token, pos):
    parame = ''
    pos += 1
    i = 0
    while token[pos][0] != 'RIGHT_PAREN':

        if token[pos][0] == 'KEYWORD':
            if token[pos + 1][0] == 'IDENTIFIER':
                if token[pos + 2][0] == 'COMMA':
                    parame += token[pos][1] + ' ' + token[pos + 1][1] + ' ' + token[pos + 2][1]
                    pos += 1
                else:
                    parame += token[pos][1] + '  ' + token[pos + 1][1]
                    pos += 1
            else:
                print("Error Expected IDENTIFIER")
        elif token[pos][0] == 'IDENTIFIER':
            if token[pos + 1][0] == 'COMMA':
                parame += token[pos][1] + ' ' + token[pos + 1][1]
            else:
                parame += token[pos][1]
        pos += 1
        i += 1
    return parame, pos


def condition(tokens, position):
    global express_n
    condition_statment = ''
    current_token = position
    current_token, left_operand, = expression(tokens, current_token)
    condition_statment += left_operand
    express_n = ''
    token_type = tokens[current_token][0]
    if token_type == 'EQUAL' or token_type == 'NOT_EQUAL' or token_type == 'LESS_THAN' or token_type == 'GREATER_THAN' or token_type == 'LESS_THAN_EQUAL' or token_type == 'GREATER_THAN_EQUAL':
        conditional_operator = tokens[current_token][1]
        condition_statment += " " + conditional_operator
        current_token, right_operand, = expression(tokens, current_token)
        condition_statment += " " + right_operand
        express_n = ''
    if len(condition_statment) == 0:
        print("Syntax Error: Condition statement not provided")
    return current_token, condition_statment


def statments(token, postion):  # statement: (declaration | initializing | function_call | assignment | if_statement | while_statement | return_statement)*;
    global express_n
    statment_block = ''
    block_track = 1
    current_token = postion
    print("wewe", token[0])
    while block_track != 0:
        current_token += 1
        print("ddf", token[current_token][0], current_token)
        if tokens[current_token][0] == 'RIGHT_BRACE':
            block_track -= 1
        elif tokens[current_token][0] == "KEYWORD" and tokens[current_token][1] != 'return':
            type = tokens[current_token][1]
            if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == "IDENTIFIER":
                name = tokens[current_token + 1][1]
                if (current_token + 2) < len(tokens) and tokens[current_token + 2][0] == "SEMICOLON":  # handle declaration
                    terminator = tokens[current_token + 2][1]
                    print(f"Declaration {type} {name} {terminator}")
                    current_token += 2

                elif (current_token + 2) < len(tokens) and tokens[current_token + 2][0] == "LEFT_PAREN":  # handle functions
                    f_lp = tokens[current_token + 2][1]
                    function_parameter, pos = parma(tokens, (current_token + 2))
                    current_token = pos
                    if current_token < len(tokens) and tokens[current_token][0] == "RIGHT_PAREN":
                        block_track += 1
                        f_rp = tokens[current_token][1]
                        if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == "LEFT_BRACE":
                            block_track -= 1
                            f_lb = tokens[current_token + 1][1]
                            current_token, function_body = statments(tokens, current_token + 1)
                            # call function body
                            if current_token < len(tokens) and tokens[current_token][0] == "RIGHT_BRACE":
                                block_track += 1
                                f_rb = tokens[current_token][1]
                                print(f"Function: {type}  {name} {f_lp} {function_parameter} {f_rp} {f_lb} {function_body} {f_rb}")
                            else:
                                print("Syntax Error: <missing '}',  function block not closed")
                                print(f"Function: {type}  {name} {f_lp} {function_parameter} {f_rp} {f_lb} {function_body}  <missing RIGHT_BRACE' >")
                        else:
                            print("Syntax Error: Functon definition   <missing '{'>")
                            print(f"Function: {type}  {name} {f_lp} {function_parameter} <missing LEFT_BRACE>...")
                    else:
                        print("Syntax Error: <missing '('")

                elif (current_token + 2) < len(tokens) and tokens[current_token + 2][0] == "ASSIGN":  # initialization
                    type = tokens[current_token][1]
                    namr = tokens[current_token + 1][1]
                    asg = tokens[current_token + 2][1]
                    current_token, express = expression(tokens, current_token + 2)
                    express_n = ''

                    if len(express) != 0:
                        if current_token < len(tokens) and tokens[current_token][0] == "SEMICOLON":
                            s_tm = tokens[current_token][1]
                            print(f"initialization: {type} {namr} {asg} {express} {s_tm}")
                        else:
                            print(f"initialization: {type} {namr} {asg} {express} <missing ';'>")
                            print(f"Syntax Error: missing statement terminator")
                            continue
                    else:
                        print("Syntax Error: variable Initialization error, no value was assigned ")
                        if current_token < len(tokens) and tokens[current_token][0] == "SEMICOLON":
                            s_tm = tokens[current_token][1]
                            print(f"initialization: {type} {namr} {asg} ~{None}~ {s_tm}")
                        else:
                            print(f"initialization: {type} {namr} {asg} ~{None}~ <missing ';'>")
                            print(f"Syntax Error: missing statement terminator")
                            continue
                else:
                    print(f"Declaration: {type}  {name} <missing ';' >")
                    print(" Syntax Error : unterminated statement ", tokens[current_token + 1][0])
                    current_token += 1
            else:
                print(" Syntax Error : expected token IDENTIFIER goten ")

        elif tokens[current_token][0] == 'IF':
            gm = ""
            else_if = 0
            while True:
                if_key_word = tokens[current_token][1]
                gm += if_key_word + ' '
                if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == 'LEFT_PAREN':
                    l_p = tokens[current_token + 1][1]
                    gm += l_p + ' '
                    current_token, if_condition = condition(tokens, current_token + 1)
                    gm += if_condition + ' '
                    if current_token < len(tokens) and tokens[current_token][0] == 'RIGHT_PAREN':
                        r_p = tokens[current_token][1]
                        gm += r_p + ' '
                        if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == 'LEFT_BRACE':
                            block_track += 1
                            l_b = tokens[current_token + 1][1]
                            gm += l_b + ' '
                            if_statment = 'None'  # statment()
                            gm += if_statment + ' '
                            if (current_token + 2) < len(tokens) and tokens[current_token + 2][0] == 'RIGHT_BRACE':
                                block_track -= 1
                                r_b = tokens[current_token + 2][1]
                                gm += r_b + ' '
                                current_token += 2
                                if (current_token + 1) == len(tokens):
                                    print(f"IF statement: {gm}")
                                    break
                                elif tokens[current_token + 1][0] != 'ELSE':
                                    print(f"IF statement: {gm}")
                                    break
                                else:
                                    if tokens[current_token + 1][0] == 'ELSE' and tokens[current_token + 2][0] != 'IF':
                                        if (current_token + 2) < len(tokens) and tokens[current_token + 2][0] == 'LEFT_BRACE':
                                            block_track += 1
                                            else_key = tokens[current_token + 1][1]
                                            gm += else_key + ' '
                                            e_lb = tokens[current_token + 2][1]
                                            gm += e_lb + ' '
                                            else_statment = "None"  # statment()
                                            gm += else_statment + ' '
                                            if tokens[current_token + 3][0] == 'RIGHT_BRACE':
                                                block_track -= 1
                                                e_rb = tokens[current_token + 3][1]
                                                gm += e_rb + ' '
                                                current_token += 3
                                                if else_if == 0:
                                                    print(f"IF-ELSE statement: {gm}")
                                                else:
                                                    print(f"IF-ELSE-IF statement: {gm}")
                                                break
                                            else:
                                                print(f"IF statement: {gm} < missing 'RIGHT_BRACE'>")
                                                print("Syntax Error: incomplete else statment  missing <RIGHT_BRACE>")
                                                break
                                        else:
                                            else_key = tokens[current_token + 1][1]
                                            gm += else_key + ' '
                                            print(f"IF statement: {gm} < missing 'LEFT_BRACE' 'RIGHT_BRACE'>")
                                            print("Syntax Error: incomplete else statment ")
                                            break
                                    elif tokens[current_token + 1][0] == 'ELSE' and tokens[current_token + 2][0] == 'IF':
                                        else_key = tokens[current_token + 1][1]
                                        gm += else_key + " "
                                        else_if += 1
                                        current_token += 2

                            else:
                                print(" Syntax Error : if-statment expected  RIGHT_BRACE   ")
                                print(f"IF statement: {gm} < missing 'RIGHT_BRACE'>")
                                break
                        else:
                            print(" Syntax Error : if-statment expected  LEFT_BRACE  < missing '{'> ")
                            print(f"IF statement: {gm} ... <statement incomplete> ...")
                            break

                    else:
                        print(" Syntax Error : if-statment expected  LEFT_PAREN  < missing ')'> ")
                        print(f"IF statement: {gm} ... <statement incomplete> ...")
                        break

        elif tokens[current_token][0] == 'WHILE':
            while_key = tokens[current_token][0]
            if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == 'LEFT_PAREN':
                wh_lp = tokens[current_token + 1][1]
                current_token, condition_statment = condition(tokens, current_token + 1)
                if current_token < len(tokens) and tokens[current_token][0] == 'RIGHT_PAREN':
                    wh_rp = tokens[current_token][1]
                    if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == 'LEFT_BRACE':
                        block_track += 1
                        wh_lb = tokens[current_token + 1][1]
                        # statment()
                        if tokens[current_token + 2][0] == 'RIGHT_BRACE':
                            block_track -= 1
                            wh_rb = tokens[current_token + 2][1]
                            wh_condition = condition_statment
                            wh_statment = None
                            print(F"WHILE-STATEMENT: {while_key} {wh_lp} {wh_condition} {wh_rp} {wh_lb} {wh_statment} {wh_rb}")
                            current_token += 2

        elif tokens[current_token][0] == 'IDENTIFIER':
            name = tokens[current_token][1]
            if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == 'ASSIGN':
                asg = tokens[current_token + 1][1]
                if (current_token + 2) < len(tokens) and (current_token + 3) < len(tokens) and tokens[current_token + 2][0] == 'IDENTIFIER' and tokens[current_token + 3][0] == 'LEFT_PAREN':  # function_assignment_call
                    f_name = tokens[current_token + 2][1]
                    l_p = tokens[current_token + 3][1]
                    f_parameter, current_token = parma(tokens, (current_token + 3))
                    r_p = tokens[current_token][1]
                    if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == 'SEMICOLON':
                        s_tm = tokens[current_token + 1][1]
                        print(f"Function Assignment: {name} {asg} {f_name} {l_p} {f_parameter} {r_p} {s_tm}")
                        current_token += 1
                    else:
                        print(f"Function Assignment: {name} {asg} {f_name} {l_p} {f_parameter} {r_p} <missing ';'>")
                else:
                    current_token, express = expression(tokens, current_token + 1)
                    express_n = ''
                    if len(express) != 0:
                        if current_token < len(tokens) and tokens[current_token][0] != "SEMICOLON":
                            print("Syntax Error: statement terminator missing")
                            print(f"Variable assignment: {name} {asg} {express}  <missing ';'>")
                        else:
                            print(f"Variable assignment: {name} {asg} {express} <missing semicolon>")
                    else:
                        print("Syntax Error: variable assignment error, no value was assigned ")
                        if tokens[current_token][0] == "SEMICOLON":
                            s_tm = tokens[current_token][1]
                            print(f"Variable assignment: {name} {asg} {None} {s_tm}")


            elif tokens[current_token + 1][0] == 'LEFT_PAREN':
                l_p = tokens[current_token + 1][1]
                function_parameter, pos = parma(tokens, (current_token + 1))
                current_token = pos
                if tokens[current_token][0] == "RIGHT_PAREN":
                    f_rp = tokens[current_token][1]
                    if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == "SEMICOLON":
                        tm = tokens[current_token + 1][1]
                        print(f"Function Call: {name} {l_p} {function_parameter} {f_rp} {tm}")
                        current_token += 1
                    else:
                        print(f"Function Call: {name} {l_p} {function_parameter} {f_rp}  < missing ';'>")
                        print('Syntax Error: function call missing statement terminator')

        elif tokens[current_token][1] == 'return':
            current_token, express = expression(tokens, current_token)
            express_n = ''
            print("fef ", tokens[current_token-1])
            if current_token < len(tokens) and tokens[current_token][0] == "SEMICOLON":
                if len(express_n) != 0:
                    print("RETURN-STATMENT  : return ", express, tokens[current_token][1])
                else:
                    print("RETURN-STATMENT  : return  <error 'no value'>", tokens[current_token][1])
                    print("Syntax error: no return value was specified")
            else:
                if len(express_n) != 0:
                    print(f"RETURN-STATMENT  : return {express} < missing ';'>")
                    print("Syntax error: no return value was specified")
                else:
                    print(f"RETURN-STATMENT  : return  <missing return-value>  <missing ';'>")
                    print("Syntax error: no return value was specified, missing statement terminator for return statement")


        else:
            print("Syntax Error  : ", tokens[current_token])

    return current_token, statment_block





def expression(tokens, position):
    global express_n
    express_n += ''
    current_token = position + 1
    while current_token < len(tokens):
        token_type, token_value = tokens[current_token]
        if token_type == 'IDENTIFIER':
            express_n += token_value + ' '
        elif token_type == 'INTEGER':
            express_n += token_value + ' '
        elif token_type == 'LEFT_PAREN':
            express_n += token_value + ' '
            expression(tokens, current_token)  # Handle nested expressions recursively
            while tokens[current_token][0] != 'RIGHT_PAREN':  # Skip to the end of the nested expression
                current_token += 1
            express_n += tokens[current_token][1] + ' '
        elif token_type == 'PLUS':
            express_n += token_value + ' '
        elif token_type == 'SEMICOLON' or token_type == 'RIGHT_PAREN' or token_type == 'EQUAL' or token_type == 'NOT_EQUAL' or token_type == 'LESS_THAN' or token_type == 'GREATER_THAN' or token_type == 'LESS_THAN_EQUAL' or token_type == 'GREATER_THAN_EQUAL':
            break
        else:
            print(f"Sytax error -- Expression Error Cause:  {tokens[current_token][1]}")
            break
        current_token += 1
    return current_token, express_n


def parse_program(tokens, postion):
    global express_n
    current_token = postion
    while current_token < len(tokens):
        if tokens[current_token][0] == "INCLUDE_ID":
            if tokens[current_token + 1][0] == 'INCLUDE_DIRECTIVE':
                # handle include list
                include_directive = tokens[current_token][1] + ' ' + tokens[current_token + 1][1]
                current_token += 1
                print(f"include list: {include_directive}")
            else:
                print(f"SYNTAX ERROR: INCLUDE_DIRECTIVE: {tokens[current_token + 1][1]}")
                current_token += 1

        elif tokens[current_token][0] == "KEYWORD" and tokens[current_token][1] != 'return':
            type = tokens[current_token][1]
            if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == "IDENTIFIER":
                name = tokens[current_token + 1][1]
                if (current_token + 2) < len(tokens) and tokens[current_token + 2][0] == "SEMICOLON":  # handle declaration
                    terminator = tokens[current_token + 2][1]
                    print(f"Declaration {type} {name} {terminator}")
                    current_token += 2

                elif (current_token + 2) < len(tokens) and tokens[current_token + 2][0] == "LEFT_PAREN":  # handle functions
                    f_lp = tokens[current_token + 2][1]
                    function_parameter, pos = parma(tokens, (current_token + 2))
                    current_token = pos
                    if current_token < len(tokens) and tokens[current_token][0] == "RIGHT_PAREN":
                        f_rp = tokens[current_token][1]
                        if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == "LEFT_BRACE":
                            f_lb = tokens[current_token + 1][1]
                            current_token, function_body = statments(tokens, current_token + 1)
                            # call function body
                            if current_token < len(tokens) and tokens[current_token][0] == "RIGHT_BRACE":
                                f_rb = tokens[current_token][1]
                                print(f"Function: {type}  {name} {f_lp} {function_parameter} {f_rp} {f_lb} {function_body} {f_rb}")
                            else:
                                print("Syntax Error: <missing '}',  function block not closed")
                                print(f"Function: {type}  {name} {f_lp} {function_parameter} {f_rp} {f_lb} {function_body}  <missing RIGHT_BRACE' >")
                        else:
                            print("Syntax Error: Functon definition   <missing '{'>")
                            print(f"Function: {type}  {name} {f_lp} {function_parameter} <missing LEFT_BRACE>...")
                    else:
                        print("Syntax Error: <missing '('")

                elif (current_token + 2) < len(tokens) and tokens[current_token + 2][0] == "ASSIGN":  # initialization
                    type = tokens[current_token][1]
                    namr = tokens[current_token + 1][1]
                    asg = tokens[current_token + 2][1]
                    current_token, express = expression(tokens, current_token + 2)
                    express_n = ''

                    if len(express) != 0:
                        if current_token < len(tokens) and tokens[current_token][0] == "SEMICOLON":
                            s_tm = tokens[current_token][1]
                            print(f"initialization: {type} {namr} {asg} {express} {s_tm}")
                        else:
                            print(f"initialization: {type} {namr} {asg} {express} <missing ';'>")
                            print(f"Syntax Error: missing statement terminator")
                            continue
                    else:
                        print("Syntax Error: variable Initialization error, no value was assigned ")
                        if current_token < len(tokens) and tokens[current_token][0] == "SEMICOLON":
                            s_tm = tokens[current_token][1]
                            print(f"initialization: {type} {namr} {asg} ~{None}~ {s_tm}")
                        else:
                            print(f"initialization: {type} {namr} {asg} ~{None}~ <missing ';'>")
                            print(f"Syntax Error: missing statement terminator")
                            continue
                else:
                    print(f"Declaration: {type}  {name} <missing ';' >")
                    print(" Syntax Error : unterminated statement ", tokens[current_token + 1][0])
                    current_token += 1
            else:
                print(" Syntax Error : expected token IDENTIFIER goten ")

        elif tokens[current_token][0] == 'IF':
            gm = ""
            else_if = 0
            while True:
                if_key_word = tokens[current_token][1]
                gm += if_key_word + ' '
                if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == 'LEFT_PAREN':
                    l_p = tokens[current_token + 1][1]
                    gm += l_p + ' '
                    current_token, if_condition = condition(tokens, current_token + 1)
                    gm += if_condition + ' '
                    if current_token < len(tokens) and tokens[current_token][0] == 'RIGHT_PAREN':
                        r_p = tokens[current_token][1]
                        gm += r_p + ' '
                        if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == 'LEFT_BRACE':
                            l_b = tokens[current_token + 1][1]
                            gm += l_b + ' '
                            if_statment = 'None'  # statment()
                            gm += if_statment + ' '
                            if (current_token + 2) < len(tokens) and tokens[current_token + 2][0] == 'RIGHT_BRACE':
                                r_b = tokens[current_token + 2][1]
                                gm += r_b + ' '
                                current_token += 2
                                if (current_token + 1) == len(tokens):
                                    print(f"IF statement: {gm}")
                                    break
                                elif tokens[current_token + 1][0] != 'ELSE':
                                    print(f"IF statement: {gm}")
                                    break
                                else:
                                    if tokens[current_token + 1][0] == 'ELSE' and tokens[current_token + 2][0] != 'IF':
                                        if (current_token + 2) < len(tokens) and tokens[current_token + 2][0] == 'LEFT_BRACE':
                                            else_key = tokens[current_token + 1][1]
                                            gm += else_key + ' '
                                            e_lb = tokens[current_token + 2][1]
                                            gm += e_lb + ' '
                                            else_statment = "None"  # statment()
                                            gm += else_statment + ' '
                                            if tokens[current_token + 3][0] == 'RIGHT_BRACE':
                                                e_rb = tokens[current_token + 3][1]
                                                gm += e_rb + ' '
                                                current_token += 3
                                                if else_if == 0:
                                                    print(f"IF-ELSE statement: {gm}")
                                                else:
                                                    print(f"IF-ELSE-IF statement: {gm}")
                                                break
                                            else:
                                                print(f"IF statement: {gm} < missing 'RIGHT_BRACE'>")
                                                print("Syntax Error: incomplete else statment  missing <RIGHT_BRACE>")
                                                break
                                        else:
                                            else_key = tokens[current_token + 1][1]
                                            gm += else_key + ' '
                                            print(f"IF statement: {gm} < missing 'LEFT_BRACE' 'RIGHT_BRACE'>")
                                            print("Syntax Error: incomplete else statment ")
                                            break
                                    elif tokens[current_token + 1][0] == 'ELSE' and tokens[current_token + 2][0] == 'IF':
                                        else_key = tokens[current_token + 1][1]
                                        gm += else_key + " "
                                        else_if += 1
                                        current_token += 2

                            else:
                                print(" Syntax Error : if-statment expected  RIGHT_BRACE   ")
                                print(f"IF statement: {gm} < missing 'RIGHT_BRACE'>")
                                break
                        else:
                            print(" Syntax Error : if-statment expected  LEFT_BRACE  < missing '{'> ")
                            print(f"IF statement: {gm} ... <statement incomplete> ...")
                            break

                    else:
                        print(" Syntax Error : if-statment expected  LEFT_PAREN  < missing ')'> ")
                        print(f"IF statement: {gm} ... <statement incomplete> ...")
                        break

        elif tokens[current_token][0] == 'WHILE':
            while_key = tokens[current_token][0]
            if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == 'LEFT_PAREN':
                wh_lp = tokens[current_token + 1][1]
                current_token, condition_statment = condition(tokens, current_token + 1)
                if current_token < len(tokens) and tokens[current_token][0] == 'RIGHT_PAREN':
                    wh_rp = tokens[current_token][1]
                    if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == 'LEFT_BRACE':
                        wh_lb = tokens[current_token + 1][1]
                        current_token, while_body = statments(tokens, current_token + 1)
                        if tokens[current_token][0] == 'RIGHT_BRACE':
                            wh_rb = tokens[current_token][1]
                            wh_condition = condition_statment
                            wh_statment = None
                            print(F"WHILE-STATEMENT: {while_key} {wh_lp} {wh_condition} {wh_rp} {wh_lb} {while_body} {wh_rb}")
                            current_token += 2

        elif tokens[current_token][0] == 'IDENTIFIER':
            name = tokens[current_token][1]
            if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == 'ASSIGN':
                asg = tokens[current_token + 1][1]
                if (current_token + 2) < len(tokens) and (current_token + 3) < len(tokens) and tokens[current_token + 2][0] == 'IDENTIFIER' and tokens[current_token + 3][0] == 'LEFT_PAREN':  # function_assignment_call
                    f_name = tokens[current_token + 2][1]
                    l_p = tokens[current_token + 3][1]
                    f_parameter, current_token = parma(tokens, (current_token + 3))
                    r_p = tokens[current_token][1]
                    if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == 'SEMICOLON':
                        s_tm = tokens[current_token + 1][1]
                        print(f"Function Assignment: {name} {asg} {f_name} {l_p} {f_parameter} {r_p} {s_tm}")
                        current_token += 1
                    else:
                        print(f"Function Assignment: {name} {asg} {f_name} {l_p} {f_parameter} {r_p} <missing ';'>")
                else:
                    current_token, express = expression(tokens, current_token + 1)
                    express_n = ''
                    if len(express) != 0:
                        if current_token < len(tokens) and tokens[current_token][0] != "SEMICOLON":
                            print("Syntax Error: statement terminator missing")
                            print(f"Variable assignment: {name} {asg} {express}  <missing ';'>")
                        else:
                            print(f"Variable assignment: {name} {asg} {express} <missing semicolon>")
                    else:
                        print("Syntax Error: variable assignment error, no value was assigned ")
                        if tokens[current_token][0] == "SEMICOLON":
                            s_tm = tokens[current_token][1]
                            print(f"Variable assignment: {name} {asg} {None} {s_tm}")


            elif tokens[current_token + 1][0] == 'LEFT_PAREN':
                l_p = tokens[current_token + 1][1]
                function_parameter, pos = parma(tokens, (current_token + 1))
                current_token = pos
                if tokens[current_token][0] == "RIGHT_PAREN":
                    f_rp = tokens[current_token][1]
                    if (current_token + 1) < len(tokens) and tokens[current_token + 1][0] == "SEMICOLON":
                        tm = tokens[current_token + 1][1]
                        print(f"Function Call: {name} {l_p} {function_parameter} {f_rp} {tm}")
                        current_token += 1
                    else:
                        print(f"Function Call: {name} {l_p} {function_parameter} {f_rp}  < missing ';'>")
                        print('Syntax Error: function call missing statement terminator')

        elif tokens[current_token][1] == 'return':
            current_token, express = expression(tokens, current_token)
            express_n = ''
            print("fef ", tokens[current_token-1])
            if current_token < len(tokens) and tokens[current_token][0] == "SEMICOLON":
                if len(express_n) != 0:
                    print("RETURN-STATMENT  : return ", express, tokens[current_token][1])
                else:
                    print("RETURN-STATMENT  : return  <error 'no value'>", tokens[current_token][1])
                    print("Syntax error: no return value was specified")
            else:
                if len(express_n) != 0:
                    print(f"RETURN-STATMENT  : return {express} < missing ';'>")
                    print("Syntax error: no return value was specified")
                else:
                    print(f"RETURN-STATMENT  : return  <missing return-value>  <missing ';'>")
                    print("Syntax error: no return value was specified, missing statement terminator for return statement")

        else:
            print("Syntax Error  : ", tokens[current_token])
        current_token += 1


parse_program(tokens, 0)