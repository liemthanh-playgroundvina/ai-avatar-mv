download_model:
	git clone https://huggingface.co/fudan-generative-ai/hallo pretrained_models

config:
	mkdir -p logs && touch logs/celery.log
	cp configs/env.example configs/.env
	# And add params ...

# Docker
build:
	docker pull nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04
	docker build -t ai-avatar-mv -f Dockerfile .

start:
	docker compose -f docker-compose.yml down
	docker compose -f docker-compose.yml up -d

start-prod:
	docker compose -f docker-compose-prod.yml down
	docker compose -f docker-compose-prod.yml up -d

stop:
	docker compose -f docker-compose.yml down

stop-prod:
	docker compose -f docker-compose-prod.yml down

# Checker
cmd-image:
	# python inference.py --source_image examples/Miku\(1\).jpg --driving_audio examples/Audio_10s.mp3 --output .cache/output_15st.mp4
	docker run -it --gpus all --rm --runtime=nvidia -v ./pretrained_models:/pretrained_models -v .:/app ai-avatar-mv /bin/bash

cmd-worker:
	docker compose exec worker-ai-avatar-mv /bin/bash

log-worker:
	cat logs/celery.log

