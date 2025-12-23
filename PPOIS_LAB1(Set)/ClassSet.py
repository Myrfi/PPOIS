class ClassSet:
    def __init__(self, elements = None):
        self._elements = []

        if elements is not None:
            if isinstance(elements, str):
                self._parse_string(elements)
            elif isinstance(elements, (list, tuple)):
                self._add_elements(elements)
            else:
                raise TypeError("Неподдерживаемый тип элементов")

    def _parse_string(self, s):
        s = s.strip()

        if not s.startswith('{') or not s.endswith('}'):
            raise ValueError("Строка должна начинаться с '{' и заканчиваться '}'")

        content = s[1:-1].strip()

        if not content:
            return

        elements = self._split_elements(content)

        for element in elements:
            element = element.strip()

            if not element:
                continue
            if element.startswith('{'):
                nested_set = ClassSet(element)
                self.add(nested_set)
            else:
                if (element.startswith('"') and element.endswith('"')) or (element.startswith("'") and element.endswith("'")):
                    element = element[1:-1]

                self.add(element)

    def _split_elements(self, content):
        elements = []
        current = ""
        brace_count = 0
        i = 0

        while i < len(content):
            char = content[i]

            if char == '{':
                brace_count += 1
                current += char
            elif char == '}':
                brace_count -= 1
                current += char
            elif char == ',' and brace_count == 0:
                elements.append(current)
                current = ""
            else:
                current += char

            i += 1

        if current.strip():
            elements.append(current)

            return elements

    def _add_elements(self, elements):
        for element in elements:
            self.add(element)

    def _find_element_index(self, element):
        for i, existing_element in enumerate(self._elements):
            if self._are_equal(existing_element, element):
                return i
        return -1

    def _are_equal(self, elem1, elem2):
        if isinstance(elem1, ClassSet) and isinstance(elem2, ClassSet):
            return elem1 == elem2
        return elem1 == elem2

    def add(self, element):
        if not isinstance(element, (str, ClassSet)):
            raise TypeError("Элемент должен быть строкой или CantorSet")
        if self._find_element_index(element) == -1:
            self._elements.append(element)

    def remove(self, element):
        index = self._find_element_index(element)

        if index == -1:
            raise KeyError(f"Элемент {element} не найден")

        self._elements.pop(index)

    def __contains__(self, item):
        return self._find_element_index(item) != -1

    def __iter__(self):
        return iter(self._elements)

    def __len__(self):
        return len(self._elements)

    def __eq__(self, other):
        if not isinstance(other, ClassSet):
            return False
        if len(other) != len(self):
            return False

        for element in self:
            if element not in other:
                return False

        return True

    def __hash__(self):
        element_hashes = []

        for element in self._elements:
            if isinstance(element, ClassSet):
                element_hashes.append(hash(element))
            else:
                element_hashes.append(hash(str(element)))

        return hash(tuple(sorted(element_hashes)))

    def __str__(self):
        if not self._elements:
            return "{}"

        elements_str = []

        for element in self._elements:
            if isinstance(element, ClassSet):
                elements_str.append(str(element))
            else:
                elements_str.append(str(element))

        return "{" + ",".join(elements_str) + "}"

    def __repr__(self):
        return f"ClassSet({str(self)})"

    def union(self, other):
        if not isinstance(other, ClassSet):
            raise TypeError("Операнд должен быть CantorSet")

        result = ClassSet()

        for element in self:
            result.add(element)

        for element in other:
            result.add(element)

        return result

    def intersection(self, other):
        if not isinstance(other, ClassSet):
            raise TypeError("Операнд должен быть CantorSet")

        result = ClassSet()

        for element in self:
            if element in other:
                result.add(element)

        return result

    def difference(self, other):
        if not isinstance(other, ClassSet):
            raise TypeError("Операнд должен быть CantorSet")

        result = ClassSet()

        for element in self:
            if element not in other:
                result.add(element)

        return result

    def __add__(self, other):
        if not isinstance(other, ClassSet):
            raise TypeError("Операнд должен быть ClassSet")
        return self.union(other)

    def __iadd__(self, other):
        if not isinstance(other, ClassSet):
            raise TypeError("Операнд должен быть ClassSet")
        for element in other:
            self.add(element)
        return self

    def __mul__(self, other):
        if not isinstance(other, ClassSet):
            raise TypeError("Операнд должен быть ClassSet")
        return self.intersection(other)

    def __imul__(self, other):
        if not isinstance(other, ClassSet):
            raise TypeError("Операнд должен быть ClassSet")

        elements_to_remove = []
        for element in self:
            if element not in other:
                elements_to_remove.append(element)

        for element in elements_to_remove:
            self.remove(element)

        return self

    def __sub__(self, other):
        if not isinstance(other, ClassSet):
            raise TypeError("Операнд должен быть ClassSet")
        return self.difference(other)

    def __isub__(self, other):
        if not isinstance(other, ClassSet):
            raise TypeError("Операнд должен быть ClassSet")
        for element in other:
            if element in self:
                self.remove(element)
        return self

    def is_subset(self, other):
        if not isinstance(other, ClassSet):
            raise TypeError("Операнд должен быть CantorSet")

        for element in self:
            if element not in other:
                return False

        return True

    def is_empty(self):
        return len(self._elements) == 0

    def is_superset(self, other):
        if not isinstance(other, ClassSet):
            raise TypeError("Операнд должен быть CantorSet")

        return other.is_subset(self)

    def clear(self):
        self._elements = []

    def copy(self):
        new_set = ClassSet()
        for element in self._elements:
            if isinstance(element, ClassSet):
                new_set.add(element.copy())
            else:
                new_set.add(element)
        return new_set

    def power_set(self):
        elements = list(self._elements)
        result = ClassSet()

        result.add(ClassSet())

        for element in elements:
            current_subsets = list(result)
            for subset in current_subsets:
                new_subset = subset.copy()
                new_subset.add(element)
                result.add(new_subset)

        return result

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= len(self._elements):
            raise IndexError("Индекс вне диапазона")
        return self._elements[index]
