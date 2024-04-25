The way how CPU instruction IDs are encoded is described in the `Data types` section.

The data from the "BIOS" memory chip is loaded into the RAM at address 0.

The instructions are encoded by just putting the instruction ID, then the arguments, right after each other without any additional separation.

# Instructions

## Nothing -> 0
Does nothing.

## Jump (unsigned big int) -> 1
Jumps to an address represented by an unsigned big int
|Argument name|Data type|Purpose|
|-------------|---------|-------|
|Address|Unsigned big int|The location to jump to|

## Copy data -> 2
Copy data from one memory location to an another one
|Argument name|Data type|Purpose|
|-------------|---------|-------|
|Source address|Unsigned big int|The source address to copy from|
|Destination address|Unsigned big int|The location to copy to|
|Amount of bytes|Unsigned big int|The amount of bytes to copy|

## Erase memory -> 3
Erases a specific amount of bytes at a specified memory location
|Argument name|Data type|Purpose|
|-------------|---------|-------|
|Source address|Unsigned big int|The source address to start erasing bytes from|
|Amount of bytes|Unsigned big int|The amount of bytes to erase|


<!--?generate
output = ""
int_types = ["unsigned byte", "signed byte", "unsigned short", "signed short", "unsigned int", "signed int", "unsigned big int", "signed big int"]
instruction_id = 4
for x in int_types:
    output += f"""## Add ({x}) -> {instruction_id}
Adds 2 numbers together
|Argument name|Data type|Purpose|
|-------------|---------|-------|
|Address of the first number|{x}|The first number|
|Address of the second number|{x}|The second number|
|Address of the result|{x}|The result|

"""
    output += f"""## Subtract ({x}) -> {instruction_id + 1}
Subtracts numbers.
|Argument name|Data type|Purpose|
|-------------|---------|-------|
|Address of the first number|{x}|The first number|
|Address of the second number|{x}|The second number|
|Address of the result|{x}|The result|

"""
    output += f"""## Multiply ({x}) -> {instruction_id + 2}
Multiplies 2 numbers
|Argument name|Data type|Purpose|
|-------------|---------|-------|
|Address of the first number|{x}|The first number|
|Address of the second number|{x}|The second number|
|Address of the result|{x}|The result|

"""
    output += f"""## Divide ({x}) -> {instruction_id + 3}
Divides 2 numbers
|Argument name|Data type|Purpose|
|-------------|---------|-------|
|Address of the first number|{x}|The first number|
|Address of the second number|{x}|The second number|
|Address of the result|{x}|The result|

"""
    output += f"""## Remainder ({x}) -> {instruction_id + 4}
Finds the remainder after dividing 2 numbers.
|Argument name|Data type|Purpose|
|-------------|---------|-------|
|Address of the first number|{x}|The first number|
|Address of the second number|{x}|The second number|
|Address of the result|{x}|The result (remainder)|

"""
    instruction_id += 5

set_output(output.removesuffix("\n\n"))
-->