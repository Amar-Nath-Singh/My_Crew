# My_Crew

**My_Crew** is a cutting-edge **Customer Service LLM Swarm Architecture** designed to automate service tasks using Large Language Model (LLM) agents with advanced reasoning and autonomy capabilities. This project introduces a robust framework for agent-to-agent interaction and function calling to improve service task efficiency.

---

## Key Features

### 🚀 **Agent Swarm Architecture**
- **Base LLM:** Deployed **Llama 3.1 8B-Instruct** with Q4_0 quantization, supporting up to **128K context windows**.
- **Hardware Setup:** Optimized to run on **2x Nvidia T4 GPUs** for efficient and scalable performance.

### 🛠 **Reasoning and Automation**
- **Chain-of-Thought (CoT) Prompts:** Enhanced reasoning capabilities through structured CoT prompting.
- **Tool Calling:** Automated task execution using tools like MySQL queries, DuckDuckGo searches, and task planning.
- **Agent-to-Agent Interaction:** Improved autonomy with a robust interaction chain.

### 📊 **Graph-Based Agent Interaction**
- Introduced a **graph-based framework** to enable collaboration between agents with distinct expertise, such as:
  - **Database Management:** MySQL Query Execution
  - **Information Retrieval:** DuckDuckGo Search
  - **Task Planning:** Autonomous decision-making and planning

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YourUsername/My_Crew.git
   cd My_Crew
   ```

2. **Set Up Environment**
   - Configure GPU drivers and dependencies for Nvidia T4 GPUs.
   - Ensure access to Llama 3.1 8B-Instruct model with Q4_0 quantization.

3. **Run the Application**
   ```bash
   python main.py
   ```

---

## Project Structure

```plaintext
My_Crew/
├── agents.py        # Core logic for LLM agents
├── config.py        # Configuration settings
├── crew.py          # Swarm management and task orchestration
├── main.py          # Entry point of the application
├── memory.py        # Agent memory management
├── memory_db/       # Persistent storage for agent memory
├── prompts.py       # Chain-of-Thought prompts and tool calls
├── tools.py         # Custom tools for LLM function calls
├── utils.py         # Helper functions and utilities
```

---

## Use Cases

- **Customer Service Automation:** Automate complex customer queries by delegating tasks to specialized LLM agents.
- **Data Management:** Efficiently query and manipulate databases with natural language instructions.
- **Information Retrieval:** Perform quick and accurate searches using DuckDuckGo and similar tools.
- **Planning and Scheduling:** Delegate and plan tasks autonomously using an interconnected swarm of LLM agents.

---

## Future Enhancements

- Extend the toolset with integrations for APIs like GPT, AWS, or Azure.
- Improve graph-based agent interaction with dynamic learning from tasks.
- Support for multi-GPU setups and larger models for advanced use cases.

---

## Contributors

- **Amar Nath Singh**  
  Email: [amarnathsingh.iitm@gmail.com]  
  GitHub: [Amar-Nath-Singh](https://github.com/Amar-Nath-Singh)

---
