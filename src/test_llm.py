from services.llm_client import call_llm_with_sdk


respuesta = call_llm_with_sdk(
    "hola como estas?"
)

print(respuesta)