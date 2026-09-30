from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Body, FastAPI
from fastapi.responses import HTMLResponse

from app.model_service import ModelService
from app.schemas import FlowerSample, ModelInfoResponse, PredictionResponse


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.model_service = ModelService()
    yield


app = FastAPI(title="ModelServe", version="1.0.0", lifespan=lifespan)


def get_model_service() -> ModelService:
    if not hasattr(app.state, "model_service"):
        app.state.model_service = ModelService()
    return app.state.model_service


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "ModelServe is running"}


@app.get("/ui", response_class=HTMLResponse)
def dashboard() -> HTMLResponse:
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>ModelServe Dashboard</title>
        <style>
            :root {
                --bg: #f5f7fb;
                --card: #ffffff;
                --primary: #3b82f6;
                --primary-dark: #1d4ed8;
                --success: #16a34a;
                --success-soft: #dcfce7;
                --danger: #dc2626;
                --text: #111827;
                --muted: #6b7280;
                --border: #e5e7eb;
                --shadow: 0 10px 25px rgba(15, 23, 42, 0.07);
            }

            * { box-sizing: border-box; }
            body {
                font-family: Arial, Helvetica, sans-serif;
                margin: 0;
                background: var(--bg);
                color: var(--text);
            }
            .container {
                max-width: 1100px;
                margin: 40px auto;
                padding: 20px;
            }
            .card {
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 18px;
                box-shadow: var(--shadow);
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 28px 32px;
                margin-bottom: 24px;
            }
            .brand h1 {
                margin: 0;
                font-size: 2rem;
            }
            .brand p {
                margin: 6px 0 0;
                color: var(--muted);
            }
            .online {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: var(--success-soft);
                color: var(--success);
                border-radius: 999px;
                padding: 8px 12px;
                font-weight: 700;
            }
            .dot {
                width: 10px;
                height: 10px;
                background: var(--success);
                border-radius: 50%;
            }
            .layout {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 24px;
            }
            .panel {
                padding: 28px 24px;
            }
            .panel h2 {
                margin: 0 0 20px;
                font-size: 1.15rem;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                color: var(--muted);
            }
            .info-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(120px, 1fr));
                gap: 12px;
            }
            .metric {
                background: #f9fafb;
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 14px 12px;
            }
            .metric-label {
                color: var(--muted);
                font-size: 0.8rem;
                display: block;
                margin-bottom: 8px;
            }
            .metric-value {
                font-weight: 700;
                font-size: 1.05rem;
            }
            .forms {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 16px;
            }
            label {
                display: flex;
                flex-direction: column;
                gap: 8px;
                font-weight: 600;
                color: var(--muted);
            }
            input {
                width: 100%;
                padding: 12px 14px;
                border: 1px solid var(--border);
                border-radius: 10px;
                background: white;
                font-size: 1rem;
                color: var(--text);
            }
            input:focus {
                outline: 2px solid rgba(59, 130, 246, 0.2);
                border-color: var(--primary);
            }
            button {
                border: none;
                border-radius: 12px;
                padding: 14px 18px;
                background: var(--primary);
                color: white;
                font-weight: 700;
                cursor: pointer;
                transition: 0.2s ease;
            }
            button:hover {
                background: var(--primary-dark);
            }
            button:disabled {
                opacity: 0.7;
                cursor: wait;
            }
            .result-box {
                background: #f9fafb;
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 20px;
                min-height: 180px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                gap: 12px;
            }
            .result-label {
                color: var(--muted);
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-size: 0.8rem;
            }
            .result-value {
                font-size: 1.9rem;
                font-weight: 800;
            }
            .confidence-row {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .progress {
                flex: 1;
                height: 14px;
                border-radius: 999px;
                background: #e5e7eb;
                overflow: hidden;
            }
            .progress-bar {
                display: block;
                height: 100%;
                border-radius: inherit;
                background: linear-gradient(90deg, var(--primary), #60a5fa);
            }
            .message {
                margin-top: 12px;
                min-height: 24px;
                color: var(--muted);
                font-weight: 600;
            }
            .error {
                color: var(--danger);
            }
            @media (max-width: 800px) {
                .layout,
                .forms {
                    grid-template-columns: 1fr;
                }
                .header {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 14px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card header">
                <div class="brand">
                    <h1>ModelServe</h1>
                    <p>Machine Learning Prediction API</p>
                </div>
                <div class="online"><span class="dot"></span> ONLINE</div>
            </div>

            <div class="layout">
                <section class="card panel">
                    <h2>Model</h2>
                    <div class="info-grid">
                        <div class="metric">
                            <span class="metric-label">Model</span>
                            <span class="metric-value">Random Forest</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Dataset</span>
                            <span class="metric-value">Iris</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Features</span>
                            <span class="metric-value">4</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Classes</span>
                            <span class="metric-value">3</span>
                        </div>
                    </div>
                    <div style="margin-top: 30px;">
                        <h2>Flower Measurements</h2>
                        <form id="flower-form">
                            <div class="forms">
                                <label>
                                    Sepal Length
                                    <input type="number" name="sepal_length" value="5.1" step="0.1" min="0.1" />
                                </label>
                                <label>
                                    Sepal Width
                                    <input type="number" name="sepal_width" value="3.5" step="0.1" min="0.1" />
                                </label>
                                <label>
                                    Petal Length
                                    <input type="number" name="petal_length" value="1.4" step="0.1" min="0.1" />
                                </label>
                                <label>
                                    Petal Width
                                    <input type="number" name="petal_width" value="0.2" step="0.1" min="0.1" />
                                </label>
                            </div>
                            <div style="margin-top: 20px;">
                                <button id="predict-button" type="submit">Predict Flower</button>
                            </div>
                        </form>
                    </div>
                </section>

                <section class="card panel">
                    <h2>Prediction</h2>
                    <div class="result-box">
                        <span class="result-label">Species</span>
                        <div id="prediction-value" class="result-value">Waiting</div>
                        <span class="result-label">Confidence</span>
                        <div class="confidence-row">
                            <div class="progress"><span id="confidence-bar" class="progress-bar" style="width: 0%"></span></div>
                            <strong id="confidence-value">0%</strong>
                        </div>
                    </div>
                    <div id="status-message" class="message">Prediction Ready</div>
                </section>
            </div>
        </div>

        <script>
            const form = document.getElementById('flower-form');
            const button = document.getElementById('predict-button');
            const statusMessage = document.getElementById('status-message');
            const predictionValue = document.getElementById('prediction-value');
            const confidenceBar = document.getElementById('confidence-bar');
            const confidenceValue = document.getElementById('confidence-value');

            function setStatus(message, error = false) {
                statusMessage.textContent = message;
                statusMessage.classList.toggle('error', error);
            }

            async function sendPrediction(event) {
                event.preventDefault();
                button.disabled = true;
                button.textContent = 'Predicting...';
                setStatus('Predicting...');

                const formData = new FormData(form);
                const payload = Object.fromEntries(formData.entries());

                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(data.detail || 'Prediction failed. Please try again.');
                    }

                    const confidencePercent = Math.round((Number(data.confidence) || 0) * 100);
                    predictionValue.textContent = data.prediction.toUpperCase();
                    confidenceValue.textContent = `${confidencePercent}%`;
                    confidenceBar.style.width = `${confidencePercent}%`;
                    setStatus('Prediction Ready');
                } catch (error) {
                    predictionValue.textContent = 'Error';
                    confidenceBar.style.width = '0%';
                    confidenceValue.textContent = '0%';
                    setStatus(error.message || 'Prediction failed. Please try again.', true);
                } finally {
                    button.disabled = false;
                    button.textContent = 'Predict Flower';
                }
            }

            form.addEventListener('submit', sendPrediction);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: FlowerSample) -> PredictionResponse:
    model_service = get_model_service()
    return model_service.predict_one(payload)


@app.get("/model-info", response_model=ModelInfoResponse)
def model_info() -> ModelInfoResponse:
    model_service = get_model_service()
    return model_service.model_info()


@app.post("/predict/batch", response_model=list[PredictionResponse])
def predict_batch(payload: list[FlowerSample] = Body(..., min_length=1)) -> list[PredictionResponse]:
    model_service = get_model_service()
    return model_service.predict_batch(payload)
