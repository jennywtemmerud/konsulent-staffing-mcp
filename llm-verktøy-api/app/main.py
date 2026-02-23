from fastapi import FastAPI, Query, HTTPException
import httpx
import os

app = FastAPI(title="llm-verktøy-api")

KONSULENT_API_BASE = os.getenv("KONSULENT_API_BASE", "http://konsulent-api:8000")

def tilgjengelighet(belastning_prosent: int) -> int:
    return max(0, min(100, 100 - belastning_prosent))

@app.get("/tilgjengelige-konsulenter/sammendrag")
async def tilgjengelige_konsulenter_sammendrag(
    min_tilgjengelighet_prosent: int = Query(..., ge=0, le=100),
    påkrevd_ferdighet: str = Query(..., min_length=1),
):
    skill = påkrevd_ferdighet.strip().lower()

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{KONSULENT_API_BASE}/konsulenter")
            r.raise_for_status()
            konsulenter = r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Klarte ikke hente konsulenter: {e}")

    filtrert = []
    for k in konsulenter:
        bel = int(k.get("belastning_prosent", 100))
        avail = tilgjengelighet(bel)
        ferdigheter = [str(s).lower() for s in (k.get("ferdigheter") or [])]
        if avail >= min_tilgjengelighet_prosent and skill in ferdigheter:
            filtrert.append((k.get("navn", "Ukjent"), avail))

    if not filtrert:
        return {
            "sammendrag": (
                f"Fant 0 konsulenter med minst {min_tilgjengelighet_prosent}% tilgjengelighet "
                f"og ferdigheten '{påkrevd_ferdighet}'."
            )
        }

    deler = [
        f"Fant {len(filtrert)} konsulenter med minst {min_tilgjengelighet_prosent}% tilgjengelighet "
        f"og ferdigheten '{påkrevd_ferdighet}'."
    ]
    for navn, avail in filtrert:
        deler.append(f"{navn} har {avail}% tilgjengelighet.")
    return {"sammendrag": " ".join(deler)}