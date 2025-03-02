from agents_core.base_agent import BaseAgent


class IPBlockDetectorAgent(BaseAgent):
    """
    Detects if the request is ip_blocked due to IP or proxy issues using both
    deterministic checks and low-cost LLM-augmented analysis via bound tools.
    """

    def run(self, status: int, headers: dict) -> dict:
        # --- Deterministic checks ---
        if status in (403, 429):
            return {
                "ip_blocked": True,
                "ip_reason": f"HTTP status {status} indicates possible IP block.",
            }

        proxy_block_headers = ["X-Blocked-Reason", "X-IP-Blocked"]
        for header in proxy_block_headers:
            if header in headers:
                return {
                    "ip_blocked": True,
                    "ip_reason": f"Header {header} indicates an IP block.",
                }

        # --- Low-cost LLM analysis via bound tools ---
        def analyze_status(s: int) -> str:
            if s in (403, 429):
                return f"Status code {s} strongly suggests an IP block."
            return f"Status code {s} appears normal."

        def analyze_headers(h: dict) -> str:
            for key in proxy_block_headers:
                if key in h:
                    return f"Header {key} indicates an IP block."
            return "No blocking indicators found in headers."

        llm_with_tools = self.llm.bind_tools([analyze_status, analyze_headers])
        prompt = (
            "Based on the following metadata, determine if there is an IP block and explain your reasoning.\n"
            f"Status: {status}\n"
            f"Headers: {headers}\n"
            "Answer in the format: 'blocked: <reason>' or 'not blocked: <explanation>'."
        )
        response = llm_with_tools.invoke(prompt)
        # Ensure a fallback is provided if the response is empty.
        if response and response.content:
            if "blocked" in response.content.lower():
                return {"ip_blocked": True, "ip_reason": response.content.strip()}
            else:
                return {"ip_blocked": False, "ip_reason": response.content.strip()}
        else:
            return {
                "ip_blocked": False,
                "ip_reason": f"Status code {status} appears normal.",
            }
