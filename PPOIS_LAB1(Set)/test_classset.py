import pytest
from ClassSet import ClassSet

class TestClassSet:

    def test_empty_initialization(self):
        s = ClassSet()
        assert len(s) == 0
        assert str(s) == "{}"

    def test_initialization_with_list(self):
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

    def test_initialization_with_quoted_strings(self):
        s = ClassSet('{"hello", "world"}')
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

    def test_invalid_initialization_type(self):
        with pytest.raises(TypeError):
            ClassSet(123)

    def test_invalid_string_format(self):
        with pytest.raises(ValueError):
            ClassSet('1,2,3')

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

    def test_iteration(self):
        s = ClassSet(['a', 'b', 'c'])
        elements = list(s)

        assert len(elements) == 3
        assert set(elements) == {'a', 'b', 'c'}

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

    def test_union(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['b', 'c'])
        result = s1.union(s2)

        assert len(result) == 3
        assert 'a' in result
        assert 'b' in result
        assert 'c' in result

    def test_intersection(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['b', 'c', 'd'])
        result = s1.intersection(s2)

        assert len(result) == 2
        assert 'b' in result
        assert 'c' in result
        assert 'a' not in result
        assert 'd' not in result

    def test_difference(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['b', 'c', 'd'])
        result = s1.difference(s2)

        assert len(result) == 1
        assert 'a' in result
        assert 'b' not in result
        assert 'c' not in result
        assert 'd' not in result

    def test_add_operator(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['b', 'c'])
        result = s1 + s2

        assert len(result) == 3
        assert 'a' in result
        assert 'b' in result
        assert 'c' in result

    def test_iadd_operator(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['b', 'c'])
        s1 += s2

        assert len(s1) == 3
        assert 'a' in s1
        assert 'b' in s1
        assert 'c' in s1

    def test_multiply_operator(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['b', 'c', 'd'])
        result = s1 * s2

        assert len(result) == 2
        assert 'b' in result
        assert 'c' in result

    def test_imultiply_operator(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['b', 'c', 'd'])
        s1 *= s2

        assert len(s1) == 2
        assert 'b' in s1
        assert 'c' in s1
        assert 'a' not in s1

    def test_subtract_operator(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['b', 'c', 'd'])
        result = s1 - s2

        assert len(result) == 1
        assert 'a' in result

    def test_isubtract_operator(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['b', 'c', 'd'])
        s1 -= s2

        assert len(s1) == 1
        assert 'a' in s1
        assert 'b' not in s1
        assert 'c' not in s1

    def test_is_subset(self):
        s1 = ClassSet(['a', 'b'])
        s2 = ClassSet(['a', 'b', 'c'])
        s3 = ClassSet(['x', 'y'])

        assert s1.is_subset(s2)
        assert not s1.is_subset(s3)
        assert s1.is_subset(s1)

    def test_is_superset(self):
        s1 = ClassSet(['a', 'b', 'c'])
        s2 = ClassSet(['a', 'b'])
        s3 = ClassSet(['x', 'y'])

        assert s1.is_superset(s2)
        assert not s1.is_superset(s3)
        assert s1.is_superset(s1)

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

    def test_getitem(self):
        s = ClassSet(['a', 'b', 'c'])

        assert s[0] == 'a'
        assert s[1] == 'b'
        assert s[2] == 'c'

    def test_getitem_invalid_index(self):
        s = ClassSet(['a', 'b'])

        with pytest.raises(IndexError):
            _ = s[2]

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

    def test_repr(self):
        s = ClassSet(['a', 'b'])
        repr_str = repr(s)

        assert repr_str.startswith('ClassSet({')
        assert 'a' in repr_str
        assert 'b' in repr_str

    def test_complex_operations(self):
        inner1 = ClassSet(['1', '2'])
        inner2 = ClassSet(['3', '4'])
        outer = ClassSet(['a', inner1, inner2])

        copy_outer = outer.copy()
        assert outer == copy_outer

        temp = outer + ClassSet(['b'])
        assert len(outer) == 3
        assert len(temp) == 4


if __name__ == "__main__":
    pytest.main([
        __file__,
        "-v",
        "--cov=ClassSet",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-branch"
    ])