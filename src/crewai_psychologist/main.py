#!/usr/bin/env python
import warnings
from crew import Interview

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():

    interview = Interview()

    print("\n🧠 Psychologist: Hello, I am Elias, your personal psychologist. Can you please tell me your name, surname and age? :)?\n")
    conversation = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("\n🧠 Psychologist: Thank you for sharing. Let's continue next time.")
            break

        conversation.append({"patient": user_input})

        convo_text = "\n".join([
            f"Patient: {msg['patient']}\nPsychologist: {msg.get('psychologist', '')}"
            for msg in conversation
        ])

        inputs = {
            "conversation": convo_text,
            "input": user_input
        }

        try:
            result = interview.crew().kickoff(inputs=inputs)
        except Exception as e:
            print(f"\n⚠️ Error: {e}")
            break

        print(f"\n🧠 Psychologist: {result}\n")
        conversation[-1]["psychologist"] = result

    # === Run summary agent after exit ===
    full_convo_text = "\n".join([
        f"Patient: {msg['patient']}\nPsychologist: {msg['psychologist']}"
        for msg in conversation
    ])
    summary_inputs = {"conversation": full_convo_text}

    try:
        from crewai import Crew, Process
        summary_task = interview.summary_task()
        summary_agent = interview.summary_agent()

        summary_crew = Crew(
            agents=[summary_agent],
            tasks=[summary_task],
            process=Process.sequential,
            verbose=True
        )

        summary_result = summary_crew.kickoff(inputs=summary_inputs)

        print("\n📄 Summary agent response:")
        print(summary_result)

    except Exception as e:
        print(f"\n⚠️ Failed to generate summary: {e}")


if __name__ == "__main__":
    run()
