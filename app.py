from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai.project import load_crew
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Market Research Crew API")


class ResearchRequest(BaseModel):
    topic: str


@app.post("/research")
def run_research(request: ResearchRequest):
    logger.info(f"Received research request for topic: {request.topic}")

    try:
        crew, default_inputs = load_crew(Path(__file__).with_name("crew.jsonc"))
        result = crew.kickoff(inputs={**default_inputs, "topic": request.topic})
    except Exception as e:
        logger.error(f"Crew execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Research crew failed: {str(e)}")

    # result.pydantic gives you the validated MarketResearchReport object
    # when output_pydantic was set on the final task
    if result.pydantic:
        return result.pydantic.model_dump()

    # Fallback: if Pydantic validation failed upstream, return raw text
    logger.warning("Pydantic validation missing — returning raw output")
    return {"raw_output": result.raw}