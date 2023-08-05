from inkprint import InkPrinter


def main():
    # normal print without colors
    print('This line is normal.')

    # print with coloars
    inkp = InkPrinter(paper_color='r', ink_color='y')
    inkp.print('Hello world! (printed with ink)')

    # normal print without colors
    print('This line is normal.')


if __name__ == '__main__':
    main()