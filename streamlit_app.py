from pathlib import Path
from typing import Any, Callable

import streamlit as st
from crewai.project import load_crew


def _value(event: Any, name: str, default: str = "") -> str:
    value = getattr(event, name, default)
    return str(value) if value is not None else default


def _agent_step_message(step: Any) -> str:
    agent = _value(step, "agent", "Agent")
    thought = _value(step, "thought")
    tool = _value(step, "tool")
    tool_input = _value(step, "tool_input")

    if tool:
        message = f"{agent} is using `{tool}`"
        return f"{message} with `{tool_input}`" if tool_input else message
    if thought:
        return f"{agent}: {thought}"
    return f"{agent} is working"


def run_research(topic: str, on_event: Callable[[str, str], None]) -> Any:
    crew, default_inputs = load_crew(Path(__file__).with_name("crew.jsonc"))

    def on_step(step: Any) -> None:
        on_event("agent", _agent_step_message(step))

    def on_task(task: Any) -> None:
        on_event("task", f"Completed: {_value(task, 'task', 'Task')}")

    crew.step_callback = on_step
    crew.task_callback = on_task
    return crew.kickoff(inputs={**default_inputs, "topic": topic})


def render_report(result: Any) -> None:
    report = result.pydantic
    if report is None:
        st.markdown(result.raw)
        return

    st.subheader("Market Overview")
    st.write(report.market_overview)

    st.subheader("Competitive Landscape")
    for competitor in report.competitive_landscape:
        with st.expander(competitor.name, expanded=True):
            st.write(competitor.description)
            st.markdown("**Strengths**")
            st.write("\n".join(f"- {item}" for item in competitor.strengths))
            st.markdown("**Weaknesses**")
            st.write("\n".join(f"- {item}" for item in competitor.weaknesses))

    st.subheader("SWOT Insights")
    swot = report.swot_insights
    columns = st.columns(4)
    for column, title, items in zip(
        columns,
        ("Strengths", "Weaknesses", "Opportunities", "Threats"),
        (swot.strengths, swot.weaknesses, swot.opportunities, swot.threats),
    ):
        with column:
            st.markdown(f"**{title}**")
            st.write("\n".join(f"- {item}" for item in items))

    st.subheader("Strategic Recommendations")
    for recommendation in report.strategic_recommendations:
        st.markdown(f"**{recommendation.priority}: {recommendation.action}**")
        st.write(recommendation.justification)

    st.subheader("Sources")
    for source in report.sources:
        st.markdown(f"- [{source}]({source})")


st.set_page_config(page_title="Market Research Crew", page_icon=":bar_chart:", layout="wide")
st.title("Market Research Crew")
st.caption("A live research briefing from four collaborating agents")

with st.sidebar:
    st.header("New research brief")
    topic = st.text_input("Market or topic", placeholder="Healthcare market")
    start = st.button("Start research", type="primary", use_container_width=True)
    st.divider()
    st.caption("The activity panel updates as agents plan, search, analyze, and synthesize.")

if start:
    if not topic.strip():
        st.warning("Enter a market or topic first.")
        st.stop()

    st.subheader(f"Researching: {topic.strip()}")
    activity = st.empty()
    status = st.status("Crew is starting...", expanded=True)
    events: list[str] = []

    def show_event(kind: str, message: str) -> None:
        label = "AGENT" if kind == "agent" else "TASK"
        events.append(f"**{label}**  {message}")
        activity.markdown("\n\n".join(events[-12:]))

    try:
        result = run_research(topic.strip(), show_event)
        status.update(label="Research complete", state="complete")
        st.success("Your market research report is ready.")
        render_report(result)
    except Exception as error:
        status.update(label="Research failed", state="error")
        st.error(f"The research crew failed: {error}")
