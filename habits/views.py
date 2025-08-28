from ninja import Router, Query
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from datetime import date
from .models import Habit, HabitLog
from .schemas import (
    HabitCreate, HabitUpdate, HabitOut, HabitWithLogs,
    HabitLogCreate, HabitLogUpdate, HabitLogOut
)

router = Router(tags=["habits"])

def _require_auth(request: HttpRequest):
    if not request.user.is_authenticated:
        raise PermissionError("Not authenticated")
    return request.user

@router.get("/", response=List[HabitOut])
def list_habits(request: HttpRequest, limit: int = 20, offset: int = 0, q: Optional[str] = None):
    user = _require_auth(request)
    qs = Habit.objects.filter(user=user).order_by("-id")
    if q:
        qs = qs.filter(title__icontains=q)
    return list(qs[offset : offset + limit])

@router.post("/", response=HabitOut)
def create_habit(request: HttpRequest, payload: HabitCreate):
    user = _require_auth(request)
    habit = Habit.objects.create(user=user, **payload.dict())
    return habit

@router.get("/{habit_id}", response=HabitWithLogs)
def get_habit(request: HttpRequest, habit_id: int):
    user = _require_auth(request)
    habit = get_object_or_404(Habit, id=habit_id, user=user)
    logs = list(habit.logs.order_by("-date")[:100])  # cap 100 log terakhir
    return {
        "id": habit.id,
        "title": habit.title,
        "description": habit.description,
        "freq_count": habit.freq_count,
        "freq_period": habit.freq_period,
        "created_at": habit.created_at.isoformat(),
        "logs": [
            {"id": lg.id, "habit_id": habit.id, "date": lg.date, "status": lg.status, "notes": lg.notes}
            for lg in logs
        ],
    }

@router.put("/{habit_id}", response=HabitOut)
def update_habit(request: HttpRequest, habit_id: int, payload: HabitUpdate):
    user = _require_auth(request)
    habit = get_object_or_404(Habit, id=habit_id, user=user)
    data = payload.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(habit, k, v)
    habit.save()
    return habit

@router.delete("/{habit_id}")
def delete_habit(request: HttpRequest, habit_id: int):
    user = _require_auth(request)
    habit = get_object_or_404(Habit, id=habit_id, user=user)
    habit.delete()
    return {"success": True}

@router.get("/{habit_id}/logs", response=List[HabitLogOut])
def list_logs(
    request: HttpRequest,
    habit_id: int,
    start: Optional[date] = Query(None),
    end: Optional[date] = Query(None),
    limit: int = 50,
    offset: int = 0,
):
    user = _require_auth(request)
    habit = get_object_or_404(Habit, id=habit_id, user=user)
    qs = habit.logs.all().order_by("-date")
    if start:
        qs = qs.filter(date__gte=start)
    if end:
        qs = qs.filter(date__lte=end)
    return list(qs[offset : offset + limit])

@router.post("/{habit_id}/logs", response=HabitLogOut)
def create_log(request: HttpRequest, habit_id: int, payload: HabitLogCreate):
    user = _require_auth(request)
    habit = get_object_or_404(Habit, id=habit_id, user=user)
    log, created = HabitLog.objects.get_or_create(
        habit=habit, date=payload.date,
        defaults={"status": payload.status, "notes": payload.notes or ""},
    )
    if not created:
        log.status = payload.status
        log.notes = payload.notes or ""
        log.save()
    return {"id": log.id, "habit_id": habit.id, "date": log.date, "status": log.status, "notes": log.notes}

@router.put("/{habit_id}/logs/{log_id}", response=HabitLogOut)
def update_log(request: HttpRequest, habit_id: int, log_id: int, payload: HabitLogUpdate):
    user = _require_auth(request)
    habit = get_object_or_404(Habit, id=habit_id, user=user)
    log = get_object_or_404(HabitLog, id=log_id, habit=habit)
    data = payload.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(log, k, v)
    log.save()
    return {"id": log.id, "habit_id": habit.id, "date": log.date, "status": log.status, "notes": log.notes}

@router.delete("/{habit_id}/logs/{log_id}")
def delete_log(request: HttpRequest, habit_id: int, log_id: int):
    user = _require_auth(request)
    habit = get_object_or_404(Habit, id=habit_id, user=user)
    log = get_object_or_404(HabitLog, id=log_id, habit=habit)
    log.delete()
    return {"success": True}