import os
import gradio as gr
from dotenv import load_dotenv
from pro_implementation.answer import answer_question

load_dotenv(override=True)


ULL_CSS = """
/* ── Google Font ─────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Root & Global Reset ─────────────────────────────────────────── */
:root {
    --ull-red:    #CC0000;
    --ull-red-dk: #A00000;
    --ull-gold:   #F0A500;
    --ull-navy:   #0A1628;
    --ull-navy2:  #112240;
    --ull-card:   #162032;
    --ull-border: #1E3050;
    --ull-text:   #E8EAF0;
    --ull-muted:  #8A9BBE;
    --radius:     12px;
    --shadow:     0 4px 24px rgba(0,0,0,0.4);
}

body, .gradio-container {
    background: var(--ull-navy) !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    color: var(--ull-text) !important;
}

/* ── Header Banner ───────────────────────────────────────────────── */
#ull-header {
    background: linear-gradient(135deg, var(--ull-red) 0%, #8B0000 60%, var(--ull-navy) 100%);
    border-radius: var(--radius);
    padding: 28px 36px;
    margin-bottom: 20px;
    border-left: 6px solid var(--ull-gold);
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
}
#ull-header::before {
    content: "";
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    background: rgba(240,165,0,0.08);
    border-radius: 50%;
}
#ull-header::after {
    content: "";
    position: absolute;
    bottom: -60px; right: 60px;
    width: 240px; height: 240px;
    background: rgba(240,165,0,0.05);
    border-radius: 50%;
}
#ull-header h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    margin: 0 0 6px 0 !important;
    letter-spacing: -0.5px;
}
#ull-header p {
    font-size: 1rem !important;
    color: rgba(255,255,255,0.80) !important;
    margin: 0 !important;
}
.ull-badge {
    display: inline-block;
    background: var(--ull-gold);
    color: var(--ull-navy) !important;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    margin-left: 10px;
    vertical-align: middle;
    letter-spacing: 0.5px;
}

/* ── Stats Bar ───────────────────────────────────────────────────── */
#stats-bar {
    background: var(--ull-navy2);
    border: 1px solid var(--ull-border);
    border-radius: var(--radius);
    padding: 14px 24px;
    margin-bottom: 20px;
}
#stats-bar .stat-item {
    text-align: center;
}
#stats-bar .stat-number {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--ull-gold);
}
#stats-bar .stat-label {
    font-size: 0.72rem;
    color: var(--ull-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Panel Cards ─────────────────────────────────────────────────── */
.ull-panel {
    background: var(--ull-card) !important;
    border: 1px solid var(--ull-border) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow) !important;
}

/* ── Panel Headers ───────────────────────────────────────────────── */
.panel-header {
    background: linear-gradient(90deg, var(--ull-navy2), var(--ull-card));
    border-bottom: 2px solid var(--ull-red);
    border-radius: var(--radius) var(--radius) 0 0;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--ull-text);
}
.panel-header .dot {
    width: 10px; height: 10px;
    background: var(--ull-red);
    border-radius: 50%;
    box-shadow: 0 0 6px var(--ull-red);
}

/* ── Chatbot ─────────────────────────────────────────────────────── */
#chatbot {
    background: var(--ull-navy) !important;
    border: none !important;
}
#chatbot .message-wrap {
    padding: 8px 12px !important;
}

/* User bubble */
#chatbot [data-testid="user"] .bubble-wrap,
#chatbot .user .message {
    background: linear-gradient(135deg, var(--ull-red), var(--ull-red-dk)) !important;
    color: #fff !important;
    border-radius: 18px 18px 4px 18px !important;
    box-shadow: 0 2px 12px rgba(204,0,0,0.3) !important;
    border: none !important;
    padding: 16px 24px !important;
}
/* Assistant bubble */
#chatbot [data-testid="bot"] .bubble-wrap,
#chatbot .bot .message {
    background: var(--ull-navy2) !important;
    color: var(--ull-text) !important;
    border-radius: 18px 18px 18px 4px !important;
    border: 1px solid var(--ull-border) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    padding: 16px 24px !important;
}

/* ── Input Textbox ───────────────────────────────────────────────── */
#msg-input textarea {
    background: var(--ull-navy2) !important;
    color: var(--ull-text) !important;
    border: 2px solid var(--ull-border) !important;
    border-radius: 12px !important;
    font-size: 0.95rem !important;
    padding: 14px 18px !important;
    resize: none !important;
    transition: border-color 0.2s ease !important;
}
#msg-input textarea:focus {
    border-color: var(--ull-red) !important;
    box-shadow: 0 0 0 3px rgba(204,0,0,0.15) !important;
    outline: none !important;
}
#msg-input textarea::placeholder {
    color: var(--ull-muted) !important;
}

/* ── Send Button ─────────────────────────────────────────────────── */
#send-btn {
    background: linear-gradient(135deg, var(--ull-red), var(--ull-red-dk)) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 14px 28px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(204,0,0,0.35) !important;
    letter-spacing: 0.3px;
}
#send-btn:hover {
    background: linear-gradient(135deg, #E60000, var(--ull-red)) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(204,0,0,0.45) !important;
}
#send-btn:active {
    transform: translateY(0px) !important;
}

/* ── Clear Button ────────────────────────────────────────────────── */
#clear-btn {
    background: transparent !important;
    color: var(--ull-muted) !important;
    border: 1px solid var(--ull-border) !important;
    border-radius: 12px !important;
    font-size: 0.85rem !important;
    padding: 14px 20px !important;
    transition: all 0.2s ease !important;
}
#clear-btn:hover {
    border-color: var(--ull-red) !important;
    color: var(--ull-red) !important;
}

/* ── Context Panel ───────────────────────────────────────────────── */
#context-panel {
    background: var(--ull-navy) !important;
    border: none !important;
    overflow-y: auto !important;
    padding: 16px !important;
    height: 480px !important;
}
#context-panel h2 {
    color: var(--ull-gold) !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    border-bottom: 2px solid var(--ull-border) !important;
    padding-bottom: 8px !important;
    margin-bottom: 16px !important;
}
#context-panel .source-tag {
    display: inline-block;
    background: rgba(204,0,0,0.15);
    border: 1px solid rgba(204,0,0,0.3);
    color: #FF6666 !important;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 8px;
    letter-spacing: 0.3px;
}
#context-panel .source-content {
    font-size: 0.85rem;
    line-height: 1.65;
    color: var(--ull-text);
    border-left: 3px solid var(--ull-border);
    padding-left: 12px;
    margin-bottom: 20px;
}
#context-panel hr {
    border-color: var(--ull-border) !important;
    margin: 16px 0 !important;
}

/* ── Quick Question Chips ────────────────────────────────────────── */
.quick-chip button {
    background: var(--ull-navy2) !important;
    color: var(--ull-muted) !important;
    border: 1px solid var(--ull-border) !important;
    border-radius: 20px !important;
    font-size: 0.78rem !important;
    padding: 6px 14px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
}
.quick-chip button:hover {
    background: rgba(204,0,0,0.15) !important;
    border-color: var(--ull-red) !important;
    color: #FF8888 !important;
}

/* ── Footer ──────────────────────────────────────────────────────── */
#ull-footer {
    text-align: center;
    color: var(--ull-muted);
    font-size: 0.75rem;
    padding: 14px 0 4px 0;
    border-top: 1px solid var(--ull-border);
    margin-top: 20px;
}
#ull-footer a { color: var(--ull-gold); text-decoration: none; }
#ull-footer a:hover { text-decoration: underline; }

/* ── Scrollbars ──────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--ull-navy); }
::-webkit-scrollbar-thumb { background: var(--ull-border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--ull-red); }

/* ── Label overrides ─────────────────────────────────────────────── */
label, .label-wrap span {
    color: var(--ull-muted) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* ── Light/dark lock ─────────────────────────────────────────────────
   The theme above fixes Gradio's own variables. This block covers the
   markdown Gradio renders INSIDE chat bubbles, whose nested <p>, <li>,
   <strong> and <code> tags carry their own colours and would otherwise
   stay dark-on-dark when the OS is set to light mode.                  */

.gradio-container, .gradio-container.dark, body, body.dark {
    --body-text-color: var(--ull-text) !important;
    --body-text-color-subdued: var(--ull-muted) !important;
    --block-title-text-color: var(--ull-text) !important;
    --block-label-text-color: var(--ull-muted) !important;
    --link-text-color: var(--ull-gold) !important;
    --table-text-color: var(--ull-text) !important;
    color-scheme: dark;
}

/* Assistant bubble: force every nested element to light text */
#chatbot .bot .message, #chatbot .bot .message *,
#chatbot [data-testid="bot"] .bubble-wrap,
#chatbot [data-testid="bot"] .bubble-wrap * {
    color: var(--ull-text) !important;
}

/* User bubble: white on red */
#chatbot .user .message, #chatbot .user .message *,
#chatbot [data-testid="user"] .bubble-wrap,
#chatbot [data-testid="user"] .bubble-wrap * {
    color: #FFFFFF !important;
}

/* Re-assert accents the wildcards above would have flattened */
#chatbot .message a, #chatbot .bubble-wrap a { color: var(--ull-gold) !important; }
#chatbot .message code, #chatbot .bubble-wrap code {
    color: var(--ull-gold) !important;
    background: rgba(240,165,0,0.10) !important;
}
#chatbot .message th, #chatbot .bubble-wrap th { color: var(--ull-gold) !important; }

/* Context panel and its markdown */
#context-panel, #context-panel *, .prose, .prose * { color: var(--ull-text) !important; }
#context-panel a, .prose a { color: var(--ull-gold) !important; }

/* Textareas, inputs, placeholders */
textarea, input[type="text"], .gradio-container textarea {
    color: var(--ull-text) !important;
    -webkit-text-fill-color: var(--ull-text) !important;
}
textarea::placeholder, input::placeholder {
    color: var(--ull-muted) !important;
    -webkit-text-fill-color: var(--ull-muted) !important;
}

/* Empty-state and misc Gradio chrome */
.empty, .empty *, .wrap.default, .html-container, .html-container * {
    color: var(--ull-text) !important;
}
"""


