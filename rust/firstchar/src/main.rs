use std::io;

fn main() {
    println!("Hello, world!");

    let mut input = String::new();
    io::stdin().read_line(&mut input)
        .expect("Failed to read line");

    let firstchar = input.trim().chars().next().unwrap_or('\0');

    println!("{firstchar}");
}
