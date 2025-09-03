from crewai.tools import BaseTool
import os

class CustomFileWriteTool(BaseTool):
    name: str = "write_to_file"
    description: str = "Writes given content to a file named using the patient's name and age, saved in the 'data' folder."

    def _run(self, content: str) -> str:
        os.makedirs("data", exist_ok=True)

        # Try to extract title from content (first line assumed to contain it)
        lines = content.strip().splitlines()
        title_line = lines[0] if lines else "Session Summary"
        filename_safe = title_line.replace("**", "").replace(" ", "_").replace(",", "")

        filename = f"data/{filename_safe}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            return f"✅ Summary written to {filename}"
        except Exception as e:
            return f"❌ Failed to write file: {e}"
