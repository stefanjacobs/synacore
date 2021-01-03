import numpy as np
import sys

class VM:
    
    MAX_INT = 32768

    def __init__(self):
        self.memory = [0 for i in range(0, self.MAX_INT)]
        self.register = [0 for i in range(0, 8)]
        self.stack = []
        self.xptr = 0
        self.inbuffer = ""
        return

    def loadprogram(self, filename):
        # load program from filename -> challenge.bin
        data = np.fromfile(filename, dtype=np.uint16)
        for i, v in enumerate(data):
            self.memory[i] = int(v)
        return
    
    def get_val(self, t):
        # get a value from <t>. <t> may be eiter a value, a register, or invalid
        if t < self.MAX_INT: # literal value
            retval = t
        elif t < self.MAX_INT+8:
            retval = self.register[t-self.MAX_INT]
        else:
            print("VM: invalid get value", t)
            retval = 0
        return retval
    
    def set_val(self, r, t):
        # put value <t> into register <r>
        if r < self.MAX_INT: # literal value, no register:
            print("VM: invalid register, seems like a value ", r)
        elif r < self.MAX_INT+8:
            self.register[r-self.MAX_INT] = self.get_val(t)
        else:
            print("VM: invalid register, invalid value ", r)
        return
    
    def op_1_set(self, a, b):
        # set register <a> to the value of <b>
        if a >= self.MAX_INT and a < self.MAX_INT+8:
            self.register[a-self.MAX_INT] = self.get_val(b)
        else:
            print("VM: unknown register", a, "- val to write ", b)
        self.xptr += 2
        return
    
    def op_2_push(self, a):
        # push <a> onto the stack
        self.stack.append(self.get_val(a))
        self.xptr += 1
        return

    def op_3_pop(self, a):
        # remove the top element from the stack and write it into <a>; empty stack = error
        self.set_val(a, self.stack.pop())
        self.xptr += 1
        return

    def op_4_eq(self, a, b, c):
        # set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
        if self.get_val(b) == self.get_val(c):
            self.set_val(a, 1)
        else:
            self.set_val(a, 0)
        self.xptr += 3
        return

    def op_5_gt(self, a, b, c):
        # set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
        if self.get_val(b) > self.get_val(c):
            self.set_val(a, 1)
        else:
            self.set_val(a, 0)
        self.xptr += 3
        return

    def op_6_jmp(self, t):
        # jump to <a>
        self.xptr = self.get_val(t)
        return
    
    def op_7_jt(self, a, b):
        # if <a> is nonzero, jump to <b>
        if not self.get_val(a) == 0:
            self.xptr = self.get_val(b)
        else:
            self.xptr += 2
        return

    def op_8_jf(self, a, b):
        # if <a> is zero, jump to <b>
        if self.get_val(a) == 0:
            self.xptr = self.get_val(b)
        else:
            self.xptr += 2
        return
    
    def op_9_add(self, a, b, c):
        # assign into <a> the sum of <b> and <c> (modulo 32768)
        self.set_val(a, (self.get_val(b)+self.get_val(c))%self.MAX_INT)
        self.xptr += 3
        return
    
    def op_10_mult(self, a, b, c):
        # store into <a> the product of <b> and <c> (modulo 32768)
        self.set_val(a, (self.get_val(b)*self.get_val(c))%self.MAX_INT)
        self.xptr += 3
        return

    def op_11_mod(self, a, b, c):
        # store into <a> the remainder of <b> divided by <c>
        self.set_val(a, self.get_val(b)%self.get_val(c))
        self.xptr += 3
        return
    
    def op_12_and(self, a, b, c):
        # stores into <a> the bitwise and of <b> and <c>
        self.set_val(a, self.get_val(b) & self.get_val(c))
        self.xptr += 3
        return

    def op_13_or(self, a, b, c):
        # stores into <a> the bitwise or of <b> and <c>
        self.set_val(a, self.get_val(b) | self.get_val(c))
        self.xptr += 3
        return

    def op_14_not(self, a, b):
        # stores 15-bit bitwise inverse of <b> in <a>
        self.set_val(a, ~self.get_val(b)%self.MAX_INT )
        self.xptr += 2
        return
    
    def op_15_rmem(self, a, b):
        # read memory at address <b> and write it to <a>
        self.set_val(a, self.memory[self.get_val(b)])
        self.xptr += 2
        return

    def op_16_wmem(self, a, b):
        # write the value from <b> into memory at address <a>
        self.memory[self.get_val(a)] = self.get_val(b)
        self.xptr += 2
        return

    def op_17_call(self, a):
        # write the address of the next instruction to the stack and jump to <a>
        self.stack.append(self.xptr+1)
        self.xptr = self.get_val(a)
        return

    def op_18_ret(self):
        # remove the top element from the stack and jump to it; empty stack = halt
        if len(self.stack) == 0:
            print("VM: Error, stack is empty!")
        else:
            self.xptr = self.stack.pop()
        return

    def op_19_out(self, c):
        # write the character represented by ascii code <a> to the terminal
        print(chr(self.get_val(c)), end='')
        self.xptr += 1
        return
    
    def op_20_in(self, a):
        # read a character from the terminal and write its ascii code to <a>; it can 
        # be assumed that once input starts, it will continue until a newline is 
        # encountered; this means that you can safely read whole lines from the 
        # keyboard and trust that they will be fully read
        if len(self.inbuffer) == 0:
            self.inbuffer = input("--> ") + "\n"
            print("VM: Input was ", self.inbuffer)
        
        self.set_val(a, ord(self.inbuffer[0]))
        self.inbuffer = self.inbuffer[1:]

        # self.set_val(a, ord(readchar.readchar()))
        self.xptr += 1
        return

    def execute_step(self, op):
        if op == 1: # found 'set' operation
            return self.op_1_set(self.memory[self.xptr], self.memory[self.xptr+1])
        if op == 2: # found 'push' operation
            return self.op_2_push(self.memory[self.xptr])
        if op == 3: # found 'pop' operation
            return self.op_3_pop(self.memory[self.xptr])
        if op == 4: # found 'eq' operation
            return self.op_4_eq(self.memory[self.xptr], self.memory[self.xptr+1], self.memory[self.xptr+2])
        if op == 5: # found 'gt' operation
            return self.op_5_gt(self.memory[self.xptr], self.memory[self.xptr+1], self.memory[self.xptr+2])
        if op == 6: # found 'jmp' operation
            return self.op_6_jmp(self.memory[self.xptr])
        if op == 7: # found 'jt' operation
            return self.op_7_jt(self.memory[self.xptr], self.memory[self.xptr+1])
        if op == 8: # found 'jf' operation
            return self.op_8_jf(self.memory[self.xptr], self.memory[self.xptr+1])
        if op == 9: # found 'add' operation
            return self.op_9_add(self.memory[self.xptr], self.memory[self.xptr+1], self.memory[self.xptr+2])
        if op == 10: # found 'mult' operation
            return self.op_10_mult(self.memory[self.xptr], self.memory[self.xptr+1], self.memory[self.xptr+2])
        if op == 11: # found 'mod' operation
            return self.op_11_mod(self.memory[self.xptr], self.memory[self.xptr+1], self.memory[self.xptr+2])
        if op == 12: # found 'and' operation
            return self.op_12_and(self.memory[self.xptr], self.memory[self.xptr+1], self.memory[self.xptr+2])
        if op == 13: # found 'or' operation
            return self.op_13_or(self.memory[self.xptr], self.memory[self.xptr+1], self.memory[self.xptr+2])
        if op == 14: # found 'not' operation
            return self.op_14_not(self.memory[self.xptr], self.memory[self.xptr+1])
        if op == 15: # found 'rmem' operation
            return self.op_15_rmem(self.memory[self.xptr], self.memory[self.xptr+1])
        if op == 16: # found 'wmem' operation
            return self.op_16_wmem(self.memory[self.xptr], self.memory[self.xptr+1])
        if op == 17: # found 'call' operation
            return self.op_17_call(self.memory[self.xptr])
        if op == 18: # found 'ret' operation
            return self.op_18_ret()
        if op == 19: # found 'out' operation
            return self.op_19_out(self.memory[self.xptr])
        if op == 20: # found 'in' operation
            return self.op_20_in(self.memory[self.xptr])
        if op == 21: # found 'noop' operation
            return

        print("Unknown operand", op)
        return

    def execute(self):
        while True:
            op = self.memory[self.xptr]
            self.xptr += 1
            if op == 0:
                break
            self.execute_step(op)
        print("VM: Found Halt Signal, stopping")
        return

vm = VM()
vm.loadprogram('challenge.bin')
vm.execute()