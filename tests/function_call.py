import lib


def bind_test(gen):
	gen.start('my_test')

	lib.bind_defaults(gen)

	# inject test code in the wrapper
	gen.insert_code('''\
int get_int() { return 8; }

int get() { return 0; }
int get(int v) { return v / 2; }
int get(int v, int k) { return v * k; }
int get(int v, int k, int b) { return v * k + b; }

static int global_int = 0;

void set_global_int() { global_int = 8; }
int get_global_int() { return global_int; }

int get_global_int_multiplied(int k = 5) { return 3 * k; }

void get_modify_arg_in_out(int &v, int k=5) { v = 3 * k + v; }
''', True, False)

	gen.bind_function('get_int', 'int', [])
	gen.bind_function_overloads('get', [
		('int', [], []),
		('int', ['int v'], []),
		('int', ['int v', 'int k'], []),
		('int', ['int v', 'int k', 'int b'], [])
	])

	gen.bind_function('set_global_int', 'void', [])
	gen.bind_function('get_global_int', 'int', [])

	gen.bind_function('get_global_int_multiplied', 'int', ['?int k'])

	gen.bind_function('get_modify_arg_in_out', 'void', ['int &v', '?int k'], {'arg_in_out': ['v']})

	gen.finalize()
	return gen.get_output()


test_python = '''\
import my_test

assert my_test.get_int() == 8

assert my_test.get_global_int() == 0
my_test.set_global_int()
assert my_test.get_global_int() == 8

# overload
assert my_test.get() == 0
assert my_test.get(2) == 1
assert my_test.get(4, 3) == 12
assert my_test.get(4, 3, 2) == 14

# optional argument
assert my_test.get_global_int_multiplied() == 15
assert my_test.get_global_int_multiplied(2) == 6
'''

test_lua = '''\
my_test = require "my_test"

assert(my_test.get_int() == 8)

assert(my_test.get_global_int() == 0)
my_test.set_global_int()
assert(my_test.get_global_int() == 8)

-- overload
assert(my_test.get() == 0)
assert(my_test.get(2) == 1)
assert(my_test.get(4, 3) == 12)
assert(my_test.get(4, 3, 2) == 14)

-- optional argument
assert(my_test.get_global_int_multiplied() == 15)
assert(my_test.get_global_int_multiplied(2) == 6)
'''

test_go = '''\
package mytest

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Test ...
func Test(t *testing.T) {
	assert.Equal(t, GetInt(), int32(8), "should be the same.")

	assert.Equal(t, GetGlobalInt(), int32(0), "should be the same.")

	SetGlobalInt()
	assert.Equal(t, GetGlobalInt(), int32(8), "should be the same.")

	// overload
	assert.Equal(t, Get(), int32(0), "should be the same.")
	assert.Equal(t, GetWithV(2), int32(1), "should be the same.")
	assert.Equal(t, GetWithVK(4, 3), int32(12), "should be the same.")
	assert.Equal(t, GetWithVKB(4, 3, 2), int32(14), "should be the same.")

	// optional argument
	assert.Equal(t, GetGlobalIntMultiplied(), int32(15), "should be the same.")
	assert.Equal(t, GetGlobalIntMultipliedWithK(2), int32(6), "should be the same.")

	// argument in out
	v := int32(2)
	GetModifyArgInOut(&v)
	assert.Equal(t, v, int32(17), "should be the same.")

	v = int32(2)
	GetModifyArgInOutWithK(&v, 4)
	assert.Equal(t, v, int32(14), "should be the same.")
}
'''

test_rust = '''\

	include!("../src/bindings.rs");

	#[cfg(test)]
	mod tests {
		use super::*;

		fn test() {
			unsafe {
				assert_eq!(get_int(), 8);

				assert_eq!(get_global_int(), 0);
				set_global_int();
				assert_eq!(get_global_int(), 8);

				// overload
				assert_eq!(get(), 0);
				assert_eq!(get1(2), 1);
				assert_eq!(get2(4, 3), 12);
				assert_eq!(get3(4, 3, 2), 14);

				// optional argument
				//assert_eq!(get_global_int_multiplied(), 15);
				assert_eq!(get_global_int_multiplied(2), 6);
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
                if ip == "int get_int() { return 8; }"{
                    flag = true;
                }
                if ip == "// type_tag based cast system"{
                    flag = false;
                }
                if flag{
                    if ip != "static int global_int = 0;"{
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