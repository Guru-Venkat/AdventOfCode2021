import enum
import pprint


class Day1:
    """
    --- Day 1: Sonar Sweep --- You're minding your own business on a ship at sea when the overboard-alarm goes off!
    You rush to see if you can help. Apparently, one of the Elves tripped and accidentally sent the sleigh keys
    flying into the ocean!

    Before you know it, you're inside a submarine the Elves keep ready for situations like this. It's covered in
    Christmas lights (because of course it is), and it even has an experimental antenna that should be able to track
    the keys if you can boost its signal strength high enough; there's a little meter that indicates the antenna's
    signal strength by displaying 0-50 stars.

    Your instincts tell you that in order to save Christmas, you'll need to get all fifty stars by December 25th.

    Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the
    second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

    As the submarine drops below the surface of the ocean, it automatically performs a sonar sweep of the nearby sea
    floor. On a small screen, the sonar sweep report (your puzzle input) appears: each line is a measurement of the
    sea floor depth as the sweep looks further and further away from the submarine.

    For example, suppose you had the following report:

    199 200 208 210 200 207 240 269 260 263

    This report indicates that, scanning outward from the submarine,
    the sonar sweep found depths of 199, 200, 208, 210, and so on.
    """

    def __init__(self):
        with open("Data/Day1Data.txt", "r") as f:
            self.data = tuple(int(d) for d in f.read().splitlines())

    def part1_IncreaseInDepth(self, data=None):
        """
        The first order of business is to figure out how quickly the depth increases, just so you know what you're
        dealing with - you never know if the keys will get carried into deeper water by an ocean current or a fish or
        something.

        To do this, count the number of times a depth measurement increases from the previous measurement. (There is no
        measurement before the first measurement.) In the example above, the changes are as follows:

        199 (N/A - no previous measurement)
        200 (increased)
        208 (increased)
        210 (increased)
        200 (decreased)
        207 (increased)
        240 (increased)
        269 (increased)
        260 (decreased)
        263 (increased)
        In this example, there are 7 measurements that are larger than the previous measurement.
        :return:
        """
        if data is None:
            data = self.data
        prev = data[0]
        result = 0
        for dataPoint in data:
            if dataPoint > prev:
                result += 1
            prev = dataPoint

        return result

    def part2_IncreaseInDepthIn3Points(self):
        """
        --- Part Two ---
        Considering every single measurement isn't as useful as you expected: there's just too much noise in the data.

        Instead, consider sums of a three-measurement sliding window. Again considering the above example:

        199  A
        200  A B
        208  A B C
        210    B C D
        200  E   C D
        207  E F   D
        240  E F G
        269    F G H
        260      G H
        263        H

        Start by comparing the first and second three-measurement windows. The measurements in the first window
        are marked A (199, 200, 208); their sum is 199 + 200 + 208 = 607. The second window is marked B (200,
        208, 210); its sum is 618. The sum of measurements in the second window is larger than the sum of the
        first, so this first comparison increased.

        Your goal now is to count the number of times the sum of measurements in this sliding window increases from
        the previous sum. So, compare A with B, then compare B with C, then C with D, and so on. Stop when there
        aren't enough measurements left to create a new three-measurement sum.

        In the above example, the sum of each three-measurement window is as follows:

        A: 607 (N/A - no previous sum)
        B: 618 (increased)
        C: 618 (no change)
        D: 617 (decreased)
        E: 647 (increased)
        F: 716 (increased)
        G: 769 (increased)
        H: 792 (increased)
        In this example, there are 5 sums that are larger than the previous sum.
        :return:
        """
        return self.part1_IncreaseInDepth(tuple(sum(self.data[i: i + 3]) for i in range(len(self.data) - 2)))


