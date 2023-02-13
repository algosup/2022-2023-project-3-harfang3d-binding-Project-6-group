import lib


def bind_test(gen):
	gen.start('my_test')

	lib.bind_defaults(gen)

	gen.insert_code('''
int *return_nullptr() { return nullptr; }
''')
	gen.bind_function('return_nullptr', 'int *', [])

	gen.finalize()
	return gen.get_output()


test_python = '''\
import my_test

v = my_test.return_nullptr()
assert v is None
'''

test_lua = '''\
my_test = require "my_test"

v = my_test.return_nullptr()
assert(v == nil)
'''

test_go = '''\
package mytest

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// Test ...
func Test(t *testing.T) {	
	v := ReturnNullptr()
	assert.Nil(t, v, "should be nil.")
}
'''


test_rust = '''\
include!("../src/bindings.rs");

#[cfg(test)]
mod tests {
    use super::*;

	#[test]
    fn test() {
		unsafe {
			let v = return_nullptr();
			assert_eq!(v.is_null(), true);
		}
	}
}
'''
build_rust = '''\
use std::env;
use std::path::PathBuf;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::fs::OpenOptions;
use std::io::Write;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn extract_what_we_want()-> String{
    let mut result = "".to_owned();
    if let Ok(lines) = read_lines("./cpp/fabgen.cpp") {
        // Consumes the iterator, returns an (Optional) String
        let mut flag = false;
        for line in lines {
            
            if let Ok(ip) = line {
                if ip == "int *return_nullptr() { return nullptr; }"{
                    flag = true;
                }
                if ip == "// type_tag based cast system"{
                    flag = false;
                }
                if flag{
                    if ip != "static int static_int = 9;"{
                        result.push_str(&ip);
                        result.push_str("\n");
                    }
                }
            }
        }
    }
    result
}

fn get_rid_of_mustach(mut text: String) -> String{
    let mut flag = false;
    //println!("{}", text);
    let mut i = 0;
    while i < text.len() {
        if text.chars().nth(i).unwrap() == '{'{
            flag = true;
        }
        if text.chars().nth(i).unwrap() == '}'{
            flag = false;
            text.replace_range(i..i+1, ";");
        }
        if flag{
            text.replace_range(i..i+1, "");
            i-=1;
        }
        i += 1;
    }
	i = 0;
    while i < text.len() {
        if text.chars().nth(i).unwrap() == '='{
            flag = true;
        }
        if text.chars().nth(i).unwrap() == ')' || text.chars().nth(i).unwrap() == ','{
            flag = false;
        }
        if flag{
            text.replace_range(i..i+1, "");
            i-=1;
        }
        i += 1;
    }
    text
}

fn main() {

    let text = get_rid_of_mustach(extract_what_we_want());
    let mut file = OpenOptions::new().append(true).open("./cpp/fabgen.h").expect("cannot open file");
    file.write_all(text.as_bytes()).expect("write failed");
    println!("file append success");

    println!("cargo:rerun-if-changed=fabgen.h");
    let src = ["cpp/fabgen.cpp"];

    cc::Build::new()
        .cpp(true)
        .files(src.iter())
        .compile("mybar");

    let bindings = bindgen::Builder::default()
        .header("cpp/fabgen.h")
        .layout_tests(false)
        .clang_arg("-xc++").clang_arg("-std=c++11").clang_arg("-Wc++11-extensions")
        //.clang_arg("-Ivendor/cpp")
        // .allowlist_function("barfunc")
        .generate()
        .expect("Unable to generate bindings");

    let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    bindings
        .write_to_file(out_path.join("bindings.rs"))
        .expect("Couldn't write bindings!");

    // write bindings in src/bindings.rs
    bindings.write_to_file("src/bindings.rs").expect("Couldn't write bindings!");
}

'''