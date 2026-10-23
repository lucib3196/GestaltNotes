from backend.storage.utils import normalize_storage_key


def test_normalize_storage_key_joins_parts() -> None:
    assert (
        normalize_storage_key("user/user123", "courses/course123")
        == "user/user123/courses/course123"
    )


def test_normalize_storage_key_strips_extra_slashes() -> None:
    assert (
        normalize_storage_key("/user/user123/", "/courses/course123/")
        == "user/user123/courses/course123"
    )


def test_normalize_storage_key_accepts_iterable_parts() -> None:
    assert (
        normalize_storage_key(["user/user123", "courses/course123"])
        == "user/user123/courses/course123"
    )


def test_normalize_storage_key_accepts_file_name() -> None:
    assert (
        normalize_storage_key(
            "users/user123",
            "courses/course123",
            "lecture-note.pdf",
        )
        == "users/user123/courses/course123/lecture-note.pdf"
    )


def test_normalize_storage_key_strips_slashes_from_file_name() -> None:
    assert (
        normalize_storage_key(
            "/users/user123/",
            "/courses/course123/",
            "/lecture-note.pdf",
        )
        == "users/user123/courses/course123/lecture-note.pdf"
    )
