import os
import re
import requests
import base64

# Config
# Get the directory where the script is located (the 'notes' folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR = os.path.join(BASE_DIR, "md")
OUTPUT_DIR = os.path.join(BASE_DIR, "flash-cards")

def mermaid_to_svg(mermaid_code):
    """Converts mermaid code to SVG using Mermaid.ink (Reliable fallback for Mermaid)."""
    try:
        # Mermaid.ink requires base64 encoding of the mermaid code
        # We use standard b64 as it's what their API expects
        message_bytes = mermaid_code.strip().encode('utf-8')
        base64_bytes = base64.b64encode(message_bytes)
        base64_string = base64_bytes.decode('utf-8')
        
        url = f"https://mermaid.ink/svg/{base64_string}"
        
        # Adding a timeout and a browser-like user agent to avoid being blocked
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error from Mermaid.ink: {response.status_code}")
            return f"<p style='color:red'>SVG Generation Failed (Status {response.status_code})</p>"
    except Exception as e:
        print(f"Error connecting to SVG service: {e}")
        return f"<p style='color:red'>SVG Connection Error: {e}</p>"

def parse_md(file_path):
    """Parses the .md file for Anki fields."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find field content
    front = re.search(r"## Field: Front\n(.*?)(?=\n## Field:|$)", content, re.DOTALL)
    back = re.search(r"## Field: Back\n(.*?)(?=\n## Field:|$)", content, re.DOTALL)
    diagram = re.search(r"## Field: Diagram\n(.*?)(?=\n## Field:|$)", content, re.DOTALL)
    
    return {
        "front": front.group(1).strip() if front else "",
        "back": back.group(1).strip() if back else "",
        "diagram": diagram.group(1).strip() if diagram else ""
    }

def markdown_to_html(text):
    """Converts basic markdown (bold, inline code, code blocks) to Anki-compatible HTML."""
    # 1. Handle code blocks: ```python ... ```
    def code_block_repl(match):
        code = match.group(1).strip()
        # Escape HTML entities inside code blocks
        code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<pre style="text-align: left; background-color: rgba(0,0,0,0.05); padding: 10px; border-radius: 5px; font-family: monospace; white-space: pre-wrap;"><code>{code}</code></pre>'
    
    text = re.sub(r"```(?:\w+)?\n([\s\S]+?)\n```", code_block_repl, text)
    
    # 2. Handle inline code: `code`
    text = re.sub(r"`([^`]+)`" , r"<code>\1</code>", text)
    
    # 3. Handle bold: **text**
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    
    # 4. Handle newlines (only those NOT inside <pre> tags)
    # This is a bit tricky with regex, so we'll do a simple split/join
    parts = re.split(r"(<pre[\s\S]*?</pre>)", text)
    for i in range(len(parts)):
        if not parts[i].startswith("<pre"):
            parts[i] = parts[i].replace("\n", "<br>")
    
    return "".join(parts)

def generate():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # Keep track of generated cards for a summary file
    all_cards = []
    
    for filename in sorted(os.listdir(NOTES_DIR)):
        if filename.endswith(".md") and filename not in ["ANKI_SETUP.md", "ANKI_GUIDE.md"]:
            print(f"Processing {filename}...")
            file_path = os.path.join(NOTES_DIR, filename)
            data = parse_md(file_path)
            
            if not data["front"]:
                continue
                
            # Generate SVG
            svg_markup = ""
            if data["diagram"]:
                svg_markup = mermaid_to_svg(data["diagram"])
            
            # Convert Markdown to HTML for the Back field
            html_back = markdown_to_html(data["back"])
            
            # Combine Back and SVG
            combined_back = f"<div style='text-align: left;'>{html_back}</div><br>{svg_markup}"
            
            # Prepare for Anki Import (Tab-separated)
            def escape_for_tsv(text):
                # Replace tabs with spaces to avoid breaking TSV format
                # Replace actual newlines with nothing (since we already have <br>)
                return text.replace("\t", "    ").replace("\n", "").replace("\r", "")
            
            front_escaped = escape_for_tsv(data["front"])
            back_escaped = escape_for_tsv(combined_back)
            
            all_cards.append(f"{front_escaped}\t{back_escaped}")
            
            # Also write individual files as requested
            output_filename = os.path.splitext(filename)[0] + ".txt"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"{front_escaped}\t{back_escaped}\n")
            
            print(f"✅ Generated {output_path}")

    # Generate a master import file for all cards
    master_path = os.path.join(OUTPUT_DIR, "_all_cards.txt")
    with open(master_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(all_cards))
    print(f"\n✨ Master import file created: {master_path}")
    print("You can import this single file into Anki!")

if __name__ == "__main__":
    generate()
