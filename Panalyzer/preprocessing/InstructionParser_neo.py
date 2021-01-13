import re
from Panalyzer.preprocessing.InstructionParser import InstructionParser

'''
ARMv8 W registers forms the lower half of the corresponding 64 bit X register.
31 64bit Regs Referred as W/X0 ~ W/X30; reg31 is encoded to represent the zr register or sp register 
'''


class InstructionParserNeo(InstructionParser):
    def __init__(self, instruction):
        super(InstructionParserNeo, self).__init__(instruction)

    def arm64parser(self):
        inst_length = self.len_inst
        current_op = self.op
        # print(current_op)
        res = {'d1': None, 'd2': None, 's1': None, 's2': None, 's3': None, 'offset': None, 'op': self.op}  # default values of operands
        current_operands = None
        if 'ret' in current_op:
            res = {'d1': None, 'd2': None, 's1': 'x30', 's2': None, 's3': None, 'offset': None, 'op': self.op}
        if inst_length > 1:
            current_operands = re.split(r',\s*(?![^[]*\])', self.inst[1])  # Split by commas outside of "[]"
            num_operands = len(current_operands)
            '''
                The pattern of Source/Destination operands:
                0. Single operand:
                    That operand can only be Source1
                1. Two operands:
                    a. STR: source1, source2
                    c. other cases: d1, s1
                2. Three operands (the most common case):
                    a. STR/STUR: op[0]source1, op[1]source2, op[2]offset on source2
                    b. cbz/cbnz: source1, source2, target
                    c. other cases: d1, s1, s2
                3. Four operands
                    a. (s)BFM: op[0] d1, op[1] s1, imm1, imm2
                    b. CCMP: op[0] s1, imm1, imm2, condition
                    c. csel/csinv/csneg: op[0] d1, op[1] s1, op[2] s2 , condition
                    d. extr: op[0] d1, op[1] s1, op[2] s2 , imm
                    e. (s)madd/msub: op[0] d1, op[1] s1, op[2] s2 , op[3] s3
            '''
            if num_operands == 1:
                res['s1'] = current_operands[0]
            elif num_operands == 2:
                if 'str' in current_op or 'stur' in current_op:
                    res['s1'], res['s2'] = current_operands[0], current_operands[1]
                elif 'bnz' in current_op or 'bz' in current_op:
                    res['s1'], res['s2'] = current_operands[0], current_operands[1]
                else:
                    res['d1'], res['s1'] = current_operands[0], current_operands[1]
            elif num_operands == 3:
                if 'str' in current_op or 'stur' in current_op:
                    res['s1'], res['s2'] = current_operands[0], current_operands[1]
                elif 'bnz' in current_op or 'bz' in current_op:
                    res['s1'], res['s2'] = current_operands[0], current_operands[1]
                else:
                    res['d1'], res['s1'], res['s2'] = current_operands[0], current_operands[1], current_operands[2]
            elif num_operands == 4:
                if 'cmp' in current_op:
                    res['d1'] = current_operands[0]
                elif 'madd' in current_op or 'msub' in current_op:
                    res['d1'], res['s1'], res['s2'], res['s3'] = current_operands[0], current_operands[1], \
                                                                 current_operands[2], current_operands[3]
                else:
                    res['d1'], res['s1'], res['s2'], res['s3'] = current_operands[0], current_operands[1], \
                                                                 current_operands[2], current_operands[3]
            else:
                pass

            # Clean up operands in formats of addresses or immediate values
            if res['s1'] is not None:
                if "[" in res['s1'] and "#" in res['s1']:
                    if "[" in current_operands[1]:  # ldr r3, [r3, #13]！
                        dst_address = re.split(" ", current_operands[1].strip("[]"))  # calculating address using reg
                        res['s1'] = dst_address[0].strip("[]").strip(",")
                        res['offset'] = re.sub("[^\d\.]", "", dst_address[1])  # Offsets are formatted in decimal
                    elif "#" in current_operands[1]:  # ldr fp, #0
                        res['offset'] = current_operands[1].strip("#")
                    else:
                        pass
            if res['s2'] is not None:
                if "[" in res['s2'] and "#" in res['s2']:
                    if "[" in current_operands[1]:  # ldr r3, [r3, #13]！
                        dst_address = re.split(" ", current_operands[1].strip("[]"))  # calculating address using reg
                        # value and offset
                        res['s2'] = dst_address[0].strip("[]").strip(",")
                        res['offset'] = re.sub("[^\d\.]", "", dst_address[1])  # Offsets are formatted in decimal
                    elif "#" in current_operands[1]:  # ldr fp, #0
                        res['offset'] = current_operands[1].strip("#")
                    else:
                        pass

            for key, value in res.items():
                if value is not None:
                    if "[" in value:
                        res[key] = value.strip("[]").strip(",")
                    elif "#" in value:
                        res[key] = value.strip("#")
                    else:
                        res[key] = value
                else:
                    res[key] = value

        return res

        # print(inst_length, current_op, current_operands)


if __name__ == "__main__":  # Test
    line = ' 1362219: system.cpu: 0x41a630    :   ret                      : IntAlu :  '
    split_line = line.strip().split(":")  # Split raw trace line with comma delimiter
    inst = split_line[3].strip()
    message = InstructionParserNeo(inst).arm64parser()
    print(message)
