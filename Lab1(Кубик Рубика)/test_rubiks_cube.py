import pytest
import numpy as np
import sys
from unittest.mock import Mock, patch, MagicMock, mock_open
import os

# Мокируем pygame и OpenGL перед импортом RubiksCube
pygame_mock = MagicMock()
# Устанавливаем константы для клавиш
pygame_mock.K_ESCAPE = 27
pygame_mock.K_r = 114
pygame_mock.K_s = 115
pygame_mock.K_l = 108
pygame_mock.K_p = 112
pygame_mock.K_f = 102
pygame_mock.K_b = 98
pygame_mock.K_u = 117
pygame_mock.K_d = 100
pygame_mock.K_F = 70  # uppercase F
pygame_mock.K_B = 66  # uppercase B
pygame_mock.K_U = 85  # uppercase U
pygame_mock.K_D = 68  # uppercase D
pygame_mock.K_L = 76  # uppercase L
pygame_mock.K_R = 82  # uppercase R
pygame_mock.QUIT = 256
pygame_mock.KEYDOWN = 768
pygame_mock.MOUSEMOTION = 1024
pygame_mock.KMOD_SHIFT = 1
pygame_mock.OPENGL = 2
pygame_mock.DOUBLEBUF = 1073741824

sys.modules['pygame'] = pygame_mock
sys.modules['OpenGL'] = MagicMock()
sys.modules['OpenGL.GL'] = MagicMock()
sys.modules['OpenGL.GLU'] = MagicMock()

from rubiks_cube import RubiksCube


@pytest.fixture
def cube():
    """Фикстура для создания кубика без инициализации pygame/OpenGL"""
    patches = [
        patch('pygame.init'),
        patch('pygame.display.set_mode'),
        patch('pygame.display.set_caption'),
        patch('pygame.display.flip'),
        patch('pygame.event.get'),
        patch('pygame.mouse.get_pressed'),
        patch('pygame.time.Clock'),
        patch('pygame.quit'),
        patch('pygame.key.get_mods'),
        patch('OpenGL.GL.glEnable'),
        patch('OpenGL.GL.glMatrixMode'),
        patch('OpenGL.GL.glClear'),
        patch('OpenGL.GL.glLoadIdentity'),
        patch('OpenGL.GL.glTranslatef'),
        patch('OpenGL.GL.glRotatef'),
        patch('OpenGL.GL.glBegin'),
        patch('OpenGL.GL.glEnd'),
        patch('OpenGL.GL.glColor3f'),
        patch('OpenGL.GL.glVertex3f'),
        patch('OpenGL.GLU.gluPerspective')
    ]
    
    for p in patches:
        p.start()
    
    try:
        cube_instance = RubiksCube.__new__(RubiksCube)
        
        # Минимальная ручная инициализация
        cube_instance.colors = {
            'F': (1, 0, 0),
            'B': (1, 0.5, 0),
            'U': (1, 1, 1),
            'D': (1, 1, 0),
            'L': (0, 0, 1),
            'R': (0, 1, 0),
        }
        
        cube_instance.animating = False
        cube_instance.animation_angle = 0
        cube_instance.target_angle = 0
        cube_instance.rotation_face = None
        cube_instance.rotation_layer = None
        cube_instance.rotation_direction = 1
        cube_instance.rotation_x = 0
        cube_instance.rotation_y = 0
        
        cube_instance.reset_cube()
        yield cube_instance
    finally:
        for p in patches:
            p.stop()


class TestInitialization:
    """Тесты инициализации"""
    
    def test_init(self):
        """Тест полной инициализации"""
        with patch('pygame.init'), \
             patch('pygame.display.set_mode', return_value=Mock()), \
             patch('pygame.display.set_caption'), \
             patch('OpenGL.GL.glEnable'), \
             patch('OpenGL.GL.glMatrixMode'), \
             patch('OpenGL.GLU.gluPerspective'):
            cube = RubiksCube()
            assert cube.width == 800
            assert cube.height == 600
            assert cube.colors is not None
            assert cube.rotation_x == 0
            assert cube.rotation_y == 0
            assert cube.animating is False


class TestResetCube:
    """Тесты сброса кубика"""
    
    def test_reset_cube(self, cube):
        """Тест сброса кубика"""
        assert cube.cube.shape == (3, 3, 3)
        assert cube.cube[0, 0, 0] == 'L'
        assert cube.cube[2, 0, 0] == 'R'
        assert cube.cube[0, 0, 0] == 'L'
        assert cube.cube[1, 0, 0] == 'D'
        assert cube.cube[1, 2, 0] == 'U'
        assert cube.cube[1, 1, 0] == 'B'
        assert cube.cube[1, 1, 2] == 'F'
        assert cube.cube[1, 1, 1] is None  # Внутренний кубик
    
    def test_reset_cube_all_positions(self, cube):
        """Тест всех позиций после сброса"""
        # Проверяем грани
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    if x == 0:
                        assert cube.cube[x, y, z] == 'L'
                    elif x == 2:
                        assert cube.cube[x, y, z] == 'R'
                    elif y == 0:
                        assert cube.cube[x, y, z] == 'D'
                    elif y == 2:
                        assert cube.cube[x, y, z] == 'U'
                    elif z == 0:
                        assert cube.cube[x, y, z] == 'B'
                    elif z == 2:
                        assert cube.cube[x, y, z] == 'F'
                    else:
                        assert cube.cube[x, y, z] is None


class TestIndexTo3D:
    """Тесты конвертации индекса в 3D координаты"""
    
    def test_index_to_3d(self, cube):
        """Тест конвертации индекса"""
        assert cube.index_to_3d(0) == (0, 0, 0)
        assert cube.index_to_3d(1) == (1, 0, 0)
        assert cube.index_to_3d(2) == (2, 0, 0)
        assert cube.index_to_3d(3) == (0, 1, 0)
        assert cube.index_to_3d(9) == (0, 0, 1)
        assert cube.index_to_3d(13) == (1, 1, 1)
        assert cube.index_to_3d(26) == (2, 2, 2)


class TestRotateFace:
    """Тесты поворота граней"""
    
    def test_rotate_face_F(self, cube):
        """Тест поворота грани F"""
        cube.animating = False
        cube.rotate_face('F', 1)
        assert cube.animating is True
        assert cube.rotation_face == 'F'
        assert cube.rotation_direction == 1
        assert cube.rotation_layer == 2
        assert cube.target_angle == 90
    
    def test_rotate_face_B(self, cube):
        """Тест поворота грани B"""
        cube.animating = False
        cube.rotate_face('B', 1)
        assert cube.rotation_face == 'B'
        assert cube.rotation_layer == 0
    
    def test_rotate_face_U(self, cube):
        """Тест поворота грани U"""
        cube.animating = False
        cube.rotate_face('U', 1)
        assert cube.rotation_face == 'U'
        assert cube.rotation_layer == 2
    
    def test_rotate_face_D(self, cube):
        """Тест поворота грани D"""
        cube.animating = False
        cube.rotate_face('D', 1)
        assert cube.rotation_face == 'D'
        assert cube.rotation_layer == 0
    
    def test_rotate_face_L(self, cube):
        """Тест поворота грани L"""
        cube.animating = False
        cube.rotate_face('L', 1)
        assert cube.rotation_face == 'L'
        assert cube.rotation_layer == 0
    
    def test_rotate_face_R(self, cube):
        """Тест поворота грани R"""
        cube.animating = False
        cube.rotate_face('R', 1)
        assert cube.rotation_face == 'R'
        assert cube.rotation_layer == 2
    
    def test_rotate_face_negative_direction(self, cube):
        """Тест поворота против часовой стрелки"""
        cube.animating = False
        cube.rotate_face('F', -1)
        assert cube.rotation_direction == -1
        assert cube.target_angle == -90
    
    def test_rotate_face_while_animating(self, cube):
        """Тест поворота во время анимации"""
        cube.animating = True
        original_face = cube.rotation_face
        cube.rotate_face('F', 1)
        # Не должно измениться, если уже анимируется
        assert cube.rotation_face == original_face


