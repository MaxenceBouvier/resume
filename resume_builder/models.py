"""Pydantic models for CV data validation."""

from pydantic import BaseModel, Field


class Contact(BaseModel):
    """Contact information."""

    name: str
    email: str
    phone: str
    linkedin: str
    scholar: str
    location: str = ""
    website: str = ""
    github: str = ""


class Summary(BaseModel):
    """Summary/professional statement."""

    variant: str
    text: str


class Experience(BaseModel):
    """Single achievement row from experiences.csv (denormalized)."""

    company: str
    location: str
    position: str
    period: str
    achievement_group: str = ""
    achievement_text: str
    papers: int = 0
    patents: int = 0
    tags: str = ""
    weight: int = 0


class GroupedExperience(BaseModel):
    """Grouped experience for output (hierarchical)."""

    company: str
    location: str
    position: str
    period: str
    achievements: list[str] = Field(default_factory=list)
    # Optional: grouped achievement sections
    achievement_groups: dict[str, list[str]] = Field(default_factory=dict)


class Skill(BaseModel):
    """Single skill row."""

    category: str
    skill: str
    tags: str = ""
    icon: str = "Code"
    weight: int = 0


class GroupedSkill(BaseModel):
    """Grouped skills by category for output."""

    category: str
    icon: str = "Code"
    skills: list[str] = Field(default_factory=list)


class Education(BaseModel):
    """Education entry."""

    institution: str
    location: str
    degree: str
    period: str
    description: str = ""
    tags: str = ""


class Patent(BaseModel):
    """Patent entry."""

    authors: str
    title: str
    reference: str
    url: str
    year: int
    tags: str = ""
    weight: int = 0


class Publication(BaseModel):
    """Publication entry."""

    authors: str
    title: str
    venue: str
    year: int
    url: str
    tags: str = ""
    weight: int = 0


class CVData(BaseModel):
    """Complete CV data container."""

    contact: Contact
    summary: str = ""
    experiences: list[GroupedExperience] = Field(default_factory=list)
    skills: list[GroupedSkill] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    patents: list[Patent] = Field(default_factory=list)
    publications: list[Publication] = Field(default_factory=list)