class Submarine:
    class Commands(enum.Enum):
        FORWARD = 'forward'
        UP = 'up'
        DOWN = 'down'

    class InvalidCommandException(Exception):
        pass

    @property
    def location(self):
        return self.position * self.depth

    @property
    def powerConsumption(self):
        return self.gammaRate * self.epsilonRate

    @property
    def lifeSupportRating(self):
        return self.oxygenGeneratorRating * self.co2ScrubberRating

    def __init__(self):
        self.oxygenGeneratorRating = 0
        self.co2ScrubberRating = 0
        self.position = 0
        self.depth = 0
        self.aim = 0
        self.gammaRate = 0
        self.epsilonRate = 0

    def processCommand(self, command, step):
        # noinspection PyUnusedLocal
        match command:
            case Submarine.Commands.FORWARD:
                self.position += step
                self.depth += self.aim * step
            case Submarine.Commands.UP:
                self.aim -= step
            case Submarine.Commands.DOWN:
                self.aim += step
            case default:
                print(f"Invalid Command {command}")

    def processDiagnostic(self, diagnostic_data):
        self._calculateGammaRate(diagnostic_data)
        self._calculateEpsilonRate(diagnostic_data)
        self._calculateOxygenGeneratorRating(diagnostic_data)
        self._calculateCO2ScrubberRating(diagnostic_data)

    def _calculateGammaRate(self, data):
        data = tuple(map(tuple, zip(*data)))  # Transpose the 2D list
        gammaRate = ''

        for d in data:
            if d.count('1') >= len(d) / 2:
                gammaRate += '1'
            else:
                gammaRate += '0'

        self.gammaRate = int(gammaRate, 2)
        return gammaRate

    def _calculateEpsilonRate(self, data):
        data = tuple(map(tuple, zip(*data)))  # Transpose the 2D list
        epsilonRate = ''

        for d in data:
            if d.count('1') >= len(d) / 2:
                epsilonRate += '0'
            else:
                epsilonRate += '1'

        self.epsilonRate = int(epsilonRate, 2)
        return epsilonRate

    def _calculateOxygenGeneratorRating(self, data: list):
        for i in range(len(data[0])):
            if len(data) == 1:
                self.oxygenGeneratorRating = int(data[0], 2)
                return data[0]
            else:
                data = [x for x in data if x[i] == self._calculateGammaRate(data)[i]]

        if len(data) == 1:
            self.oxygenGeneratorRating = int(data[0], 2)
            return data[0]

    def _calculateCO2ScrubberRating(self, data: list):
        for i in range(len(data[0])):
            if len(data) == 1:
                self.co2ScrubberRating = int(data[0], 2)
                return data[0]
            else:
                data = [x for x in data if x[i] == self._calculateEpsilonRate(data)[i]]

        if len(data) == 1:
            self.co2ScrubberRating = int(data[0], 2)
            return data[0]


class Day2:
    """
    --- Day 2: Dive! ---
    Now, you need to figure out how to pilot this thing.

    It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

    forward X increases the horizontal position by X units. down X increases the depth by X units. up X decreases the
    depth by X units. Note that since you're on a submarine, down and up affect your depth, and so they have the
    opposite result of what you might expect.

    The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's
    going. For example:

    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2

    --- Part 1 ---
    Your horizontal position and depth both start at 0. The steps above would then modify them as follows:

    forward 5 adds 5 to your horizontal position, a total of 5. down 5 adds 5 to your depth, resulting in a value of
    5. forward 8 adds 8 to your horizontal position, a total of 13. up 3 decreases your depth by 3, resulting in a
    value of 2. down 8 adds 8 to your depth, resulting in a value of 10. forward 2 adds 2 to your horizontal
    position, a total of 15. After following these instructions, you would have a horizontal position of 15 and a
    depth of 10. (Multiplying these together produces 150.)

    --- Part Two ---
    Based on your calculations, the planned course doesn't seem to make any sense. You find the
    submarine manual and discover that the process is actually slightly more complicated.

    In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at
    0. The commands also mean something entirely different from you first thought:

    down X increases your aim by X units. up X decreases your aim by X units. forward X does two things: It increases
    your horizontal position by X units. It increases your depth by your aim multiplied by X. Again note that since
    you're on a submarine, down and up do the opposite of what you might expect: "down" means aiming in the positive
    direction.

    Now, the above example does something different:

    forward 5 adds 5 to your horizontal position, a total of 5. Because your aim is 0, your depth does not change.
    down 5 adds 5 to your aim, resulting in a value of 5.
    forward 8 adds 8 to your horizontal position, a total of 13. Because your aim is 5, your depth increases by 8*5=40.
    up 3 decreases your aim by 3, resulting in a value of 2.
    down 8 adds 8 to your aim, resulting in a value of 10.
    forward 2 adds 2 to your horizontal position, a total of 15. Because your aim is 10, your depth increases by 2*10=20
    to a total of 60.
    After following these
    new instructions, you would have a horizontal position of 15 and a depth of 60. (Multiplying these produces 900.)
    """

    def __init__(self):
        self.submarine = Submarine()
        try:
            with open("Data/Day2Data.txt", "r") as f:
                self.data = tuple((Submarine.Commands.__dict__['_value2member_map_'][d.split()[0]],
                                   int(d.split()[1]))
                                  for d in f.read().splitlines())
        except KeyError as e:
            print(f"Invalid Command {e.args}")

    def part1(self):
        for (command, step) in self.data:
            self.submarine.processCommand(command, step)

        return self.submarine.location


