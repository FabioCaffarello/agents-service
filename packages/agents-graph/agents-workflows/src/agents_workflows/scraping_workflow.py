import asyncio
import subprocess
from typing_extensions import TypedDict
from logger.log import get_logger_from_env
from langgraph.graph import StateGraph, START, END
from application.dtos.agent_dto import ScrapingPayloadDTO
from agents_core.dynamic_agent_factory import DynamicAgentFactory


log = get_logger_from_env(__file__)


def render_mermaid_diagram(
    mermaid_text: str, mmd_file: str = "diagram.mmd", output_file: str = "diagram.png"
):
    # Save the Mermaid code to a file.
    with open(mmd_file, "w") as f:
        f.write(mermaid_text)
    try:
        # Run Mermaid CLI to generate a PNG.
        subprocess.run(["mmdc", "-i", mmd_file, "-o", output_file], check=True)
        print(f"Mermaid diagram rendered and saved to {output_file}")
    except Exception as e:
        print(f"Error rendering mermaid diagram: {e}")


class State(TypedDict):
    topic: str
    joke: str
    improved_joke: str
    final_joke: str


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

        # Dynamically create agents using the factory.
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

        workflow.add_edge(START, "joke_generator")
        workflow.add_conditional_edges(
            "joke_generator",
            self.check_punchline,
            {"Fail": "joke_improver", "Pass": END},
        )
        workflow.add_edge("joke_improver", "joke_polisher")
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

        return {
            "usage": "scraping",
            "bot_name": self.payload.bot_name,
            "processed_data": self.payload,
            "message": "Processed using ScrapingWorkflow.",
        }

    def check_punchline(self, state: State):
        """Gate function to check if the joke has a punchline."""
        return "Fail" if ("?" in state["joke"] or "!" in state["joke"]) else "Pass"
