from pydantic import BaseModel, Field
from typing import List, Optional


class CompetitorProfile(BaseModel):
    name: str = Field(description="The competitor's company or product name")
    description: str = Field(description="What they do, in 1-2 sentences")
    strengths: List[str] = Field(description="Key competitive strengths, 2-4 bullet points")
    weaknesses: List[str] = Field(description="Known weaknesses or gaps, 1-3 bullet points")


class SWOT(BaseModel):
    strengths: List[str] = Field(description="Strengths of the market opportunity or dominant players")
    weaknesses: List[str] = Field(description="Weaknesses or gaps in the current market")
    opportunities: List[str] = Field(description="Untapped opportunities or emerging trends to exploit")
    threats: List[str] = Field(description="Risks, threats, or headwinds facing entrants in this market")


class Recommendation(BaseModel):
    action: str = Field(description="A single, concrete, actionable recommendation")
    justification: str = Field(description="Which insight or data point this recommendation is based on")
    priority: str = Field(description="Priority level: High, Medium, or Low")


class MarketResearchReport(BaseModel):
    market_overview: str = Field(description="Market size, growth rate, and key trends, in prose form")
    competitive_landscape: List[CompetitorProfile] = Field(description="Profiles of key competitors identified")
    swot_insights: SWOT = Field(description="SWOT analysis of the market opportunity")
    strategic_recommendations: List[Recommendation] = Field(description="Actionable recommendations, each justified")
    sources: List[str] = Field(description="All source URLs referenced across the research")