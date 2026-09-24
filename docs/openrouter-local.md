# Activar JEV Chat con OpenRouter

El Chat de GesKio usa un modelo generativo normal, `openai/gpt-6-luna`, a través de OpenRouter. `OPENROUTER_MODEL` permite elegir otro modelo de texto compatible; si falta, se conserva GPT-6 Luna. Esto no usa el modelo Jev de TypeSafe, que devuelve decisiones tipadas y no texto conversacional.

GesKio lee `OPENROUTER_API_KEY` desde el entorno del proceso. La clave no se guarda en el JSON de datos ni en el historial del chat.

En PowerShell, pedí la clave sin mostrarla en pantalla, iniciá GesKio desde esa misma sesión y limpiá la variable al cerrar:

```powershell
$jevKeySecure = Read-Host "Clave de OpenRouter" -AsSecureString
$jevKeyPtr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($jevKeySecure)
try {
    $env:OPENROUTER_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($jevKeyPtr)
    # Opcional: seleccioná otro modelo generativo de texto disponible en OpenRouter.
    # $env:OPENROUTER_MODEL = "openai/gpt-6-luna"
    python app/main.py
}
finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($jevKeyPtr)
    Remove-Item Env:OPENROUTER_API_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:OPENROUTER_MODEL -ErrorAction SilentlyContinue
    Remove-Variable jevKeySecure, jevKeyPtr -ErrorAction SilentlyContinue
}
```

Cada consulta envía a OpenRouter el texto, hasta ocho mensajes previos y un resumen limitado de ventas, inventario y saldos. Los teléfonos, IDs y el archivo JSON completo quedan fuera. El modelo y la cuenta de OpenRouter pueden tener cargos o límites propios. Si falta la clave, el Chat muestra el paso de configuración; el resto de GesKio permanece disponible.

## Jev de TypeSafe (roadmap separado)

Jev no reemplaza al modelo de Chat: no genera respuestas en prosa. Acepta `state` y preguntas tipadas `choice`, `score` o `noul`, y devuelve decisiones estructuradas/probabilidades. Un uso futuro posible es clasificar la intención del mensaje para enrutarla a consultas locales permitidas; el texto final lo redactaría el modelo generativo del Chat. OpenRouter documenta Jev en el endpoint de decisiones `/api/alpha/decisions`, distinto de Chat Completions; tratar esa API alpha como experimento con adaptador aislado, fake local y fallback. Jev tampoco acepta audio según la documentación actual: la captura por voz necesitaría STT, y Jev no puede producir por sí mismo nombres o precios arbitrarios de producto.

Fuentes: [TypeSafe AI: Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [Jev 1.13 en OpenRouter](https://openrouter.ai/typesafe/jev-1.13), [API de decisiones de Jev en OpenRouter](https://openrouter.ai/blog/insights/what-is-jev/), [GPT-6 Luna en OpenRouter](https://openrouter.ai/openai/gpt-6-luna).

Las pruebas locales usan un transporte simulado y no requieren clave ni realizan solicitudes de red.
