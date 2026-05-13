"""
Representação Intermédia

Estrutura:
    IRProgram
        IRUnit[]   (uma por PROGRAM/FUNCTION/SUBROUTINE)
            IRInstr[]  (sequência de instruções)
"""

from dataclasses import dataclass, field

class IRInstr:
    """Classe base para todas as instruções IR."""
    pass

# --- Literais / empilhar constantes ----------------------------------------
@dataclass
class IRPushI(IRInstr):
    """PUSHI n  —  empilha inteiro n."""
    val: int

@dataclass
class IRPushF(IRInstr):
    """PUSHF x  —  empilha real x."""
    val: float

@dataclass
class IRPushS(IRInstr):
    """PUSHS "s"  —  arquiva s na string heap e empilha o endereço."""
    val: str

@dataclass
class IRPushN(IRInstr):
    """PUSHN n  —  empilha n zeros (alocação de variáveis locais/globais)."""
    n: int

# --- Acesso a variáveis (stack frame) --------------------------------------
@dataclass
class IRPushG(IRInstr):
    """PUSHG n  —  empilha gp[n]."""
    idx: int

@dataclass
class IRPushL(IRInstr):
    """PUSHL n  —  empilha fp[n].  n pode ser negativo (parâmetros)."""
    idx: int

@dataclass
class IRStoreG(IRInstr):
    """STOREG n  —  guarda topo em gp[n]."""
    idx: int

@dataclass
class IRStoreL(IRInstr):
    """STOREL n  —  guarda topo em fp[n]."""
    idx: int

@dataclass
class IRPushGP(IRInstr):
    """PUSHGP  —  empilha o valor do registo gp (endereço base global)."""
    pass

@dataclass
class IRPushFP(IRInstr):
    """PUSHFP  —  empilha o valor do registo fp."""
    pass

# --- Heap (arrays dinâmicos) -----------------------------------------------
@dataclass
class IRAlloc(IRInstr):
    """ALLOC n  —  aloca bloco de n slots na heap e empilha o endereço."""
    n: int

@dataclass
class IRLoadN(IRInstr):
    """LOADN  —  pilha [..., addr, idx] → empilha addr[idx]."""
    pass

@dataclass
class IRStoreN(IRInstr):
    """STOREN  —  pilha [..., addr, idx, val] → guarda val em addr[idx]."""
    pass

# --- Manipulação de pilha --------------------------------------------------
@dataclass
class IRPop(IRInstr):
    """POP n  —  descarta n valores do topo."""
    n: int

@dataclass
class IRSwap(IRInstr):
    """SWAP  —  troca os dois valores no topo."""
    pass

@dataclass
class IRDup(IRInstr):
    """DUP n  —  duplica o topo n vezes."""
    n: int

@dataclass
class IRCopyK(IRInstr):
    """COPY n  —  copia os n valores do topo e empilha-os na mesma ordem."""
    n: int

#  --- Aritmética inteira ---------------------------------------------------
@dataclass
class IRAdd(IRInstr):
    """ADD  —  m + n."""
    pass

@dataclass
class IRSub(IRInstr):
    """SUB  —  m - n."""
    pass

@dataclass
class IRMul(IRInstr):
    """MUL  —  m * n."""
    pass

@dataclass
class IRDiv(IRInstr):
    """DIV  —  m / n."""
    pass

@dataclass
class IRMod(IRInstr):
    """MOD  —  m mod n."""
    pass


# --- Aritmética real -------------------------------------------------------

@dataclass
class IRFAdd(IRInstr):
    """FADD."""
    pass

@dataclass
class IRFSub(IRInstr):
    """FSUB."""
    pass

@dataclass
class IRFMul(IRInstr):
    """FMUL."""
    pass

@dataclass
class IRFDiv(IRInstr):
    """FDIV."""
    pass

# --- Operações lógicas e comparações ---------------------------------------
@dataclass
class IRAnd(IRInstr):
    """AND  —  n && m."""
    pass

