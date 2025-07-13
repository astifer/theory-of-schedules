from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Set

from coffman import coffman_graham
from common import Task, get_graph

# Default configuration variables
DEFAULT_MACHINES: int = 2
DEFAULT_DURATION: int = 1

app = FastAPI(title="Scheduling API")


class TaskInput(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор задачи")
    duration: int = Field(DEFAULT_DURATION, gt=0, description="Длительность задачи, целое положительное")
    predecessors: List[int] = Field([], description="Список ID задач, которые должны быть выполнены до этой задачи")


class ScheduleRequest(BaseModel):
    tasks: List[TaskInput] = Field(..., description="Список задач для расписания")
    machines: int = Field(DEFAULT_MACHINES, gt=0, description="Количество машин для выполнения задач")

    class Config:
        schema_extra = {
            "example": {
                "tasks": [
                    {"id": 1, "duration": 2, "predecessors": []},
                    {"id": 2, "duration": 1, "predecessors": []},
                    {"id": 3, "duration": 2, "predecessors": [1, 2]},
                    {"id": 4, "duration": 1, "predecessors": [3]}
                ],
                "machines": 2
            }
        }


class TaskOutput(BaseModel):
    id: int
    start_time: int
    end_time: int
    machine: int


class ScheduleResponse(BaseModel):
    schedule: List[List[TaskOutput]] = Field(..., description="Расписание по машинам: список списков задач")


@app.post("/schedule/coffman", response_model=ScheduleResponse)
def schedule_coffman(request: ScheduleRequest):
    # Собираем Task-объекты
    tasks_dict: Dict[int, Task] = {}
    for t in request.tasks:
        if t.id in tasks_dict:
            raise HTTPException(status_code=400, detail=f"Duplicate task id: {t.id}")
        tasks_dict[t.id] = Task(id=t.id, duration=t.duration)

    # Строим граф предшествований
    precedence: Dict[int, Set[int]] = {t.id: set(t.predecessors) for t in request.tasks}

    # Валидация: все упомянутые предшественники должны существовать
    all_ids = set(tasks_dict.keys())
    for preds in precedence.values():
        for p in preds:
            if p not in all_ids:
                raise HTTPException(status_code=400, detail=f"Unknown predecessor id: {p}")

    # Запуск алгоритма
    schedule = coffman_graham(tasks_dict, precedence, m=request.machines)

    # Сборка ответа
    response_schedule: List[List[TaskOutput]] = []
    for machine_tasks in schedule:
        out_tasks = [
            TaskOutput(
                id=task.id,
                start_time=task.start_time,
                end_time=task.end_time,
                machine=task.machine
            )
            for task in machine_tasks
        ]
        out_tasks.sort(key=lambda x: x.start_time)
        response_schedule.append(out_tasks)

    return ScheduleResponse(schedule=response_schedule)
