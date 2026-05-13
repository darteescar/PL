from .ir import (
    IRInstr, IRUnit, IRProgram,
    IRPushI, IRPushF, IRPushS, IRPushN,
    IRPushG, IRPushL, IRStoreG, IRStoreL,
    IRPushGP, IRPushFP,
    IRAlloc, IRLoadN, IRStoreN,
    IRPop, IRSwap, IRDup, IRCopyK,
    IRAdd, IRSub, IRMul, IRDiv, IRMod,
    IRFAdd, IRFSub, IRFMul, IRFDiv,
    IRAnd, IROr, IRNot, IREqual,
    IRInf, IRInfEq, IRSup, IRSupEq,
    IRFInf, IRFInfEq, IRFSup, IRFSupEq,
    IRItoF, IRFtoI, IRAtoi, IRAtof,
    IRPAdd, IRStore,
    IRLabel, IRJump, IRJZ, IRPushA, IRCall, IRReturn,
    IRRead, IRWriteI, IRWriteF, IRWriteS, IRWriteLn,
    IRStart, IRStop,
)


class IRCodeGen:
    def generate(self, program: IRProgram, needs_power: bool = False) -> str:
        lines: list[str] = []

        for unit in program.units:
            lines += self._gen_unit(unit)

        if needs_power:
            lines += self._power_helper()

        return '\n'.join(lines)

    def _gen_unit(self, unit: IRUnit) -> list[str]:
        return [self._instr_to_str(i) for i in unit.instrs]


    def _instr_to_str(self, instr: IRInstr) -> str:
        # --- Literais ---
        if isinstance(instr, IRPushI):   return f'PUSHI {instr.val}'
        if isinstance(instr, IRPushF):   return f'PUSHF {instr.val:g}'
        if isinstance(instr, IRPushS):
            escaped = instr.val.replace('"', '\\"')
            return f'PUSHS "{escaped}"'
        if isinstance(instr, IRPushN):   return f'PUSHN {instr.n}'

        # --- Variáveis ---
        if isinstance(instr, IRPushG):   return f'PUSHG {instr.idx}'
        if isinstance(instr, IRPushL):   return f'PUSHL {instr.idx}'
        if isinstance(instr, IRStoreG):  return f'STOREG {instr.idx}'
        if isinstance(instr, IRStoreL):  return f'STOREL {instr.idx}'
        if isinstance(instr, IRPushGP):  return 'PUSHGP'
        if isinstance(instr, IRPushFP):  return 'PUSHFP'

        # --- Heap ---
        if isinstance(instr, IRAlloc):   return f'ALLOC {instr.n}'
        if isinstance(instr, IRLoadN):   return 'LOADN'
        if isinstance(instr, IRStoreN):  return 'STOREN'

        # --- Pilha ---
        if isinstance(instr, IRPop):     return f'POP {instr.n}'
        if isinstance(instr, IRSwap):    return 'SWAP'
        if isinstance(instr, IRDup):     return f'DUP {instr.n}'
        if isinstance(instr, IRCopyK):   return f'COPY {instr.n}'

        # --- Aritmética inteira ---
        if isinstance(instr, IRAdd):     return 'ADD'
        if isinstance(instr, IRSub):     return 'SUB'
        if isinstance(instr, IRMul):     return 'MUL'
        if isinstance(instr, IRDiv):     return 'DIV'
        if isinstance(instr, IRMod):     return 'MOD'

        # --- Aritmética real ---
        if isinstance(instr, IRFAdd):    return 'FADD'
        if isinstance(instr, IRFSub):    return 'FSUB'
        if isinstance(instr, IRFMul):    return 'FMUL'
        if isinstance(instr, IRFDiv):    return 'FDIV'

        # --- Lógica / comparação ---
        if isinstance(instr, IRAnd):     return 'AND'
        if isinstance(instr, IROr):      return 'OR'
        if isinstance(instr, IRNot):     return 'NOT'
        if isinstance(instr, IREqual):   return 'EQUAL'
        if isinstance(instr, IRInf):     return 'INF'
        if isinstance(instr, IRInfEq):   return 'INFEQ'
        if isinstance(instr, IRSup):     return 'SUP'
        if isinstance(instr, IRSupEq):   return 'SUPEQ'
        if isinstance(instr, IRFInf):    return 'FINF'
        if isinstance(instr, IRFInfEq):  return 'FINFEQ'
        if isinstance(instr, IRFSup):    return 'FSUP'
        if isinstance(instr, IRFSupEq):  return 'FSUPEQ'

        # --- Conversões ---
        if isinstance(instr, IRItoF):    return 'ITOF'
        if isinstance(instr, IRFtoI):    return 'FTOI'
        if isinstance(instr, IRAtoi):    return 'ATOI'
        if isinstance(instr, IRAtof):    return 'ATOF'

        # --- Endereços ---
        if isinstance(instr, IRPAdd):    return 'PADD'
        if isinstance(instr, IRStore):   return f'STORE {instr.n}'

        # --- Controlo de fluxo ---
        if isinstance(instr, IRLabel):   return f'{instr.name}:'
        if isinstance(instr, IRJump):    return f'JUMP {instr.label}'
        if isinstance(instr, IRJZ):      return f'JZ {instr.label}'
        if isinstance(instr, IRPushA):   return f'PUSHA {instr.label}'
        if isinstance(instr, IRCall):    return 'CALL'
        if isinstance(instr, IRReturn):  return 'RETURN'

        # --- I/O ---
        if isinstance(instr, IRRead):    return 'READ'
        if isinstance(instr, IRWriteI):  return 'WRITEI'
        if isinstance(instr, IRWriteF):  return 'WRITEF'
        if isinstance(instr, IRWriteS):  return 'WRITES'
        if isinstance(instr, IRWriteLn): return 'WRITELN'

        # --- Programa ---
        if isinstance(instr, IRStart):   return 'START'
        if isinstance(instr, IRStop):    return 'STOP'

        return f'; UNKNOWN IR: {instr!r}'

    # --- Função auxiliar para potência -------------------------------------
    def _power_helper(self) -> list[str]:
        return [
            'POWERFUNClabel:',
            'PUSHN 2',          # aloca result(fp[0]), i(fp[1])
            'PUSHI 1',
            'STOREL 0',         # result = 1
            'PUSHI 1',
            'STOREL 1',         # i = 1
            'POWERlabel:',
            'PUSHL 1',          # i
            'PUSHL -2',         # exp
            'INFEQ',            # i <= exp?
            'JZ POWERendlabel',
            'PUSHL 0',          # result
            'PUSHL -1',         # base
            'MUL',
            'STOREL 0',         # result = result * base
            'PUSHL 1',
            'PUSHI 1',
            'ADD',
            'STOREL 1',         # i = i + 1
            'JUMP POWERlabel',
            'POWERendlabel:',
            'PUSHL 0',          # result
            'STOREL -3',        # escreve no slot de retorno (fp[-3], arity=2)
            'POP 2',            # limpa locais (fp[0]=result, fp[1]=i); só locais
            'RETURN',           # chamador faz POP 2 (exp, base) após RETURN
        ]