def format_context(context):
    if not context:
        return """
<div style='text-align:center; padding:60px 20px; color:#8A9BBE;'>
  <div style='font-size:2.5rem; margin-bottom:12px;'>📚</div>
  <div style='font-weight:600; margin-bottom:6px; color:#B0BCDA;'>No context retrieved yet</div>
  <div style='font-size:0.85rem;'>Ask a question to see the relevant source documents retrieved from the UL Lafayette knowledge base.</div>
</div>"""

    result = "<h2>📄 Retrieved Source Documents</h2>\n\n"
    for i, doc in enumerate(context, 1):
        src = doc.metadata.get("source", "Unknown")
        filename = src.split("/")[-1] if "/" in src else src
        result += f"<div class='source-tag'>📁 Source {i}: {filename}</div>\n\n"
        result += f"<div class='source-content'>{doc.page_content}</div>\n"
        if i < len(context):
            result += "<hr/>\n"
    return result


def add_user_message(message, history):
    history = history or []
    history = history + [{"role": "user", "content": message}]
    return "", history, history


def respond(history):
    last_message = history[-1]["content"]
    prior = history[:-1]
    answer, context = answer_question(last_message, prior)
    history = history + [{"role": "assistant", "content": answer}]
    return history, history, format_context(context)


def use_quick_question(q, history):
    history = history or []
    history = history + [{"role": "user", "content": q}]
    return history, history


