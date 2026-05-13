from dataclasses import dataclass
from parser.ast import Program
from .ir_builder   import IRBuilder
from .ir_optimizer import IROptimizer
from .ir_codegen   import IRCodeGen


@dataclass
class TranslatorError(Exception):
    message: str
    line:    int

    def __str__(self) -> str:
        return f"[Translator] Linha {self.line}: {self.message}"


class Translator:
    def __init__(self) -> None:
        self._builder   = IRBuilder()
        self._optimizer = IROptimizer()
        self._codegen   = IRCodeGen()

    def translate(self, ast: Program) -> str:
        ir, needs_power = self._builder.build(ast)
        ir              = self._optimizer.optimize(ir)
        return self._codegen.generate(ir, needs_power)
