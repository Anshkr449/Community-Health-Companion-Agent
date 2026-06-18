try:
    import gradio as gr
except Exception:
    gr = None

from project.main_agent import run_agent


def chat(message, history=None):
    return run_agent(message)


if __name__ == "__main__":
    if gr is None:
        print("Gradio is not installed. Install requirements.txt first.")
    else:
        demo = gr.ChatInterface(
            fn=chat,
            title="Community Health Companion Agent",
            description="Agents for Good demo: safe, non-diagnostic community health guidance."
        )
        demo.launch()
