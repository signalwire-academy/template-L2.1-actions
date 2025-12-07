#!/usr/bin/env python3
"""Appointment agent with action chaining.

Lab 2.1 Deliverable: Demonstrates SwaigFunctionResult action chaining
including post-process actions for transfers and callbacks.
"""

from signalwire_agents import AgentBase, SwaigFunctionResult


class AppointmentAgent(AgentBase):
    """Agent for scheduling appointments with action chaining."""

    def __init__(self):
        super().__init__(name="appointment-agent")

        self.prompt_add_section(
            "Role",
            "You help customers schedule and confirm appointments."
        )

        self.prompt_add_section(
            "Capabilities",
            bullets=[
                "Confirm appointments with SMS notifications",
                "Schedule callbacks for follow-up",
                "Escalate to supervisor when needed"
            ]
        )

        self.add_language("English", "en-US", "rime.spore")
        self._setup_functions()

    def _setup_functions(self):
        @self.tool(
            description="Confirm an appointment",
            parameters={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Appointment date"},
                    "time": {"type": "string", "description": "Appointment time"},
                    "phone": {"type": "string", "description": "Customer phone"}
                },
                "required": ["date", "time", "phone"]
            }
        )
        def confirm_appointment(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            """Confirm appointment with multiple chained actions."""
            date = args.get("date", "")
            time = args.get("time", "")
            phone = args.get("phone", "")
            return (
                SwaigFunctionResult(
                    f"Your appointment is confirmed for {date} at {time}. "
                    "I've sent a confirmation to your phone."
                )
                .send_sms(
                    to_number=phone,
                    from_number="+15559999999",
                    body=f"Appointment confirmed: {date} at {time}"
                )
                .update_global_data({
                    "appointment_date": date,
                    "appointment_time": time,
                    "confirmed": True
                })
            )

        @self.tool(
            description="Schedule a callback for the customer",
            parameters={
                "type": "object",
                "properties": {
                    "phone": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": ["phone", "reason"]
            }
        )
        def schedule_callback(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            """Schedule callback using post-process action."""
            phone = args.get("phone", "")
            reason = args.get("reason", "")
            return (
                SwaigFunctionResult(
                    "I've scheduled a callback for you. "
                    "One of our team members will reach out soon.",
                    post_process=True
                )
                .update_global_data({
                    "callback_phone": phone,
                    "callback_reason": reason,
                    "callback_scheduled": True
                })
            )

        @self.tool(
            description="Escalate call to supervisor",
            parameters={
                "type": "object",
                "properties": {
                    "reason": {"type": "string", "description": "Escalation reason"}
                },
                "required": ["reason"]
            }
        )
        def escalate_call(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            """Escalate to supervisor with post-process transfer."""
            reason = args.get("reason", "")
            return (
                SwaigFunctionResult(
                    "I understand this needs supervisor attention. "
                    "Let me transfer you now.",
                    post_process=True
                )
                .update_global_data({"escalation_reason": reason})
                .connect("+15551234567", final=True)
            )

        @self.tool(
            description="Cancel an appointment",
            parameters={
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "string"},
                    "phone": {"type": "string"}
                },
                "required": ["appointment_id", "phone"]
            }
        )
        def cancel_appointment(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            """Cancel appointment with SMS confirmation."""
            appointment_id = args.get("appointment_id", "")
            phone = args.get("phone", "")
            return (
                SwaigFunctionResult(
                    f"Appointment {appointment_id} has been cancelled. "
                    "I've sent a confirmation to your phone. "
                    "Would you like to reschedule?"
                )
                .send_sms(
                    to_number=phone,
                    from_number="+15559999999",
                    body=f"Appointment {appointment_id} cancelled."
                )
                .update_global_data({
                    "cancelled_appointment": appointment_id,
                    "cancellation_confirmed": True
                })
            )


if __name__ == "__main__":
    agent = AppointmentAgent()
    agent.run()
