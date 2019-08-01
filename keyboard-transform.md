# keyboard-transform

Write a program that maintains the state of a 10x4 subset of the keyboard.  From left to right:

    1 -> 0 (10 keys)
    q -> p (10 keys)
    a -> ; (10 keys)
    z -> / (10 keys)

Given these keys, you could apply various transforms:

    H - horizontal mirror (about Y-axis)
    V - vertical mirror (about X-axis)
    N - Keys shifted by right (+N) or left (-N)

Given an input string and a string representing a transform, what would the output look like on this transformed keyboard?

    For a horizontal (H) flip: 1 becomes 0, 2 becomes 9, ... , q becomes p, w becomes o
    For a vertical (V) flip: 1 becomes z, q becomes a, ..., 0 becomes /, p becomes ; and Q remains Q (not in transform list)
    A +-ive shift: 1 becomes 2, 2 becomes 3, ... / becomes 1 (wrap around)
    A -ive shift: 1 becomes /, 2 becomes 1, ...

Example transforms:

    Transform "Hello" by H V -1  and you get "Hjqqa".
    Transform "Hello" by H V V H and you get "Hello" (identity transform)

1. Write a program that can transform any string given list of transformations.
2. Can you think of any optimizations? 
3. What order complexity, O(n), is your program? 

Take as long as (or little) time as you like. Tell us how long it took you, what took you the longest time.