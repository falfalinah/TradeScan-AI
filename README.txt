TradeScan AI — Live Analysis Starter

This is the phone-friendly web app we are building. It accepts an MT5 screenshot and sends it to an AI vision model through the server, returning BUY/SELL/WAIT, Entry, SL, TP1, TP2, R:R, setup strength, reason and invalidation.

Deploy on Render:
1. Put this folder in a GitHub repository.
2. Render → New → Web Service → connect the repository.
3. Build command: pip install -r requirements.txt
4. Start command: gunicorn app:app
5. Add environment variable OPENAI_API_KEY (keep it private).
6. Optional OPENAI_MODEL=gpt-5.6-luna.
7. Deploy and open the generated onrender.com URL in Safari.

Do not put the API key in index.html. This version does not execute trades.
