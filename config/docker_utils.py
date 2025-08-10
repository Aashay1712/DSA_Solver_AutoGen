async def start_docker_container(docker):
    print("Starting docker container...")
    await docker.start()

async def stop_docker_container(docker):
    print("Stoppind docker container...")
    await docker.stop()
    print("Docker container stopped.")