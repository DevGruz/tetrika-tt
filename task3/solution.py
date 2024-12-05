def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    sorted_intervals = sorted(intervals)
    merged: list[tuple[int, int]] = []

    for start, end in sorted_intervals:
        if merged and merged[-1][1] >= start:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


def calculating_total_time_between_intervals(
    *,
    lesson_intervals: list[int],
    pupil_intervals: list[tuple[int, int]],
    tutor_intervals: list[tuple[int, int]],
):
    i, j = 0, 0
    result = 0

    while i < len(pupil_intervals) and j < len(tutor_intervals):
        pupil_interval = pupil_intervals[i]
        tutor_interval = tutor_intervals[j]

        mx = max(pupil_interval[0], tutor_interval[0], lesson_intervals[0])
        mn = min(pupil_interval[1], tutor_interval[1], lesson_intervals[1])

        if mx < mn:
            result += mn - mx

        if pupil_interval[1] < tutor_interval[1]:
            i += 1
        else:
            j += 1

        if mn == lesson_intervals[1]:
            break

    return result


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_intervals = [intervals["lesson"][0], intervals["lesson"][1]]
    pupil_intervals = list(zip(intervals["pupil"][::2], intervals["pupil"][1::2]))
    tutor_intervals = list(zip(intervals["tutor"][::2], intervals["tutor"][1::2]))

    pupil_intervals = merge_intervals(pupil_intervals)
    tutor_intervals = merge_intervals(tutor_intervals)

    return calculating_total_time_between_intervals(
        lesson_intervals=lesson_intervals,
        pupil_intervals=pupil_intervals,
        tutor_intervals=tutor_intervals,
    )


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594691033, 1594691038],
             'tutor': [1594691037, 1594691040]},
    'answer': 0
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'