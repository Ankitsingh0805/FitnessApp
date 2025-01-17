import random
from typing import List, Dict
from ..database.exercise_db import EXERCISE_DATABASE


def generate_exercise_plan(intensity: float) -> List[Dict]:
    weekly_plan = []
    day_splits = ['push', 'pull', 'legs', 'core', 'cardio', 'push']

    for day_num, split in enumerate(day_splits, 1):
        exercises = random.sample(EXERCISE_DATABASE[split], k=min(4, len(EXERCISE_DATABASE[split])))
        day_exercises = []

        for exercise in exercises:
            sets = max(3, min(5, int(3 * (intensity / 3))))
            reps = max(6, min(15, int(10 * (intensity / 3))))
            rest = max(30, min(90, int(90 - (intensity * 10))))

            day_exercises.append({
                'name': exercise,
                'sets': sets,
                'reps': reps,
                'rest': rest
            })

        weekly_plan.append({
            'day': f'Day {day_num}',
            'focus': split.capitalize(),
            'exercises': day_exercises
        })

    return weekly_plan

