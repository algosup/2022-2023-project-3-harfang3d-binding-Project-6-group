import lib


def bind_test(gen):
	gen.start('my_test')

	lib.bind_defaults(gen)

	# inject test code in the wrapper
	gen.insert_code('''\
// basic interoperability
int return_int() { return 8; }
float return_float() { return 8.f; }
const char *return_const_char_ptr() { return "const char * -> string"; }

static int static_int = 9;

int *return_int_by_pointer() { return &static_int; }
int &return_int_by_reference() { return static_int; }

// argument passing
int add_int_by_value(int a, int b) { return a + b; }
int add_int_by_pointer(int *a, int *b) { return *a + *b; }
int add_int_by_reference(int &a, int &b) { return a + b; }
\n''', True, False)

	gen.add_include('string', True)

	gen.bind_function('return_int', 'int', [])
	gen.bind_function('return_float', 'float', [])
	gen.bind_function('return_const_char_ptr', 'const char *', [])

	gen.bind_function('return_int_by_pointer', 'int*', [])
	gen.bind_function('return_int_by_reference', 'int&', [])

	gen.bind_function('add_int_by_value', 'int', ['int a', 'int b'])
	gen.bind_function('add_int_by_pointer', 'int', ['int *a', 'int *b'])
	gen.bind_function('add_int_by_reference', 'int', ['int &a', 'int &b'])

	gen.finalize()
	return gen.get_output()


test_python = '''\
import my_test

assert my_test.return_int() == 8
assert my_test.return_float() == 8
assert my_test.return_const_char_ptr() == "const char * -> string"

assert my_test.return_int_by_pointer() == 9
assert my_test.return_int_by_reference() == 9

assert my_test.add_int_by_value(3, 4) == 7
assert my_test.add_int_by_pointer(3, 4) == 7
assert my_test.add_int_by_reference(3, 4) == 7
'''

test_lua = '''\
my_test = require "my_test"

assert(my_test.return_int() == 8)
assert(my_test.return_float() == 8)
assert(my_test.return_const_char_ptr() == "const char * -> string")

assert(my_test.return_int_by_pointer() == 9)
assert(my_test.return_int_by_reference() == 9)

assert(my_test.add_int_by_value(3, 4) == 7)
assert(my_test.add_int_by_pointer(3, 4) == 7)
assert(my_test.add_int_by_reference(3, 4) == 7)
'''


test_go = '''\
package mytest

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// Test ...
func Test(t *testing.T) {
	assert.Equal(t, ReturnInt(), 8, "should be the same.")
	assert.Equal(t, ReturnFloat(), float32(8), "should be the same.")
	assert.Equal(t, ReturnConstCharPtr(), "const char * -> string", "should be the same.")

	assert.Equal(t, *ReturnIntByPointer(), 9, "should be the same.")
	assert.Equal(t, *ReturnIntByReference(), 9, "should be the same.")
	
	assert.Equal(t, AddIntByValue(3, 4), 7, "should be the same.")
	a := int32(3)
	b := int32(4)
	assert.Equal(t, AddIntByPointer(&a, &b), 7, "should be the same.")
	assert.Equal(t, AddIntByReference(&a, &b), 7, "should be the same.")
}
'''

test_rust = '''\
use std::ffi::CStr;

include!("../src/bindings.rs");

#[cfg(test)]
mod tests {
    use super::*;

    fn test() {
		unsafe {
			let value = return_const_char_ptr();
			let string = CStr::from_ptr(value).to_str().unwrap();

			let mut x: i32 = 3;
			let mut y: i32 = 4;
			
			assert!(return_int() == 8);
			assert!(return_float() == 8.0);
			assert!(string == "const char * -> string");
			assert!(*return_int_by_pointer() == 9);
			assert!(*return_int_by_reference() == 9);
			assert!(add_int_by_value(3, 4) == 7);
			assert!(add_int_by_pointer(&mut x, &mut y) == 7);
			assert!(add_int_by_reference(&mut x, &mut y) == 7);

		}
	}
}
'''

# Required for the lib to Build
# TODO: Make this global to all tests
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
                if ip == "// basic interoperability"{
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