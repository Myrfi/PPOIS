from ClassSet import ClassSet

s1_input = input("Введите множество(1): ").strip()
s1 = ClassSet(s1_input)
print("Множество 1:", s1)

s2_input = input("Введите множество(2): ").strip()
s2 = ClassSet(s2_input)
print("Множество 2:", s2)

# 1. Проверка на пустое множество
print("\n1. Проверка на пустое множество:")
print(f"s1 пустое: {s1.is_empty()}")
print(f"s2 пустое: {s2.is_empty()}")

# 2. Мощность множества
print(f"\n2. Мощность множества:")
print(f"|s1| = {len(s1)}")
print(f"|s2| = {len(s2)}")

# 3. Проверка принадлежности элемента []
print(f"\n3. Проверка принадлежности:")
if len(s1) > 0:
    print(f"s1[0] = {s1[0]} (первый элемент)")
test_elem = input("Проверить элемент в s1: ").strip()
if test_elem:
    print(f"'{test_elem}' в s1: {test_elem in s1}")

# 4. Элементом множества может быть другое множество
print(f"\n4. Вложенные множества:")
print(f"Множества в s1:")
for elem in s1:
    if isinstance(elem, ClassSet):
        print(f"  - {elem} (вложенное множество)")

# 5. Объединение + и +=
print(f"\n5. Объединение:")
print(f"s1 + s2 = {s1 + s2}")
s1_union = s1.copy()
s1_union += s2
print(f"s1 += s2 = {s1_union}")

# 6. Пересечение * и *=
print(f"\n6. Пересечение:")
print(f"s1 * s2 = {s1 * s2}")
s1_intersect = s1.copy()
s1_intersect *= s2
print(f"s1 *= s2 = {s1_intersect}")

# 7. Разность - и -=
print(f"\n7. Разность:")
print(f"s1 - s2 = {s1 - s2}")
s1_diff = s1.copy()
s1_diff -= s2
print(f"s1 -= s2 = {s1_diff}")

# 8. Добавление элемента
print(f"\n8. Добавление элемента:")
add_elem = input("Добавить элемент в s1: ").strip()
if add_elem:
    s1.add(add_elem)
    print(f"После добавления: {s1}")

# 9. Удаление элемента
print(f"\n9. Удаление элемента:")
if len(s1) > 0:
    print("Текущие элементы s1:")
    for i, elem in enumerate(s1, 1):
        print(f"  {i}. {elem}")

    remove_choice = input("Введите номер элемента для удаления: ").strip()
    if remove_choice.isdigit():
        index = int(remove_choice) - 1
        elements = list(s1)
        if 0 <= index < len(elements):
            removed_elem = elements[index]
            s1.remove(removed_elem)
            print(f"После удаления '{removed_elem}': {s1}")

# 10. Булеан
print(f"\n10. Булеан:")
if len(s1) <= 4:
    bool_set = s1.power_set()
    print(f"Булеан s1: {bool_set}")
    print(f"Мощность булеана: {len(bool_set)}")
else:
    print("Множество слишком большое для отображения булеана")
