import csv
from pathlib import Path
from Panalyzer.preprocessing.InstructionParser import InstructionParser
from Panalyzer.preprocessing.InstructionParser_neo import InstructionParserNeo


def txt2csv(trace_name, trace_dir='TraceExamples', arch='arm32'):
    # Initialize Path variables to store converted csv file
    project_dir = Path(__file__).resolve().parent.parent
    csv_dir = project_dir.joinpath('tempcsv')
    trace_file = project_dir.joinpath(trace_dir) / (trace_name + ".txt")
    csv_fname = csv_dir / (trace_name + ".csv")

    # Processing raw txt trace file
    with open(csv_fname, "w", newline="") as my_empty_csv:
        writer = csv.writer(my_empty_csv)
        """
                             Columns of converted trace file in csv format are defined as:
        ['Tick', 'CPU_ID', 'PC', 'INST', 'DST1', 'DST2', 'SRC1', 'SRC2', 'OFFSET', 'TYPE', 'DATA', #'ADDR'#]
        """
        lineoffset = []
        offset = 0
        for i, line in enumerate(open(trace_file)):
            lineoffset.append(offset)
            offset = offset + len(line)
            if arch == 'arm32':
                line = line.replace('fp', 'r11').replace('sp', 'r13').replace('lr', 'r14').replace('pc',
                                                                                                   'r15')  # Rename registers
                # with specific names to avoid unnecessary troubles in subsequent modules
                split_line = line.strip().split(":")  # Split raw trace line with comma delimiter
                current_tick = split_line[0]  # Tick
                current_cpu = split_line[1]  # CPU ID
                current_pc = split_line[2]  # PC VALUE
                current_inst = split_line[3].strip()  # INST TO BE SPLIT
                current_access_type = split_line[-2]  # Access type

                if 'Predicated False' not in split_line[-1]:
                    detailed_inst = InstructionParser(current_inst).arm32parser()
                    current_d1 = detailed_inst['d1']
                    current_d2 = detailed_inst['d2']
                    current_s1 = detailed_inst['s1']
                    current_s2 = detailed_inst['s2']
                    current_offset = detailed_inst['offset']
                    current_op = detailed_inst['op']

                    if "D=" in split_line[-1]:
                        current_data_full = int(split_line[-1].split("=", 1)[1], 16)
                        current_data = current_data_full & 0xFFFFFFFF  # Only keep lower 32bit of the data in register
                    else:
                        current_data = 0

                    writer.writerow([current_tick, current_cpu, current_pc, current_op, current_d1, current_d2,
                                     current_s1, current_s2, current_offset, current_access_type, current_data])
                else:
                    current_d1 = None
                    current_d2 = None
                    current_s1 = None
                    current_s2 = None
                    current_offset = None
                    current_op = None
                    current_data = None
                    writer.writerow([current_tick, current_cpu, current_pc, current_op, current_d1, current_d2,
                                     current_s1, current_s2, current_offset, current_access_type, current_data])

            elif arch == "arm64":
                line = line.replace('zr', '31').replace('sp', 'w31')
                split_line = line.strip().split(":")  # Split raw trace line with comma delimiter
                current_tick = split_line[0]  # Tick
                current_cpu = split_line[1]  # CPU ID
                current_pc = split_line[2]  # PC VALUE
                current_inst = split_line[3].strip()  # INST TO BE SPLIT
                current_access_type = split_line[-2]  # Access type
                if 'Predicated False' not in split_line[-1]:
                    detailed_inst = InstructionParserNeo(current_inst).arm64parser()
                    current_d1 = detailed_inst['d1']
                    current_d2 = detailed_inst['d2']
                    current_s1 = detailed_inst['s1']
                    current_s2 = detailed_inst['s2']
                    current_offset = detailed_inst['offset']
                    current_op = detailed_inst['op']

                    if 'Simd' not in split_line[-2]:
                        if "D=" in split_line[-1] and '0_0' not in split_line[-1]:
                            current_data_full = int(split_line[-1].split("=", 1)[1], 16)
                            current_data = current_data_full & 0xFFFFFFFF  # Only keep lower 32bit of the data in register
                        else:
                            current_data = 0
                else:
                    current_d1 = None
                    current_d2 = None
                    current_s1 = None
                    current_s2 = None
                    current_offset = None
                    current_op = None
                    current_data = None

                writer.writerow([current_tick, current_cpu, current_pc, current_op, current_d1, current_d2,
                                 current_s1, current_s2, current_offset, current_access_type, current_data])
    inst_length = i
    print('csvdone')
    return inst_length, lineoffset


if __name__ == "__main__":  # Test
    print(txt2csv("prime", arch='arm64')[0])