QUICK_QUESTIONS = [
    "What scholarships are available?",
    "Tell me about the College of Engineering",
    "Who is the President of UL Lafayette?",
    "What graduate programs are offered?",
    "What is the NCLEX pass rate for Nursing?",
]


def main():
    # Every Gradio theme variable has a light value and a *_dark twin. The browser
    # picks which set to use from the OS appearance setting. This app is designed
    # dark-only, so both twins are given the same value -- otherwise light mode
    # keeps Gradio's dark grey default text and it vanishes against the navy.
    NAVY, NAVY2, CARD = "#0A1628", "#112240", "#162032"
    BORDER, TEXT, MUTED = "#1E3050", "#E8EAF0", "#8A9BBE"
    RED, RED_HOVER, GOLD = "#CC0000", "#E60000", "#F0A500"

    theme = gr.themes.Base(
        font=["Inter", "system-ui", "sans-serif"],
        primary_hue=gr.themes.colors.red,
        neutral_hue=gr.themes.colors.slate,
    ).set(
        body_background_fill=NAVY,
        body_background_fill_dark=NAVY,
        body_text_color=TEXT,
        body_text_color_dark=TEXT,
        body_text_color_subdued=MUTED,
        body_text_color_subdued_dark=MUTED,
        block_background_fill=CARD,
        block_background_fill_dark=CARD,
        panel_background_fill=CARD,
        panel_background_fill_dark=CARD,
        block_border_color=BORDER,
        block_border_color_dark=BORDER,
        border_color_primary=BORDER,
        border_color_primary_dark=BORDER,
        block_label_text_color=MUTED,
        block_label_text_color_dark=MUTED,
        block_title_text_color=TEXT,
        block_title_text_color_dark=TEXT,
        block_info_text_color=MUTED,
        block_info_text_color_dark=MUTED,
        input_background_fill=NAVY2,
        input_background_fill_dark=NAVY2,
        input_placeholder_color=MUTED,
        input_placeholder_color_dark=MUTED,
        button_primary_background_fill=RED,
        button_primary_background_fill_dark=RED,
        button_primary_background_fill_hover=RED_HOVER,
        button_primary_background_fill_hover_dark=RED_HOVER,
        button_primary_text_color="#FFFFFF",
        button_primary_text_color_dark="#FFFFFF",
        link_text_color=GOLD,
        link_text_color_dark=GOLD,
        link_text_color_hover=GOLD,
        link_text_color_hover_dark=GOLD,
        link_text_color_visited=GOLD,
        link_text_color_visited_dark=GOLD,
        table_text_color=TEXT,
        table_text_color_dark=TEXT,
    )

    with gr.Blocks(title="UL Lafayette RAG Assistant") as ui:

        # ── Header ───────────────────────────────────────────────────────
        gr.HTML("""
        <div id="ull-header">
          <h1>🎓 UL Lafayette RAG Assistant
            <span class="ull-badge">POWERED BY AI</span>
          </h1>
          <p>Your intelligent guide to the University of Louisiana at Lafayette — ask about programs, faculty, scholarships, research, and more.</p>
        </div>
        """)

        # ── Stats Bar ─────────────────────────────────────────────────────
        gr.HTML("""
        <div id="stats-bar">
          <div style="display:flex; justify-content:space-around; flex-wrap:wrap; gap:12px;">
            <div class="stat-item"><div class="stat-number">16,100+</div><div class="stat-label">Students Enrolled</div></div>
            <div class="stat-item"><div class="stat-number">240+</div><div class="stat-label">Majors & Minors</div></div>
            <div class="stat-item"><div class="stat-number">45+</div><div class="stat-label">Graduate Programs</div></div>
            <div class="stat-item"><div class="stat-number">$4.4B</div><div class="stat-label">Economic Impact</div></div>
            <div class="stat-item"><div class="stat-number">R1</div><div class="stat-label">Carnegie Classification</div></div>
            <div class="stat-item"><div class="stat-number">20+</div><div class="stat-label">Knowledge Base Files</div></div>
          </div>
        </div>
        """)

        history_state = gr.State([])

        # ── Main Layout ───────────────────────────────────────────────────
        with gr.Row(equal_height=True):

            # Left: Chat panel
            with gr.Column(scale=6, elem_classes="ull-panel"):
                gr.HTML("""
                <div class="panel-header">
                  <div class="dot"></div>
                  💬 Conversation
                </div>
                """)

                chatbot = gr.Chatbot(
                    elem_id="chatbot",
                    label="",
                    height=460,
                    show_label=False,
                )

                # Quick questions — store refs, wire AFTER context_display is defined
                gr.HTML("<div style='padding:8px 4px 4px; color:#8A9BBE; font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;'>⚡ Quick Questions</div>")
                chips = []
                with gr.Row():
                    for q in QUICK_QUESTIONS:
                        chip = gr.Button(q, elem_classes="quick-chip", size="sm")
                        chips.append((q, chip))

                # Input row
                with gr.Row(equal_height=True):
                    message = gr.Textbox(
                        elem_id="msg-input",
                        placeholder="💬  Ask anything about UL Lafayette — scholarships, faculty, programs...",
                        show_label=False,
                        lines=1,
                        max_lines=4,
                        scale=8,
                    )
                    send_btn = gr.Button(
                        "Send ➤",
                        elem_id="send-btn",
                        scale=2,
                        variant="primary",
                    )

                with gr.Row():
                    clear_btn = gr.Button(
                        "🗑️  Clear Conversation",
                        elem_id="clear-btn",
                        size="sm",
                    )

            # Right: Context panel
            with gr.Column(scale=4, elem_classes="ull-panel"):
                gr.HTML("""
                <div class="panel-header">
                  <div class="dot"></div>
                  📚 Knowledge Base Context
                </div>
                """)

                context_display = gr.HTML(
                    elem_id="context-panel",
                    value="""
                    <div style='text-align:center; padding:60px 20px; color:#8A9BBE;'>
                      <div style='font-size:2.5rem; margin-bottom:12px;'>📚</div>
                      <div style='font-weight:600; margin-bottom:6px; color:#B0BCDA;'>Knowledge Base Ready</div>
                      <div style='font-size:0.85rem;'>Retrieved source documents from the UL Lafayette knowledge base will appear here when you ask a question.</div>
                    </div>""",
                )

        # ── Footer ────────────────────────────────────────────────────────
        gr.HTML("""
        <div id="ull-footer">
          🏛️ University of Louisiana at Lafayette &nbsp;|&nbsp;
          <a href="https://louisiana.edu" target="_blank">louisiana.edu</a>
          &nbsp;|&nbsp; 104 E. University Circle, Lafayette, LA 70503
          &nbsp;|&nbsp; (337) 482-1000
          &nbsp;&nbsp;·&nbsp;&nbsp;
          <span style="color:#CC0000">Geaux Cajuns!</span> 🔴⚡
        </div>
        """)

        # ── Event Wiring ──────────────────────────────────────────────────

        # Quick-chip buttons — wired here so context_display is already defined
        for q, chip in chips:
            chip.click(
                use_quick_question,
                inputs=[gr.State(q), history_state],
                outputs=[history_state, chatbot],
            ).then(
                respond,
                inputs=[history_state],
                outputs=[history_state, chatbot, context_display],
            )
        message.submit(
            add_user_message,
            inputs=[message, history_state],
            outputs=[message, history_state, chatbot],
        ).then(
            respond,
            inputs=[history_state],
            outputs=[history_state, chatbot, context_display],
        )

        send_btn.click(
            add_user_message,
            inputs=[message, history_state],
            outputs=[message, history_state, chatbot],
        ).then(
            respond,
            inputs=[history_state],
            outputs=[history_state, chatbot, context_display],
        )

        clear_btn.click(
            lambda: ([], [], format_context([])),
            outputs=[history_state, chatbot, context_display],
        )

    # HF Spaces needs 0.0.0.0; on EC2 we bind to loopback and let Nginx face the internet
    default_host = "0.0.0.0" if os.getenv("SPACE_ID") else "127.0.0.1"

    auth = None
    app_user = os.getenv("APP_USER")
    app_password = os.getenv("APP_PASSWORD")
    if app_user and app_password:
        auth = (app_user, app_password)

    ui.launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", default_host),
        server_port=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
        share=False,
        inbrowser=False,
        auth=auth,
        theme=theme,
        css=ULL_CSS,
    )


if __name__ == "__main__":
    main()
