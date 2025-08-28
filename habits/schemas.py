from ninja import Schema
from typing import Optional, List
from datetime import date

# ---- Habit ----
class HabitBase(Schema):
    title: str
    description: Optional[str] = None
    freq_count: int
    freq_period: str  # "daily" | "weekly" | "monthly"

class HabitCreate(HabitBase):
    pass

class HabitUpdate(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    freq_count: Optional[int] = None
    freq_period: Optional[str] = None

class HabitOut(HabitBase):
    id: int
    created_at: str

# ---- HabitLog ----
class HabitLogBase(Schema):
    date: date
    status: str          # "done" | "skip"
    notes: Optional[str] = None

class HabitLogCreate(HabitLogBase):
    pass

class HabitLogUpdate(Schema):
    status: Optional[str] = None
    notes: Optional[str] = None

class HabitLogOut(HabitLogBase):
    id: int
    habit_id: int

class HabitWithLogs(HabitOut):
    logs: List[HabitLogOut] = []


# class UserOut(Schema):
#     id: int
#     username: st