import asyncio
from typing_extensions import TypedDict
from logger.log import get_logger_from_env
from langgraph.graph import StateGraph, START, END
from application.dtos.agent_dto import ScrapingPayloadDTO
from agents_core.dynamic_agent_factory import DynamicAgentFactory

log = get_logger_from_env(__file__)


class State(TypedDict):
    topic: str
    joke: str
    improved_joke: str
    final_joke: str
    ip_blocked: bool
    ip_reason: str
    combined_output: str


class ScrapingWorkflow:
    def __init__(self, llm, payload: ScrapingPayloadDTO):
        self.llm = llm
        self.payload = payload
        self.agent_factory = DynamicAgentFactory(llm)

    async def run(self):
        """
        Runs the scraping workflow.
        """
        await asyncio.sleep(0.5)
        workflow = StateGraph(State)

        # Dynamically create agents.
        ip_detector = self.agent_factory.create_agent("ip_detector")
        gen_agent = self.agent_factory.create_agent("joke_generator")
        improve_agent = self.agent_factory.create_agent("joke_improver")
        polish_agent = self.agent_factory.create_agent("joke_polisher")

        # Register workflow nodes.
        workflow.add_node(
            "joke_generator", lambda state: gen_agent.run(topic=state["topic"])
        )
        workflow.add_node(
            "joke_improver", lambda state: improve_agent.run(joke=state["joke"])
        )
        workflow.add_node(
            "joke_polisher",
            lambda state: polish_agent.run(improved_joke=state["improved_joke"]),
        )
        # IP detector node; its result will be stored under "ip_detector".
        workflow.add_node(
            "ip_detector",
            lambda state: ip_detector.run(
                status=self.payload.response.status,
                headers=self.payload.response.headers,
            ),
        )

        # Aggregator node.
        def format_topic(state: dict) -> str:
            topic = state.get("topic", "N/A")
            return f"Topic: {topic}"

        def format_joke(state: dict) -> str:
            if state.get("joke"):
                return f"Initial Joke: {state['joke']}"
            return "Initial Joke: N/A"

        def format_ip_info(state: dict) -> str:
            status_line = "BLOCKED" if state.get("ip_blocked") else "Not Blocked"
            reason = state.get("ip_reason", "No block indicators detected")
            return f"IP Detector: {status_line} ({reason})"

        def aggregator(state: dict) -> dict:
            parts = [format_topic(state), format_joke(state), format_ip_info(state)]
            combined = "\n".join(parts)
            return {"combined_output": combined}

        workflow.add_node("aggregator", aggregator)

        # Build edges: run ip_detector and joke_generator in parallel,
        # then merge their outputs in aggregator.
        workflow.add_edge(START, "ip_detector")
        workflow.add_edge(START, "joke_generator")
        workflow.add_conditional_edges(
            "joke_generator",
            self.check_punchline,
            {"Fail": "joke_improver", "Pass": END},
        )
        workflow.add_edge("joke_improver", "joke_polisher")
        workflow.add_edge("ip_detector", "aggregator")
        workflow.add_edge("joke_generator", "aggregator")
        workflow.add_edge("aggregator", END)
        workflow.add_edge("joke_polisher", END)

        chain = workflow.compile()
        log.debug("Workflow graph:")
        chain.get_graph().print_ascii()

        state = chain.invoke({"topic": "cats"})

        log.debug("Initial joke:")
        log.debug(state["joke"])
        log.debug("\n--- --- ---\n")

        if "improved_joke" in state:
            log.debug("Improved joke:")
            log.debug(state["improved_joke"])
            log.debug("\n--- --- ---\n")
            log.debug("Final joke:")
            log.debug(state["final_joke"])
        else:
            log.debug("Joke failed quality gate - no punchline detected!")

        log.debug("\n---")
        log.debug("State")
        log.debug(state)
        log.debug("\n---")

        return {
            "usage": "scraping",
            "bot_name": self.payload.bot_name,
            "processed_data": self.payload,
            "message": state["combined_output"],
        }

    def check_punchline(self, state: State):
        """Gate function to check if the joke has a punchline."""
        return "Fail" if ("?" in state["joke"] or "!" in state["joke"]) else "Pass"
