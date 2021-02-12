import argparse , csv

def print_file_content(file):
    with open(file) as file_object:
        contents = file_object.read()
    
    print(contents)
    
def write_list_to_file_A(output_file, lst):
    with open(output_file, "w") as file:
        for e in lst:
            file.write(e + "\n")
            
def write_list_to_file_B(output_file, *str):
    with open(output_file, "w") as file:
        for s in str:
            file.write(s + "\n")
            
def write_list_to_file_C(output_file, lst):
    with open(output_file, "w") as file:
        for l in lst:
            for e in l:
                file.write(e + "\n")

def read_csv(input_file):
    new_list = []
    
    with open(input_file, "r") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            new_list.append(row)
    
    return new_list

if __name__ == "__main__":
    """run with python week2.py input.txt -f output.txt -l word1 word2 word3"""
    parser = argparse.ArgumentParser(description='Solution to handin week 2')
    parser.add_argument('input_file', help='the input file to consume')
    parser.add_argument('-l', '--list', nargs='*', help='extra words', required=False) # nargs='*' means 0 or more args, nargs='+' means 1 or more
    parser.add_argument('-f', '--output_file', help='the file to print to. (console if nothing is given)')
    args = parser.parse_args()
    print('INPUT:', args.input_file)
    print('File:', args.output_file)
    print('Len', vars(args))
    # only first arg
    if not (args.output_file and args.list):
        print_file_content(args.input_file)
    # only input and output
    else:
        lst = read_csv(args.input_file)
        if args.list:
            lst.extend(args.list)
        print('LISTEN:',lst)
        write_list_to_file_C(args.output_file,lst)