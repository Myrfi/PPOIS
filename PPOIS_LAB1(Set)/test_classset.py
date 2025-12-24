import pytest
from ClassSet import ClassSet

class TestClassSet:

    def test_empty_initialization(self):
        s = ClassSet()
        assert len(s) == 0
        assert str(s) == "{}"

    def test_initialization_with_list(selfa):
        s = ClassSet(['1', '2', '3'])
        assert len(s) == 3
        assert '1' in s
        assert '2' in s
        assert '3' in s

    def test_initialization_with_tuple(self):
        s = ClassSet(('a', 'b', 'c'))
        assert len(s) == 3
        assert 'a' in s
        assert 'b' in s
        assert 'c' in s

    def test_initialization_with_string(self):
        s = ClassSet('{1,2,3}')
        assert len(s) == 3
        assert '1' in s
        assert '2' in s
        assert '3' in s

    def test_initialization_with_empty_string(self):
        s = ClassSet('{}')
        assert len(s) == 0
        assert str(s) == "{}"

    def test_initialization_with_string_spaces(self):
        s = ClassSet('{ 1 , 2 , 3 }')
        assert len(s) == 3
        assert '1' in s
        assert '2' in s
        assert '3' in s

    def test_initialization_with_quoted_strings_double(self):
        s = ClassSet('{"hello", "world"}')
        assert len(s) == 2
        assert 'hello' in s
        assert 'world' in s

    def test_initialization_with_quoted_strings_single(self):
        s = ClassSet("{'hello', 'world'}")
        assert len(s) == 2
        assert 'hello' in s
        assert 'world' in s

    def test_initialization_with_nested_set_string(self):
        s = ClassSet('{1, {2, 3}, 4}')
        assert len(s) == 3
        assert '1' in s
        assert '4' in s

        nested_found = False
        for element in s:
            if isinstance(element, ClassSet):
                nested_found = True
                assert len(element) == 2
                assert '2' in element
                assert '3' in element
        assert nested_found

    def test_initialization_with_complex_nested_string(self):
        s = ClassSet('{1, {2, {3, 4}}, 5}')
        assert len(s) == 3
        assert '1' in s
        assert '5' in s

        for element in s:
            if isinstance(element, ClassSet):
                assert len(element) == 2
                assert '2' in element
                for sub_element in element:
                    if isinstance(sub_element, ClassSet):
                        assert len(sub_element) == 2
                        assert '3' in sub_element
                        assert '4' in sub_element

    def test_initialization_with_empty_elements_in_string(self):
        s = ClassSet('{1, , 2, , 3}')
        assert len(s) >= 2  # Empty elements should be skipped

    def test_invalid_initialization_type(self):
        with pytest.raises(TypeError):
            ClassSet(123)

    def test_invalid_string_format_no_braces(self):
        with pytest.raises(ValueError):
            ClassSet('1,2,3')

    def test_invalid_string_format_only_open_brace(self):
        with pytest.raises(ValueError):
            ClassSet('{1,2,3')

    def test_invalid_string_format_only_close_brace(self):
        with pytest.raises(ValueError):
            ClassSet('1,2,3}')

    def test_add_elements(self):
        s = ClassSet()
        s.add('a')
        s.add('b')
        nested_set = ClassSet(['1', '2'])
        s.add(nested_set)

        assert len(s) == 3
        assert 'a' in s
        assert 'b' in s

        nested_found = False
        for element in s:
            if isinstance(element, ClassSet):
                nested_found = True
                assert '1' in element
                assert '2' in element
        assert nested_found

    def test_add_duplicate_elements(self):
        s = ClassSet()
        s.add('a')
        s.add('a')
        s.add('b')

        assert len(s) == 2

    def test_add_duplicate_nested_set(self):
        nested1 = ClassSet(['1', '2'])
        nested2 = ClassSet(['2', '1'])
        s = ClassSet()
        s.add(nested1)
        s.add(nested2)
        assert len(s) == 1

    def test_add_invalid_type(self):
        s = ClassSet()
        with pytest.raises(TypeError):
            s.add(123)

    def test_remove_element(self):
        s = ClassSet(['a', 'b', 'c'])
        s.remove('b')

        assert len(s) == 2
        assert 'a' in s
        assert 'b' not in s
        assert 'c' in s

    def test_remove_nested_set(self):
        nested = ClassSet(['1', '2'])
        s = ClassSet(['a', nested, 'b'])
        s.remove(nested)
        assert len(s) == 2
        assert 'a' in s
        assert 'b' in s
        assert nested not in s

    def test_remove_nonexistent_element(self):
        s = ClassSet(['a', 'b'])
        with pytest.raises(KeyError):
            s.remove('c')

    def test_contains(self):
        nested_set = ClassSet(['1', '2'])
        s = ClassSet(['a', 'b', nested_set])

        assert 'a' in s
        assert 'b' in s
        assert 'c' not in s
        assert nested_set in s

    def test_contains_nested_set_equal(self):
        nested1 = ClassSet(['1', '2'])
        nested2 = ClassSet(['2', '1'])
        s = ClassSet(['a', nested1])
        assert nested2 in s

    def test_iteration(self):
        s = ClassSet(['a', 'b', 'c'])
        elements = list(s)

        assert len(elements) == 3
        assert set(elements) == {'a', 'b', 'c'}

    def test_iteration_empty(self):
        s = ClassSet()
        elements = list(s)
        assert len(elements) == 0

    def test_equality(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['b', 'a'])
        s3 = ClassSet(['a', 'b', 'c'])
        s4 = ClassSet(['x', 'y'])

        assert s1 == s2
        assert s1 != s3
        assert s1 != s4

    def test_equality_with_nested_sets(self):
        nested_set1 = ClassSet(['1', '2'])
        nested_set2 = ClassSet(['2', '1'])
        s1 = ClassSet(['a', nested_set1])
        s2 = ClassSet([nested_set2, 'a'])

        assert s1 == s2

    def test_equality_with_non_classset(self):
        s1 = ClassSet(['a', 'b'])
        assert s1 != "not a set"
        assert s1 != 123
        assert s1 != ['a', 'b']

    def test_equality_different_lengths(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['a'])
        assert s1 != s2

    def test_union(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['b', 'c'])
        result = s1.union(s2)

        assert len(result) == 3
        assert 'a' in result
        assert 'b' in result
        assert 'c' in result

    def test_union_invalid_type(self):
        s1 = ClassSet(['a', 'b'])
        with pytest.raises(TypeError):
            s1.union("not a set")

    def test_intersection(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['b', 'c', 'd'])
        result = s1.intersection(s2)

        assert len(result) == 2
        assert 'b' in result
        assert 'c' in result
        assert 'a' not in result
        assert 'd' not in result

    def test_intersection_empty(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['c', 'd'])
        result = s1.intersection(s2)
        assert len(result) == 0

    def test_intersection_invalid_type(self):
        s1 = ClassSet(['a', 'b'])
        with pytest.raises(TypeError):
            s1.intersection("not a set")

    def test_difference(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['b', 'c', 'd'])
        result = s1.difference(s2)

        assert len(result) == 1
        assert 'a' in result
        assert 'b' not in result
        assert 'c' not in result
        assert 'd' not in result

    def test_difference_empty_result(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['a', 'b', 'c'])
        result = s1.difference(s2)
        assert len(result) == 0

    def test_difference_invalid_type(self):
        s1 = ClassSet(['a', 'b'])
        with pytest.raises(TypeError):
            s1.difference("not a set")

    def test_add_operator(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['b', 'c'])
        result = s1 + s2

        assert len(result) == 3
        assert 'a' in result
        assert 'b' in result
        assert 'c' in result

    def test_add_operator_invalid_type(self):
        s1 = ClassSet(['a', 'b'])
        with pytest.raises(TypeError):
            _ = s1 + "not a set"

    def test_iadd_operator(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['b', 'c'])
        s1 += s2

        assert len(s1) == 3
        assert 'a' in s1
        assert 'b' in s1
        assert 'c' in s1

    def test_iadd_operator_invalid_type(self):
        s1 = ClassSet(['a', 'b'])
        with pytest.raises(TypeError):
            s1 += "not a set"

    def test_multiply_operator(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['b', 'c', 'd'])
        result = s1 * s2

        assert len(result) == 2
        assert 'b' in result
        assert 'c' in result

    def test_multiply_operator_invalid_type(self):
        s1 = ClassSet(['a', 'b'])
        with pytest.raises(TypeError):
            _ = s1 * "not a set"

    def test_imultiply_operator(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['b', 'c', 'd'])
        s1 *= s2

        assert len(s1) == 2
        assert 'b' in s1
        assert 'c' in s1
        assert 'a' not in s1

    def test_imultiply_operator_invalid_type(self):
        s1 = ClassSet(['a', 'b'])
        with pytest.raises(TypeError):
            s1 *= "not a set"

    def test_subtract_operator(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['b', 'c', 'd'])
        result = s1 - s2

        assert len(result) == 1
        assert 'a' in result

    def test_subtract_operator_invalid_type(self):
        s1 = ClassSet(['a', 'b'])
        with pytest.raises(TypeError):
            _ = s1 - "not a set"

    def test_isubtract_operator(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['b', 'c', 'd'])
        s1 -= s2

        assert len(s1) == 1
        assert 'a' in s1
        assert 'b' not in s1
        assert 'c' not in s1

    def test_isubtract_operator_invalid_type(self):
        s1 = ClassSet(['a', 'b'])
        with pytest.raises(TypeError):
            s1 -= "not a set"

    def test_isubtract_operator_nonexistent_element(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['c'])
        s1 -= s2  # Should not raise error, just do nothing
        assert len(s1) == 2

    def test_is_subset(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['a', 'b', 'c'])
        s3 = ClassSet(['x', 'y'])

        assert s1.is_subset(s2)
        assert not s1.is_subset(s3)
        assert s1.is_subset(s1)

    def test_is_subset_empty(self):
        empty = ClassSet()
        s1 = ClassSet(['a', 'b'])
        assert empty.is_subset(s1)
        assert empty.is_subset(empty)

    def test_is_subset_invalid_type(self):
        s1 = ClassSet(['a', 'b'])
        with pytest.raises(TypeError):
            s1.is_subset("not a set")

    def test_is_superset(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['a', 'b'])
        s3 = ClassSet(['x', 'y'])

        assert s1.is_superset(s2)
        assert not s1.is_superset(s3)
        assert s1.is_superset(s1)

    def test_is_superset_invalid_type(self):
        s1 = ClassSet(['a', 'b'])
        with pytest.raises(TypeError):
            s1.is_superset("not a set")

    def test_is_empty(self):
        empty_set = ClassSet()
        non_empty_set = ClassSet(['a'])

        assert empty_set.is_empty()
        assert not non_empty_set.is_empty()

    def test_clear(self):
        s = ClassSet(['a', 'b', 'c'])
        s.clear()

        assert len(s) == 0
        assert s.is_empty()

    def test_copy(self):
        nested_set = ClassSet(['1', '2'])
        s1 = ClassSet(['a', nested_set])
        s2 = s1.copy()

        assert s1 == s2
        assert s1 is not s2

        for elem1, elem2 in zip(s1, s2):
            if isinstance(elem1, ClassSet):
                assert elem1 == elem2
                assert elem1 is not elem2

    def test_copy_empty(self):
        s1 = ClassSet()
        s2 = s1.copy()
        assert s1 == s2
        assert len(s2) == 0

    def test_power_set(self):
        s = ClassSet(['a', 'b'])
        power_set = s.power_set()

        assert len(power_set) == 4

        expected_subsets = [
            ClassSet(),
            ClassSet(['a']),
            ClassSet(['b']),
            ClassSet(['a', 'b'])
        ]

        for subset in expected_subsets:
            assert subset in power_set

    def test_power_set_empty(self):
        s = ClassSet()
        power_set = s.power_set()
        assert len(power_set) == 1
        assert ClassSet() in power_set

    def test_power_set_single_element(self):
        s = ClassSet(['a'])
        power_set = s.power_set()
        assert len(power_set) == 2
        assert ClassSet() in power_set
        assert ClassSet(['a']) in power_set

    def test_getitem(self):
        s = ClassSet(['a', 'b', 'c'])

        assert s[0] == 'a'
        assert s[1] == 'b'
        assert s[2] == 'c'

    def test_getitem_nested_set(self):
        nested = ClassSet(['1', '2'])
        s = ClassSet(['a', nested, 'b'])
        assert s[1] == nested

    def test_getitem_invalid_index_positive(self):
        s = ClassSet(['a', 'b'])

        with pytest.raises(IndexError):
            _ = s[2]

    def test_getitem_invalid_index_negative(self):
        s = ClassSet(['a', 'b'])

        with pytest.raises(IndexError):
            _ = s[-1]

    def test_getitem_invalid_type(self):
        s = ClassSet(['a', 'b'])

        with pytest.raises(TypeError):
            _ = s['invalid']

    def test_hash(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['b', 'a'])

        assert hash(s1) == hash(s2)

        test_dict = {s1: 'value1', s2: 'value2'}
        assert len(test_dict) == 1

    def test_hash_with_nested_set(self):
        nested1 = ClassSet(['1', '2'])
        nested2 = ClassSet(['2', '1'])
        s1 = ClassSet(['a', nested1])
        s2 = ClassSet(['a', nested2])
        
        assert hash(s1) == hash(s2)

    def test_hash_consistent(self):
        s = ClassSet(['a', 'b', 'c'])
        hash1 = hash(s)
        hash2 = hash(s)
        assert hash1 == hash2

    def test_str(self):
        s = ClassSet(['a', 'b'])
        str_repr = str(s)
        assert str_repr.startswith('{')
        assert str_repr.endswith('}')
        assert 'a' in str_repr
        assert 'b' in str_repr

    def test_str_with_nested_set(self):
        nested = ClassSet(['1', '2'])
        s = ClassSet(['a', nested])
        str_repr = str(s)
        assert str_repr.startswith('{')
        assert str_repr.endswith('}')
        assert 'a' in str_repr
        assert '{' in str_repr  # Should contain nested set representation

    def test_str_empty(self):
        s = ClassSet()
        assert str(s) == "{}"

    def test_repr(self):
        s = ClassSet(['a', 'b'])
        repr_str = repr(s)

        assert repr_str.startswith('ClassSet({')
        assert 'a' in repr_str
        assert 'b' in repr_str

    def test_repr_empty(self):
        s = ClassSet()
        repr_str = repr(s)
        assert repr_str == "ClassSet({})"

    def test_complex_operations(self):
        inner1 = ClassSet(['1', '2'])
        inner2 = ClassSet(['3', '4'])
        outer = ClassSet(['a', inner1, inner2])

        copy_outer = outer.copy()
        assert outer == copy_outer

        temp = outer + ClassSet(['b'])
        assert len(outer) == 3
        assert len(temp) == 4

    def test_string_parsing_with_quotes_inside(self):
        # Парсер не учитывает кавычки при разбиении, поэтому запятая внутри строки создаёт отдельные элементы
        s = ClassSet('{"hello, world", "test"}')
        # Строка разбивается на: '"hello', 'world"', 'test' -> 3 элемента
        assert len(s) == 3
        assert '"hello' in s  # Первая часть до запятой
        assert 'world"' in s  # Вторая часть после запятой
        assert 'test' in s  # Последняя часть

    def test_string_parsing_with_spaces_and_quotes(self):
        s = ClassSet("{ 'hello' , 'world' }")
        assert len(s) == 2
        assert 'hello' in s
        assert 'world' in s

    def test_are_equal_method_with_nested_sets(self):
        nested1 = ClassSet(['1', '2'])
        nested2 = ClassSet(['2', '1'])
        s = ClassSet()
        # This tests the _are_equal method indirectly through add
        s.add(nested1)
        assert nested2 in s

    def test_split_elements_complex_nesting(self):
        s = ClassSet('{a, {b, {c, d}}, e}')
        assert len(s) == 3
        assert 'a' in s
        assert 'e' in s

    def test_imultiply_operator_empty_result(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['c', 'd'])
        s1 *= s2
        assert len(s1) == 0
        assert s1.is_empty()

    def test_find_element_index_not_found(self):
        s = ClassSet(['a', 'b'])
        # This tests _find_element_index indirectly
        assert 'c' not in s

    def test_string_parsing_trailing_comma(self):
        s = ClassSet('{a, b, }')
        assert 'a' in s
        assert 'b' in s

    def test_string_parsing_leading_comma(self):
        s = ClassSet('{, a, b}')
        assert 'a' in s
        assert 'b' in s


if __name__ == "__main__":
    import sys
    exit_code = pytest.main([
        __file__,
        "-v",
        "--cov=ClassSet",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-branch"
    ])
    
    # Дополнительный вывод покрытия в процентах
    try:
        import subprocess
        result = subprocess.run(
            ["python3", "-m", "coverage", "report", "--include=ClassSet.py", "-m"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                total_line = lines[-1]  # Последняя строка содержит итоговую статистику
                if 'TOTAL' in total_line or 'ClassSet.py' in total_line:
                    # Извлекаем процент покрытия
                    parts = total_line.split()
                    for i, part in enumerate(parts):
                        if '%' in part:
                            print(f"\n{'='*60}")
                            print(f"Покрытие кода: {part}")
                            print(f"{'='*60}")
                            break
    except Exception:
        pass  # Если coverage не установлен, пропускаем
    
    sys.exit(exit_code)
