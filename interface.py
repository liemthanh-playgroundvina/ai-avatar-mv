import subprocess
import json
import time
import logging

def avatar_mv(image: str, audio: str):
    """

        {
            "path": ".cache/123.mp4",
            "execution_time": 60.870914936065674,
        }

    """
    args = ["python", "main.py", "--source_image", image, "--driving_audio", audio, "--output", f".cache/{int(time.time() * 10**7)}.mp4"]
    print(args)
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        encoding='utf-8',
    )
    output = result.stdout.strip()
    logging.getLogger('celery').info(output)

    output = json.loads(output, strict=False)

    output_dir = ".cache"

    if output['error']:
        if output['error']['type'] == "ValueError":
            raise ValueError(output['error']['message'])
        elif output['error']['type'] == "Exception":
            raise Exception(output['error']['message'])

    return output_dir, output['path'], output['execution_time']