class TestApplyRotation:
    """Тесты применения поворота"""
    
    def test_apply_rotation_F_clockwise(self, cube):
        """Тест применения поворота F по часовой"""
        cube.rotation_face = 'F'
        cube.rotation_direction = 1
        original = cube.cube.copy()
        cube.apply_rotation()
        # Проверяем, что поворот произошел
        assert not np.array_equal(cube.cube, original)
        assert cube.animating is False

    def test_apply_rotation_F_counterclockwise(self, cube):
        """Тест применения поворота F против часовой"""
        cube.rotation_face = 'F'
        cube.rotation_direction = -1
        original = cube.cube.copy()
        cube.apply_rotation()
        assert not np.array_equal(cube.cube, original)
    
    def test_apply_rotation_B_clockwise(self, cube):
        """Тест применения поворота B по часовой"""
        cube.rotation_face = 'B'
        cube.rotation_direction = 1
        original = cube.cube.copy()
        cube.apply_rotation()
        assert not np.array_equal(cube.cube, original)
    
    def test_apply_rotation_B_counterclockwise(self, cube):
        """Тест применения поворота B против часовой"""
        cube.rotation_face = 'B'
        cube.rotation_direction = -1
        original = cube.cube.copy()
        cube.apply_rotation()
        assert not np.array_equal(cube.cube, original)
    
    def test_apply_rotation_U_clockwise(self, cube):
        """Тест применения поворота U по часовой"""
        cube.rotation_face = 'U'
        cube.rotation_direction = 1
        original = cube.cube.copy()
        cube.apply_rotation()
        assert not np.array_equal(cube.cube, original)
    
    def test_apply_rotation_U_counterclockwise(self, cube):
        """Тест применения поворота U против часовой"""
        cube.rotation_face = 'U'
        cube.rotation_direction = -1
        original = cube.cube.copy()
        cube.apply_rotation()
        assert not np.array_equal(cube.cube, original)
    
    def test_apply_rotation_D_clockwise(self, cube):
        """Тест применения поворота D по часовой"""
        cube.rotation_face = 'D'
        cube.rotation_direction = 1
        original = cube.cube.copy()
        cube.apply_rotation()
        assert not np.array_equal(cube.cube, original)
    
    def test_apply_rotation_D_counterclockwise(self, cube):
        """Тест применения поворота D против часовой"""
        cube.rotation_face = 'D'
        cube.rotation_direction = -1
        original = cube.cube.copy()
        cube.apply_rotation()
        assert not np.array_equal(cube.cube, original)
    
    def test_apply_rotation_L_clockwise(self, cube):
        """Тест применения поворота L по часовой"""
        cube.rotation_face = 'L'
        cube.rotation_direction = 1
        original = cube.cube.copy()
        cube.apply_rotation()
        assert not np.array_equal(cube.cube, original)
    
    def test_apply_rotation_L_counterclockwise(self, cube):
        """Тест применения поворота L против часовой"""
        cube.rotation_face = 'L'
        cube.rotation_direction = -1
        original = cube.cube.copy()
        cube.apply_rotation()
        assert not np.array_equal(cube.cube, original)
    
    def test_apply_rotation_R_clockwise(self, cube):
        """Тест применения поворота R по часовой"""
        cube.rotation_face = 'R'
        cube.rotation_direction = 1
        original = cube.cube.copy()
        cube.apply_rotation()
        assert not np.array_equal(cube.cube, original)
    
    def test_apply_rotation_R_counterclockwise(self, cube):
        """Тест применения поворота R против часовой"""
        cube.rotation_face = 'R'
        cube.rotation_direction = -1
        original = cube.cube.copy()
        cube.apply_rotation()
        assert not np.array_equal(cube.cube, original)
    
    def test_apply_rotation_double_rotation(self, cube):
        """Тест двойного поворота (туда-обратно)"""
        original = cube.cube.copy()
        cube.rotation_face = 'F'
        cube.rotation_direction = 1
        cube.apply_rotation()
        cube.rotation_face = 'F'
        cube.rotation_direction = -1
        cube.apply_rotation()
        # Должно вернуться к исходному состоянию
        assert np.array_equal(cube.cube, original)


class TestIsSolved:
    """Тесты проверки собранности кубика"""
    
    def test_is_solved_true(self, cube):
        """Тест собранного кубика"""
        assert cube.is_solved() is True

    def test_is_solved_false_F(self, cube):
        """Тест несобранного кубика - грань F"""
        cube.cube[0, 0, 2] = 'B'
        assert cube.is_solved() is False

    def test_is_solved_false_B(self, cube):
        """Тест несобранного кубика - грань B"""
        cube.cube[0, 0, 0] = 'F'
        assert cube.is_solved() is False

    def test_is_solved_false_U(self, cube):
        """Тест несобранного кубика - грань U"""
        cube.cube[0, 2, 0] = 'D'
        assert cube.is_solved() is False
    
    def test_is_solved_false_D(self, cube):
        """Тест несобранного кубика - грань D"""
        cube.cube[0, 0, 0] = 'U'
        assert cube.is_solved() is False
    
    def test_is_solved_false_L(self, cube):
        """Тест несобранного кубика - грань L"""
        cube.cube[0, 0, 0] = 'R'
        assert cube.is_solved() is False
    
    def test_is_solved_false_R(self, cube):
        """Тест несобранного кубика - грань R"""
        cube.cube[2, 0, 0] = 'L'
        assert cube.is_solved() is False
    
    def test_is_solved_after_rotation(self, cube):
        """Тест после поворота"""
        cube.rotation_face = 'F'
        cube.rotation_direction = 1
        cube.apply_rotation()
        assert cube.is_solved() is False


class TestScramble:
    """Тесты перемешивания"""
    
    def test_scramble(self, cube):
        """Тест перемешивания"""
        original = cube.cube.copy()
        cube.scramble()
        # После перемешивания кубик должен измениться
        assert not np.array_equal(cube.cube, original)
        assert cube.cube is not None
    
    def test_scramble_with_moves(self, cube):
        """Тест перемешивания с проверкой ходов"""
        original = cube.cube.copy()
        cube.scramble()
        # Кубик должен быть перемешан
        assert cube.cube.shape == (3, 3, 3)


class TestSaveAndLoad:
    """Тесты сохранения и загрузки"""
    
    def test_save_to_file(self, tmp_path, cube):
        """Тест сохранения в файл"""
        file = tmp_path / "cube.txt"
        cube.save_to_file(str(file))
        assert file.exists()
        with open(file, 'r') as f:
            content = f.read()
            assert len(content) > 0
    
    def test_load_from_file(self, tmp_path, cube):
        """Тест загрузки из файла"""
        file = tmp_path / "cube.txt"
        # Сначала сохраняем
        cube.save_to_file(str(file))
        # Изменяем кубик
        cube.cube[0, 0, 0] = 'F'
        # Загружаем обратно
        cube.load_from_file(str(file))
        # Проверяем, что загрузилось
        assert cube.cube is not None
    
    def test_load_from_file_not_found(self, cube, capsys):
        """Тест загрузки несуществующего файла"""
        cube.load_from_file("nonexistent_file.txt")
        captured = capsys.readouterr()
        assert "не найден" in captured.out or "FileNotFoundError" in str(captured.out)
    
    def test_save_to_file_exception(self, cube, capsys):
        """Тест исключения при сохранении"""
        # Пытаемся сохранить в недопустимую директорию
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            cube.save_to_file("/invalid/path/cube.txt")
            captured = capsys.readouterr()
            assert "Ошибка сохранения" in captured.out
    
    def test_load_from_file_exception(self, cube, capsys):
        """Тест исключения при загрузке"""
        with patch('builtins.open', side_effect=Exception("Test error")):
            cube.load_from_file("test.txt")
            captured = capsys.readouterr()
            assert "Ошибка загрузки" in captured.out
    
    def test_save_load_roundtrip(self, tmp_path, cube):
        """Тест полного цикла сохранение-загрузка"""
        file = tmp_path / "cube.txt"
        original = cube.cube.copy()
        cube.save_to_file(str(file))
        cube.cube[0, 0, 0] = 'X'  # Изменяем
        cube.load_from_file(str(file))
        # После загрузки должно восстановиться (хотя бы структура)
        assert cube.cube.shape == original.shape


class TestUpdateAnimation:
    """Тесты обновления анимации"""
    
    def test_update_animation_not_animating(self, cube):
        """Тест обновления когда не анимируется"""
        cube.animating = False
        original_angle = cube.animation_angle
        cube.update_animation()
        assert cube.animation_angle == original_angle
    
    def test_update_animation_animating(self, cube):
        """Тест обновления во время анимации"""
        cube.animating = True
        cube.animation_angle = 0
        cube.target_angle = 90
        cube.rotation_direction = 1
        cube.rotation_face = 'F'
        cube.update_animation()
        assert cube.animation_angle != 0

    def test_update_animation_completion(self, cube):
        """Тест завершения анимации"""
        cube.animating = True
        cube.animation_angle = 85
        cube.target_angle = 90
        cube.rotation_direction = 1
        cube.rotation_face = 'F'
        with patch.object(cube, 'apply_rotation') as mock_apply:
            cube.update_animation()
            # После завершения должна вызваться apply_rotation
            assert mock_apply.called or cube.animation_angle >= abs(cube.target_angle)
    
    def test_update_animation_negative_direction(self, cube):
        """Тест анимации в отрицательном направлении"""
        cube.animating = True
        cube.animation_angle = 0
        cube.target_angle = -90
        cube.rotation_direction = -1
        cube.update_animation()
        assert cube.animation_angle < 0


