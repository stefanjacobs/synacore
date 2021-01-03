# Contents

This is a solution to the [Synacore Challenge](https://challenge.synacor.com/)using mostly Python 3 and some C. It consists of some very nice programming puzzles and computer basics... And I admit, for one step, I had to Google (teleport anyone???).

This solution consists of the following files, more or less in the order of their creation:

- `01_vm_base.py` is a base implementation of the virtual machine described in the arch-spec. Because of some design flaws, I refactored this solution and used the 02 implementation from that point on.
- `02_vm_enhanced.py` is the same implementation extended for some more functions and readability. E.g. there are `load #nr` and `save #nr` functionalities, an operations dictionary, where all ops are registered and some code duplication removed. Additionally it extends the `use teleporter` function to override security mechanisms and setting the teleporter to the second destination as described in the Strange Book.
- `03_coins.py` calculates the solution to the Coins Problem.
- `04_disassemble.py` disassembles the challenge.bin and writes some nice, readable assembler code. Combined with Debugging in Visual Studio Code you can have a deep inspection into the challenge itself which you need when you want to solve the teleporter problem.
- `05_pirates.py` calculates a solution to the Pirates Cove Problem.

## Coin Puzzle

The solution to the coin puzzle is found in `03_coins.py`:

    Task:
    _ + _ * _^2 + _^3 - _ = 399

    Inputs:
    - red coin, two dots
    - concave coin, seven dots
    - blue coin, nine dots
    - shiny coin, pentagon (e.g. 5 dots?)
    - corroded coin, triangle (e.g. 3 dots?)

## The Strange Book Puzzle

The cover of this book subtly swirls with colors.  It is titled "A Brief Introduction to Interdimensional Physics".  It reads:

Recent advances in interdimensional physics have produced fascinating predictions about the fundamentals of our universe!  For example, interdimensional physics seems to predict that the universe is, at its root, a purely mathematical construct, and that all events are caused by the interactions between eight pockets of energy called "registers". Furthermore, it seems that while the lower registers primarily control mundane things like sound and light, the highest register (the so-called "eighth register") is used to control interdimensional events such as teleportation.

A hypothetical such teleportation device would need to have have exactly two destinations.  One destination would be used when the eighth register is at its minimum energy level - this would be the default operation assuming the user has no way to control the eighth register.  In this situation, the teleporter should send the user to a preconfigured safe location as a default.

The second destination, however, is predicted to require a very specific energy level in the eighth register.  The teleporter must take great care to confirm that this energy level is exactly correct before teleporting its user! If it is even slightly off, the user would (probably) arrive at the correct location, but would briefly experience anomalies in the fabric of reality itself - this is, of course, not recommended.  Any teleporter would need to test the energy level in the eighth register and abort teleportation if it is not exactly correct.

This required precision implies that the confirmation mechanism would be very computationally expensive.  While this would likely not be an issue for large- scale teleporters, a hypothetical hand-held teleporter would take billions of years to compute the result and confirm that the eighth register is correct.

If you find yourself trapped in an alternate dimension with nothing but a hand-held teleporter, you will need to extract the confirmation algorithm, reimplement it on more powerful hardware, and optimize it.  This should, at the very least, allow you to determine the value of the eighth register which would have been accepted by the teleporter's confirmation mechanism.

Then, set the eighth register to this value, activate the teleporter, and bypass the confirmation mechanism.  If the eighth register is set correctly, no anomalies should be experienced, but beware - if it is set incorrectly, the now-bypassed confirmation mechanism will not protect you!

Of course, since teleportation is impossible, this is all totally ridiculous.

### Disassembling the Challenge

Details are found in 04_disassemble.py. I set a breakpoint in VSCode, whenever register 7 was read or written to, and could find the following interesting things:

    5451  |  jf $7 5605
    ....
    5470  |  call 1458 --> utility method it occurs very often, so I ignore that
    ....
    5483  |  set $0 4
    5486  |  set $1 1
    5489  |  call 6027 --> that is an interesting function, see next observation
    5491  |  eq $1 $0 6
    5495  |  jf $1 5579

and

    6027  |  jt $0 6035
    6030  |  add $0 $1 1 --> $0 = $1 + 1
    6034  |  ret
    6035  |  jt $1 6048
    6038  |  add $0 $0 32767 --> $0 -= 1
    6042  |  set $1 $7
    6045  |  call 6027  --> some recursion going on
    6047  |  ret
    6048  |  push $0
    6050  |  add $1 $1 32767 --> $1 -= 1
    6054  |  call 6027  --> some recursion going on
    6056  |  set $1 $0
    6059  |  pop $0
    6061  |  add $0 $0 32767 --> $0 -= 1
    6065  |  call 6027  --> some recursion going on
    6067  |  ret

I admit, **I googled here** and found Ackerman functions and solutions of other Synacore challenge contenders... --> in the teleport folder is the teleporter function... After getting the result, I changed some ops to `Noops` (see `op_20_in` for details) and set the register 8 correctly and beamed on the beach, nice!

## The Pirates Cove Story

Day 1: We have reached what seems to be the final in a series of puzzles guarding an ancient treasure.  I suspect most adventurers give up long before this point, but we're so close!  We must press on!

Day 1: P.S.: It's a good thing the island is tropical.  We should have food for weeks!

Day 2: The vault appears to be sealed by a mysterious force - the door won't budge an inch.  We don't have the resources to blow it open, and I wouldn't risk damaging the contents even if we did.  We'll have to figure out the lock mechanism.

Day 3: The door to the vault has a number carved into it.  Each room leading up to the vault has more numbers or symbols embedded in mosaics in the floors.  We even found a strange glass orb in the antechamber on a pedestal itself labeled with a number.  What could they mean?

Day 5: We finally built up the courage to touch the strange orb in the antechamber.  It flashes colors as we carry it from room to room, and sometimes the symbols in the rooms flash colors as well.  It simply evaporates if we try to leave with it, but another appears on the pedestal in the antechamber shortly thereafter.  It also seems to do this even when we return with it to the antechamber from the other rooms.

Day 8: When the orb is carried to the vault door, the numbers on the door flash black, and then the orb evaporates.  Did we do something wrong?  Doesn't the door like us?  We also found a small hourglass near the door, endlessly running.  Is it waiting for something?

Day 13: Some of my crew swear the orb actually gets heaver or lighter as they walk around with it.  Is that even possible?  They say that if they walk through certain rooms repeatedly, they feel it getting lighter and lighter, but it eventually just evaporates and a new one appears as usual.

Day 21: Now I can feel the orb changing weight as I walk around.  It depends on the area - the change is very subtle in some places, but certainly more noticeable in others, especially when I walk into a room with a larger number or out of a room marked '*'.  Perhaps we can actually control the weight of this mysterious orb?

Day 34: One of the crewmembers was wandering the rooms today and claimed that the numbers on the door flashed white as he approached!  He said the door still didn't open, but he noticed that the hourglass had run out and flashed black.  When we went to check on it, it was still running like it always does.  Perhaps he is going mad?  If not, which do we need to appease: the door or the hourglass?  Both?

Day 55: The fireflies are getting suspicious.  One of them looked at me funny today and then flew off.  I think I saw another one blinking a little faster than usual.  Or was it a little slower?  We are getting better at controlling the weight of the orb, and we think that's what the numbers are all about.  The orb starts at the weight labeled on the pedestal, and goes down as we leave a room marked '-', up as we leave a room marked '+', and up even more as we leave a room marked '*'.  Entering rooms with larger numbers has a greater effect.

Day 89: Every once in a great while, one of the crewmembers has the same story: that the door flashes white, the hourglass had already run out, it flashes black, and the orb evaporates.  Are we too slow?  We can't seem to find a way to make the orb's weight match what the door wants before the hourglass runs out.  If only we could find a shorter route through the rooms...

Day 144: We are abandoning the mission.  None of us can work out the solution to the puzzle.  I will leave this journal here to help future adventurers, though I am not sure what help it will give.  Good luck!

### Room Layout

Walking around leads to the following layout and math problem:

                    go for 30
        *   8   -   1
        4   *   11  *
        +   4   -   18
        22  -   9   *
    start

This is a classical search problem, the solution can be found in `05_pirates.py`. It seems that the starting room and the door room has to be avoided, because the orb evaporates when entering the room again... The shortest solution would be much shorter without those constraints.
