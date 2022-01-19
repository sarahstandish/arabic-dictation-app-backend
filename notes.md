# General notes
- *Code points* are the basic elements of unicode, kind of like characters
  - They are identified by number
  - They are usually written in hexadecimal with the prefix "U+", which represents their index in the code space
  - All listed in the unicode character database: http://www.unicode.org/reports/tr44/
  - The *codespace* is the set of all possible code points
    - Only about 12% has been assigned so far
  - The *basic multilingual plane* contains all the characters needed for modern text in any script, including Arabic
    - This was part of the original 16-bit encoding; Unicode was later expanded when that was insufficient
  - *endianness* is the pattern for byte-ordering.  *Big endian* means that the most significant byte comes first, and *little endian* means that the least significant byte comes first.
  - *Dynamically composing* characters means combining multiple code points together, such as combining diacritics with a letter of the alphabet (this prevents a "combinatorial explosion").  This is what enables certain symbols to be automatically stacked over or under a character.  This is used in *vowel pointing notation* in Arabic.
- *Canonically equivalent* strings are strings in which diacritics have been applied in different orders, but look visually the same.  This can happen when more than one diacritic is applied to the same letter, but the appearance is not changed (e.g. شدة and فتحة appearing on the same letter).  Canonically equivalent strings are supposed to be treated as identical for purposes of searching, sorting, rendering, etc.  This m eans that if you have a "find in file" operation in an app and a user searches for بَّ, the user should be able to find any combination of characters.
- *Normalization forms* are ways of converting strings into a canonical form so they can be compared code-point-to-code-point or byte-to-byte
  - *NDF normalization* decomposes every character down to its component base and combining marks, taking apart any precomposed code points in the string
  - *NFC normalization* puts items together into precomposed code points as much as possible
- *Grapheme clusters* are basically combinations of letters & diacritics which combine to what the user would perceive as a character, and is mainly used for editing because it points to a logical place to put a cursor.
- 
# Encoding
- *UTF* or *Unicode Transformation Format* is a system to map Unicode code points into sequences of 'termed code values' (still not sure what that means)
- *UTF-8* is the most popular
  - Designed for backwards compatibilit with ASCII encoding.  
  - Takes a different amount of space for differe characters: one byte for English letters and symbols and two bytes for Latin and Middle Eastern characters; characters can take up to 4 bytes.
  - Two-byte code points range from U+0080 to U+07FF
  - Works well with string-programming conventions like delimiters, because ASCII bytes never occur inside the encoding of non-ASCII code points
  - However, it might cause some issues when iterating over 'characters' in a string--it will need to decode UTF-8 and iterate over code points, not bytes. 
  - When you measure the length of a string, you'll need to think about whether you want the length in bytes, code points, the width of the text when rendered, or something else.
- *UTF-16* uses 16-bit characters.  
  - A descendant of the transition from the original Unicode code space where unicode was supposed to be all 16-bits
  - This is the standard string representation in JavaScript
  - Can be stored as either big-endian or little-endian
  - When using UTF-16, Unicode recommends putting a *byte-order mark* at the top of the page to signify which endianness is being used, however, this can cause problems when using UTF-8. For UTF-16, `U+FEFF` may be placed as the first character of a file or character stream for this purpose.
- *UTF-32* 32-bit integer encoding
  - Encodes all characters using 4 bytes, which adds up to a lot of additional memory and ultimately performance concerns.
  - This is rarely used for storage; it might be used as a temporary internal representation for examining or operating on the code points in a string.

Sources:
https://www.reedbeta.com/blog/programmers-intro-to-unicode/ (2017)