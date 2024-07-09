# AI Avatar MV
- Link: https://github.com/fudan-generative-vision/hallo

- Queue System using celery(python) + redis + rabbitMQ

- Image information: Python 3.9


1. Clone & download model
```# command
git clone https://github.com/liemthanh-playgroundvina/ai-avatar-mv.git
cd ai-avatar-mv
```

2. Build Image
```# command
make build
```

3. Download Model
```# command
make download_model
```

4. Config
```# command
make config
... And add your config
```

5. Start
```# command
make start
```

## Config:
inference_steps: 15 (./configs/inference/default.yaml)