import json
from utils import convert_to_xlam_tool

AGENT_INTRUCTION_PROMPT = lambda agent_desp : f"""
{agent_desp}
You are also an expert in composing functions and generating detailed action plans. You have been given a query and a set of possible functions. Based on the query, you need to determine which function calls are needed and generate a detailed action plan to address the query.

**Instructions:**

1. **Analyze the Query:** Break down the query into key components and identify the core problem or opportunity. Determine if the provided functions can be used to address the query.

2. **Function Calls Determination:**
   - If the given query and functions are sufficient, decide which function(s) to call.
   - If no functions can be used, or if the query lacks required parameters, state this clearly.

3. **Thought Process:** Describe your thought process as an expert in composing functions. Consider the relevance and appropriateness of each function, the completeness of the query, and any assumptions you might have.

4. **Action Plan:** Based on your analysis, outline the specific actions you will take to address the query. Include:
   - Short-term and long-term strategies.
   - Details of the function calls required (if any).
   - Any other relevant steps.

5. **Rationale:** Explain the reasoning behind your chosen actions, including any assumptions, risks, and expected outcomes.

"""

AGENT_OUTPUT_PROMPT = """
**Output:**
Generate the output in JSON format with the following structure:

```json
{
  "Thought": "[Your Thought Process here]",
  "Actions": [
    {
      "ActionID": "[action_1]"
      "Action": "[Describe Action 1]",
      "tool_calls": [
        {"name": "func_name1", "parameters": {"parameter1": "value1", "parameter2": "value2"}},
        // Add more tool calls as required
      ]
    },
    {
      "ActionID": "[action_2]"
      "Action": "[Describe Action 2]",
      "tool_calls": [
        {"name": "func_name1", "parameters": {"parameter1": "value1", "parameter2": "value2"}},
        // Add more tool calls as required
      ]
    }
    // Add more steps as needed
  ]
}
"""

AGENT_THOUGHT_PROMPT = lambda agent_desp, tools, query :f"""
[BEGIN OF TASK INSTRUCTION]\n{AGENT_INTRUCTION_PROMPT(agent_desp)}\n[END OF TASK INSTRUCTION]\n\n
[BEGIN OF AVAILABLE TOOLS]\n{json.dumps(convert_to_xlam_tool(tools))}\n[END OF AVAILABLE TOOLS]\n\n
[BEGIN OF FORMAT INSTRUCTION]\n{AGENT_OUTPUT_PROMPT}\n[END OF FORMAT INSTRUCTION]\n\n"
[BEGIN OF QUERY]\n{query}\n[END OF QUERY]\n\n"""


AGENT_RESPONSE_PROMPT = lambda agent_desp, thought, observations, query: f"""
{agent_desp}
You were given a query for which you thought of taking actions.
Based on the observations from these actions, proceed to complete your task and provide a final output that addresses the original query.
If none of the observations can be used to provide final output, or observations lacks required information, state this clearly.

[BEGIN OF THOUGHT]\n{thought}\n[END OF THOUGHT]\n\n
[BEGIN OF OBSERVATIONS]\n{observations}\n[END OF OBSERVATIONS]\n\n
[BEGIN OF QUERY]\n{query}\n[END OF QUERY]\n\n"""


AGENT_RESPONSE_NO_OBSERVATIONS_PROMPT = lambda agent_desp, thought, query: f"""
{agent_desp}
You were given a query for which you thought of taking actions but none of the action gave relevent output.

[BEGIN OF THOUGHT]\n{thought}\n[END OF THOUGHT]
[BEGIN OF QUERY]\n{query}\n[END OF QUERY]\n\n"""