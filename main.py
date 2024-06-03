"""
Rebeca Padovani Ederli
RA: 201482
"""
from tabulate import tabulate

instructions_str = None
def print_instructions_table(instructions, status_list):
    headers = ["Instruction", "Issued", "Read", "Executed", "Written"]
    max_width = max(len(instr.strip()) for instr in instructions)
    header_line = "| " + headers[0].ljust(max_width) + " | " + " | ".join(header.ljust(10) for header in headers[1:]) + " |"
    separator = "-" * len(header_line)
    print(separator)
    print(header_line)
    print(separator)
    for status in status_list:
        instr_index = status['instruction']
        issued = str(status['issued']).ljust(10)
        read = str(status['read']).ljust(10)
        executed = str(status['executed']).ljust(10)
        written = str(status['written']).ljust(10)
        instr_detail = instructions[instr_index].strip().ljust(max_width)
        line = f"| {instr_detail} | {issued} | {read} | {executed} | {written} |"
        print(line)
    print(separator)

def print_fu(fu):
    print("==============================================")
    headers = fu[0].keys()
    rows = [item.values() for item in fu]
    print(tabulate(rows, headers=headers, tablefmt='grid'))

def print_instructions_table_to_file(instructions, status_list, file_path):
    with open(file_path, 'w') as file:
        headers = ["Instruction", "Issued", "Read", "Executed", "Written"]
        max_width = max(len(instr.strip()) for instr in instructions)
        header_line = "| " + headers[0].ljust(max_width) + " | " + " | ".join(header.ljust(10) for header in headers[1:]) + " |"
        separator = "-" * len(header_line)

        print(separator, file=file)
        print(header_line, file=file)
        print(separator, file=file)
        for status in status_list:
            instr_index = status['instruction']
            issued = str(status['issued']).ljust(10)
            read = str(status['read']).ljust(10)
            executed = str(status['executed']).ljust(10)
            written = str(status['written']).ljust(10)
            instr_detail = instructions[instr_index].strip().ljust(max_width)
            line = f"| {instr_detail} | {issued} | {read} | {executed} | {written} |"
            print(line, file=file)
        print(separator, file=file)

OPCODES = {
    'fld': 0,
    'fsd': 1,
    'fadd': 2,
    'fsub': 3,
    'fmul': 4,
    'fdiv': 5
}

REG_PREFIXES = {
    'x': 'int',
    'f': 'float'
}

def parse_file(filename):
    instructions = []
    with open(filename, 'r') as f:
        for line in f:
            fields = line.strip().replace(',', ' ').split()
            opcode = fields[0].lower()
            if opcode not in OPCODES:
                raise ValueError(f'Invalid opcode: {opcode}')
            opcode = OPCODES[opcode]
            rs1, rs2, rd, imm = 0, 0, 0, None  # Set imm to None by default
            rs1_type, rs2_type, rd_type = None, None, None
            if opcode == 0:  # fld format: "instruction rd imm(rs1)"
                rd = int(fields[1][1:])
                rd_type = REG_PREFIXES[fields[1][0].lower()]
                rs1_imm = fields[2].split('(')
                imm = int(rs1_imm[0])
                rs1 = int(rs1_imm[1][1:-1])
                rs1_type = REG_PREFIXES[rs1_imm[1][0:1].lower()]
            elif opcode == 1:  # fsd format: "instruction rs2 imm(rs1)"
                rs2 = int(fields[1][1:])
                rs2_type = REG_PREFIXES[fields[1][0].lower()]
                rs1_imm = fields[2].split('(')
                imm = int(rs1_imm[0])
                rs1 = int(rs1_imm[1][1:-1])
                rs1_type = REG_PREFIXES[rs1_imm[1][0:1].lower()]
            else:  # Other instructions format: "instruction rd rs1 rs2"
                rd = int(fields[1][1:])
                rd_type = REG_PREFIXES[fields[1][0].lower()]
                rs1 = int(fields[2][1:])
                rs1_type = REG_PREFIXES[fields[2][0].lower()]
                if len(fields) > 3:
                    rs2 = int(fields[3][1:])
                    rs2_type = REG_PREFIXES[fields[3][0].lower()]
                else:
                    rs2 = 0
                    rs2_type = None
            instructions.append({
                'opcode': opcode,
                'rs1': rs1,
                'rs1_type': rs1_type,
                'rs2': rs2,
                'rs2_type': rs2_type,
                'rd': rd,
                'rd_type': rd_type,
                'imm': imm
            })
    return instructions

