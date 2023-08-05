use std::fs;

use advent_of_code_2017_day_1::Capcha;

fn main() {
    let input = fs::read_to_string("input.txt").unwrap();
    let cap = Capcha::new(input);
    println!(
        "The results are part1: {} and part2: {}",
         cap.part1(),
         cap.part2()
    );
}
