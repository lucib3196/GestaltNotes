from typing import Any


class ThreadStats:
    def summarize_thread_usage(self, thread: dict[str, Any]) -> dict[str, Any]:
        """
        Summarize message count and token usage from a single thread payload.

        Args:
            thread: dict with shape like:
                    {
                        "values": {
                            "messages": [...]
                        }
                    }

        Returns:
            dict with total_messages, input_tokens, output_tokens, total_tokens
        """

        messages = thread.get("values", {}).get("messages", [])

        created_at = thread.get("created_at")
        updated_at = thread.get("updated_at")

        input_tokens = 0
        output_tokens = 0
        total_tokens = 0
        model_name = None

        for msg in messages:
            usage = msg.get("usage_metadata", {})
            input_tokens += usage.get("input_tokens", 0)
            output_tokens += usage.get("output_tokens", 0)
            total_tokens += usage.get("total_tokens", 0)
            model_name = msg.get("response_metadata", {}).get("model_name")

        return {
            "total_messages": len(messages),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "model_name": model_name,
            "created_at": created_at,
            "updated_at": updated_at
        }