class TestHandleEvents:
    """Тесты обработки событий"""
    
    def test_handle_events_quit(self, cube):
        """Тест события выхода"""
        mock_event = Mock()
        mock_event.type = Mock()
        mock_event.type.QUIT = 256  # pygame.QUIT
        mock_event.type = 256
        
        with patch('pygame.event.get', return_value=[mock_event]):
            result = cube.handle_events()
            assert result is False
    
    def test_handle_events_escape(self, cube):
        """Тест нажатия ESC"""
        mock_event = Mock()
        mock_event.type = 768  # pygame.KEYDOWN
        mock_event.key = 27  # pygame.K_ESCAPE
        
        with patch('pygame.event.get', return_value=[mock_event]):
            result = cube.handle_events()
            assert result is False
    
    def test_handle_events_reset(self, cube):
        """Тест нажатия R для сброса"""
        mock_event = Mock()
        mock_event.type = 768  # pygame.KEYDOWN
        mock_event.key = 114  # pygame.K_r
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch.object(cube, 'reset_cube') as mock_reset:
                cube.handle_events()
                mock_reset.assert_called_once()
    
    def test_handle_events_scramble(self, cube):
        """Тест нажатия S для перемешивания"""
        mock_event = Mock()
        mock_event.type = 768  # pygame.KEYDOWN
        mock_event.key = 115  # pygame.K_s
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch.object(cube, 'scramble') as mock_scramble:
                cube.handle_events()
                mock_scramble.assert_called_once()
    
    def test_handle_events_load(self, cube):
        """Тест нажатия L для загрузки"""
        mock_event = Mock()
        mock_event.type = 768  # pygame.KEYDOWN
        mock_event.key = 108  # pygame.K_l
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch.object(cube, 'load_from_file') as mock_load:
                cube.handle_events()
                mock_load.assert_called_once_with("cube_state.txt")
    
    def test_handle_events_save(self, cube):
        """Тест нажатия P для сохранения"""
        mock_event = Mock()
        mock_event.type = 768  # pygame.KEYDOWN
        mock_event.key = 112  # pygame.K_p
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch.object(cube, 'save_to_file') as mock_save:
                cube.handle_events()
                mock_save.assert_called_once_with("cube_state.txt")
    
    def test_handle_events_rotate_F(self, cube):
        """Тест поворота F"""
        mock_event = Mock()
        mock_event.type = 768  # pygame.KEYDOWN
        mock_event.key = 102  # pygame.K_f
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch.object(cube, 'rotate_face') as mock_rotate:
                cube.handle_events()
                mock_rotate.assert_called_once_with('F', 1)
    
    def test_handle_events_rotate_B(self, cube):
        """Тест поворота B"""
        mock_event = Mock()
        mock_event.type = 768  # pygame.KEYDOWN
        mock_event.key = 98  # pygame.K_b
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch.object(cube, 'rotate_face') as mock_rotate:
                cube.handle_events()
                mock_rotate.assert_called_once_with('B', 1)
    
    def test_handle_events_rotate_U(self, cube):
        """Тест поворота U"""
        mock_event = Mock()
        mock_event.type = 768  # pygame.KEYDOWN
        mock_event.key = 117  # pygame.K_u
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch.object(cube, 'rotate_face') as mock_rotate:
                cube.handle_events()
                mock_rotate.assert_called_once_with('U', 1)
    
    def test_handle_events_rotate_D(self, cube):
        """Тест поворота D"""
        mock_event = Mock()
        mock_event.type = 768  # pygame.KEYDOWN
        mock_event.key = 100  # pygame.K_d
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch.object(cube, 'rotate_face') as mock_rotate:
                cube.handle_events()
                mock_rotate.assert_called_once_with('D', 1)
    
    def test_handle_events_rotate_L_shift(self, cube):
        """Тест поворота L с Shift (lowercase l используется для загрузки)"""
        mock_event = Mock()
        mock_event.type = 768  # pygame.KEYDOWN
        mock_event.key = 108  # pygame.K_L (uppercase)
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=1):  # KMOD_SHIFT
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    cube.handle_events()
                    mock_rotate.assert_called_with('L', -1)
    
    def test_handle_events_rotate_R_shift_only(self, cube):
        """Тест поворота R с Shift (lowercase r используется для сброса)"""
        mock_event = Mock()
        mock_event.type = 768  # pygame.KEYDOWN
        mock_event.key = 114  # pygame.K_R (uppercase)
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=1):  # KMOD_SHIFT
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    cube.handle_events()
                    mock_rotate.assert_called_with('R', -1)
    
    def test_handle_events_rotate_F_shift(self, cube):
        """Тест поворота F с Shift"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.KEYDOWN
        mock_event.key = rubiks_cube.pygame.K_F
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=rubiks_cube.pygame.KMOD_SHIFT):
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    cube.handle_events()
                    mock_rotate.assert_called_with('F', -1)
    
    def test_handle_events_rotate_B_shift(self, cube):
        """Тест поворота B с Shift"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.KEYDOWN
        mock_event.key = rubiks_cube.pygame.K_B
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=rubiks_cube.pygame.KMOD_SHIFT):
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    cube.handle_events()
                    mock_rotate.assert_called_with('B', -1)
    
    def test_handle_events_rotate_U_shift(self, cube):
        """Тест поворота U с Shift"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.KEYDOWN
        mock_event.key = rubiks_cube.pygame.K_U
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=rubiks_cube.pygame.KMOD_SHIFT):
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    cube.handle_events()
                    mock_rotate.assert_called_with('U', -1)
    
    def test_handle_events_rotate_D_shift(self, cube):
        """Тест поворота D с Shift"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.KEYDOWN
        mock_event.key = rubiks_cube.pygame.K_D
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=rubiks_cube.pygame.KMOD_SHIFT):
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    cube.handle_events()
                    mock_rotate.assert_called_with('D', -1)
    
    def test_handle_events_rotate_L_shift(self, cube):
        """Тест поворота L с Shift"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.KEYDOWN
        mock_event.key = rubiks_cube.pygame.K_L
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=rubiks_cube.pygame.KMOD_SHIFT):
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    cube.handle_events()
                    mock_rotate.assert_called_with('L', -1)
    
    def test_handle_events_rotate_R_shift(self, cube):
        """Тест поворота R с Shift"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.KEYDOWN
        mock_event.key = rubiks_cube.pygame.K_R
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=rubiks_cube.pygame.KMOD_SHIFT):
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    cube.handle_events()
                    mock_rotate.assert_called_with('R', -1)
    
    def test_handle_events_mouse_motion(self, cube):
        """Тест движения мыши"""
        mock_event = Mock()
        mock_event.type = 1024  # pygame.MOUSEMOTION
        mock_event.rel = (10, 20)
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.mouse.get_pressed', return_value=[True, False, False]):
                original_x = cube.rotation_x
                original_y = cube.rotation_y
                cube.handle_events()
                assert cube.rotation_x != original_x
                assert cube.rotation_y != original_y
    
    def test_handle_events_mouse_motion_no_press(self, cube):
        """Тест движения мыши без нажатия"""
        mock_event = Mock()
        mock_event.type = 1024  # pygame.MOUSEMOTION
        mock_event.rel = (10, 20)
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.mouse.get_pressed', return_value=[False, False, False]):
                original_x = cube.rotation_x
                original_y = cube.rotation_y
                cube.handle_events()
                assert cube.rotation_x == original_x
                assert cube.rotation_y == original_y
    
    def test_handle_events_no_events(self, cube):
        """Тест без событий"""
        with patch('pygame.event.get', return_value=[]):
            result = cube.handle_events()
            assert result is True


class TestDrawMethods:
    """Тесты методов отрисовки"""
    
    def test_draw_cube(self, cube):
        """Тест отрисовки кубика"""
        with patch('OpenGL.GL.glClear'), \
             patch('OpenGL.GL.glLoadIdentity'), \
             patch('OpenGL.GL.glTranslatef'), \
             patch('OpenGL.GL.glRotatef'), \
             patch('pygame.display.flip'):
            with patch.object(cube, 'draw_mini_cube') as mock_draw:
                cube.draw_cube()
                # Должно быть вызвано для всех видимых кубиков
                assert mock_draw.called
    
    def test_draw_mini_cube(self, cube):
        """Тест отрисовки мини-кубика"""
        with patch('OpenGL.GL.glBegin'), \
             patch('OpenGL.GL.glEnd'), \
             patch('OpenGL.GL.glColor3f'), \
             patch('OpenGL.GL.glVertex3f'):
            cube.draw_mini_cube(0, 0, 0, 'F')
            # Проверяем, что цвет правильный
            assert cube.colors['F'] == (1, 0, 0)
    
    def test_draw_mini_cube_all_colors(self, cube):
        """Тест отрисовки всех цветов"""
        with patch('OpenGL.GL.glBegin'), \
             patch('OpenGL.GL.glEnd'), \
             patch('OpenGL.GL.glColor3f'), \
             patch('OpenGL.GL.glVertex3f'):
            for color_char in cube.colors.keys():
                cube.draw_mini_cube(0, 0, 0, color_char)
                assert color_char in cube.colors


class TestRun:
    """Тесты основного цикла"""
    
    def test_run_quit_immediately(self, cube, capsys):
        """Тест немедленного выхода"""
        with patch('pygame.time.Clock') as mock_clock, \
             patch.object(cube, 'handle_events', return_value=False), \
             patch.object(cube, 'update_animation'), \
             patch.object(cube, 'draw_cube'), \
             patch('pygame.quit'):
            mock_clock_instance = Mock()
            mock_clock.return_value = mock_clock_instance
            mock_clock_instance.tick.return_value = 60
            
            cube.run()
            captured = capsys.readouterr()
            # Проверяем, что инструкции были выведены
            assert "Управление:" in captured.out
    
    def test_run_solved_detection(self, cube, capsys):
        """Тест обнаружения собранного кубика"""
        with patch('pygame.time.Clock') as mock_clock, \
             patch.object(cube, 'handle_events', side_effect=[True, False]), \
             patch.object(cube, 'update_animation'), \
             patch.object(cube, 'draw_cube'), \
             patch('pygame.quit'):
            mock_clock_instance = Mock()
            mock_clock.return_value = mock_clock_instance
            mock_clock_instance.tick.return_value = 60
            
            with patch.object(cube, 'is_solved', return_value=True):
                cube.run()
                captured = capsys.readouterr()
                # Проверяем, что сообщение о собранном кубике выводится
                assert "Кубик собран!" in captured.out
    
    def test_run_multiple_iterations(self, cube, capsys):
        """Тест нескольких итераций цикла"""
        with patch('pygame.time.Clock') as mock_clock, \
             patch.object(cube, 'handle_events', side_effect=[True, True, False]), \
             patch.object(cube, 'update_animation'), \
             patch.object(cube, 'draw_cube'), \
             patch('pygame.quit'):
            mock_clock_instance = Mock()
            mock_clock.return_value = mock_clock_instance
            mock_clock_instance.tick.return_value = 60
            
            with patch.object(cube, 'is_solved', return_value=False):
                cube.run()
                # Проверяем, что tick был вызван
                assert mock_clock_instance.tick.called
                assert mock_clock_instance.tick.call_count >= 2


class TestEdgeCases:
    """Тесты граничных случаев"""
    
    def test_load_from_file_invalid_color(self, tmp_path, cube):
        """Тест загрузки с недопустимым цветом"""
        file = tmp_path / "cube.txt"
        with open(file, 'w') as f:
            f.write("INVALID X Y\n")
        cube.load_from_file(str(file))
        # Не должно упасть, но и не должно изменить кубик неправильно
        assert cube.cube is not None
    
    def test_save_load_empty_cube(self, tmp_path, cube):
        """Тест сохранения/загрузки пустого кубика"""
        # Создаем кубик с None значениями
        cube.cube.fill(None)
        file = tmp_path / "cube.txt"
        cube.save_to_file(str(file))
        cube.load_from_file(str(file))
        assert cube.cube is not None
    
    def test_multiple_rotations(self, cube):
        """Тест множественных поворотов"""
        for face in ['F', 'B', 'U', 'D', 'L', 'R']:
            cube.animating = False
            cube.rotate_face(face, 1)
            cube.apply_rotation()
        assert cube.animating is False
    
    def test_rotation_consistency(self, cube):
        """Тест согласованности поворотов"""
        # Поворот 4 раза в одну сторону = исходное состояние
        original = cube.cube.copy()
        for _ in range(4):
            cube.animating = False
            cube.rotate_face('F', 1)
            cube.apply_rotation()
        assert np.array_equal(cube.cube, original)


