
class Day6:
    """

    """
    def __init__(self):
        with open("Data/Day3Data.txt", "r") as f:
            self.data = tuple(f.read().splitlines())

    def part1(self):
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(Day6().part1())
