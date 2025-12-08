#!/usr/bin/env python3
"""Lab 2.1: Function Results & Actions - Starter Template

Complete the TODOs to implement the lab requirements.
"""

from signalwire_agents import AgentBase, SwaigFunctionResult


class AppointmentAgent(AgentBase):
    def __init__(self):
        super().__init__(name="appointment-agent", route="/agent")

        self.prompt_add_section(
            "Role",
            "You are a friendly appointment scheduling assistant. "
            "Help callers confirm their appointments and send SMS confirmations."
        )

        self.add_language("English", "en-US", "rime.spore")

        # TODO: Define confirm_appointment function using define_tool()
        # The function should:
        # - Accept date, time, and phone parameters
        # - Return a SwaigFunctionResult with confirmation message
        # - Add a send_sms action to send confirmation to the phone number

    def confirm_appointment(self, args, raw_data):
        """Confirm appointment and send SMS."""
        # TODO: Implement this handler
        # 1. Extract date, time, phone from args
        # 2. Create SwaigFunctionResult with confirmation message
        # 3. Add send_sms action with to_number and body
        # 4. Return the result
        pass


agent = AppointmentAgent()

if __name__ == "__main__":
    agent.run()