def get_instructions_str(filename):
    instructions_str = []
    with open(filename, 'r') as f:
        for line in f:
            instructions_str.append(line)
    return instructions_str

## Inicializar tabelas
def inicializa_status_instrucao(instructions):
    instruction_status = [
        {'instruction': instr, 'issued': False, 'read': False, 'executed': False, 'written': False}
        for instr in range(len(instructions))
    ]
    return instruction_status

def inicializa_unidades_funcionais(configuracoes):
    function_units = []
    for config in configuracoes:
        parts = config.split()
        unit_type = parts[0]  
        num_units = int(parts[1])  
        cycles = int(parts[2])  
        
        for i in range(num_units):
            unit = {
                'name': unit_type,
                'busy': False,
                'operation': None,
                'dest': None,
                'dest_type': None,
                'src1': None,
                'src1_type':None,
                'src2': None,
                'src2_type': None,
                'q1': None,
                'q2': None,
                'r1': True,
                'r2': True, 
                'cycles_needed': cycles,
                'cycles_remaining': cycles,
                'instruction': None  
            }
            function_units.append(unit)
    #print_fu(function_units)
    return function_units

def inicializa_registradores_resultado_status():
    register_result_status = {}
    for i in range(32):
        reg_name = f'x{i}'
        register_result_status[reg_name] = {'unit': None, 'ready': True} 
    for i in range(32): 
        reg_name = f'f{i}'
        register_result_status[reg_name] = {'unit': None, 'ready': True} 
    return register_result_status


def todas_instrucoes_escritas(instruction_status):
    #print_instructions_table(instructions_str, instruction_status)
    for inst in instruction_status:
        if inst['written']==False:
            return False
    return True

def busca_fu(fu, instruciton_index, unidades_funcionais, instruction):
    #print_fu(unidades_funcionais)
    reservou = False
    for name_fu in unidades_funcionais:
        if fu[:3] == name_fu['name'][:3]:
            if name_fu['busy'] == False:
                name_fu['busy'] = True
                name_fu['operation'] = instruction['opcode']
                name_fu['dest'] = instruction['rd']
                name_fu['dest_type'] = instruction['rd_type']
                name_fu['src1'] = instruction['rs1']
                name_fu['src1_type'] = instruction['rs1_type']
                name_fu['src2'] = instruction['rs2']
                name_fu['src2_type'] = instruction['rs2_type']
                name_fu['instruction'] = instruciton_index
                return True, unidades_funcionais
    return reservou, unidades_funcionais

def reserva_unidade_funcional(instruction, instruction_index, unidades_funcionais):
    if instruction['opcode'] == 0 or instruction['opcode'] == 1:
        fu = 'int'
    elif instruction['opcode'] == 2 or instruction['opcode'] == 3:
        fu = 'add'
    elif instruction['opcode'] == 4:
        fu = 'mult'
    elif instruction['opcode'] == 5:
        fu = 'div'
    reservou, unidades_funcionais = busca_fu(fu, instruction_index, unidades_funcionais, instruction)
    return reservou, unidades_funcionais

def busca_waw(instruction, unidades_funcionais):
    reg_destino_inst = instruction['rd']
    reg_destino_inst_type = instruction['rd_type']
    for fu in unidades_funcionais:
        if reg_destino_inst == fu['dest'] and reg_destino_inst_type == fu['dest_type']:
            return False
    return True

def busca_fu_instruction(instruction_index, tabela_unidades_funcionais):
    for fu in tabela_unidades_funcionais:
        if fu['instruction'] ==  instruction_index:
            return fu
    return None    


def reserva_reg_resultado(instruction, instruction_index, resgister_result_status, tabela_unidades_funcionais):
    reg_dest = instruction['rd']
    reg_dest_type = instruction['rd_type']
    if reg_dest_type == 'int':
        reg_dest = "x"+str(reg_dest)
    else:
        reg_dest = "f"+str(reg_dest)
    if resgister_result_status[reg_dest] == None:
        name_fu = busca_fu_instruction(instruction_index, tabela_unidades_funcionais)
        if name_fu !=None:
            resgister_result_status[reg_dest] = busca_fu_instruction(instruction_index, tabela_unidades_funcionais)['name']
    return resgister_result_status

    
