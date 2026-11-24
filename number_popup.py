# python3 assignment3.py input.txt

import re
import sys

def main_interface(inputtxt):

    contents = inputtxt.read()
    print("~" * 13)
    print()
    print(contents)
    print()
    print("~" * 13)

    while True:

        chosen_p, rows, columns = suitable_checker(contents)
        message = game_over_controller(rows, columns)
        if message == "game over":
            print(f"GAME OVER YOU LOSER! .·°՞(˃ ᗜ ˂)՞°·., ꉂꉂ◟(˃᷄ꇴ˂᷅๑)༡ , (╥ ᴗ ╥) [you made me cry... :3], total point: {points}")
            break
        side_list = side_by_side_finder(chosen_p, rows, columns)
        contents = content_creator(side_list, columns)
        cleaned_content = re.sub("11", " ", contents)
        points = len(re.findall("11", contents))
        print(f"your current points by every number you popu: {points}!")
        print("~" * (2*len(rows) - 1))
        print()
        print(cleaned_content)
        print()
        print("~" * (2*len(rows) - 1))

        message = game_over_controller(rows, columns)
        if message == "game over":
            print(f"GAME OVER YOU LOSER! .·°՞(˃ ᗜ ˂)՞°·., ꉂꉂ◟(˃᷄ꇴ˂᷅๑)༡ , (╥ ᴗ ╥) [you made me cry... :3], total point: {points}")
            break


def game_over_controller(rows, columns):
    st = set()
    for row in rows:
        st = st | set(row)
    list_of_existince_numbers = list(st)

    if 11 in list_of_existince_numbers:
        list_of_existince_numbers.remove(11)

    empty_counter = 0
    list_counter = 0

    for number in list_of_existince_numbers:
        for row in rows:
            if number in row:
                chosen_p = [rows.index(row), row.index(number)]
                existince_list = side_by_side_finder(chosen_p, rows, columns)
                if not existince_list:
                    empty_counter += 1
                list_counter += 1
    if empty_counter == list_counter:
        return "game over"
    return "go on"
        

def suitable_checker(contents):

    rawrows = re.split("\n", contents)
    rows = [[int(numb) for numb in rawrow.split(" ")] for rawrow in rawrows]
    columns = [[row[m] for row in rows] for m in range(0, len(rows[0]))]

    print("Choose the row and column in order to pop up a number and write them with between gap (or you can write 'quit'). (like: \"3 5\")")
    while True:
        prompt = input()
        try:
            c_row, c_column = [int(numb) - 1 for numb in prompt.split(" ")] #chosen (c) ones direkt -1 ile indekslenmis hali 
            if c_row <= len(rows) and c_column <= len(columns):
                break

            else:
                print("Please enter a correct size!")  
        except:
            print("Please enter a correct size!")

    chosen_p = [c_row, c_column] #chosen positions

    return chosen_p, rows, columns


def side_by_side_finder(chosen_p, rows, columns):

    c_row, c_column = chosen_p
    chosen_number = rows[c_row][c_column] 
    i = c_row #c_column burada direkt o satirdaki indeksine denk geliyor

    processing_list = []
    finished_list = []
    processing_list.append((c_column, i)) # burada sag ve sol columndaki aradigimiz sayilari kaydetiyoruz column index / sayinin o columndaki indexsi tuple olarak

    while len(processing_list) != 0:
        for column_index, number_index in processing_list:

            for n in range(number_index - 1, -1, -1): #sola akis yani column cinsinden yukari
                if chosen_number == columns[column_index][n] and (column_index, n) not in finished_list and (column_index, n) not in processing_list:
                    processing_list.append((column_index, n))
                else:
                    break

            for n in range(number_index + 1, len(columns[column_index])): #saga akis yani column cinsinden asagi
                if chosen_number == columns[column_index][n] and (column_index, n) not in finished_list and (column_index, n) not in processing_list:
                    processing_list.append((column_index, n))
                else:
                    break

            for column_i in range(column_index - 1, -1, -1): #columnlar arasi sola akis
                if chosen_number == columns[column_i][number_index] and (column_i, number_index) not in finished_list and (column_i, number_index) not in processing_list:
                    processing_list.append((column_i, number_index))
                else:
                    break

            for column_i in range(column_index + 1, len(columns)): #columnlar arasi saga akis
                if chosen_number == columns[column_i][number_index] and (column_i, number_index) not in finished_list and (column_i, number_index) not in processing_list:
                    processing_list.append((column_i, number_index))
                else:
                    break

            finished_list.append(processing_list.pop(processing_list.index((column_index, number_index))))
            break
    if len(finished_list) == 1:
        return []
    return finished_list


def content_creator(side_list, columns):

    try:
        side_list.sort(key=lambda x: x[1])
        for col_i, i in side_list:
            columns[col_i].remove(columns[col_i][i])
            columns[col_i].insert(0, 11)
    except IndexError:
        print("there is only 1 number INDEED... (\"-ࡇ-)")
        pass
    rows = [[column[m] for column in columns] for m in range(0, len(columns[0]))]
    content = "\n".join([" ".join([str(numb) for numb in row]) for row in rows])
    return content


def main():
    with open(sys.argv[1],"r") as inputtxt:
        main_interface(inputtxt)


if __name__ == "__main__":
    main()



