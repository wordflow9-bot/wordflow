from google.api_core.exceptions import ResourceExhausted, GoogleAPIError
from .google_vision import extract_text_google
from .fallback_easyocr import extract_text_easyocr


def extract_text(input_image_bytes: bytes) -> dict:
    # try: #WORKS
    #     text = extract_text_google(input_image_bytes)
    #     if text and text.strip():
    #         return {
    #             "engine": "google",
    #             "text": text
    #         }
    #     elif not text:
    #         return {
    #             "engine": "google",
    #             "text": "not found"
    #         }

    # except ResourceExhausted:
    #     # print("Resource Exausted") #debug
    #     pass

    # except GoogleAPIError:
    #     # print("Google API Error") #debug
    #     pass

    # except Exception:
    #     # print("Unkown Exception") #debug
    #     pass 

    try:
        text = extract_text_easyocr(input_image_bytes)
        if text and text.strip():
                return {
                    "engine": "easyocr",
                    "text": text
                }
        elif not text:
            return {
                "engine": "easyocr",
                "text": "not found"
            }
    except Exception:
        print(Exception)
        raise RuntimeError("OCR temporarily unavailable")