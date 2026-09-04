"""
Executable JIT Skill Vault Engine.
Self-compiles successful multi-step agent workflows into executable Python CLI tools and maintains a discoverable manifest.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from core.config import CONFIG
from core.ast_engine.navigator import ASTNavigator
from core.skills.models import JITSkill, SkillManifest



class SkillVaultEngine:
    """
    JIT Skill compilation, discovery, and execution vault.
    """

    def __init__(self, skills_dir: Optional[Path] = None):
        self.skills_dir = skills_dir or (CONFIG.workspace_root / "core" / "skills")
        self.manifest_path = self.skills_dir / "manifest.json"
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.ast_navigator = ASTNavigator()
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> SkillManifest:
        """Load manifest from JSON or initialize with default skills."""
        if self.manifest_path.exists():
            try:
                data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
                return SkillManifest.model_validate(data)
            except Exception:
                pass
        
        manifest = SkillManifest(skills=[])
        self._save_manifest(manifest)
        return manifest

    def _save_manifest(self, manifest: Optional[SkillManifest] = None) -> None:
        """Persist manifest to JSON."""
        man = manifest or self.manifest
        man.updated_at = datetime.utcnow()
        self.manifest_path.write_text(
            json.dumps(man.model_dump(), indent=2, default=str),
            encoding="utf-8"
        )

    def compile_and_register_skill(
        self,
        name: str,
        domain: str,
        description: str,
        author_agent_id: str,
        python_code: str,
        input_parameters: Optional[Dict[str, str]] = None,
        output_schema: Optional[Dict[str, str]] = None
    ) -> JITSkill:
        """
        Validate, compile, and register an executable Python script as a JIT Skill.
        """
        # 1. Verify AST Syntax
        ast_rep = self.ast_navigator.verify_ast_integrity(python_code)
        if not ast_rep.is_valid_syntax:
            raise ValueError(f"Cannot compile skill '{name}': {ast_rep.error_message}")

        # 2. Write executable script
        domain_dir = self.skills_dir / domain
        domain_dir.mkdir(parents=True, exist_ok=True)
        script_filename = f"{name.lower().replace(' ', '_')}.py"
        script_path = domain_dir / script_filename
        script_path.write_text(python_code, encoding="utf-8")

        # 3. Create JITSkill entry
        try:
            rel_path = str(script_path.relative_to(CONFIG.workspace_root))
        except ValueError:
            rel_path = str(script_path)

        skill = JITSkill(
            name=name,
            domain=domain,
            description=description,
            author_agent_id=author_agent_id,
            executable_path=rel_path,
            cli_command_template=f"python3 {rel_path}",
            input_parameters=input_parameters or {},
            output_schema=output_schema or {},
            invocations_count=0
        )

        # Check if updating existing skill
        existing_idx = next((i for i, s in enumerate(self.manifest.skills) if s.name == name), None)
        if existing_idx is not None:
            self.manifest.skills[existing_idx] = skill
        else:
            self.manifest.skills.append(skill)

        self._save_manifest()
        return skill

    def discover_skills(self, query: str = "") -> List[JITSkill]:
        """
        Search for available skills matching a query or domain.
        """
        if not query:
            return self.manifest.skills

        q = query.lower()
        return [
            s for s in self.manifest.skills
            if q in s.name.lower() or q in s.domain.lower() or q in s.description.lower()
        ]

    def execute_skill(self, skill_id: str, cli_args: Optional[List[str]] = None) -> str:
        """
        Execute a registered skill script synchronously.
        """
        skill = next((s for s in self.manifest.skills if s.skill_id == skill_id or s.name == skill_id), None)
        if not skill:
            raise ValueError(f"Skill '{skill_id}' not found in manifest.")

        full_path = Path(skill.executable_path)
        if not full_path.is_absolute():
            full_path = CONFIG.workspace_root / full_path

        if not full_path.exists():
            raise FileNotFoundError(f"Skill executable '{full_path}' does not exist.")

        cmd = [sys.executable, str(full_path)] + (cli_args or [])
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(CONFIG.workspace_root), timeout=30)
        
        skill.invocations_count += 1
        self._save_manifest()
        return res.stdout.strip() or res.stderr.strip()



# Global Singleton Skill Vault
GLOBAL_SKILL_VAULT = SkillVaultEngine()
