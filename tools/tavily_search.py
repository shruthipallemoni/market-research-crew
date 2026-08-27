from crewai_tools import TavilySearchTool


def get_tavily_search_tool() -> TavilySearchTool:
    return TavilySearchTool(
        search_depth="advanced",
        topic="general",
        max_results=3,
        include_answer=False,
    )