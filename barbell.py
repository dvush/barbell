#/usr/bin/python3

import copy
import sys

# available plates
plates = { 15.0: 2, 10.0: 4, 5.0: 20, 2.5: 20, 1.25: 20 }
target = 100.0
start_weight = 20.0
warm_up_sets = 3

def find_optimal_plates(target, last_set = []):
    no_bar_weight = target - 20.0
    one_side_weight = no_bar_weight / 2.0
    return find_next_set(one_side_weight, last_set)

def greedy_find_plates(w, on_bar = []):
    plates_used = copy.deepcopy(plates)
    result = copy.deepcopy(on_bar)
    w -= sum(on_bar)
    plate_was_added = True
    last_plate_added = on_bar[-1] if len(on_bar) > 0 else 9999998

    while plate_was_added:
        plate_was_added = False

        for plate_w in reversed(sorted(plates_used)):
            if plate_w > last_plate_added:
                continue

            if plates_used[plate_w] == 0:
                continue

            if w - plate_w >= 0:
                w -= plate_w
                result += [plate_w]
                plates_used[plate_w] -= 1
                plate_was_added = True
                last_plate_added = plate_w
                break
    return result

def get_plate_composition_penalty(w, plates):
    if len(plates) > 5:
        return 999999
    return abs(w - sum(plates))

def find_next_set(w, last_set = []):
    best_plates = greedy_find_plates(w, last_set)
    best_penalty = get_plate_composition_penalty(w, best_plates)/0.5 + len(best_plates) - len(last_set)

    removed_plates = 0
    while len(last_set) > 0:
        last_set.reverse()
        last_set.pop()
        last_set.reverse()
        removed_plates += 1

        plates = greedy_find_plates(w, last_set)

        added_plates = len(plates) - len(last_set)

        penalty = get_plate_composition_penalty(w, best_plates)/0.5 + added_plates

        if penalty < best_penalty:
            best_penalty = penalty
            best_plates = plates
    return best_plates
    



if __name__ == "__main__":
    if len(sys.argv) >= 2:
        target = float(sys.argv[1])
    if len(sys.argv) >= 3:
        start_weight = float(sys.argv[2])
    if len(sys.argv) >= 4:
        warm_up_sets = int(sys.argv[3])

    print("Target weight: ", target)
    print("Starting weight: ", start_weight)
    print("Warm up sets: ", warm_up_sets)

    total_used_plates = {}

    jump = (target - start_weight) / warm_up_sets
    weight = start_weight
    last_set = []
    for s in range(warm_up_sets+1):
        set_plates = find_optimal_plates(weight, last_set)
        last_set = set_plates
        print("Total",sum(set_plates)*2 + 20.0, "Plates", set_plates)

        set_used_plates = {}
        for p in set_plates:
            set_used_plates[p] = set_used_plates.get(p, 0) + 1

        for k in set_used_plates:
            total_used_plates[k] = max( total_used_plates.get(k,0), set_used_plates[k])

        weight += jump

    print("Plates needed for this set")
    for k in sorted(total_used_plates):
        print(k, total_used_plates[k])
