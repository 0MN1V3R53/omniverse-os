#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from core.ast_engine.navigator import ASTNavigator

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'core/cognition/models.py'
    nav = ASTNavigator()
    rep = nav.verify_ast_integrity(open(target, 'r').read())
    print(f"AST_VERIFIED:{target}:NODES={rep.node_count}:CLASSES={len(rep.defined_classes)}")
