import pytest
import numpy as np
from rubiks_cube import RubiksCube


@pytest.fixture
def cube():
    cube = RubiksCube.__new__(RubiksCube)

    # минимальная ручная инициализация
    cube.colors = {
        'F': (1, 0, 0),
        'B': (1, 0.5, 0),
        'U': (1, 1, 1),
        'D': (1, 1, 0),
        'L': (0, 0, 1),
        'R': (0, 1, 0),
    }

    cube.animating = False
    cube.animation_angle = 0
    cube.target_angle = 0
    cube.rotation_face = None
    cube.rotation_layer = None
    cube.rotation_direction = 1

    cube.reset_cube()
    return cube


def test_reset_cube(cube):
    assert cube.cube.shape == (3, 3, 3)
    assert cube.cube[0, 0, 0] == 'L'


def test_index_to_3d(cube):
    assert cube.index_to_3d(0) == (0, 0, 0)
    assert cube.index_to_3d(26) == (2, 2, 2)


def test_rotate_and_apply(cube):
    cube.rotate_face('F', 1)
    cube.apply_rotation()
    assert cube.animating is False


def test_scramble(cube):
    cube.scramble()
    assert cube.cube is not None


def test_is_solved_true(cube):
    assert cube.is_solved() is True


def test_is_solved_false(cube):
    cube.cube[0, 0, 0] = 'F'
    assert cube.is_solved() is False


def test_update_animation(cube):
    cube.rotate_face('F', 1)
    cube.update_animation()
    assert cube.animation_angle != 0


def test_save_and_load(tmp_path, cube):
    file = tmp_path / "cube.txt"
    cube.save_to_file(file)
    cube.load_from_file(file)
    assert cube.cube is not None
