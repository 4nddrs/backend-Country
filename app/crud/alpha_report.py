from datetime import datetime
from typing import List, Tuple, Dict, Optional
from collections import defaultdict
from app.supabase_client import get_supabase

def _month_bounds(period_month: str) -> Tuple[datetime, datetime, str]:
    y, m = map(int, period_month.split("-"))
    start = datetime(y, m, 1)
    end = datetime(y + (m // 12), (m % 12) + 1, 1)
    return start, end, f"{y:04d}-{m:02d}"

async def _fetch_horses_with_owner_and_plan():
    supabase = await get_supabase()
    horses = await supabase.table("horse").select(
        "idHorse,horseName,fk_idOwner,fl_idNutritionalPlan"
    ).execute()
    horses = horses.data or []

    owner_ids = list({h["fk_idOwner"] for h in horses})
    owners: Dict[int, str] = {}
    if owner_ids:
        o = await supabase.table("owner").select("idOwner,name,FirstName,SecondName") \
            .in_("idOwner", owner_ids).execute()
        for it in (o.data or []):
            full = " ".join(filter(None, [
                str(it.get("name","")).strip(),
                str(it.get("FirstName","")).strip(),
                str(it.get("SecondName","") or "").strip()
            ])).strip()
            owners[it["idOwner"]] = full or str(it["idOwner"])
    return horses, owners

async def _fetch_foods(q: Optional[str] = None, limit: int = 200):
    supabase = await get_supabase()
    query = supabase.table("food_stock").select("idFood,foodName").limit(limit).order("foodName")
    if q and q.strip():
        query = query.ilike("foodName", f"%{q.strip()}%")
    res = await query.execute()
    return res.data or []

async def _fetch_details_for_month(plan_ids: List[int], start: datetime, end: datetime,
                                   food_id: Optional[int] = None):
    if not plan_ids:
        return []
    supabase = await get_supabase()
    sel = supabase.table("nutritional_plan_details").select(
        "fk_idNutritionalPlan,fk_idFood,consumptionKlg,daysConsumptionMonth,period"
    ).in_("fk_idNutritionalPlan", plan_ids) \
     .gte("period", start.date().isoformat()) \
     .lt("period", end.date().isoformat())
    if food_id:
        sel = sel.eq("fk_idFood", food_id)
    res = await sel.execute()
    return res.data or []

async def list_periods(food_id: Optional[int] = None) -> List[str]:
    supabase = await get_supabase()
    sel = supabase.table("nutritional_plan_details").select("period").order("period", desc=True)
    if food_id:
        sel = sel.eq("fk_idFood", food_id)
    res = await sel.execute()
    periods = set()
    for r in (res.data or []):
        periods.add(r["period"][:7])  # YYYY-MM
    return sorted(periods, reverse=True)

async def build_consumption_report(period_month: str, food_id: Optional[int] = None):
    start, end, period_tag = _month_bounds(period_month)

    # 1) todos los caballos y owners
    horses, owners_map = await _fetch_horses_with_owner_and_plan()
    total_caballos = len(horses)

    # 2) si se filtra por alimento, busca su nombre (para devolverlo)
    food_name: Optional[str] = None
    if food_id:
        foods = await get_supabase()
        fr = await foods.table("food_stock").select("idFood,foodName").eq("idFood", food_id).single().execute()
        if fr.data:
            food_name = fr.data["foodName"]

    # 3) detalles mensuales (filtra por food_id si viene)
    plan_ids = [h["fl_idNutritionalPlan"] for h in horses if h.get("fl_idNutritionalPlan")]
    details = await _fetch_details_for_month(plan_ids, start, end, food_id=food_id)

    # 4) agregado por plan
    agg_by_plan = defaultdict(lambda: {"klg": 0.0, "days": 0.0, "klgMes": 0.0})
    for d in details:
        c = float(d.get("consumptionKlg") or 0.0)
        dy = float(d.get("daysConsumptionMonth") or 0.0)
        a = agg_by_plan[d["fk_idNutritionalPlan"]]
        a["klg"] += c
        a["days"] += dy
        a["klgMes"] += c * dy

    rows = []
    total_klg = 0.0
    total_klg_mes = 0.0
    comen = 0
    no_comen = 0

    for h in horses:
        hid = h["idHorse"]
        oid = h["fk_idOwner"]
        plan_id = h.get("fl_idNutritionalPlan")
        owner_name = owners_map.get(oid, "")

        klg = days = klg_mes = 0.0
        if plan_id and plan_id in agg_by_plan:
            klg = round(agg_by_plan[plan_id]["klg"], 2)
            days = round(agg_by_plan[plan_id]["days"], 2)
            klg_mes = round(agg_by_plan[plan_id]["klgMes"], 2)

        if klg_mes > 0:
            comen += 1
        else:
            no_comen += 1

        total_klg += klg
        total_klg_mes += klg_mes

        rows.append({
            "horse_id": hid,
            "horse_name": h["horseName"],
            "owner_id": oid,
            "owner_name": owner_name,
            "period": period_tag,
            "consumptionKlg": klg,
            "daysConsumptionMonth": days,
            "klgMes": klg_mes
        })

    rows.sort(key=lambda x: x["klgMes"], reverse=True)
    summary = {
        "comen": comen,
        "no_comen": no_comen,
        "caballos_escuela": 0,                 # por ahora 0
        "total_caballos": total_caballos,
        "total_klg": round(total_klg, 2),
        "total_klg_mes": round(total_klg_mes, 2),
    }
    return {
        "period_month": period_tag,
        "food_id": food_id,
        "food_name": food_name,
        "rows": rows,
        "summary": summary
    }

# Utilidades públicas para router
async def list_foods(q: Optional[str] = None):
    return await _fetch_foods(q=q)

async def list_periods_by_food(food_id: Optional[int] = None):
    return await list_periods(food_id=food_id)

async def report_all_months_all_foods():
    months = await list_periods(food_id=None)
    out = []
    for m in months:
        out.append(await build_consumption_report(m, food_id=None))
    return out