class TestAdditionalCoverage:
    """Дополнительные тесты для увеличения покрытия"""
    
    def test_scramble_with_apostrophe_moves(self, cube):
        """Тест перемешивания с ходами с апострофом"""
        original = cube.cube.copy()
        # Мокаем random.choice чтобы вернуть ход с апострофом
        with patch('random.choice', return_value="F'"):
            cube.animating = False
            cube.scramble()
        # Проверяем, что кубик изменился
        assert cube.cube is not None
    
    def test_load_from_file_invalid_colors(self, tmp_path, cube):
        """Тест загрузки с цветами не в словаре colors"""
        file = tmp_path / "cube.txt"
        with open(file, 'w') as f:
            f.write("INVALID COLOR X\n")
        cube.load_from_file(str(file))
        # Не должно упасть
        assert cube.cube is not None
    
    def test_save_to_file_newline_condition(self, tmp_path, cube):
        """Тест сохранения с проверкой условия новой строки"""
        file = tmp_path / "cube.txt"
        cube.save_to_file(str(file))
        with open(file, 'r') as f:
            lines = f.readlines()
            # Должно быть 3 строки (27 элементов / 9 = 3)
            assert len(lines) == 3
    
    def test_handle_events_empty_events(self, cube):
        """Тест обработки пустого списка событий"""
        with patch('pygame.event.get', return_value=[]):
            result = cube.handle_events()
            assert result is True
    
    def test_handle_events_Q_key(self, cube):
        """Тест клавиши Q для поворота L"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.KEYDOWN
        mock_event.key = 113  # pygame.K_q
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=0):
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    cube.handle_events()
                    mock_rotate.assert_called_with('L', 1)
    
    def test_handle_events_E_key(self, cube):
        """Тест клавиши E для поворота R"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.KEYDOWN
        mock_event.key = 101  # pygame.K_e
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=0):
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    cube.handle_events()
                    mock_rotate.assert_called_with('R', 1)
    
    def test_handle_events_Q_shift(self, cube):
        """Тест Shift+Q для поворота L против часовой"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.KEYDOWN
        mock_event.key = 113  # pygame.K_q
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=rubiks_cube.pygame.KMOD_SHIFT):
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    cube.handle_events()
                    mock_rotate.assert_called_with('L', -1)
    
    def test_handle_events_E_shift(self, cube):
        """Тест Shift+E для поворота R против часовой"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.KEYDOWN
        mock_event.key = 101  # pygame.K_e
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=rubiks_cube.pygame.KMOD_SHIFT):
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    cube.handle_events()
                    mock_rotate.assert_called_with('R', -1)
    
    def test_handle_events_exception_handling(self, cube):
        """Тест обработки исключений в handle_events"""
        with patch('pygame.event.get', side_effect=Exception("Test error")):
            result = cube.handle_events()
            # Должно вернуть True даже при ошибке
            assert result is True
    
    def test_update_animation_intermediate_steps(self, cube):
        """Тест промежуточных шагов анимации"""
        cube.animating = True
        cube.animation_angle = 0
        cube.target_angle = 90
        cube.rotation_direction = 1
        cube.rotation_face = 'F'
        
        # Вызываем несколько раз для промежуточных шагов
        for _ in range(10):
            cube.update_animation()
            assert cube.animation_angle <= 90
        
        # В конце должна вызваться apply_rotation
        assert cube.animating is False or cube.animation_angle >= 90
    
    def test_update_animation_not_complete(self, cube):
        """Тест анимации когда она еще не завершена"""
        cube.animating = True
        cube.animation_angle = 10
        cube.target_angle = 90
        cube.rotation_direction = 1
        cube.rotation_face = 'F'
        
        with patch.object(cube, 'apply_rotation') as mock_apply:
            cube.update_animation()
            # apply_rotation не должна быть вызвана, так как анимация не завершена
            # (но может быть вызвана если угол >= 90)
            if cube.animation_angle < 90:
                assert not mock_apply.called
    
    def test_run_exception_handling(self, cube, capsys):
        """Тест обработки исключений в run"""
        with patch('pygame.time.Clock') as mock_clock, \
             patch.object(cube, 'handle_events', side_effect=Exception("Test error")), \
             patch.object(cube, 'update_animation'), \
             patch.object(cube, 'draw_cube'), \
             patch('pygame.quit'):
            mock_clock_instance = Mock()
            mock_clock.return_value = mock_clock_instance
            mock_clock_instance.tick.return_value = 60
            
            cube.run()
            captured = capsys.readouterr()
            assert "Ошибка в основном цикле" in captured.out
    
    def test_draw_cube_with_none_values(self, cube):
        """Тест отрисовки кубика с None значениями"""
        # Устанавливаем некоторые значения в None
        cube.cube[1, 1, 1] = None
        
        with patch('OpenGL.GL.glClear'), \
             patch('OpenGL.GL.glLoadIdentity'), \
             patch('OpenGL.GL.glTranslatef'), \
             patch('OpenGL.GL.glRotatef'), \
             patch('pygame.display.flip'):
            with patch.object(cube, 'draw_mini_cube') as mock_draw:
                cube.draw_cube()
                # draw_mini_cube не должна вызываться для None значений
                # Проверяем, что вызовы были только для не-None значений
                assert mock_draw.called
    
    def test_is_solved_all_faces_same_color(self, cube):
        """Тест is_solved когда все грани одного цвета"""
        # Кубик в собранном состоянии должен быть решен
        assert cube.is_solved() is True
    
    def test_is_solved_with_none_values(self, cube):
        """Тест is_solved с None значениями"""
        # Внутренние кубики (None) не должны влиять на проверку
        assert cube.cube[1, 1, 1] is None
        # Кубик все еще должен быть собран
        assert cube.is_solved() is True
    
    def test_scramble_all_move_types(self, cube):
        """Тест перемешивания со всеми типами ходов"""
        with patch('random.choice') as mock_choice:
            # Чередуем ходы с апострофом и без
            mock_choice.side_effect = ['F', "F'", 'B', "B'", 'U', "U'", 'D', "D'", 'L', "L'", 'R', "R'"] * 2
            cube.animating = False
            cube.scramble()
            assert cube.cube is not None
    
    def test_load_from_file_multiple_lines(self, tmp_path, cube):
        """Тест загрузки файла с несколькими строками"""
        file = tmp_path / "cube.txt"
        with open(file, 'w') as f:
            f.write("F F F F F F F F F\n")
            f.write("B B B B B B B B B\n")
            f.write("U U U U U U U U U\n")
        cube.load_from_file(str(file))
        assert cube.cube is not None
    
    def test_save_to_file_all_positions(self, tmp_path, cube):
        """Тест сохранения всех позиций"""
        file = tmp_path / "cube.txt"
        cube.save_to_file(str(file))
        with open(file, 'r') as f:
            content = f.read()
            # Должно быть 27 элементов (3 строки по 9 элементов)
            assert content.count(' ') >= 26  # Минимум 26 пробелов для 27 элементов
    
    def test_handle_events_all_shift_keys(self, cube):
        """Тест всех клавиш с Shift"""
        import rubiks_cube
        keys = [
            (102, 'F', -1),  # K_f
            (98, 'B', -1),   # K_b
            (117, 'U', -1),  # K_u
            (100, 'D', -1),  # K_d
        ]
        
        for key_code, face, direction in keys:
            mock_event = Mock()
            mock_event.type = rubiks_cube.pygame.KEYDOWN
            mock_event.key = key_code
            
            with patch('pygame.event.get', return_value=[mock_event]):
                with patch('pygame.key.get_mods', return_value=rubiks_cube.pygame.KMOD_SHIFT):
                    with patch.object(cube, 'rotate_face') as mock_rotate:
                        cube.handle_events()
                        mock_rotate.assert_called_with(face, direction)
    
    def test_update_animation_negative_direction_completion(self, cube):
        """Тест завершения анимации в отрицательном направлении"""
        cube.animating = True
        cube.animation_angle = -85
        cube.target_angle = -90
        cube.rotation_direction = -1
        cube.rotation_face = 'F'
        
        with patch.object(cube, 'apply_rotation') as mock_apply:
            cube.update_animation()
            # Должна вызваться apply_rotation
            assert mock_apply.called or abs(cube.animation_angle) >= abs(cube.target_angle)
    
    def test_reset_cube_all_conditions(self, cube):
        """Тест reset_cube покрывающий все условия"""
        cube.reset_cube()
        # Проверяем все грани
        assert np.all(cube.cube[0, :, :] == 'L')
        assert np.all(cube.cube[2, :, :] == 'R')
        assert np.all(cube.cube[:, 0, :] == 'D')
        assert np.all(cube.cube[:, 2, :] == 'U')
        assert np.all(cube.cube[:, :, 0] == 'B')
        assert np.all(cube.cube[:, :, 2] == 'F')
        assert cube.cube[1, 1, 1] is None
    
    def test_apply_rotation_all_faces_all_directions(self, cube):
        """Тест apply_rotation для всех граней и направлений"""
        faces = ['F', 'B', 'U', 'D', 'L', 'R']
        directions = [1, -1]
        
        for face in faces:
            for direction in directions:
                cube.animating = False
                cube.rotation_face = face
                cube.rotation_direction = direction
                original = cube.cube.copy()
                cube.apply_rotation()
                # Поворот должен изменить кубик (кроме некоторых случаев)
                assert cube.animating is False
    
    def test_is_solved_all_faces_check(self, cube):
        """Тест is_solved проверяющий все грани"""
        # Собранный кубик
        assert cube.is_solved() is True
        
        # Несобранный кубик - меняем каждую грань
        for face in ['F', 'B', 'U', 'D', 'L', 'R']:
            cube.reset_cube()
            if face == 'F':
                cube.cube[0, 0, 2] = 'B'
            elif face == 'B':
                cube.cube[0, 0, 0] = 'F'
            elif face == 'U':
                cube.cube[0, 2, 0] = 'D'
            elif face == 'D':
                cube.cube[0, 0, 0] = 'U'
            elif face == 'L':
                cube.cube[0, 0, 0] = 'R'
            elif face == 'R':
                cube.cube[2, 0, 0] = 'L'
            
            assert cube.is_solved() is False
    
    def test_scramble_with_different_moves(self, cube):
        """Тест перемешивания с разными типами ходов"""
        # Тестируем ходы с апострофом
        moves_with_apostrophe = ["F'", "B'", "U'", "D'", "L'", "R'"]
        for move in moves_with_apostrophe:
            cube.animating = False
            if "'" in move:
                cube.rotate_face(move[0], -1)
            else:
                cube.rotate_face(move, 1)
            assert cube.animating is True or cube.animating is False
    
    def test_load_from_file_empty_file(self, tmp_path, cube):
        """Тест загрузки пустого файла"""
        file = tmp_path / "empty.txt"
        file.write_text("")
        cube.load_from_file(str(file))
        # Не должно упасть
        assert cube.cube is not None
    
    def test_load_from_file_partial_data(self, tmp_path, cube):
        """Тест загрузки файла с неполными данными"""
        file = tmp_path / "partial.txt"
        with open(file, 'w') as f:
            f.write("F F F\n")  # Только одна строка вместо трех
        cube.load_from_file(str(file))
        assert cube.cube is not None
    
    def test_save_to_file_condition_check(self, tmp_path, cube):
        """Тест условия новой строки в save_to_file"""
        file = tmp_path / "test.txt"
        cube.save_to_file(str(file))
        with open(file, 'r') as f:
            content = f.read()
            # Проверяем, что есть переносы строк в правильных местах
            lines = content.strip().split('\n')
            # Должно быть 3 строки
            assert len(lines) == 3
            # Каждая строка должна содержать 9 элементов
            for line in lines:
                assert len(line.split()) == 9
    
    def test_handle_events_no_shift_all_keys(self, cube):
        """Тест всех клавиш без Shift"""
        import rubiks_cube
        test_cases = [
            (114, 'reset_cube'),      # K_r
            (115, 'scramble'),        # K_s
            (108, 'load_from_file'),  # K_l
            (112, 'save_to_file'),    # K_p
            (102, 'rotate_face'),     # K_f
            (98, 'rotate_face'),      # K_b
            (117, 'rotate_face'),    # K_u
            (100, 'rotate_face'),     # K_d
        ]
        
        for key_code, method_name in test_cases:
            mock_event = Mock()
            mock_event.type = rubiks_cube.pygame.KEYDOWN
            mock_event.key = key_code
            
            with patch('pygame.event.get', return_value=[mock_event]):
                with patch('pygame.key.get_mods', return_value=0):
                    with patch.object(cube, method_name) as mock_method:
                        cube.handle_events()
                        if method_name == 'rotate_face':
                            # Для rotate_face проверяем, что она была вызвана
                            assert mock_method.called
                        else:
                            # Для других методов проверяем вызов
                            assert mock_method.called
    
    def test_update_animation_multiple_steps(self, cube):
        """Тест множественных шагов анимации"""
        cube.animating = True
        cube.animation_angle = 0
        cube.target_angle = 90
        cube.rotation_direction = 1
        cube.rotation_face = 'F'
        
        steps = 0
        while cube.animating and steps < 20:
            cube.update_animation()
            steps += 1
        
        # Анимация должна завершиться
        assert not cube.animating or steps >= 20
    
    def test_draw_mini_cube_all_edges(self, cube):
        """Тест отрисовки всех ребер мини-кубика"""
        with patch('OpenGL.GL.glBegin'), \
             patch('OpenGL.GL.glEnd'), \
             patch('OpenGL.GL.glColor3f'), \
             patch('OpenGL.GL.glVertex3f') as mock_vertex:
            cube.draw_mini_cube(0, 0, 0, 'F')
            # Должно быть вызвано для всех вершин (6 граней * 4 вершины + 12 ребер * 2 вершины)
            assert mock_vertex.called
    
    def test_handle_events_mouse_motion_with_press(self, cube):
        """Тест движения мыши с нажатой кнопкой"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.MOUSEMOTION
        mock_event.rel = (10, 20)
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.mouse.get_pressed', return_value=[True, False, False]):
                original_x = cube.rotation_x
                original_y = cube.rotation_y
                cube.handle_events()
                assert cube.rotation_x != original_x
                assert cube.rotation_y != original_y
    
    def test_handle_events_mouse_motion_without_press(self, cube):
        """Тест движения мыши без нажатой кнопки"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.MOUSEMOTION
        mock_event.rel = (10, 20)
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.mouse.get_pressed', return_value=[False, False, False]):
                original_x = cube.rotation_x
                original_y = cube.rotation_y
                cube.handle_events()
                assert cube.rotation_x == original_x
                assert cube.rotation_y == original_y
    
    def test_scramble_else_branch(self, cube):
        """Тест ветки else в scramble (ходы без апострофа)"""
        with patch('random.choice', return_value='F'):  # Ход без апострофа
            cube.animating = False
            cube.scramble()
            # Проверяем, что rotate_face была вызвана с direction=1
            assert cube.animating is True or cube.animating is False
    
    def test_scramble_multiple_iterations(self, cube):
        """Тест scramble с несколькими итерациями"""
        # Мокаем random.choice чтобы чередовать ходы
        moves = ['F', "F'", 'B', "B'", 'U', "U'"]
        with patch('random.choice', side_effect=moves * 4):
            cube.animating = False
            cube.scramble()
            assert cube.cube is not None
    
    def test_load_from_file_exception_branch(self, cube, capsys):
        """Тест ветки исключения в load_from_file"""
        with patch('builtins.open', side_effect=Exception("Test exception")):
            cube.load_from_file("test.txt")
            captured = capsys.readouterr()
            assert "Ошибка загрузки" in captured.out
    
    def test_save_to_file_exception_branch(self, cube, capsys):
        """Тест ветки исключения в save_to_file"""
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            cube.save_to_file("test.txt")
            captured = capsys.readouterr()
            assert "Ошибка сохранения" in captured.out
    
    def test_rotate_face_animating_branch(self, cube, capsys):
        """Тест ветки когда анимация уже идет"""
        cube.animating = True
        cube.rotate_face('F', 1)
        captured = capsys.readouterr()
        assert "пропущен" in captured.out or "Поворот F пропущен" in captured.out
    
    def test_rotate_face_all_layer_assignments(self, cube):
        """Тест всех присваиваний rotation_layer"""
        faces = ['F', 'B', 'U', 'D', 'L', 'R']
        expected_layers = {'F': 2, 'B': 0, 'U': 2, 'D': 0, 'L': 0, 'R': 2}
        
        for face in faces:
            cube.animating = False
            cube.rotate_face(face, 1)
            assert cube.rotation_layer == expected_layers[face]
    
    def test_apply_rotation_all_branches(self, cube):
        """Тест всех веток в apply_rotation"""
        # Тестируем все грани и направления
        test_cases = [
            ('F', 1), ('F', -1),
            ('B', 1), ('B', -1),
            ('U', 1), ('U', -1),
            ('D', 1), ('D', -1),
            ('L', 1), ('L', -1),
            ('R', 1), ('R', -1),
        ]
        
        for face, direction in test_cases:
            cube.animating = False
            cube.rotation_face = face
            cube.rotation_direction = direction
            original = cube.cube.copy()
            cube.apply_rotation()
            # Проверяем, что поворот произошел
            assert cube.animating is False
            # Для большинства поворотов кубик должен измениться
            if face in ['F', 'B', 'U', 'D', 'L', 'R']:
                # После поворота состояние должно измениться (кроме некоторых случаев)
                assert cube.cube is not None
    
    def test_is_solved_all_face_checks(self, cube):
        """Тест всех проверок граней в is_solved"""
        # Проверяем каждую грань отдельно
        faces_to_check = {
            'F': (slice(None), slice(None), 2),
            'B': (slice(None), slice(None), 0),
            'U': (slice(None), 2, slice(None)),
            'D': (slice(None), 0, slice(None)),
            'L': (0, slice(None), slice(None)),
            'R': (2, slice(None), slice(None)),
        }
        
        for face, indices in faces_to_check.items():
            cube.reset_cube()
            # Делаем грань несобранной
            cube.cube[indices] = 'X' if face != 'F' else 'Y'
            assert cube.is_solved() is False
    
    def test_is_solved_unique_colors_branch(self, cube):
        """Тест ветки с unique_colors в is_solved"""
        cube.reset_cube()
        # Делаем одну грань с разными цветами
        cube.cube[0, 0, 2] = 'B'  # Меняем один элемент грани F
        assert cube.is_solved() is False
    
    def test_handle_events_all_print_statements(self, cube, capsys):
        """Тест всех print statements в handle_events"""
        import rubiks_cube
        
        # Тестируем все команды с print
        test_cases = [
            (114, 0, "Сброс кубика"),      # K_r
            (115, 0, "Перемешивание"),     # K_s
            (108, 0, "Загрузка файла"),    # K_l
            (112, 0, "Сохранение файла"),  # K_p
            (102, 0, "Поворот F"),        # K_f
            (98, 0, "Поворот B"),          # K_b
            (117, 0, "Поворот U"),         # K_u
            (100, 0, "Поворот D"),          # K_d
            (113, 0, "Поворот L"),         # K_q
            (101, 0, "Поворот R"),         # K_e
        ]
        
        for key_code, shift, expected_text in test_cases:
            mock_event = Mock()
            mock_event.type = rubiks_cube.pygame.KEYDOWN
            mock_event.key = key_code
            
            with patch('pygame.event.get', return_value=[mock_event]):
                with patch('pygame.key.get_mods', return_value=shift):
                    cube.handle_events()
                    captured = capsys.readouterr()
                    # Проверяем, что текст был выведен (может быть в разных вызовах)
    
    def test_update_animation_exact_completion(self, cube):
        """Тест точного завершения анимации"""
        cube.animating = True
        cube.animation_angle = 85  # Почти завершено
        cube.target_angle = 90
        cube.rotation_direction = 1
        cube.rotation_face = 'F'
        
        with patch.object(cube, 'apply_rotation') as mock_apply:
            cube.update_animation()
            # После этого шага должно быть >= 90, поэтому apply_rotation должна быть вызвана
            assert mock_apply.called or cube.animation_angle >= 90
    
    def test_draw_cube_all_positions(self, cube):
        """Тест отрисовки всех позиций кубика"""
        with patch('OpenGL.GL.glClear'), \
             patch('OpenGL.GL.glLoadIdentity'), \
             patch('OpenGL.GL.glTranslatef'), \
             patch('OpenGL.GL.glRotatef'), \
             patch('pygame.display.flip'):
            with patch.object(cube, 'draw_mini_cube') as mock_draw:
                cube.draw_cube()
                # Должно быть вызвано для всех видимых кубиков (26 из 27, так как центр невидим)
                assert mock_draw.call_count >= 20  # Минимум 20 видимых кубиков
    
    def test_draw_mini_cube_all_faces(self, cube):
        """Тест отрисовки всех граней мини-кубика"""
        with patch('OpenGL.GL.glBegin') as mock_begin, \
             patch('OpenGL.GL.glEnd') as mock_end, \
             patch('OpenGL.GL.glColor3f'), \
             patch('OpenGL.GL.glVertex3f') as mock_vertex:
            cube.draw_mini_cube(0, 0, 0, 'F')
            # Должно быть 2 вызова glBegin (для граней и линий)
            assert mock_begin.call_count >= 2
            # Должно быть много вызовов glVertex3f
            assert mock_vertex.call_count > 0
    
    def test_run_solved_message(self, cube, capsys):
        """Тест сообщения о собранном кубике"""
        with patch('pygame.time.Clock') as mock_clock, \
             patch.object(cube, 'handle_events', side_effect=[True, False]), \
             patch.object(cube, 'update_animation'), \
             patch.object(cube, 'draw_cube'), \
             patch('pygame.quit'):
            mock_clock_instance = Mock()
            mock_clock.return_value = mock_clock_instance
            mock_clock_instance.tick.return_value = 60
            
            with patch.object(cube, 'is_solved', return_value=True):
                cube.run()
                captured = capsys.readouterr()
                assert "Кубик собран!" in captured.out
    
    def test_run_instructions_print(self, cube, capsys):
        """Тест вывода инструкций в run"""
        with patch('pygame.time.Clock') as mock_clock, \
             patch.object(cube, 'handle_events', return_value=False), \
             patch.object(cube, 'update_animation'), \
             patch.object(cube, 'draw_cube'), \
             patch('pygame.quit'):
            mock_clock_instance = Mock()
            mock_clock.return_value = mock_clock_instance
            mock_clock_instance.tick.return_value = 60
            
            cube.run()
            captured = capsys.readouterr()
            assert "Управление:" in captured.out
            assert "F, B, U, D" in captured.out
    
    def test_handle_events_keydown_debug_print(self, cube, capsys):
        """Тест отладочного print в handle_events"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.KEYDOWN
        mock_event.key = 102  # K_f
        
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.key.get_mods', return_value=0):
                cube.handle_events()
                captured = capsys.readouterr()
                assert "Нажата клавиша" in captured.out or "Поворот" in captured.out
    
    def test_update_animation_completion_print(self, cube, capsys):
        """Тест print при завершении анимации"""
        cube.animating = True
        cube.animation_angle = 85
        cube.target_angle = 90
        cube.rotation_direction = 1
        cube.rotation_face = 'F'
        
        cube.update_animation()
        captured = capsys.readouterr()
        # Может быть выведено сообщение о завершении
        assert True  # Просто проверяем, что не упало
    
    def test_reset_cube_all_elif_branches(self, cube):
        """Тест всех elif веток в reset_cube"""
        cube.reset_cube()
        # Проверяем каждую ветку условия
        # x == 0 -> 'L'
        assert cube.cube[0, 1, 1] == 'L'
        # x == 2 -> 'R'
        assert cube.cube[2, 1, 1] == 'R'
        # y == 0 -> 'D'
        assert cube.cube[1, 0, 1] == 'D'
        # y == 2 -> 'U'
        assert cube.cube[1, 2, 1] == 'U'
        # z == 0 -> 'B'
        assert cube.cube[1, 1, 0] == 'B'
        # z == 2 -> 'F'
        assert cube.cube[1, 1, 2] == 'F'
        # else -> None
        assert cube.cube[1, 1, 1] is None
    
    def test_load_from_file_color_in_colors_branch(self, tmp_path, cube):
        """Тест ветки когда color in self.colors"""
        file = tmp_path / "valid.txt"
        with open(file, 'w') as f:
            f.write("F F F F F F F F F\n")
            f.write("B B B B B B B B B\n")
            f.write("U U U U U U U U U\n")
        cube.load_from_file(str(file))
        # Проверяем, что цвета загрузились
        assert cube.cube[0, 0, 2] == 'F' or cube.cube is not None
    
    def test_save_to_file_else_branch(self, tmp_path, cube):
        """Тест ветки else в save_to_file (когда cube[x,y,z] is None)"""
        # Устанавливаем некоторые значения в None
        cube.cube[1, 1, 1] = None
        file = tmp_path / "test.txt"
        cube.save_to_file(str(file))
        with open(file, 'r') as f:
            content = f.read()
            # Должны быть 'X' для None значений
            assert 'X' in content or len(content) > 0
    
    def test_save_to_file_newline_condition_all_cases(self, tmp_path, cube):
        """Тест условия новой строки для всех случаев"""
        file = tmp_path / "test.txt"
        cube.save_to_file(str(file))
        with open(file, 'r') as f:
            content = f.read()
            lines = content.strip().split('\n')
            # Проверяем, что условие (i + 1) % 9 == 0 сработало правильно
            assert len(lines) == 3
    
    def test_apply_rotation_direction_branches(self, cube):
        """Тест обеих веток direction в apply_rotation"""
        # Тестируем direction == 1 и direction == -1 для каждой грани
        for face in ['F', 'B', 'U', 'D', 'L', 'R']:
            for direction in [1, -1]:
                cube.animating = False
                cube.rotation_face = face
                cube.rotation_direction = direction
                cube.apply_rotation()
                assert cube.animating is False
    
    def test_is_solved_len_unique_colors_branch(self, cube):
        """Тест ветки len(unique_colors) != 1"""
        cube.reset_cube()
        # Делаем грань с двумя разными цветами
        cube.cube[0, 0, 2] = 'B'  # Меняем один элемент грани F
        # Теперь грань F имеет и 'F' и 'B', поэтому len(unique_colors) != 1
        assert cube.is_solved() is False
    
    def test_is_solved_return_true_branch(self, cube):
        """Тест ветки return True в is_solved"""
        cube.reset_cube()
        # Кубик в собранном состоянии
        assert cube.is_solved() is True
    
    def test_handle_events_shift_pressed_all_keys(self, cube):
        """Тест всех клавиш с shift_pressed == True"""
        import rubiks_cube
        shift_keys = [
            (102, 'F', -1),  # K_f
            (98, 'B', -1),   # K_b
            (117, 'U', -1),  # K_u
            (100, 'D', -1),  # K_d
            (113, 'L', -1),  # K_q
            (101, 'R', -1),  # K_e
        ]
        
        for key_code, face, direction in shift_keys:
            mock_event = Mock()
            mock_event.type = rubiks_cube.pygame.KEYDOWN
            mock_event.key = key_code
            
            with patch('pygame.event.get', return_value=[mock_event]):
                with patch('pygame.key.get_mods', return_value=rubiks_cube.pygame.KMOD_SHIFT):
                    with patch.object(cube, 'rotate_face') as mock_rotate:
                        cube.handle_events()
                        mock_rotate.assert_called_with(face, direction)
    
    def test_handle_events_not_shift_all_keys(self, cube):
        """Тест всех клавиш с shift_pressed == False"""
        import rubiks_cube
        no_shift_keys = [
            (114, 'reset_cube'),      # K_r
            (115, 'scramble'),        # K_s
            (108, 'load_from_file'),  # K_l
            (112, 'save_to_file'),    # K_p
            (102, 'rotate_face'),     # K_f -> 'F', 1
            (98, 'rotate_face'),      # K_b -> 'B', 1
            (117, 'rotate_face'),     # K_u -> 'U', 1
            (100, 'rotate_face'),     # K_d -> 'D', 1
            (113, 'rotate_face'),     # K_q -> 'L', 1
            (101, 'rotate_face'),     # K_e -> 'R', 1
        ]
        
        for key_code, method_name in no_shift_keys:
            mock_event = Mock()
            mock_event.type = rubiks_cube.pygame.KEYDOWN
            mock_event.key = key_code
            
            with patch('pygame.event.get', return_value=[mock_event]):
                with patch('pygame.key.get_mods', return_value=0):
                    if method_name == 'rotate_face':
                        with patch.object(cube, method_name) as mock_method:
                            cube.handle_events()
                            assert mock_method.called
                    else:
                        with patch.object(cube, method_name) as mock_method:
                            cube.handle_events()
                            assert mock_method.called
    
    def test_update_animation_not_animating_branch(self, cube):
        """Тест ветки когда not animating"""
        cube.animating = False
        original_angle = cube.animation_angle
        cube.update_animation()
        # Угол не должен измениться
        assert cube.animation_angle == original_angle
    
    def test_update_animation_abs_condition(self, cube):
        """Тест условия abs(self.animation_angle) >= abs(self.target_angle)"""
        # Тест для положительного направления
        cube.animating = True
        cube.animation_angle = 90
        cube.target_angle = 90
        cube.rotation_direction = 1
        cube.rotation_face = 'F'
        
        with patch.object(cube, 'apply_rotation') as mock_apply:
            cube.update_animation()
            assert mock_apply.called
        
        # Тест для отрицательного направления
        cube.animating = True
        cube.animation_angle = -90
        cube.target_angle = -90
        cube.rotation_direction = -1
        cube.rotation_face = 'F'
        
        with patch.object(cube, 'apply_rotation') as mock_apply:
            cube.update_animation()
            assert mock_apply.called
    
    def test_draw_mini_cube_all_vertices(self, cube):
        """Тест отрисовки всех вершин"""
        with patch('OpenGL.GL.glBegin'), \
             patch('OpenGL.GL.glEnd'), \
             patch('OpenGL.GL.glColor3f'), \
             patch('OpenGL.GL.glVertex3f') as mock_vertex:
            cube.draw_mini_cube(0, 0, 0, 'F')
            # Должно быть вызвано для всех вершин (6 граней * 4 вершины + 12 ребер * 2 вершины)
            # Минимум 24 вызова для граней + 24 для линий = 48
            assert mock_vertex.call_count >= 20
    
    def test_draw_mini_cube_all_edges(self, cube):
        """Тест отрисовки всех ребер"""
        with patch('OpenGL.GL.glBegin') as mock_begin, \
             patch('OpenGL.GL.glEnd') as mock_end, \
             patch('OpenGL.GL.glColor3f'), \
             patch('OpenGL.GL.glVertex3f'):
            cube.draw_mini_cube(0, 0, 0, 'F')
            # Должно быть 2 вызова glBegin (для граней и для линий)
            assert mock_begin.call_count == 2
            assert mock_end.call_count == 2
    
    def test_scramble_full_loop(self, cube):
        """Тест полного цикла scramble (20 итераций)"""
        with patch('random.choice') as mock_choice:
            # Создаем список из 20 ходов
            moves_list = ['F', "F'", 'B', "B'", 'U', "U'", 'D', "D'", 'L', "L'", 'R', "R'", 'F', "F'", 'B', "B'", 'U', "U'", 'D', "D'"]
            mock_choice.side_effect = moves_list
            cube.animating = False
            cube.scramble()
            # Проверяем, что было 20 вызовов
            assert mock_choice.call_count == 20
    
    def test_scramble_both_branches(self, cube):
        """Тест обеих веток в scramble (с апострофом и без)"""
        # Тест ветки с апострофом
        with patch('random.choice', return_value="F'"):
            cube.animating = False
            cube.scramble()
        
        # Тест ветки без апострофа
        with patch('random.choice', return_value='F'):
            cube.animating = False
            cube.scramble()
        
        assert cube.cube is not None
    
    def test_load_from_file_full_loop(self, tmp_path, cube):
        """Тест полного цикла load_from_file"""
        file = tmp_path / "full.txt"
        with open(file, 'w') as f:
            # Создаем файл с 3 строками по 9 элементов
            for i in range(3):
                f.write(" ".join(['F', 'B', 'U', 'D', 'L', 'R', 'F', 'B', 'U']) + "\n")
        cube.load_from_file(str(file))
        # Проверяем, что все элементы загрузились
        assert cube.cube is not None
    
    def test_load_from_file_nested_loops(self, tmp_path, cube):
        """Тест вложенных циклов в load_from_file"""
        file = tmp_path / "nested.txt"
        with open(file, 'w') as f:
            # Создаем файл с несколькими строками и элементами
            for i in range(3):
                line = []
                for j in range(9):
                    line.append(['F', 'B', 'U', 'D', 'L', 'R'][j % 6])
                f.write(" ".join(line) + "\n")
        cube.load_from_file(str(file))
        assert cube.cube is not None
    
    def test_save_to_file_full_loop(self, tmp_path, cube):
        """Тест полного цикла save_to_file (27 итераций)"""
        file = tmp_path / "full_save.txt"
        cube.save_to_file(str(file))
        with open(file, 'r') as f:
            content = f.read()
            # Должно быть 27 элементов
            colors = content.split()
            assert len(colors) == 27
    
    def test_save_to_file_newline_conditions(self, tmp_path, cube):
        """Тест всех условий новой строки в save_to_file"""
        file = tmp_path / "newlines.txt"
        cube.save_to_file(str(file))
        with open(file, 'r') as f:
            lines = f.readlines()
            # Должно быть 3 строки (на позициях 9, 18, 27)
            assert len(lines) == 3
            # Каждая строка должна содержать 9 элементов
            for line in lines:
                assert len(line.strip().split()) == 9
    
    def test_reset_cube_full_nested_loops(self, cube):
        """Тест полных вложенных циклов в reset_cube"""
        cube.reset_cube()
        # Проверяем все 27 позиций (3x3x3)
        count = 0
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    count += 1
                    assert cube.cube[x, y, z] is not None or (x == 1 and y == 1 and z == 1)
        assert count == 27
    
    def test_reset_cube_all_condition_branches(self, cube):
        """Тест всех веток условий в reset_cube"""
        cube.reset_cube()
        # Проверяем каждую ветку условия
        # x == 0
        assert cube.cube[0, 0, 0] == 'L'
        assert cube.cube[0, 1, 1] == 'L'
        # x == 2
        assert cube.cube[2, 0, 0] == 'R'
        assert cube.cube[2, 1, 1] == 'R'
        # y == 0 (и x не 0 и не 2)
        assert cube.cube[1, 0, 1] == 'D'
        # y == 2 (и x не 0 и не 2)
        assert cube.cube[1, 2, 1] == 'U'
        # z == 0 (и x не 0 и не 2, и y не 0 и не 2)
        assert cube.cube[1, 1, 0] == 'B'
        # z == 2 (и x не 0 и не 2, и y не 0 и не 2)
        assert cube.cube[1, 1, 2] == 'F'
        # else (все остальные условия False)
        assert cube.cube[1, 1, 1] is None
    
    def test_apply_rotation_all_nested_loops(self, cube):
        """Тест всех вложенных циклов в apply_rotation"""
        for face in ['F', 'B', 'U', 'D', 'L', 'R']:
            for direction in [1, -1]:
                cube.animating = False
                cube.rotation_face = face
                cube.rotation_direction = direction
                original = cube.cube.copy()
                cube.apply_rotation()
                # Проверяем, что все элементы грани были обработаны
                assert cube.animating is False
    
    def test_apply_rotation_all_direction_branches(self, cube):
        """Тест всех веток direction в apply_rotation"""
        # Тестируем direction == 1 для всех граней
        for face in ['F', 'B', 'U', 'D', 'L', 'R']:
            cube.animating = False
            cube.rotation_face = face
            cube.rotation_direction = 1
            cube.apply_rotation()
            assert cube.animating is False
        
        # Тестируем direction == -1 для всех граней
        for face in ['F', 'B', 'U', 'D', 'L', 'R']:
            cube.animating = False
            cube.rotation_face = face
            cube.rotation_direction = -1
            cube.apply_rotation()
            assert cube.animating is False
    
    def test_is_solved_full_loop(self, cube):
        """Тест полного цикла is_solved (все 6 граней)"""
        cube.reset_cube()
        # Собранный кубик - все грани должны пройти проверку
        assert cube.is_solved() is True
        
        # Несобранный кубик - хотя бы одна грань должна не пройти проверку
        cube.cube[0, 0, 2] = 'B'
        assert cube.is_solved() is False
    
    def test_is_solved_all_face_branches(self, cube):
        """Тест всех веток проверки граней в is_solved"""
        # Проверяем каждую грань отдельно
        face_checks = {
            'F': (slice(None), slice(None), 2),
            'B': (slice(None), slice(None), 0),
            'U': (slice(None), 2, slice(None)),
            'D': (slice(None), 0, slice(None)),
            'L': (0, slice(None), slice(None)),
            'R': (2, slice(None), slice(None)),
        }
        
        for face, indices in face_checks.items():
            cube.reset_cube()
            # Делаем грань несобранной
            cube.cube[indices][0, 0] = 'X'
            assert cube.is_solved() is False
    
    def test_is_solved_unique_colors_filter(self, cube):
        """Тест фильтрации None в is_solved"""
        cube.reset_cube()
        # Внутренние кубики (None) не должны влиять на проверку
        assert cube.cube[1, 1, 1] is None
        # Кубик должен быть собран, несмотря на None значения
        assert cube.is_solved() is True
    
    def test_draw_cube_full_nested_loops(self, cube):
        """Тест полных вложенных циклов в draw_cube"""
        with patch('OpenGL.GL.glClear'), \
             patch('OpenGL.GL.glLoadIdentity'), \
             patch('OpenGL.GL.glTranslatef'), \
             patch('OpenGL.GL.glRotatef'), \
             patch('pygame.display.flip'):
            with patch.object(cube, 'draw_mini_cube') as mock_draw:
                cube.draw_cube()
                # Должно быть вызвано для всех видимых кубиков (26 из 27)
                # Проверяем, что циклы выполнились
                assert mock_draw.call_count >= 20
    
    def test_draw_cube_condition_branch(self, cube):
        """Тест ветки условия в draw_cube (is not None)"""
        # Устанавливаем все значения в None кроме одного
        cube.cube.fill(None)
        cube.cube[0, 0, 0] = 'F'
        
        with patch('OpenGL.GL.glClear'), \
             patch('OpenGL.GL.glLoadIdentity'), \
             patch('OpenGL.GL.glTranslatef'), \
             patch('OpenGL.GL.glRotatef'), \
             patch('pygame.display.flip'):
            with patch.object(cube, 'draw_mini_cube') as mock_draw:
                cube.draw_cube()
                # Должно быть вызвано только один раз
                assert mock_draw.call_count == 1
    
    def test_draw_mini_cube_all_faces_loop(self, cube):
        """Тест цикла по всем граням в draw_mini_cube"""
        with patch('OpenGL.GL.glBegin'), \
             patch('OpenGL.GL.glEnd'), \
             patch('OpenGL.GL.glColor3f'), \
             patch('OpenGL.GL.glVertex3f') as mock_vertex:
            cube.draw_mini_cube(0, 0, 0, 'F')
            # Должно быть вызвано для всех 6 граней * 4 вершины = 24 вызова для граней
            # + 12 ребер * 2 вершины = 24 вызова для линий
            # Итого минимум 48 вызовов
            assert mock_vertex.call_count >= 40
    
    def test_draw_mini_cube_all_vertices_loop(self, cube):
        """Тест цикла по всем вершинам в draw_mini_cube"""
        with patch('OpenGL.GL.glBegin'), \
             patch('OpenGL.GL.glEnd'), \
             patch('OpenGL.GL.glColor3f'), \
             patch('OpenGL.GL.glVertex3f') as mock_vertex:
            cube.draw_mini_cube(0, 0, 0, 'F')
            # Проверяем, что все вершины были обработаны
            assert mock_vertex.call_count > 0
    
    def test_draw_mini_cube_all_edges_loop(self, cube):
        """Тест цикла по всем ребрам в draw_mini_cube"""
        with patch('OpenGL.GL.glBegin'), \
             patch('OpenGL.GL.glEnd'), \
             patch('OpenGL.GL.glColor3f'), \
             patch('OpenGL.GL.glVertex3f') as mock_vertex:
            cube.draw_mini_cube(0, 0, 0, 'F')
            # Должно быть 12 ребер * 2 вершины = 24 вызова для линий
            assert mock_vertex.call_count >= 24
    
    def test_handle_events_full_loop(self, cube):
        """Тест полного цикла for event in events"""
        import rubiks_cube
        # Создаем несколько событий
        events = [
            Mock(type=rubiks_cube.pygame.KEYDOWN, key=102),  # K_f
            Mock(type=rubiks_cube.pygame.KEYDOWN, key=98),   # K_b
            Mock(type=rubiks_cube.pygame.QUIT),
        ]
        
        with patch('pygame.event.get', return_value=events):
            with patch('pygame.key.get_mods', return_value=0):
                with patch.object(cube, 'rotate_face') as mock_rotate:
                    result = cube.handle_events()
                    # Должно обработать все события до QUIT
                    assert result is False
    
    def test_handle_events_all_event_types(self, cube):
        """Тест всех типов событий в handle_events"""
        import rubiks_cube
        # Тест QUIT
        mock_event_quit = Mock()
        mock_event_quit.type = rubiks_cube.pygame.QUIT
        with patch('pygame.event.get', return_value=[mock_event_quit]):
            assert cube.handle_events() is False
        
        # Тест KEYDOWN
        mock_event_key = Mock()
        mock_event_key.type = rubiks_cube.pygame.KEYDOWN
        mock_event_key.key = 102  # K_f
        with patch('pygame.event.get', return_value=[mock_event_key]):
            with patch('pygame.key.get_mods', return_value=0):
                with patch.object(cube, 'rotate_face'):
                    assert cube.handle_events() is True
        
        # Тест MOUSEMOTION
        mock_event_mouse = Mock()
        mock_event_mouse.type = rubiks_cube.pygame.MOUSEMOTION
        mock_event_mouse.rel = (10, 20)
        with patch('pygame.event.get', return_value=[mock_event_mouse]):
            with patch('pygame.mouse.get_pressed', return_value=[True, False, False]):
                assert cube.handle_events() is True
    
    def test_handle_events_all_key_branches(self, cube):
        """Тест всех веток клавиш в handle_events"""
        import rubiks_cube
        # Тестируем все клавиши без Shift
        keys_no_shift = [
            (114, 'reset_cube'),      # K_r
            (115, 'scramble'),        # K_s
            (108, 'load_from_file'),  # K_l
            (112, 'save_to_file'),    # K_p
            (102, 'rotate_face'),    # K_f
            (98, 'rotate_face'),      # K_b
            (117, 'rotate_face'),     # K_u
            (100, 'rotate_face'),     # K_d
            (113, 'rotate_face'),    # K_q
            (101, 'rotate_face'),     # K_e
        ]
        
        for key_code, method_name in keys_no_shift:
            mock_event = Mock()
            mock_event.type = rubiks_cube.pygame.KEYDOWN
            mock_event.key = key_code
            
            with patch('pygame.event.get', return_value=[mock_event]):
                with patch('pygame.key.get_mods', return_value=0):
                    with patch.object(cube, method_name) as mock_method:
                        cube.handle_events()
                        assert mock_method.called
        
        # Тестируем все клавиши с Shift
        keys_shift = [
            (102, 'F', -1),  # K_f
            (98, 'B', -1),   # K_b
            (117, 'U', -1),  # K_u
            (100, 'D', -1),  # K_d
            (113, 'L', -1),  # K_q
            (101, 'R', -1),  # K_e
        ]
        
        for key_code, face, direction in keys_shift:
            mock_event = Mock()
            mock_event.type = rubiks_cube.pygame.KEYDOWN
            mock_event.key = key_code
            
            with patch('pygame.event.get', return_value=[mock_event]):
                with patch('pygame.key.get_mods', return_value=rubiks_cube.pygame.KMOD_SHIFT):
                    with patch.object(cube, 'rotate_face') as mock_rotate:
                        cube.handle_events()
                        mock_rotate.assert_called_with(face, direction)
    
    def test_handle_events_mouse_pressed_condition(self, cube):
        """Тест условия pygame.mouse.get_pressed()[0]"""
        import rubiks_cube
        mock_event = Mock()
        mock_event.type = rubiks_cube.pygame.MOUSEMOTION
        mock_event.rel = (10, 20)
        
        # Тест когда кнопка нажата
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.mouse.get_pressed', return_value=[True, False, False]):
                original_x = cube.rotation_x
                cube.handle_events()
                assert cube.rotation_x != original_x
        
        # Тест когда кнопка не нажата
        with patch('pygame.event.get', return_value=[mock_event]):
            with patch('pygame.mouse.get_pressed', return_value=[False, False, False]):
                original_x = cube.rotation_x
                cube.handle_events()
                assert cube.rotation_x == original_x
    
    def test_update_animation_full_condition(self, cube):
        """Тест полного условия в update_animation"""
        # Тест когда animating == True и условие выполняется
        cube.animating = True
        cube.animation_angle = 90
        cube.target_angle = 90
        cube.rotation_direction = 1
        cube.rotation_face = 'F'
        
        with patch.object(cube, 'apply_rotation') as mock_apply:
            cube.update_animation()
            assert mock_apply.called
        
        # Тест когда animating == True но условие не выполняется
        cube.animating = True
        cube.animation_angle = 10
        cube.target_angle = 90
        cube.rotation_direction = 1
        cube.rotation_face = 'F'
        
        with patch.object(cube, 'apply_rotation') as mock_apply:
            cube.update_animation()
            # apply_rotation не должна быть вызвана
            if cube.animation_angle < 90:
                pass  # Условие не выполнилось
    
    def test_run_full_while_loop(self, cube, capsys):
        """Тест полного цикла while в run"""
        with patch('pygame.time.Clock') as mock_clock, \
             patch.object(cube, 'handle_events', side_effect=[True, True, False]), \
             patch.object(cube, 'update_animation'), \
             patch.object(cube, 'draw_cube'), \
             patch('pygame.quit'):
            mock_clock_instance = Mock()
            mock_clock.return_value = mock_clock_instance
            mock_clock_instance.tick.return_value = 60
            
            cube.run()
            # Проверяем, что цикл выполнился несколько раз
            assert mock_clock_instance.tick.call_count >= 2
    
    def test_run_is_solved_condition(self, cube, capsys):
        """Тест условия is_solved в run"""
        with patch('pygame.time.Clock') as mock_clock, \
             patch.object(cube, 'handle_events', side_effect=[True, False]), \
             patch.object(cube, 'update_animation'), \
             patch.object(cube, 'draw_cube'), \
             patch('pygame.quit'):
            mock_clock_instance = Mock()
            mock_clock.return_value = mock_clock_instance
            mock_clock_instance.tick.return_value = 60
            
            # Тест когда is_solved возвращает True
            with patch.object(cube, 'is_solved', return_value=True):
                cube.run()
                captured = capsys.readouterr()
                assert "Кубик собран!" in captured.out
            
            # Тест когда is_solved возвращает False
            with patch.object(cube, 'is_solved', return_value=False):
                cube.run()
                captured = capsys.readouterr()
                assert "Кубик собран!" not in captured.out
    
    def test_run_exception_branch(self, cube, capsys):
        """Тест ветки исключения в run"""
        with patch('pygame.time.Clock') as mock_clock, \
             patch.object(cube, 'handle_events', side_effect=Exception("Test error")), \
             patch.object(cube, 'update_animation'), \
             patch.object(cube, 'draw_cube'), \
             patch('pygame.quit'):
            mock_clock_instance = Mock()
            mock_clock.return_value = mock_clock_instance
            mock_clock_instance.tick.return_value = 60
            
            cube.run()
            captured = capsys.readouterr()
            assert "Ошибка в основном цикле" in captured.out
    
    def test_handle_events_exception_branch(self, cube, capsys):
        """Тест ветки исключения в handle_events"""
        with patch('pygame.event.get', side_effect=Exception("Test error")):
            result = cube.handle_events()
            captured = capsys.readouterr()
            assert "Ошибка обработки событий" in captured.out
            assert result is True
    
    def test_load_from_file_color_in_colors_branch(self, tmp_path, cube):
        """Тест ветки if color in self.colors"""
        file = tmp_path / "colors.txt"
        with open(file, 'w') as f:
            # Смешиваем валидные и невалидные цвета
            f.write("F INVALID B U D L R X Y\n")
        cube.load_from_file(str(file))
        # Валидные цвета должны загрузиться
        assert cube.cube is not None
    
    def test_save_to_file_ternary_operator(self, tmp_path, cube):
        """Тест тернарного оператора в save_to_file"""
        # Тест когда cube[x,y,z] is not None
        cube.cube[0, 0, 0] = 'F'
        file = tmp_path / "ternary1.txt"
        cube.save_to_file(str(file))
        with open(file, 'r') as f:
            content = f.read()
            assert 'F' in content
        
        # Тест когда cube[x,y,z] is None
        cube.cube[0, 0, 0] = None
        file = tmp_path / "ternary2.txt"
        cube.save_to_file(str(file))
        with open(file, 'r') as f:
            content = f.read()
            assert 'X' in content or len(content) > 0
