import pytest

if __name__ == "__main__":
    pytest.main([
        "-v",
        "--cov=rubiks_cube",
        "--cov-report=term-missing"
    ])