def issue(instruction, instruction_index, unidades_funcionais, resgister_result_status):
    sem_waw = busca_waw(instruction, unidades_funcionais)
    if sem_waw:
        reservou, unidades_funcionais = reserva_unidade_funcional(instruction, instruction_index, unidades_funcionais)
        if reservou:
            resgister_result_status = reserva_reg_resultado(instruction, instruction_index, resgister_result_status, unidades_funcionais)
            return True
    return False

def atualiza_instruction_status(instruction_index, etapa, tabela_instruction_status, ciclo_clock):
    tabela_instruction_status[instruction_index][etapa] = ciclo_clock
    return tabela_instruction_status

def verifica_operandos(instruction_index, tabela_unidades_funcionais):
    leitura_operandos = False
    fu_inst = busca_fu_instruction(instruction_index, tabela_unidades_funcionais)
    if fu_inst != None:
        name_fu = fu_inst['instruction']
        for fu in tabela_unidades_funcionais:
            if name_fu != fu['instruction']:
                if fu_inst['src1'] == fu['dest'] and fu_inst['src1_type'] == fu['dest_type'] and fu_inst['instruction'] > fu['instruction']:
                    fu_inst['q1'] = fu['instruction']
                    fu_inst['r1'] = False                   
                if fu_inst['src2'] == fu['dest'] and fu_inst['src2_type'] == fu['dest_type'] and fu_inst['instruction'] > fu['instruction']:
                    fu_inst['q2'] = fu['instruction']
                    fu_inst['r2'] = False
                
                
        for fu in tabela_unidades_funcionais:
            if name_fu == fu['instruction']:
                fu = fu_inst
                r1 = fu['r1']
                r2 = fu['r2']
    if r1 and r2:
        leitura_operandos = True
    return tabela_unidades_funcionais, leitura_operandos

def terminou_execucao(fu):
    if fu !=None and fu['cycles_remaining'] == 0:
        return True
    return False

def executa(instruction_index, tabela_unidades_funcionais):
    fu = busca_fu_instruction(instruction_index, tabela_unidades_funcionais)
    if fu!=None:
        #if fu['r1'] and fu['r2']:
        if fu['cycles_remaining'] > 0:
            fu['cycles_remaining'] -= 1
            return True, terminou_execucao(fu)
    return False, terminou_execucao(fu)

def liberar_unidades_funcionais_reg_resultados(instruction_index, tabela_unidades_funcionais, tabela_register_result_status):
    fu_inst = busca_fu_instruction(instruction_index, tabela_unidades_funcionais)
    
    if fu_inst != None:
        fu_inst = fu_inst.copy()
        for fu in tabela_unidades_funcionais:
            if fu_inst['instruction'] == fu['instruction']:
                fu['busy']= False
                fu['operation']= None
                fu['dest'] = None
                fu['dest_type'] = None
                fu['src1'] = None
                fu['src1_type'] = None
                fu['src2'] = None
                fu['src2_type'] = None
                fu['q1'] = None
                fu['q2'] = None
                fu['r1'] = True
                fu['r2'] = True 
                fu['cycles_remaining'] = fu['cycles_needed'] 
                fu['instruction'] = None
            elif fu['q1'] ==  fu_inst['instruction']:
                fu['q1'] = None
                fu['r1'] = True
            elif fu['q2'] == fu_inst['instruction']:
                fu['q2'] = None
                fu['r2'] = True

        reg = fu_inst['dest']
        if fu_inst['dest_type'] == 'float':
            reg = "f"+str(reg)
        elif fu_inst['dest_type'] == 'int':
            reg = 'x'+str(reg)
        elif fu_inst['dest_type'] == None:
            reg = fu_inst['src2']
            if fu_inst['src2_type'] == 'float':
                reg = "f"+str(reg)
            elif fu_inst['src2_type'] == 'int':
                reg = "x"+str(reg)
        tabela_register_result_status[reg]['unit'] = None
        tabela_register_result_status[reg]['ready'] = True
    
    return tabela_unidades_funcionais, tabela_register_result_status

