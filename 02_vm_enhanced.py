import numpy as np
import sys, re
import pickle5 as pickle

class VM:
    
    MAX_INT = 32768

    def __init__(self):
        self.memory = [0 for i in range(0, self.MAX_INT)]
        self.register = [0 for i in range(0, 8)]
        self.stack = []
        self.exec_ptr = 0
        self.inbuffer = ""
        self.debug = False
        # Register all operations to machine (own class for ops seems to be overengineered)
        self.ops = dict()
        self.ops[1] = self.op_1_set
        self.ops[2] = self.op_2_push
        self.ops[3] = self.op_3_pop
        self.ops[4] = self.op_4_eq
        self.ops[5] = self.op_5_gt
        self.ops[6] = self.op_6_jmp
        self.ops[7] = self.op_7_jt
        self.ops[8] = self.op_8_jf
        self.ops[9] = self.op_9_add
        self.ops[10] = self.op_10_mult
        self.ops[11] = self.op_11_mod
        self.ops[12] = self.op_12_and
        self.ops[13] = self.op_13_or
        self.ops[14] = self.op_14_not
        self.ops[15] = self.op_15_rmem
        self.ops[16] = self.op_16_wmem
        self.ops[17] = self.op_17_call
        self.ops[18] = self.op_18_ret
        self.ops[19] = self.op_19_out
        self.ops[20] = self.op_20_in
        self.ops[21] = self.op_21_noop
        return

    def loadprogram(self, filename):
        # load program from filename -> challenge.bin
        data = np.fromfile(filename, dtype=np.uint16)
        for i, v in enumerate(data):
            self.memory[i] = int(v)
    
    def dump(self, filename):
        # dump state of machine into a file
        d = dict()
        d["memory"] = self.memory
        d["stack"] = self.stack
        d["register"] = self.register
        d["xptr"] = self.exec_ptr
        with open(filename +'.pkl', 'wb+') as f:
            pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)

    def load(self, filename):
        # load state of machine from a file
        d = dict()
        if not '.pkl' in filename:
            filename += ".pkl"
        with open(filename, 'rb') as f:
            d = pickle.load(f)
        self.memory = d["memory"]
        self.stack = d["stack"]
        self.register = d["register"]
        self.exec_ptr = d["xptr"]
        self.inbuffer = "look\n"
    
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
    
    def get_mem(self):
        # get the next byte from memory (exec_ptr is pointing to that) and increase pointer
        mem = self.memory[self.exec_ptr]
        self.exec_ptr += 1
        return mem
    
    def op_1_set(self):
        # set register <a> to the value of <b>
        a, b = self.get_mem(), self.get_mem()
        if a >= self.MAX_INT and a < self.MAX_INT+8:
            self.set_val(a, self.get_val(b))
        else:
            print("VM: unknown register", a, "- val to write ", b)
    
    def op_2_push(self):
        # push <a> onto the stack
        a = self.get_mem()
        self.stack.append(self.get_val(a))

    def op_3_pop(self):
        # remove the top element from the stack and write it into <a>; empty stack = error
        a = self.get_mem()
        if (len(self.stack) == 0):
            print("VM: Error - popping stack not possible because len 0")
        else:
            self.set_val(a, self.stack.pop())

    def op_4_eq(self):
        # set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
        a, b, c = self.get_mem(), self.get_mem(), self.get_mem()
        if self.get_val(b) == self.get_val(c):
            self.set_val(a, 1)
        else:
            self.set_val(a, 0)

    def op_5_gt(self):
        # set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
        a, b, c = self.get_mem(), self.get_mem(), self.get_mem()
        if self.get_val(b) > self.get_val(c):
            self.set_val(a, 1)
        else:
            self.set_val(a, 0)

    def op_6_jmp(self):
        # jump to <a>
        a = self.get_mem()
        self.exec_ptr = self.get_val(a)
    
    def op_7_jt(self):
        # if <a> is nonzero, jump to <b>
        a, b = self.get_mem(), self.get_mem()
        if not self.get_val(a) == 0:
            self.exec_ptr = self.get_val(b)

    def op_8_jf(self):
        # if <a> is zero, jump to <b>
        a, b = self.get_mem(), self.get_mem()
        if self.get_val(a) == 0:
            self.exec_ptr = self.get_val(b)
    
    def op_9_add(self):
        # assign into <a> the sum of <b> and <c> (modulo 32768)
        a, b, c = self.get_mem(), self.get_mem(), self.get_mem()
        self.set_val(a, (self.get_val(b)+self.get_val(c))%self.MAX_INT)
    
    def op_10_mult(self):
        # store into <a> the product of <b> and <c> (modulo 32768)
        a, b, c = self.get_mem(), self.get_mem(), self.get_mem()
        self.set_val(a, (self.get_val(b)*self.get_val(c))%self.MAX_INT)

    def op_11_mod(self):
        # store into <a> the remainder of <b> divided by <c>
        a, b, c = self.get_mem(), self.get_mem(), self.get_mem()
        self.set_val(a, self.get_val(b)%self.get_val(c))
    
    def op_12_and(self):
        # stores into <a> the bitwise and of <b> and <c>
        a, b, c = self.get_mem(), self.get_mem(), self.get_mem()
        self.set_val(a, self.get_val(b) & self.get_val(c))

    def op_13_or(self):
        # stores into <a> the bitwise or of <b> and <c>
        a, b, c = self.get_mem(), self.get_mem(), self.get_mem()
        self.set_val(a, self.get_val(b) | self.get_val(c))

    def op_14_not(self):
        # stores 15-bit bitwise inverse of <b> in <a>
        a, b = self.get_mem(), self.get_mem()
        self.set_val(a, ~self.get_val(b)%self.MAX_INT )
    
    def op_15_rmem(self):
        # read memory at address <b> and write it to <a>
        a, b = self.get_mem(), self.get_mem()
        self.set_val(a, self.memory[self.get_val(b)])

    def op_16_wmem(self):
        # write the value from <b> into memory at address <a>
        a, b = self.get_mem(), self.get_mem()
        self.memory[self.get_val(a)] = self.get_val(b)

    def op_17_call(self):
        # write the address of the next instruction to the stack and jump to <a>
        a = self.get_mem()
        self.stack.append(self.exec_ptr)
        self.exec_ptr = self.get_val(a)

    def op_18_ret(self):
        # remove the top element from the stack and jump to it; empty stack = halt
        if len(self.stack) == 0:
            print("VM: Error, stack is empty!")
        else:
            self.exec_ptr = self.stack.pop()

    def op_19_out(self):
        # write the character represented by ascii code <a> to the terminal
        a = self.get_mem()
        print(chr(self.get_val(a)), end='')
    
    def op_20_in(self):
        # read a character from the terminal and write its ascii code to <a>; it can 
        # be assumed that once input starts, it will continue until a newline is 
        # encountered; this means that you can safely read whole lines from the 
        # keyboard and trust that they will be fully read
        a = self.get_mem()
        if len(self.inbuffer) == 0:
            self.inbuffer = input("--> ") + "\n" # input is without newline, so add it
            regex = r'save (\d+)'
            results = re.findall(regex, self.inbuffer)
            if len(results) != 0:
                self.inbuffer = ""
                self.exec_ptr -= 2 # go back one instruction (and the mem) to perform reading again
                self.dump("savegame_" + results[0])
                return
            regex = r'load (\d+)'
            results = re.findall(regex, self.inbuffer)
            if len(results) != 0:
                self.load("savegame_" + results[0])
                return
            
            if "use teleporter" in self.inbuffer:
                # set the correct value to register 8
                self.set_val(self.MAX_INT+7, 25734)
                # deactivate the confirmation process
                self.memory[5451] = 21
                self.memory[5452] = 21
                self.memory[5453] = 21
                for i in range(5489, 5498):
                    self.memory[i] = 21
        
        self.set_val(a, ord(self.inbuffer[0]))
        self.inbuffer = self.inbuffer[1:]
    
    def op_21_noop(self):
        # no operation
        return

    def execute(self):
        while True:
            op = self.get_mem()
            if op == 0:
                break
            self.ops.get(op, lambda: 'Invalid operation')()
        print("VM: Found Halt Signal, stopping")

import argparse
parser = argparse.ArgumentParser(description='start virtual machine')
parser.add_argument('--load', type=str, required=False, help='load vm from savegame, e.g. state_1')
args = parser.parse_args()

vm = VM()
if args.load:
    vm.load(args.load)
else:
    vm.loadprogram('challenge.bin')
vm.execute()