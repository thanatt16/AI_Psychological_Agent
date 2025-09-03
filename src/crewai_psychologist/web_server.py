from flask import Flask, render_template, request, jsonify
from crew import Interview
from crewai import Crew, Process
import os

app = Flask(__name__, static_url_path='/static')
interview = Interview()
conversation = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    conversation.append({"patient": user_input})

    convo_text = "\n".join([
        f"Patient: {msg['patient']}\nPsychologist: {msg.get('psychologist', '')}"
        for msg in conversation
    ])


    if user_input.strip().lower() in ['exit', 'quit']:
        try:
            summary_inputs = {"conversation": convo_text}
            summary_task = interview.summary_task()
            summary_agent = interview.summary_agent()

            summary_crew = Crew(
                agents=[summary_agent],
                tasks=[summary_task],
                process=Process.sequential,
                verbose=False
            )

            summary_result = summary_crew.kickoff(inputs=summary_inputs)
            summary_text = str(summary_result)

            filename = "Name_Age.txt"
            filepath = os.path.join("static", filename).replace("\\", "/")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(summary_text)

            return jsonify({
                "response": f"✅ Session saved. <a href='/{filepath}' download>📄 Download Summary</a>"
            })

        except Exception as e:
            return jsonify({'response': f"⚠️ Failed to generate summary: {e}"}), 500

    # === Normal chat response ===
    try:
        interview_task = interview.interview_task()
        interview_agent = interview.interview_agent()

        interview_crew = Crew(
            agents=[interview_agent],
            tasks=[interview_task],
            process=Process.sequential,
            verbose=False
        )

        result = interview_crew.kickoff(inputs={"conversation": convo_text, "input": user_input})
        response = str(result)
        conversation[-1]["psychologist"] = response
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'response': f"⚠️ Error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
