"""
Stage 3: Autonomous Self-Healing Fixer Engine.
Detects failed test assertions or syntax issues and attempts targeted heuristic/AI diff patching.
"""
from typing import Dict, Any, Tuple
try:
    from .ast_diff import ASTInspector
except ImportError:
    from ast_diff import ASTInspector

class SelfHealer:
    @staticmethod
    def attempt_syntax_repair(broken_code: str) -> Tuple[bool, str, str]:
        """
        Attempts autonomous syntax error remediation.
        Returns: (success: bool, healed_code: str, unified_diff: str)
        """
        is_valid, err = ASTInspector.validate_syntax(broken_code)
        if is_valid:
            return True, broken_code, ""

        # Example auto-repair pattern: missing colon or closing parenthesis
        lines = broken_code.splitlines()
        repaired_lines = []
        
        for line in lines:
            stripped = line.strip()
            # Heuristic 1: Add missing colon on def/if/for/while/class
            if any(stripped.startswith(kw) for kw in ["def ", "if ", "for ", "while ", "class ", "elif ", "else", "try", "except"]) and not stripped.endswith(":"):
                line = line + ":"
            # Heuristic 2: Missing closing quote on simple single-line string
            if line.count('"') % 2 != 0:
                line = line + '"'
            repaired_lines.append(line)

        healed_code = "\n".join(repaired_lines)
        is_healed, _ = ASTInspector.validate_syntax(healed_code)
        
        if is_healed:
            diff = ASTInspector.generate_unified_diff(broken_code, healed_code)
            return True, healed_code, diff
        
        return False, broken_code, ""
