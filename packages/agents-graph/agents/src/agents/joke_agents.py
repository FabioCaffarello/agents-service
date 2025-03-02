from agents_core.base_agent import BaseAgent


class JokeGeneratorAgent(BaseAgent):
    def run(self, topic: str) -> dict:
        prompt_template = self.config.get(
            "prompt_template", "Write a short joke about {topic}"
        )
        prompt = prompt_template.format(topic=topic)
        response = self.llm.invoke(prompt)
        return {"joke": response.content}


class JokeImproverAgent(BaseAgent):
    def run(self, joke: str) -> dict:
        prompt_template = self.config.get(
            "prompt_template", "Make this joke funnier by adding wordplay: {joke}"
        )
        prompt = prompt_template.format(joke=joke)
        response = self.llm.invoke(prompt)
        return {"improved_joke": response.content}


class JokePolisherAgent(BaseAgent):
    def run(self, improved_joke: str) -> dict:
        prompt_template = self.config.get(
            "prompt_template", "Add a surprising twist to this joke: {improved_joke}"
        )
        prompt = prompt_template.format(improved_joke=improved_joke)
        response = self.llm.invoke(prompt)
        return {"final_joke": response.content}
