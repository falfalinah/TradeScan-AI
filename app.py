import os,json,base64
from flask import Flask,request,jsonify,send_from_directory
from openai import OpenAI
app=Flask(__name__,static_folder="public",static_url_path="")
client=OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
PROMPT="""You are TradeScan AI, a cautious MT5 chart-analysis assistant.
Return ONLY valid JSON with keys: signal,entry,stop_loss,tp1,tp2,risk_reward,setup_strength,reason,invalidation.
signal must be BUY, SELL, or WAIT. If prices are unreadable, chart evidence is unclear/conflicting, use WAIT and do not invent prices.
Consider visible trend, market structure, support/resistance, momentum, candlestick confirmation and risk/reward.
Do not guarantee results. Analysis only; never execute trades."""
@app.get("/")
def home(): return send_from_directory("public","index.html")
@app.get("/health")
def health(): return jsonify(ok=True)
@app.post("/api/analyse")
def analyse():
    if not os.environ.get("OPENAI_API_KEY"): return jsonify(error="OPENAI_API_KEY is not configured."),500
    f=request.files.get("image")
    if not f: return jsonify(error="Please upload an MT5 screenshot."),400
    data=f.read(); mime=f.mimetype or "image/png"
    if mime not in {"image/png","image/jpeg","image/webp","image/gif"}: return jsonify(error="Use PNG, JPG, WEBP or GIF."),400
    market=request.form.get("market","XAUUSD"); tf=request.form.get("timeframe","M5")
    url=f"data:{mime};base64,{base64.b64encode(data).decode()}"
    try:
        r=client.responses.create(model=os.environ.get("OPENAI_MODEL","gpt-5.6-luna"),
          instructions=PROMPT,
          input=[{"role":"user","content":[
            {"type":"input_text","text":f"Market: {market}. Timeframe: {tf}. Analyze this MT5 screenshot."},
            {"type":"input_image","image_url":url,"detail":"high"}]}])
        raw=r.output_text.strip()
        try: out=json.loads(raw)
        except: out=json.loads(raw[raw.find("{"):raw.rfind("}")+1])
        return jsonify(out)
    except Exception as e: return jsonify(error=f"AI analysis failed: {e}"),500
if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT","10000")))
