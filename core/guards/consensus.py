"""
Multi-Agent Departmental Consensus and Sign-Off Engine.
Enforces quorum and cross-departmental approval before critical state mutations.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple, Any
from pydantic import BaseModel, Field


class DepartmentSignoff(BaseModel):
    department: str
    required_votes: int = 1
    authorized_agent_ids: Set[str] = Field(default_factory=set)


class ConsensusVote(BaseModel):
    vote_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ticket_id: str
    agent_id: str
    department: str
    approved: bool
    rationale: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConsensusEngine:
    """
    Evaluates multi-agent sign-offs across product, engineering, security, and QA.
    """

    def __init__(self, ticket_id: str):
        self.ticket_id = ticket_id
        self.requirements: Dict[str, DepartmentSignoff] = {}
        self.votes: List[ConsensusVote] = []

    def require_department(
        self,
        department: str,
        authorized_agents: List[str],
        required_votes: int = 1
    ) -> "ConsensusEngine":
        """Add a mandatory departmental sign-off rule."""
        self.requirements[department] = DepartmentSignoff(
            department=department,
            required_votes=required_votes,
            authorized_agent_ids=set(authorized_agents)
        )
        return self

    def cast_vote(
        self,
        agent_id: str,
        department: str,
        approved: bool,
        rationale: str = ""
    ) -> ConsensusVote:
        """Submit a signed vote from an agent."""
        req = self.requirements.get(department)
        if req and agent_id not in req.authorized_agent_ids:
            raise PermissionError(
                f"Agent '{agent_id}' is not authorized to vote for department '{department}'."
            )

        vote = ConsensusVote(
            ticket_id=self.ticket_id,
            agent_id=agent_id,
            department=department,
            approved=approved,
            rationale=rationale
        )
        self.votes.append(vote)
        return vote

    def evaluate_consensus(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Check if all required departments have fulfilled positive quorum.
        """
        dept_status: Dict[str, Dict[str, Any]] = {}
        all_satisfied = True

        for dept, req in self.requirements.items():
            dept_votes = [v for v in self.votes if v.department == dept]
            positive_votes = [v for v in dept_votes if v.approved]
            negative_votes = [v for v in dept_votes if not v.approved]

            is_satisfied = len(positive_votes) >= req.required_votes and len(negative_votes) == 0
            if not is_satisfied:
                all_satisfied = False

            dept_status[dept] = {
                "required": req.required_votes,
                "positive": len(positive_votes),
                "negative": len(negative_votes),
                "satisfied": is_satisfied,
                "signoffs": [v.agent_id for v in positive_votes]
            }

        return all_satisfied, {
            "ticket_id": self.ticket_id,
            "consensus_reached": all_satisfied,
            "departments": dept_status,
            "total_votes_cast": len(self.votes)
        }
