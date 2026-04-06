from dataclasses import dataclass

@dataclass
class LogicalLine:
    """
    Representação lógica de uma linha.
    Pode conter várias linhas originais.
    """
    label: str | None   # label da linha, se existir
    content: str        # codigo da linha sem label
    src_line: int       # numero da 1a linha original
    
@dataclass
class PreprocessorError(Exception):
    """
    Erro de pré-processamento.
    """
    message: str
    line_number: int
    
    def __str__(self) -> str:
        return f"[Preprocessor] Linha {self.line_number}: {self.message}"
    
class Preprocessor:
    _COL_COMMENT    = 0          # índice 0  -> coluna 1
    _COL_LABEL_END  = 5          # índice 0:5 -> colunas 1-5
    _COL_CONT       = 5          # índice 5   -> coluna 6
    _COL_CODE_START = 6          # índice 6   -> coluna 7
    _COL_CODE_END   = 72         # índice 72  -> coluna 73 (exclusive)
    
    def __init__(self, source_code: str) -> None:
        self._source_code = source_code
        self._logical_lines: list[LogicalLine] = []

    def process(self) -> list[LogicalLine]:
        self._logical_lines = []
        original_lines = self._source_code.splitlines()
        
        # Estado da linha a ser processada
        current_label: str | None = None
        current_content: str = ""
        current_start = 0
        in_continuation = False
        
        for lineno, raw_line in enumerate(original_lines, start=1):
            line = raw_line.upper() # Garantir que é tudo maiúsculo
            
            if not line.strip():
                continue
            
            if line[self._COL_COMMENT] in ('C', '*'): # Linha comentario
                continue
            
            # Verificar se é linha de continuação
            col6 = line[self._COL_CONT] if len(line) > self._COL_CONT else ' '
            is_continuation = col6 not in (' ', '0')
            
            if is_continuation:
                if not in_continuation:
                    raise PreprocessorError("Linha de continuação sem linha anterior", lineno)
                
                # Junta o código desta linha a linha em curso
                code = self._extract_code(line)
                current_content += code
                continue       
            
            # Nova linha lógica
            # Guardar linha lógica anterior, se existir
            if in_continuation or current_content:
                self._logical_lines.append(
                    LogicalLine(
                        label=current_label,
                        content=current_content.strip(),
                        src_line=current_start,
                    )
                )
            
            # Extrai label e código da nova linha
            current_label   = self._extract_label(line)
            current_content = self._extract_code(line)
            current_start   = lineno
            in_continuation = True
            
        # Guarda a última linha  lógica pendente
        if current_content.strip():
            self._logical_lines.append(
                LogicalLine(
                    label=current_label,
                    content=current_content.strip(),
                    src_line=current_start,
                )
            )

        return self._logical_lines
        
    def _extract_label(self, line: str) -> str | None:
        """
        Extrai o label das colunas 1-5.
        """
        raw_label = line[:self._COL_LABEL_END]
        label = raw_label.strip()
        if label:
            if not label.isdigit():
                raise PreprocessorError(
                    f"Label inválido: '{label}' (deve ser numérico).",
                    line_number=0,
                )
            return label
        return None
    
    def _extract_code(self, line: str) -> str:
        """
        Extrai o código das colunas 7-72 (índices 6:72).
        """
        if len(line) <= self._COL_CODE_START:
            return ""
        return line[self._COL_CODE_START:self._COL_CODE_END]
    
    def dump(self) -> None:
        if not self._logical_lines:
            self.process()
        print(f"{'#':<4}  {'Label':<6}  {'SrcLine':<8}  Conteúdo")
        print("-" * 70)
        for i, ll in enumerate(self._logical_lines):
            label_str = ll.label if ll.label else ""
            print(f"{i:<4}  {label_str:<6}  {ll.src_line:<8}  {ll.content}")