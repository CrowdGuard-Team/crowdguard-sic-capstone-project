import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_crowd_assessment(summary_metrics):
    prompt = f"""
You are the AI insight component of CrowdGuard, a crowd monitoring
and early risk assessment dashboard.

Measured video summary:
- Peak people count: {summary_metrics["peak_people"]}
- Peak occupancy: {summary_metrics["peak_occupancy"]:.1f}%
- Average relative movement speed: {summary_metrics["avg_speed"]:.1f} px/s
- Overall risk level: {summary_metrics["overall_risk"]}
- Peak risk level: {summary_metrics["peak_risk"]}

Generate a concise dashboard interpretation.

Use exactly this format:

Assessment:
[Maximum 2 short sentences.]

Recommended Actions:
- [Short action]
- [Short action]
- [Short action]

Rules:
- Use only the provided measurements.
- Treat the overall risk as the main video-level assessment.
- Mention a higher peak risk only as a temporary elevation.
- Focus on interpreting the result, not repeating all numeric metrics.
- Do not infer incidents, congestion, bottlenecks, safe capacity,
  abnormal behavior, or causes unless directly supported by the metrics.
- Treat occupancy as an image-based occupancy proxy, not physical crowd density.
- Treat speed as relative image-plane movement in px/s, not real-world speed.
- Keep the assessment concise and dashboard-friendly.
- Do not use Markdown headings, bold text, or decorative symbols.
- Keep the entire response under 70 words.
- Recommendations must be observational or precautionary.
- Do not repeat the human-confirmation disclaimer in the recommendations.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text