@dataclass
class IROr(IRInstr):
    """OR  —  n || m."""
    pass

@dataclass
class IRNot(IRInstr):
    """NOT  —  n == 0."""
    pass

@dataclass
class IREqual(IRInstr):
    """EQUAL  —  n == m."""
    pass

@dataclass
class IRInf(IRInstr):
    """INF  —  m < n."""
    pass

@dataclass
class IRInfEq(IRInstr):
    """INFEQ  —  m <= n."""
    pass

@dataclass
class IRSup(IRInstr):
    """SUP  —  m > n."""
    pass

@dataclass
class IRSupEq(IRInstr):
    """SUPEQ  —  m >= n."""
    pass

@dataclass
class IRFInf(IRInstr):
    """FINF  —  m < n (reais)."""
    pass

@dataclass
class IRFInfEq(IRInstr):
    """FINFEQ."""
    pass

@dataclass
class IRFSup(IRInstr):
    """FSUP."""
    pass

@dataclass
class IRFSupEq(IRInstr):
    """FSUPEQ."""
    pass

# ---- Conversões de tipo ---------------------------------------------------
@dataclass
class IRItoF(IRInstr):
    """ITOF  —  inteiro → real."""
    pass

@dataclass
class IRFtoI(IRInstr):
    """FTOI  —  real → inteiro (trunca)."""
    pass

@dataclass
class IRAtoi(IRInstr):
    """ATOI  —  string heap → inteiro."""
    pass

@dataclass
class IRAtof(IRInstr):
    """ATOF  —  string heap → real."""
    pass

# --- Aritmética de endereços -----------------------------------------------
@dataclass
class IRPAdd(IRInstr):
    """PADD  —  pilha [..., addr, n] → addr + n."""
    pass

@dataclass
class IRStore(IRInstr):
    """STORE n  —  pilha [..., val, addr] → guarda val em addr[n] (pilha ou heap)."""
    n: int

# --- Controlo de fluxo -----------------------------------------------------
@dataclass
class IRLabel(IRInstr):
    """Definição de label  →  'name:'."""
    name: str

@dataclass
class IRJump(IRInstr):
    """JUMP label  —  salto incondicional."""
    label: str

@dataclass
class IRJZ(IRInstr):
    """JZ label  —  salta se topo == 0."""
    label: str

@dataclass
class IRPushA(IRInstr):
    """PUSHA label  —  empilha endereço do label."""
    label: str

@dataclass
class IRCall(IRInstr):
    """CALL  —  chama subprograma."""
    pass

@dataclass
class IRReturn(IRInstr):
    """RETURN  —  retorna ao chamador."""
    pass

# --- I/O -------------------------------------------------------------------
@dataclass
class IRRead(IRInstr):
    """READ  —  lê string do stdin e empilha endereço na string heap."""
    pass

@dataclass
class IRWriteI(IRInstr):
    """WRITEI  —  imprime inteiro do topo."""
    pass

@dataclass
class IRWriteF(IRInstr):
    """WRITEF  —  imprime real do topo."""
    pass

@dataclass
class IRWriteS(IRInstr):
    """WRITES  —  imprime string do topo."""
    pass

@dataclass
class IRWriteLn(IRInstr):
    """WRITELN  —  imprime newline."""
    pass

#  --- Controlo de programa -------------------------------------------------
@dataclass
class IRStart(IRInstr):
    """START  —  inicializa fp = sp."""
    pass

@dataclass
class IRStop(IRInstr):
    """STOP  —  termina o programa."""
    pass

# Unidade de programa e programa completo
@dataclass
class IRUnit:
    name:   str
    kind:   str # 'PROGRAM' | 'FUNCTION' | 'SUBROUTINE'
    instrs: list[IRInstr] = field(default_factory=list)


@dataclass
class IRProgram:
    """Raiz da representação intermédia — contém todas as unidades de programa."""
    units: list[IRUnit] = field(default_factory=list)
