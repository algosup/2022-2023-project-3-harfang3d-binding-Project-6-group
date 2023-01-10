<p align="center" style="font-weight: bold;font-size: 16px"> Functional Specification </p>

Author: Lucien LAVATINE
[ALGOSUP](https://alGOsup.com/), Group 6. All Rights Reserved.
<hr>

## Introduction

### Stakeholders

- HARFANG 3D
- ALGOSUP
  
### Points of contact

This is the list of the principals points of contact for this project :
Entity | Rank | Name | Mail 
----------|------------- | ------------- | --------
ALGOSUP | Project Manager |  Guillaume Rivière | guillaume.riviere@alGOsup.com
ALGOSUP | Technical Leader |  Quentin Clément | quentin.clement@alGOsup.com
ALGOSUP | Program Manager | Lucien Lavatine | lucien.lavatine@alGOsup.com
HARFANG 3D | Client | Emmanuel Julien   | emmanuel.julien@harfang3d.com
HARFANG 3D | Client | François Gutherz | francois.gutherz@harfang3d.com

### Overview

The duration of this project is 7 weeks, (start January 2, 2023, and end February 17, 2023).

 This project was presented and proposed by HARFANG 3D, a French company working in the software development sector, created in 2016 and founded by Philippe HERBER.
HARFANG 3D have already several projects to their credit such as "Poppy Ergo Jr Digital Twin" which is a robotic arm and controllable by an application, or "DOGFIGHT SANDBOX" which is a virtual reality application, to pilot planes also used by Turkish and Chinese universities to train drones. 

#### Scope of the project

 "FABgen" was created in order to bring the C++ engine to other languages, and to replace SWIG , finding it more and more obsolete for several reasons like :
Very old and complex code base. Language support is written partially in C and SWIG interface files which are almost a language by themselves. The C codebase does everything through a single, object struct hiding the real type of variables making it extremely difficult to debug and extend the SWIG core and uneven feature support between languages with missing features although the target language could support them.
"FABgen" try to resolve that in using python and implement binding definition by themselves, as a newer project "Fabgen" also tries to leverage newer APIs whenever possible.
"FABgen" already supported : Python, Lua, GO and they looking for apply Rust and F#.
Once the Rust binding is added, the Goal will be to try to do something with it on Harfang3D

#### Why use FABgen?
The primary purpose of FABgen is to simplify the task of integrating C/C++ with other programming languages. 
However, why would anyone want to do that? 
To answer that question, it is useful to list a few strengths of C/C++ programming:
Excellent support for writing programming libraries. 
High performance (number crunching, data processing, graphics,etc.) Systems programming and systems integration.
Large user community and software base

#### Personas

```
Name : John Marston
Age : 37
Job : Software Engineer
Description : John has been working in a company for several years now and his company has given
him a new task to redo a project in a new language,so he uses FABgen to switch his code from Lua to GO 
```
```
Name : Archibald Smith
Age : 65 
Job : Senior Software Engineer
Description : Archibald has to work on a new game but for the first time in VR,
so he uses Harfang3D to understand the trajectory data and how it works 
```

### Functionalities 

we have to add a binding in Rust, to use it on Harfang3D

### Testing 

The tests will be done in the same way as the other bindings, so directly on FABgen 

#### Assumptions and Constraints 

Future events that are out of the project's control and whose results affect its success are called assumptions. Project limitations that are outside the project team's control are known as constraints. For this project, the following presumptions and restrictions apply.

#### Assumptions

- The more languages that are available, the more users there will be and it will grow and may even evolve in the future because everyone can use it, so they can help the project and make suggestions.

#### Constraints

- The binding generates errors on other bindings.
- The binding may not work with all versions of the language.
- The binding can be slower than other bindings.
- The binding needs to be as easy to use as the others bindings.

#### Glossary 

- Binding : In programming, binding is an application programming interface  that provides glue code specifically made to allow a programming language to use a foreign library or operating system service
- VR (Virtual Reality) : is a computer-generated environment with scenes and objects that appear to be real, making the user feel they are immersed in their surroundings. This environment is perceived through a device known as a Virtual Reality headset or helmet.
- Python :is an interpreted, object-oriented, high-level programming language with dynamic semantics developed by Guido van Rossum.
- F# : is a universal programming language for writing succinct, robust and performant code.
- C++ : It was developed as a cross-platform improvement of C to provide developers with a higher degree of control over memory and system resources.
- GO : also known as GOlang, is an open-source, compiled, and statically typed programming language designed by GOogle. It is built to be simple, high-performing, readable, and efficient.
- SWIG : is an open-source software tool used to connect computer programs or libraries written in C or C++ with scripting languages such as Lua, Perl, PHP, Python, R, Ruby, Tcl, and other languages like C# ...
- Rust : is a statically-typed programming language designed for performance and safety, especially safe concurrency and memory management. Its syntax is similar to that of C++.
- Lua : is a robust, lightweight, and embeddable scripting language that supports multiple programming methods, including procedural, object-oriented, functional, and data-driven programming
