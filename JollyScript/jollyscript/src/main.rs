use std::env;
use std::fs;
use std::time::Instant;

#[derive(Clone, Copy)]
struct Node {
    x: usize,
    y: usize,
    direction: usize, // 0: left, 1: right
}

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: {} <filename>", args[0]);
        std::process::exit(1);
    }

    let filename = &args[1];

    let contents = fs::read_to_string(filename).expect("Read error");

    let time_start = Instant::now();

    let lines: Vec<&str> = contents.lines().collect();

    //println!("{:#?}", lines);

    let mut node = Node {
        x: 0,
        y: lines[0].len() - 1,
        direction: 0,
    };

    let mut stack: Vec<i32> = Vec::new();
    let mut pending_nodes: Vec<Node> = Vec::new();
    let mut printing = false;
    let mut remembered_location = Node {
        x: 0,
        y: 0,
        direction: 0,
    };

    let mut commands: Vec<char> = Vec::new();

    while let Some(current_line) = lines.get(node.x) {
        if let Some(ch) = current_line.chars().nth(node.y) {
            //println!("{:#?}", node);
            commands.push(ch);

            if printing && ch != '"' {
                print!("{}", ch);
            } else {
                match ch {
                    '*' => {}
                    '/' => node.direction = 0,
                    '\\' => node.direction = 1,
                    '^' => {
                        pending_nodes.push(Node {
                            x: node.x + 1,
                            y: node.y + 1,
                            direction: 1,
                        });
                        node.direction = 0;
                    }
                    '"' => printing = !printing,
                    '{' => remembered_location = node,
                    '}' => {
                        node = Node {
                            x: remembered_location.x,
                            y: remembered_location.y,
                            direction: node.direction,
                        };
                        continue;
                    }
                    '~' => {
                        if let Some(next_node) = pending_nodes.pop() {
                            node = next_node;
                            continue;
                        } else {
                            break;
                        }
                    }
                    'n' => println!(),
                    ':' => {
                        if let Some(&last) = stack.last() {
                            stack.push(last);
                        }
                    }
                    '%' => {
                        if stack.len() >= 2 {
                            let len = stack.len();
                            stack.swap(len - 2, len - 1);
                        }
                    }
                    '+' => {
                        if stack.len() >= 2 {
                            let a = stack.pop().unwrap();
                            let b = stack.pop().unwrap();
                            stack.push(a + b);
                        }
                    }
                    '-' => {
                        if stack.len() >= 2 {
                            let a = stack.pop().unwrap();
                            let b = stack.pop().unwrap();
                            stack.push(b - a);
                        }
                    }
                    '?' => {
                        if let Some(last) = stack.last_mut() {
                            if *last == 0 {
                                node.direction = 0;
                            } else {
                                node.direction = 1;
                                *last -= 1;
                            }
                        }
                    }
                    '$' => {
                        stack.pop();
                    }
                    '.' => {
                        if let Some(last) = stack.last() {
                            print!("{:x}", *last);
                        }
                    }
                    'A'..='F' => {
                        stack.push((ch as u8 - b'A' + 10) as i32);
                    }
                    '0'..='9' => {
                        stack.push((ch as u8 - b'0') as i32);
                    }
                    _ => {}
                }
            }

            node.x += 1;
            if node.direction == 0 {
                node.y -= 1
            } else {
                node.y += 1
            };
        } else {
            break;
        }
    }
    let time_end = Instant::now();
    println!(
        "Execution complete, took: {:#?}",
        time_end.duration_since(time_start)
    );
}
