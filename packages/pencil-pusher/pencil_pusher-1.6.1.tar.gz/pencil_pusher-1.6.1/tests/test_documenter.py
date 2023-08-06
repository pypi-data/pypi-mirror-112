from pencil_pusher.documenter import Documenter
import os


def test_gen_local():
    """
    Tests generating a doc with a
    local file
    """
    Documenter.generate("pencil_pusher.documenter", "test")
    assert os.path.isfile("./test.md")
    os.remove("./test.md")


def test_toc():
    """
    Tests that toc is generated correctly
    """

    test_files = [
        "pencil_pusher.configs.base",
        "pencil_pusher.configs.manager",
        "pencil_pusher.configs.python_lang",
        "pencil_pusher.documenter",
        "pencil_pusher.input",
    ]

    test_file_map = {i: i for i in test_files}
    toc_tree = Documenter.build_toc(test_files)

    assert toc_tree == {
        "pencil_pusher": {
            "configs": {"base": {}, "manager": {}, "python_lang": {}},
            "documenter": {},
            "input": {},
        }
    }

    Documenter.generate_sidebar(
        toc_tree, test_file_map, "stephend017", "pencil-pusher"
    )

    os.remove("./_Sidebar.md")