class Day3:
    """
    --- Day 3: Binary Diagnostic ---
    The submarine has been making some odd creaking noises, so you ask it to produce a diagnostic report just in case.

    The diagnostic report (your puzzle input) consists of a list of binary numbers which, when decoded properly,
    can tell you many useful things about the conditions of the submarine. The first parameter to check is the power
    consumption.

    You need to use the binary numbers in the diagnostic report to generate two new binary numbers (called the gamma
    rate and the epsilon rate). The power consumption can then be found by multiplying the gamma rate by the epsilon
    rate.

    Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all
    numbers in the diagnostic report. For example, given the following diagnostic report:

    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010

    Considering only the first bit of each number, there are five 0 bits and seven 1 bits. Since the most common bit
    is 1, the first bit of the gamma rate is 1.

    The most common second bit of the numbers in the diagnostic report is 0, so the second bit of the gamma rate is 0.

    The most common value of the third, fourth, and fifth bits are 1, 1, and 0, respectively, and so the final three
    bits of the gamma rate are 110.

    So, the gamma rate is the binary number 10110, or 22 in decimal.

    The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from
    each position is used. So, the epsilon rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the
    epsilon rate (9) produces the power consumption, 198.

    --- Part Two --- Next, you should verify the life support rating, which can be determined by multiplying the
    oxygen generator rating by the CO2 scrubber rating.

    Both the oxygen generator rating and the CO2 scrubber rating are values that can be found in your diagnostic
    report - finding them is the tricky part. Both values are located using a similar process that involves filtering
    out values until only one remains. Before searching for either rating value, start with the full list of binary
    numbers from your diagnostic report and consider just the first bit of those numbers. Then:

    Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard
    numbers which do not match the bit criteria. If you only have one number left, stop; this is the rating value for
    which you are searching. Otherwise, repeat the process, considering the next bit to the right. The bit criteria
    depends on which type of rating value you want to find:

    To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position,
    and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the
    position being considered. To find CO2 scrubber rating, determine the least common value (0 or 1) in the current
    bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values
    with a 0 in the position being considered. For example, to determine the oxygen generator rating value using the
    same example diagnostic report from above:

    Start with all 12 numbers and consider only the first bit of each number. There are more 1 bits (7) than 0 bits (
    5), so keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000,
    and 11001. Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3),
    so keep only the 4 numbers with a 0 in the second position: 10110, 10111, 10101, and 10000. In the third
    position, three of the four numbers have a 1, so keep those three: 10110, 10111, and 10101. In the fourth
    position, two of the three numbers have a 1, so keep those two: 10110 and 10111. In the fifth position,
    there are an equal number of 0 bits and 1 bits (one each). So, to find the oxygen generator rating,
    keep the number with a 1 in that position: 10111. As there is only one number left, stop; the oxygen generator
    rating is 10111, or 23 in decimal. Then, to determine the CO2 scrubber rating value from the same example above:

    Start again with all 12 numbers and consider only the first bit of each number. There are fewer 0 bits (5) than 1
    bits (7), so keep only the 5 numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and 01010. Then,
    consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0 bits (3), so keep only the
    2 numbers with a 1 in the second position: 01111 and 01010. In the third position, there are an equal number of 0
    bits and 1 bits (one each). So, to find the CO2 scrubber rating, keep the number with a 0 in that position:
    01010. As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal. Finally,
    to find the life support rating, multiply the oxygen generator rating (23) by the CO2 scrubber rating (10) to get
    230.

    """

    def __init__(self):
        with open("Data/Day3Data.txt", "r") as f:
            self.data = tuple(f.read().splitlines())
            self.submarine = Submarine()
            self.submarine.processDiagnostic(self.data)

    def part1(self):
        return self.submarine.powerConsumption

    def part2(self):
        return self.submarine.lifeSupportRating


