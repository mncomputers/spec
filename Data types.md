# CPU instruction ID
CPU instructions are encoded in a special way. If a byte is `0xFF`, then the next byte is a part of the number too. Otherwise, it'll be the end of the number. So, the formula is `(255 * amount of FF bytes) + the last byte`. Examples:
|Instruction ID|Bytes (Python `bytes`)|Byte array|Note|
|-|-|-|-|
|0|`b'\x00'`|`[0]`|
|1|`b'\x01'`|`[1]`|
|2|`b'\x02'`|`[2]`|
|3|`b'\x03'`|`[3]`|
...
|254|`b'\xFE'`|`[254]`|
|255|`b'\xFF\x00'`|`[255, 0]`|The first byte is `0xFF` (255). The second byte is taken, and 255 is added to it. Since the second byte is 0, the value is 255.
|256|`b'\xFF\x01'`|`[255, 1]`|Here, the value is 256.
...
|509|`b'\xFF\xFE'`|`[255, 254]`|
|510|`b'\xFF\xFF\x00'`|`[255, 255, 0]`|In this case, the second byte is `0xFF` too. So, the third byte is taken, and `255 * 2 = 510` is added to it.
|511|`b'\xFF\xFF\x01'`|`[255, 255, 1]`|
...


Here's a function to encode and decode it:
```cpp
// the first value of the pair is the array size, the second one is a pointer to the first element of the array
template<typename T>
std::pair<unsigned int, uint8_t *> encode_cpu_instruction(T value) {
    unsigned int arraySize = value / 255;
    arraySize += 1;
    uint8_t * array = new uint8_t[arraySize];
    unsigned int i = 0;
    while (value >= 0xFF) {
        array[i] = 0xFF;
        i += 1;
        value -= 0xFF;
    }
    array[i] = value;
    return std::pair<unsigned int, uint8_t *>(arraySize, array);
}

// you don't need to specify the size here
template<typename T>
T decode_cpu_instruction(uint8_t* array) {
    T value = 0;
    unsigned int i = 0;
    while (true) {
        value += array[i];
        if (array[i] != 0xFF) break;
    }
    return value;
}

// example usage: output the amount of bytes that were used to encode instruction ID 0xFF
std::pair<unsigned int, uint8_t *> value = encode_cpu_instruction(0xFF);
std::cout << "size: " << value.first << std::endl;
// output the byte array in hex
std::cout << std::hex << std::setfill('0');
for (unsigned int i = 0; i < value.first; i++) {
    std::cout << std::setw(2) << unsigned(value.second[i]);
}
std::cout << std::endl;
std::cout << "decoded instruction: " << decode_cpu_instruction(value.second) << std::endl;
delete [] value.second;
```

# (unsigned/signed) Byte
If unsigned or signed is specified, an 8 bit number (1 byte).

The signed integer is represented in [twos complement notation](https://en.wikipedia.org/wiki/Two%27s_complement) (with only one byte).

The unsigned integer is represented by an unsigned binary number (with only one byte).

If unsigned or signed is not specified, it's not a number.

Example: `0xFF`

# [unsigned/signed] short integer
A 16 bit number (2 bytes). 

The signed integer is represented in [twos complement notation](https://en.wikipedia.org/wiki/Two%27s_complement), whose most significant byte is 0, and the least significant is 1.

The unsigned integer is represented by an unsigned binary number whose most significant byte is 0, and the least significant is 1.

Example (unsigned): `b'\xff\xff'` is the number 65535.

Example (signed): `b'\xff\xff'` is the number -1.

# [unsigned/signed] integer
A 32 bit number (4 bytes).

The signed integer is represented in [twos complement notation](https://en.wikipedia.org/wiki/Two%27s_complement), whose most significant byte is 0, and the least significant is 3.

The unsigned integer is represented by an unsigned binary number whose most significant byte is 0, and the least significant is 3.

Example (unsigned): `b'\xff\xff\xff\xff'` is the number 4294967295.

Example (signed): `b'\xff\xff\xff\xff'` is the number -1.

# [unsigned/signed] big integer
A 64 bit number (8 bytes). It's similar to the previous ones:

The signed integer is represented in [twos complement notation](https://en.wikipedia.org/wiki/Two%27s_complement), whose most significant byte is 0, and the least significant is 7.

The unsigned integer is represented by an unsigned binary number whose most significant byte is 0, and the least significant is 7.

Example (unsigned): `b'\xff\xff\xff\xff\xff\xff\xff\xff'` is the number 18446744073709551615.

Example (signed): `b'\xff\xff\xff\xff\xff\xff\xff\xff'` is the number -1.

Example 2 (signed): `b'\x80\x00\x00\x00\x00\x00\x00\x00'` is the number -9223372036854775808.

# Array of X
X repeated a couple of times.
If not mentioned otherwise, the array is length prefixed by an unsigned big integer.

# String with charset X
It's an array of C, where C is the character type for the encoding used.

# Dictionary with K:V
K is the key type, V is the value type. You encode it by first prefixing it with the amount of pairs in the dictionary - it's an unsigned big integer (for good measure, in case you need a dictionary with 18446744073709551615 pairs). You then write the pairs - by writing the key, then the value. You repeat it for all pairs in the dictionary.

Example: K is an unsigned byte. V is an unsigned short. The example dictionary is: `{1: 2}`. It's encoded as `[0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 2]` (`b'\0x00\0x00\0x00\0x00\0x00\0x00\0x00\0x01\0x01\0x00\0x02'`). The second example dictionary is `{1: 69, 25: 123}`. It's encoded as `[0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 69, 25, 0, 123]` (`b'\x00\x00\x00\x00\x00\x00\x00\x02\x01\x00E\x19\x00\x7b'`)