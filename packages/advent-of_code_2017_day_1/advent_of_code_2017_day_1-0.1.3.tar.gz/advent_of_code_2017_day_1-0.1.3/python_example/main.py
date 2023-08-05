import advent_of_code_2017_day_1 as aoc

input = open("input.txt").read();
cap = aoc.Capcha(input)
print( \
    "The results are part1: {0} and part2: {1}".format(
        cap.part1(),\
        cap.part2()\
))