with open('day1_input.txt', 'r') as f:
    input_list = [int(row) for row in f.read().split('\n') if row]

result = None
# ======================= part 1 ======================= #
# for index, item in enumerate(input_list):
#     for sub_item in input_list[index:]:
#         if item + sub_item == 2020:
#             result = item * sub_item
#             break
#     if result:
#         break

# ======================= part 2 ======================= #
for f_index, f_item in enumerate(input_list):
    for s_index, s_item in enumerate(input_list):
        if f_index >= s_index:
            continue
        for t_index, t_item in enumerate(input_list[s_index:]):
            if s_index >= t_index:
                continue

            if f_item + s_item + t_item == 2020:
                result = f_item * s_item * t_item
                print(f'{f_item} - {s_item} - {t_item}')

print(result)