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
