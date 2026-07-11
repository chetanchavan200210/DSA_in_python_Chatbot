from pathlib import Path

from dotenv import load_dotenv

from config import (
    LLM_PROVIDER,
    VISION_MODEL,
    OLLAMA_VISION_MODEL,
    TEMPERATURE,
)

# --------------------------------------------------
# Load Environment
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# --------------------------------------------------
# Initialize Vision Model
# --------------------------------------------------
if LLM_PROVIDER == "gemini":

    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage

    vision_model = ChatGoogleGenerativeAI(
        model=VISION_MODEL,
        temperature=TEMPERATURE,
    )

elif LLM_PROVIDER == "ollama":

    from langchain_ollama import ChatOllama

    vision_model = ChatOllama(
        model=OLLAMA_VISION_MODEL,
        temperature=TEMPERATURE,
    )

else:
    raise ValueError(
        f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}"
    )


# --------------------------------------------------
# Analyze Medical Image
# --------------------------------------------------
def describe_medical_image(image_path: str) -> str:
    """
    Analyze a medical image using Gemini Vision or Ollama Vision.

    Parameters
    ----------
    image_path : str
        Path to the uploaded medical image.

    Returns
    -------
    str
        Structured description of the medical image.
    """

    # --------------------------------------------------
    # Gemini Vision
    # --------------------------------------------------
    if LLM_PROVIDER == "gemini":

        suffix = Path(image_path).suffix.lower()

        mime_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
        }

        mime_type = mime_map.get(suffix, "image/jpeg")

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        prompt = """
You are an experienced Medical Vision AI assistant.

Analyze the uploaded medical image carefully.

The image may be:

• Dental X-ray
• Chest X-ray
• CT Scan
• MRI
• Ultrasound
• Prescription
• Blood Test
• Laboratory Report
• Histopathology Report
• Medical Photograph

Instructions:

1. Identify the image type.

2. Describe all visible findings.

3. Identify:
   - organs
   - bones
   - teeth
   - joints
   - implants
   - medical devices

4. If abnormalities are visible,
describe ONLY what is observed.

5. If the image is a prescription,
extract:
   - Doctor name (if visible)
   - Patient name (if visible)
   - Medicines
   - Dosage
   - Frequency
   - Duration

6. If the image is a laboratory report:
   - Extract all measurable values.
   - Summarize abnormal findings.

7. If text is unreadable,
state that clearly.

8. Never invent information.

Return your answer in this format:

Image Type:

Findings:

Extracted Text:

Summary:
"""

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image",
                    "data": image_bytes,
                    "mime_type": mime_type,
                },
            ]
        )

        try:
            response = vision_model.invoke([message])
            return response.content

        except Exception as e:
            return f"Vision model error: {e}"

    # --------------------------------------------------
    # Ollama Vision
    # --------------------------------------------------
    elif LLM_PROVIDER == "ollama":

        prompt = """
You are an experienced Medical Vision AI assistant.

Analyze this medical image.

Identify:

- Image type
- Visible findings
- Bones
- Teeth
- Organs
- Implants
- Medical devices
- Abnormalities

If it is a prescription:

Extract:
- Doctor
- Patient
- Medicines
- Dosage
- Frequency
- Duration

If it is a laboratory report:

Extract:
- Test names
- Values
- Units
- Abnormal findings

Never guess.

If uncertain,
say that the image is unclear.
"""

        try:

            response = vision_model.invoke(
                prompt,
                images=[image_path],
            )

            return response.content

        except Exception as e:
            return f"Vision model error: {e}"