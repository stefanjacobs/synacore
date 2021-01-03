import numpy as np
import sys

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
        self.ops[0] = self.op_0_halt
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
        return

    def get_mem(self):
        # get the next byte from memory (exec_ptr is pointing to that) and increase pointer
        mem = self.memory[self.exec_ptr]
        self.exec_ptr += 1
        return mem

    def get_val(self, t):
        # get a value from <t>. <t> may be eiter a value, a register, or invalid
        if t < self.MAX_INT: # literal value
            retval = str(t)
        elif t < self.MAX_INT+8:
            retval = "$" + str(t-self.MAX_INT)
        else:
            print("VM: invalid get value", t)
            retval = "null" 
        return retval

    def op_0_halt(self):
        print(self.exec_ptr-1, " | ", "halt")
    
    def op_1_set(self):
        print(self.exec_ptr-1, " | ", "set", self.get_val(self.get_mem()), self.get_val(self.get_mem()))

    def op_2_push(self):
        print(self.exec_ptr-1, " | ", "push", self.get_val(self.get_mem()))

    def op_3_pop(self):
        print(self.exec_ptr-1, " | ", "pop", self.get_val(self.get_mem()))
    
    def op_4_eq(self):
        print(self.exec_ptr-1, " | ", "eq", self.get_val(self.get_mem()), self.get_val(self.get_mem()), self.get_val(self.get_mem()))
    
    def op_5_gt(self):
        print(self.exec_ptr-1, " | ", "gt", self.get_val(self.get_mem()), self.get_val(self.get_mem()), self.get_val(self.get_mem()))

    def op_6_jmp(self):
        print(self.exec_ptr-1, " | ", "jmp", self.get_val(self.get_mem()))

    def op_7_jt(self):
        print(self.exec_ptr-1, " | ", "jt", self.get_val(self.get_mem()), self.get_val(self.get_mem()))

    def op_8_jf(self):
        print(self.exec_ptr-1, " | ", "jf", self.get_val(self.get_mem()), self.get_val(self.get_mem()))

    def op_9_add(self):
        print(self.exec_ptr-1, " | ", "add", self.get_val(self.get_mem()), self.get_val(self.get_mem()), self.get_val(self.get_mem()))

    def op_10_mult(self):
        print(self.exec_ptr-1, " | ", "mult", self.get_val(self.get_mem()), self.get_val(self.get_mem()), self.get_val(self.get_mem()))

    def op_11_mod(self):
        print(self.exec_ptr-1, " | ", "mod", self.get_val(self.get_mem()), self.get_val(self.get_mem()), self.get_val(self.get_mem()))

    def op_12_and(self):
        print(self.exec_ptr-1, " | ", "and", self.get_val(self.get_mem()), self.get_val(self.get_mem()), self.get_val(self.get_mem()))
    
    def op_13_or(self):
        print(self.exec_ptr-1, " | ", "or", self.get_val(self.get_mem()), self.get_val(self.get_mem()), self.get_val(self.get_mem()))

    def op_14_not(self):
        print(self.exec_ptr-1, " | ", "not", self.get_val(self.get_mem()), self.get_val(self.get_mem()))
    
    def op_15_rmem(self):
        print(self.exec_ptr-1, " | ", "rmem", self.get_val(self.get_mem()), self.get_val(self.get_mem()))

    def op_16_wmem(self):
        print(self.exec_ptr-1, " | ", "wmem", self.get_val(self.get_mem()), self.get_val(self.get_mem()))

    def op_17_call(self):
        print(self.exec_ptr-1, " | ", "call", self.get_val(self.get_mem()))

    def op_18_ret(self):
        print(self.exec_ptr-1, " | ", "ret")


    def op_19_out(self):
        m = self.get_mem()
        if m >= self.MAX_INT:
            print(self.exec_ptr-1, " | ", "out", self.get_val(self.get_mem()))
        else:
            if chr(m) == "\n":
                print(self.exec_ptr-1, " | ", "out", self.inbuffer)
                self.inbuffer = ""
            else:
                self.inbuffer += chr(m)

    def op_20_in(self):
        print(self.exec_ptr-1, " | ", "in", self.get_val(self.get_mem()))

    def op_21_noop(self):
        print(self.exec_ptr-1, " | ", "noop")

    def disassamble(self):
        while self.exec_ptr < len(self.memory):
            op = self.get_mem()
            self.ops.get(op, lambda: 'Invalid operation')()
        print("VM: Done disassembling, stopping")

vm = VM()
vm.loadprogram('challenge.bin')
vm.disassamble()