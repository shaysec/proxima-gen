import os
import sqlite3
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# 1. System Path Definitions
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'data', 'ai_vulnerabilities.db')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'src', 'ui', 'templates')

# 2. Initialize FastAPI and Jinja2 Template Engine
app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    # Check if database exists before connection
    if not os.path.exists(DB_PATH):
        return HTMLResponse(content="<h1>❌ Database file not found. Please run the scanner.</h1>", status_code=404)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    
    try:
        # Fetch verified vulnerabilities
        vuln_rows = conn.execute("SELECT * FROM vulnerabilities ORDER BY id DESC").fetchall()
        
        # Fetch research artifacts (Limited to 100 for performance)
        art_rows = conn.execute("SELECT * FROM research_artifacts ORDER BY id DESC LIMIT 100").fetchall()
        all_artifacts = [dict(a) for a in art_rows]

        vulnerabilities_list = []
        for v_row in vuln_rows:
            v_data = dict(v_row)
            cat_id = v_data.get('category_id')
            
            # Filter and deduplicate artifact URLs
            relevant_raw = [a for a in all_artifacts if a.get('vulnerability_id') == cat_id]
            seen_urls = set()
            unique_artifacts = []
            for art in relevant_raw:
                url = art.get('url')
                if url and url not in seen_urls:
                    unique_artifacts.append(art)
                    seen_urls.add(url)
            
            # Fallback: Show last 3 research items if no direct match
            if not unique_artifacts:
                unique_artifacts = all_artifacts[:3]

            vulnerabilities_list.append({
                "info": v_data,
                "artifacts": unique_artifacts
            })

        # Render response with explicit request context
        return templates.TemplateResponse(
            request=request, 
            name="dashboard.html", 
            context={"vulnerabilities": vulnerabilities_list}
        )

    except Exception as e:
        return HTMLResponse(content=f"<h1>⚠️ Error accessing database: {e}</h1>", status_code=500)
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)