class BingoBoard:
    def __init__(self, board: list[str]):
        self.board = [int(c.strip()) for r in board for c in r.split()]
        self.markTracker = [[False] * 5 for _ in range(5)]
        self.lastNumber = -1

    def printBoard(self):
        pprint.pprint([self.board[0:5]] + [self.board[5:10]] + [self.board[10:15]] +
                      [self.board[15:20]] + [self.board[20:25]])
        pprint.pprint(self.markTracker)

    def checkBingo(self):
        for row in self.markTracker:
            if all(row):
                return True

        for col in map(tuple, zip(*self.markTracker)):
            if all(col):
                return True

        return False

    def processDraw(self, number_drawn):
        if number_drawn in self.board:
            index = self.board.index(number_drawn)
            self.markTracker[(index // 5)][(index % 5)] = True
            if self.checkBingo():
                self.lastNumber = number_drawn
                return True
        return False

    def calculateScore(self):
        score = self._sumOfUnmarkedElements() * self.lastNumber
        self.printBoard()
        return score

    def _sumOfUnmarkedElements(self) -> int:
        unMarkedSum = 0
        for i, a in enumerate(self.board):
            if not self.markTracker[(i // 5)][(i % 5)]:
                unMarkedSum += a

        return unMarkedSum


class Day4:
    """
    --- Day 4: Giant Squid --- You're already almost 1.5km (almost a mile) below the surface of the ocean,
    already so deep that you can't see any sunlight. What you can see, however, is a giant squid that has attached
    itself to the outside of your submarine.

    Maybe it wants to play bingo?

    Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random,
    and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all
    numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

    The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It
    automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input).
    For example:

    7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    22 13 17 11  0
     8  2 23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19

     3 15  0  2 22
     9 18 13 17  5
    19  8  7 25 23
    20 11 10 24  4
    14 21 16 12  6

    14 21 17 24  4
    10 16 15  9 19
    18  8 23 26 20
    22 11 13  6  5
     2  0 12  3  7

    After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are marked as
    follows (shown here adjacent to each other to save space):

    22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
     8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
    21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
     6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
     1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

    After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

    22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
     8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
    21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
     6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
     1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

    Finally, 24 is drawn:

    22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
     8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
    21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
     6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
     1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

    At this point, the third board wins because it has at least one complete row or column of marked numbers (in this
    case, the entire top row is marked: 14 21 17 24 4).

    The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that
    board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board
    won, 24, to get the final score, 188 * 24 = 4512.

    To guarantee victory against the giant squid, figure out which board will win first. What will your final score
    be if you choose that board?

    --- Part Two ---
    On the other hand, it might be wise to try a different strategy: let the giant squid win.

    You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its
    arms, the safe thing to do is to figure out which board will win last and choose that one. That way,
    no matter which boards it picks, it will win for sure.

    In the above example, the second board is the last to win, which happens after 13 is eventually called and its
    middle column is completely marked. If you were to keep playing until this point, the second board would have a
    sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.
    """

    def __init__(self):
        with open("Data/Day4Data.txt", "r") as f:
            self.data = tuple(f.read().split('\n\n'))
            self.rolls = tuple(int(r) for r in self.data[0].split(','))
            self.boards = [BingoBoard(board.split('\n')) for board in self.data[1:]]

    def part1(self):
        for roll in self.rolls:
            for i, board in enumerate(self.boards):
                if board.processDraw(roll):
                    print(board.calculateScore(), roll)
                    exit(0)

    def part2(self):
        boardWon = [False] * len(self.boards)
        for roll in self.rolls:
            for i, board in enumerate(self.boards):
                if board.processDraw(roll):
                    boardWon[i] = True
                    if all(boardWon):
                        print(board.calculateScore(), roll)
                        exit(0)


class LocationMap:
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __repr__(self):
            return f"({self.x}, {self.y})"

    def __init__(self, size):
        self.size = size
        self.data = [[0] * size for _ in range(size)]

    def __repr__(self):
        return '\n'.join(''.join('.' if point == 0 else str(point) for point in d) for d in self.data)

    def markPoint(self, point: Point):
        if point.x >= self.size or point.y >= self.size:
            raise Exception("Point out of Map")

        self.data[point.y][point.x] += 1

    def markPoints(self, points: list[Point]):
        # print(points)
        for point in points:
            self.markPoint(point)

    def markLine(self, start: Point, end: Point):
        self.markPoints(self.pointsInLine(start, end))

    def pointsInLine(self, start: Point, end: Point):
        if start.x == end.x:
            return self._pointsInHorizontalLine(start.x, start.y, end.y)
        elif start.y == end.y:
            return self._pointsInVerticalLine(start.y, start.x, end.x)
        elif abs(start.x - end.x) == abs(start.y - end.y):
            return self._pointsInDiagonalLine(start, end)
        else:
            return []

    @staticmethod
    def _pointsInHorizontalLine(x, y1, y2) -> list[Point]:
        if y1 > y2:
            y1, y2 = y2, y1

        return [LocationMap.Point(x, y) for y in range(y1, y2 + 1)]

    @staticmethod
    def _pointsInVerticalLine(y, x1, x2) -> list[Point]:
        if x1 > x2:
            x1, x2 = x2, x1

        return [LocationMap.Point(x, y) for x in range(x1, x2 + 1)]

    @staticmethod
    def _pointsInDiagonalLine(start: Point, end: Point):
        if start.x > end.x:
            start, end = end, start
        movementY = 1 if start.y < end.y else -1

        return [LocationMap.Point(x, y)
                for x, y in zip(range(start.x, end.x + 1), range(start.y, end.y + movementY, movementY))]


class Day5:
    """
    --- Day 5: Hydrothermal Venture ---

    You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large,
    opaque clouds, so it would be best to avoid them if possible.

    They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input)
    for you to review. For example:

    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2

    Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one
    end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at
    both ends. In other words:

    An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
    For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

    So, the horizontal and vertical lines from the above list would produce the following diagram:

    .......1..
    ..1....1..
    ..1....1..
    .......1..
    .112111211
    ..........
    ..........
    ..........
    ..........
    222111....

    In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the
    number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example,
    comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

    To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap.
    In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

    --- Part Two --- Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture;
    you need to also consider diagonal lines.

    Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal,
    vertical, or a diagonal line at exactly 45 degrees. In other words:

    An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
    An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
    Considering all lines from the above example would now produce the following diagram:

    1.1....11.
    .111...2..
    ..2.1.111.
    ...1.2.2..
    .112313211
    ...1.2....
    ..1...1...
    .1.....1..
    1.......1.
    222111....

    You still need to determine the number of points where at least two lines overlap. In the above example,
    this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.
    """

    def __init__(self):
        with open("Data/Day5Data.txt", "r") as f:
            self.data = [[point.strip().split(',')
                          for point in line.strip().split(' -> ')]
                         for line in f.read().splitlines()]
            self.data = [[LocationMap.Point(int(point[0]), int(point[1])) for point in line]
                         for line in self.data]
            self.locationMap = LocationMap(1000)

    def part1(self):
        for start, end in self.data:
            self.locationMap.markLine(start, end)

        print(self.locationMap)

        return sum(1 for line in self.locationMap.data for point in line if point > 1)
