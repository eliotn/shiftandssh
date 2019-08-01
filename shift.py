"""# keyboard-transform

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

Take as long as (or little) time as you like. Tell us how long it took you, what took you the longest time."""


"""
V-V+
Optimization
V only matters in terms of N%2 as only horrizontal orientation is changed
1234567890
0987654321

Not true, here for reference on how it isn't
H-H+
1234567890../ - normal
0987654321 - reversed
9876543210 - +1 reversed
0123456789 - +1 normal
9012345678 - +2 normal

Horrizontal when flipped flips meaning of plus and minus

Real
String
1.../
V flip swap - swap first 10 with last 10 second 10 with 3rd 10
[ 4 ][ 3 ][ 2 ][ 1 ]
H flip reverse each section
[   ][   ][   ][   ]

- Two V flips are identical  V V
- Two H flips are identical  H H
- do H%2 H flips and V%2 V flip
- sum together + and - on each step
- Algorithm
3 Mappings:
1. Start with a keyboard
Constant keyboard to index
2. Constant Index to keyboard.
3. transformation array that translates the keyboard
"""

""" 45 minutes first session """
""" At 2 hours """

""" 
This can be done in
O(N + S) Time where N is length of char array and S is length of shift array
-Minimum bound in worst case because all characters in transform and all letters need to be read
O(1) Auxillary space

Things to note for minor optimizations
#1. transformation array will always have 10 repeating numbers
Incremented by 10 on each section.

"""
#generate keyboard translation
#we can represent them as 40 numbers
#transformation with translating 
#Things to note:
global keyboard, keys
keyboard = "1234567890qwertyuiopasdfghjkl;zxcvbnm,./"
keys = {keyboard[i]:i for i in range(40)}
def shift(_string, transform):
    global orig
    #transform to new keyboad index, starts as identity
    orig = range(40)
    #flip and shift transforms can be aggregated
    def executeTransform(transform, data, orig):
        if transform == None:
            return orig
        if transform == 'flip':
            flipV, flipH = data
            #order doesn't matter
            if flipV:
                #reverse order of buckets [0-9][10-19][20-29][30-39]
                #to [30-39][20-29][10-19][0-9]
                orig = orig[30:40] + orig[20:30] + orig[10:20] + orig[0:10]
            if flipH:
                #reverse order inside of buckets [0-9][10-19][20-29][30-39]
                orig = orig[9::-1] + orig[19:9:-1] + orig[29:19:-1] + orig[39:29:-1]
            return orig
        if transform == 'shift':
            shiftnum = data
            #https://stackoverflow.com/questions/1082917/mod-of-negative-number-is-melting-my-brain/19655679
            #always positive modulus to handle any shift case
            shiftnum = (shiftnum % 40 + 40) % 40
            #rotate array by shift
            orig = orig[shiftnum:] + orig[:shiftnum]
            return orig
    def parseShift(orig, shift):
        transformData = [None, None]
        for l in shift:
            if l == 'V' or l == 'H':
                newTransform = 'flip'
            elif l == '+' or l == '-':
                newTransform = 'shift'
            else:
                print("Error, transformation " + l + unrecognized)
                continue
            #execute queued command
            if newTransform != transformData[0]:
                orig = executeTransform(transformData[0], transformData[1], orig)
                transformData = [newTransform, None]
            if transformData[0] == 'flip':
                vFlip, hFlip = transformData[1] if transformData[1] != None else (False, False)
                transformData[1] = (vFlip ^ (l == 'V'), hFlip ^ (l == 'H'))
            else:
                shiftAmt = transformData[1] if transformData[1] != None else 0
                #shift algorithm is inverted for +/-.  May be a good idea to simplify
                transformData[1] = shiftAmt-1 if (l == '+') else shiftAmt+1
        orig = executeTransform(transformData[0], transformData[1], orig)
        return orig
    #orig = executeTransform('flip', (True, True), orig)
    #orig = executeTransform('shift', 20, orig)
    orig = parseShift(orig, transform)
    print(orig)
    global keyboard, keys
    #ignore letters that aren't part of keyboard as H is not transformed in the example
    newstring = [keyboard[orig[keys[ch]]] if ch in keys else ch for ch in _string]
    return "".join(newstring)
print(shift("Hello", "HVVH+V+HV-VVVV+VHV++V++V--VVV-H++VVH"))