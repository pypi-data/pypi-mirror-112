use pyo3::prelude::*;

/// Capcha solver for day 1 of the 2017 Advent Of Code
//
// In Rust:
// ```
// use std::fs;
// use advent_of_code_2017_day_1::Capcha;
// fn main() {
//     let input = fs::read_to_string("input.txt").unwrap();
//     let cap = Capcha::new(input);
//     println!(
//         "The results are part1: {} and part2: {}",
//         cap.part1(),
//         cap.part2()
//     );
// }
// ```
// 
// In Python:
// ```
// import advent_of_code_2017_day_1 as aoc  
// input = open("input.txt").read();  
// cap = aoc.Capcha(input)  
// print(  
//     "The results are part1: {0} and part2: {1}".format( \  
//         cap.part1(),\  
//         cap.part2()\  
// ))  
// ```
#[pyclass]
pub struct Capcha {
    input: String,
} 

#[pymethods]
impl Capcha {
    /// Creates a solver for a new capcha
    ///
    /// # Examples
    ///
    /// ```
    /// use advent_of_code_2017_day_1::Capcha; 
    /// let input = String::from("1122");
    /// let cap = Capcha::new(input);
    /// assert_eq!(cap.part1(),3);
    /// ```
    #[new]
    pub fn new(input: String) -> Capcha {
        Capcha { input }
    }

    /// Finds solution to part1 style capcha
    ///
    /// The captcha requires you to review a sequence of digits 
    /// (your puzzle input) and find the sum of all digits that 
    /// match the next digit in the list. The list is circular, 
    /// so the digit after the last digit is the first digit in 
    /// the list.
    ///
    /// For example:
    /// - 1122 produces a sum of 3 (1 + 2) because the first digit 
    ///   (1) matches the second digit and the third digit (2) matches 
    ///   the fourth digit.
    /// - 1111 produces 4 because each digit (all 1) matches the next.
    /// - 1234 produces 0 because no digit matches the next.
    /// - 91212129 produces 9 because the only digit that matches 
    ///   the next one is the last digit, 9.
    pub fn part1(&self) -> u32 {
        let mut chars = self.input.chars();
        let mut last = chars.next().unwrap();

        let mut count = 0;
        for c in chars {
            if c == last {
                count += c.to_digit(10).unwrap();
            }
            last = c;
        }
        if self.input.chars().next().unwrap() == last {
            count += last.to_digit(10).unwrap();
        }
        count
    }

    /// Finds solution to part2 style capcha
    ///
    /// Now, instead of considering the next digit, it wants you 
    /// to consider the digit halfway around the circular list. 
    /// That is, if your list contains 10 items, only include a 
    /// digit in your sum if the digit 10/2 = 5 steps forward matches 
    /// it. Fortunately, your list has an even number of elements.
    ///
    /// For example:
    ///
    /// - 1212 produces 6: the list contains 4 items, and all four 
    ///   digits match the digit 2 items ahead.
    /// - 1221 produces 0, because every comparison is between a 1 and a 2.
    /// - 123425 produces 4, because both 2s match each other, but 
    ///   no other digit has a match.
    /// - 123123 produces 12.
    /// - 12131415 produces 4.
    pub fn part2(&self) -> u32 {
        let half =  self.input.len()/2;
        let chars1 = self.input[0..half].chars();
        let chars2 = self.input[half..].chars();

        let mut count = 0;
        for (c1,c2) in chars1.zip(chars2) {
            if c1 == c2 {
                count += c1.to_digit(10).unwrap();
            }
        }
        count * 2 
    }
}

#[pymodule]
fn advent_of_code_2017_day_1(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Capcha>()?;
    Ok(())
}

#[cfg(test)]
mod part1 {
    use crate::Capcha;

    #[test]
    fn test_1122() {
        let input = String::from("1122");
        let cap = Capcha::new(input);

        assert_eq!(cap.part1(),3);
    }
    #[test]
    fn test_1111() {
        let input = String::from("1111");
        let cap = Capcha::new(input);

        assert_eq!(cap.part1(),4);
    }
    #[test]
    fn test_1234() {
        let input = String::from("1234");
        let cap = Capcha::new(input);

        assert_eq!(cap.part1(),0);
    }
    #[test]
    fn test_91212129() {
        let input = String::from("91212129");
        let cap = Capcha::new(input);

        assert_eq!(cap.part1(),9);
    }
}

#[cfg(test)]
mod part2 {
    use crate::Capcha;

    #[test]
    fn test_1212() {
        let input = String::from("1212");
        let cap = Capcha::new(input);

        assert_eq!(cap.part2(),6);
    }
    #[test]
    fn test_1221() {
        let input = String::from("1221");
        let cap = Capcha::new(input);

        assert_eq!(cap.part2(),0);
    }
    #[test]
    fn test_123425() {
        let input = String::from("123425");
        let cap = Capcha::new(input);

        assert_eq!(cap.part2(),4);
    }
    #[test]
    fn test_123123() {
        let input = String::from("123123");
        let cap = Capcha::new(input);

        assert_eq!(cap.part2(),12);
    }
    #[test]
    fn test_12131415() {
        let input = String::from("12131415");
        let cap = Capcha::new(input);

        assert_eq!(cap.part2(),4);
    }
}