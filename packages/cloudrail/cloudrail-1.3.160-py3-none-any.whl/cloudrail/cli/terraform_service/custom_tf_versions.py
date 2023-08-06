def get_custom_tf_versions():
    return {"versions":
                {"0.12": "46",
                 "0.13": "40",
                 "0.14": "44",
                 "0.15": "23",
                 "1.0": "14"},
            "architectures": {
                "0.12": ["linux-amd64", "darwin-amd64", "windows-amd64"],
                "0.13": ["linux-amd64", "darwin-amd64", "windows-amd64"],
                "0.14": ["linux-amd64", "darwin-amd64", "windows-amd64"],
                "0.15": ["linux-amd64", "darwin-amd64", "darwin-arm64", "windows-amd64"],
                "1.0": ["linux-amd64", "darwin-amd64", "darwin-arm64", "windows-amd64"]}}