def escreve(instruction_index, tabela_unidades_funcionais):
    #print_fu(tabela_unidades_funcionais)
    fu_inst = busca_fu_instruction(instruction_index, tabela_unidades_funcionais)
    if fu_inst != None:
        for fu in tabela_unidades_funcionais:
            if fu['instruction'] != fu_inst['instruction']:
                #if ((fu_inst['dest'] == fu['src1'] and fu_inst['dest_type'] == fu['src1_type'] ) or (fu_inst['dest'] == fu['src2'] and fu_inst['dest_type'] == fu['src2_type'])) and fu['instruction'] < fu_inst['instruction']:                                                                                                                                                                                                                                  
                if ((fu_inst['dest'] == fu['src1'] and fu_inst['dest_type'] == fu['src1_type']) or (fu_inst['dest'] == fu['src2'] and fu_inst['dest_type'] == fu['src2_type'])) and ((fu['r1'] == False and fu['r2']==True) or (fu['r1'] == True and fu['r2']==False)) and fu['instruction'] < fu_inst['instruction']:
                    return False
    return True
    
def ler_units_config(filename):
    units = []
    with open(filename, 'r') as file:  
        for line in file:  
            line = line.strip()  
            if line:  
                units.append(line) 
    return units

    
def scoreboard(file, unit_configs):
    instructions = parse_file(file)
    tabela_instruction_status = inicializa_status_instrucao(instructions)

    tabela_unidades_funcionais = inicializa_unidades_funcionais(unit_configs)
    tabela_register_result_status = inicializa_registradores_resultado_status()
    ciclo_clock = 0
    index_next_issue = 0 
    
    teste = False
    while not todas_instrucoes_escritas(tabela_instruction_status):
    #while teste == False:
        ciclo_clock += 1
        #print("============Index: ", index_next_issue)
        #print("====================CLOCK:", ciclo_clock)
        if index_next_issue < len(instructions):
            status_issue = issue(instructions[index_next_issue],index_next_issue, tabela_unidades_funcionais, tabela_register_result_status)
            if status_issue:
                tabela_instruction_status = atualiza_instruction_status(index_next_issue, 'issued', tabela_instruction_status, ciclo_clock)
                index_next_issue += 1  

        i = index_next_issue - 1
        while i >= 0:
            if tabela_instruction_status[i]['issued'] and not tabela_instruction_status[i]['read'] and tabela_instruction_status[i]['issued'] < ciclo_clock:
                tabela_unidades_funcionais, status_leitura_operandos = verifica_operandos(i, tabela_unidades_funcionais)
                if status_leitura_operandos:
                    tabela_instruction_status = atualiza_instruction_status(i, 'read', tabela_instruction_status, ciclo_clock)
            i -=1

        i = index_next_issue - 1
        while i >= 0:
            if tabela_instruction_status[i]['read'] and not tabela_instruction_status[i]['executed'] and tabela_instruction_status[i]['read'] < ciclo_clock:
                status_execucao, terminou_execucao = executa(i, tabela_unidades_funcionais) 
                if terminou_execucao:
                    tabela_instruction_status = atualiza_instruction_status(i, 'executed', tabela_instruction_status, ciclo_clock)
            i -= 1

        i = index_next_issue - 1
        while i >= 0:
            if tabela_instruction_status[i]['executed'] and not tabela_instruction_status[i]['written'] and tabela_instruction_status[i]['executed'] < ciclo_clock:
                status_escrita = escreve(i, tabela_unidades_funcionais) 
                if status_escrita:
                    tabela_unidades_funcionais, tabela_register_result_status = liberar_unidades_funcionais_reg_resultados(i, tabela_unidades_funcionais, tabela_register_result_status)
                    tabela_instruction_status = atualiza_instruction_status(i, 'written', tabela_instruction_status, ciclo_clock)
                if i == 1:
                    teste = True
            i-=1

    return tabela_instruction_status


unit_configs = str(input("Nome do arquivo das configurações das unidades funcionais (com extensão): "))
file = str(input("Nome do arquivo com as instruções (com extensão): "))
instructions_str = get_instructions_str(file)
unit_configs_str = ler_units_config(unit_configs)
tabela_instruction_status_final = scoreboard(file, unit_configs_str)

print_instructions_table(instructions_str, tabela_instruction_status_final)
print_instructions_table_to_file(instructions_str, tabela_instruction_status_final, "resultado_"+file[:-2]+'_'+unit_configs[:-4]+'.txt')