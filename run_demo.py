import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from project.main_agent import run_agent

if __name__ == "__main__":
    print(run_agent("Hello! This is a demo."))
    print()
    print(run_agent("I have fever and cough for 3 days. What should I do?"))
    print()
    print(run_agent("What are warning signs of dehydration?"))
