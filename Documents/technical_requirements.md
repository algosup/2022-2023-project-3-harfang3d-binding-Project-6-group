<h1 style="text-align: center">2022-2023-project-3-harfang3d-binding-Project-6-group</h1>

<details> 
<summary style="text-decoration: underline; font-size:150%">Table of contents:</summary>

- [1. Front matter](#1-front-matter)
- [2. Introduction](#2-introduction)
  - [a. Overview](#a-overview)
  - [b. Glossary](#b-glossary)
  - [c. Context or Background](#c-context-or-background)
  - [d. Product and Technical Requirements](#d-product-and-technical-requirements)
  - [e. Future Goals](#e-future-goals)
  - [f. Assumptions](#f-assumptions)
- [3. Solutions](#3-solutions)
  - [a. Existing Solution](#a-existing-solution)
  - [b. Features/functions to implement](#b-featuresfunctions-to-implement)
  - [c. Release / Roll-out and Deployment Plan](#c-release--roll-out-and-deployment-plan)
  - [d. Alternate Solutions](#d-alternate-solutions)
- [4. Further Considerations](#4-further-considerations)
  - [a. Contact with the client](#a-contact-with-the-client)
  - [b. Impact on the company](#b-impact-on-the-company)
- [5. Project Management](#5-project-management)
  - [a. Prioritization](#a-prioritization)
  - [b. Milestones](#b-milestones)
- [6. End Matter](#6-end-matter)
  - [a. References](#a-references)
  - [b. Acknowledgement](#b-acknowledgement)
</details>

--- 

# 1. Front matter

Client: [Harfang3D](https://www.harfang3d.com/)

| Role              | Name                                                                                                                                                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Project Manager   | [RIVIÈRE Guillaume](https://github.com/Guillaume-Riviere)                                                                                                                                    |
| Program Manager   | [LAVATINE Lucien](https://github.com/LucienLAVATINE)                                                                                                                                                                                           |
| Technical Leader  | [CLÉMENT Quentin](https://github.com/Quentin-Clement)                                                                                                                                                                                           |
| Software Engineer | [LEMOINE Arthur](https://github.com/arthur-lemo1ne)                                                                                                                                                                                     |
| Q&A               | [CATON CLÉMENT](https://github.com/ClementCaton) |

Author: Quentin CLEMENT 
<br>
Created on: 01/03/2023

# 2. Introduction

## a. Overview

Fabgen is a set of Python scripts to generate C++ binding code to different languages. It was deveeloped by **Harfang3D**.
It was written as a SWIG replacement for the Harfang Multimedia Framework.

Currently, you can generate bindings for the following languages:
- Python
- Lua
- GO

They now want to implement 2 new languages, Rust and F#.

Our team will work on the Rust implementation.

## b. Glossary
| Terms                        | Definition             |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Binding| Data binding, the technique of connecting two data elements together|
| SWIG| SWIG is a software development tool that connects programs written in C and C++ with a variety of high-level programming languages.|
| Software| The term software is used to describe software that enables your computer to operate and handles data processing. Several software are installed on your device to give commands, so that specific tasks are performed according to their uses.|
| C, C++, Python, Lua, GO, Rust, F#| Programming languages|
| AI| The theory and development of computer systems able to perform tasks normally requiring human intelligence, such as visual perception, speech recognition, decision-making, and translation between languages.|


## c. Context or Background

At the moment, Fabgen can generate binding for only 3 languages. But there are so many languages used, that it would be useful to add more to the list.

## d. Product and Technical Requirements

The Rust implementation in Fabgen need to be similar to previous languages already implemented. In particular GO which is the most similar language to Rust. The same features will be brought. Ideas for improvement will be welcome to improve the previous languages such as GO where there are still some problems with the bindings.

## e. Future Goals

Harfang3D will be able to generate bindings for more languages.

## f. Assumptions

Make a perect translation of the code from one language to another without the need of the rechecking/correction of the code by a human.
  
# 3. Solutions
## a. Existing Solution

SWIG: an open source software tool, allowing to connect software or software libraries written in C/C++ with scripting languages such as: Tcl, Perl, Python, Ruby, PHP, Lua or other programming languages like Java, C#, Scheme and OCaml.
Facebook’s TransCoder AI:  Trained AI capable to understand the code in a different language and able to convert the code from one language to another.

## b. Features/functions to implement

**Generated code has no dependencies and is human readable.** <br>
**Generator input is a Python script.** <br>
**Customizable type conversion from C++ and back.** <br>
**Can bind many C++ construct (function/data members, static function/data members, exceptions, etc...).** <br>
**User specifiable bound name.** <br>
**Types can be hidden from the generated binding interface.** <br>
**Feature mechanism to extend types and prototypes such as:** <br>
- arg_out, arg_in_out to support output arguments.
- route to route methods to a customizable expression.
- proxy to support wrapper types such as std::shared_ptr. <br>
**Extern type support to "link" C++ types shared by different bindings.** <br>
**Simple and hopefully easy to dive into codebase.**

## c. Release / Roll-out and Deployment Plan

At the end of the 6 weeks, **Harfang3D** will check if the software is perfectly working. They will also look at the code to confirm everything correspond to what they wanted. If they are satisfied, they will deploy a new version of Fabgen with the new languages implemented in it. After that, the users will be able to use the new features of Fabgen in their projects.

## d. Alternate Solutions 

Instead of using bindings, it could be another solution to use an AI. Instead of translating the whole code, the AI would be able to understand the logic of the code and the . It could also allow to improve some parts of the code when the writing is not optimal and better things could be brought to achieve the same goal. However, this solution is more complicated to set up because it would be too long to develop and it would be too expensive.

# 4. Further Considerations

## a. Contact with the client

The developers of Harfang3D are the one who created Fabgen and implemented the 3 first languages. If we have questions are problems, we can contact them by email. They want to know the progress of the project every week. We can use these emails to ask for help. We can also ask them if we have an idea about something out of the requirements.

## b. Impact on the company

Fabgen is an important project for **Harfang3D** because it's the development of a software which is out of their principle scope of action. By improving their library, they will attract more users so more visibility and get into a new possible market. Afterwards, it will help them to get more clients and to develop their business.

# 5. Project Management
## a. Prioritization
(F0=urgent & F2=not urgent)
| Function                        | Flexibility         |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Example| F0 |

## b. Milestones

- **1st week:**
Run test and finish documents
- **2nd week:**
- **3rd week:**
- **4rd week:**
- **5th week:**
- **6th week:**

# 6. End Matter

## a. References


## b. Acknowledgement
