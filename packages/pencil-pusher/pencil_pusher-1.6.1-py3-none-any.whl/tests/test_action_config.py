import os
from sd_utils.github_actions.action import GithubAction


def test_action_config():
    """
    Tests that the action is configured correctly
    """
    ga = GithubAction(
        "stephend017",
        "pencil-pusher",
        {
            "GITHUB_REPOSITORY": "stephend017/pencil-pusher",
            "INPUT_CONFIG_FILE": "pencil_pusher.config.json",
            "INPUT_GITHUB_TOKEN": os.environ["GH_PAT"],
        },
        os.environ["GH_PAT"],
        {"repository"},
    )

    owner_name = ga.builtins["repository"].split("/")[0]
    repository_name = ga.builtins["repository"].split("/")[1]

    assert owner_name == "stephend017"
    assert repository_name == "pencil-pusher"
