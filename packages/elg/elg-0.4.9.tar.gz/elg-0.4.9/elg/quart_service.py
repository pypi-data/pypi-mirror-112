import inspect
import json
import os
import re
import traceback
from pathlib import Path
from posixpath import expanduser
from typing import Dict, List

from loguru import logger

try:
    import aiohttp
    import docker
    from quart import Quart
    from quart import request as input_request
    from requests_toolbelt import MultipartDecoder
except:
    raise ImportError(
        "Extra dependencies need to be install to use the FlaskService class. Please run: `pip install elg[provider]`."
    )

from werkzeug.exceptions import BadRequest, RequestEntityTooLarge

from .model import AudioRequest, StructuredTextRequest, TextRequest
from .utils.docker import COPY_FOLDER, DOCKERFILE, ENTRYPOINT_QUART


class ProcessingError(Exception):
    def __init__(self, status_code, code, text, *params):
        self.status_code = status_code
        self.code = code
        self.text = text
        self.params = params

    @staticmethod
    def InternalError(text):
        return ProcessingError(500, "elg.service.internalError", "Internal error during processing: {0}", text)

    @staticmethod
    def InvalidRequest():
        return ProcessingError(400, "elg.request.invalid", "Invalid request message")

    @staticmethod
    def TooLarge():
        return ProcessingError(413, "elg.request.too.large", "Request size too large")

    @staticmethod
    def UnsupportedMime(mime):
        return ProcessingError(
            400, "elg.request.text.mimeType.unsupported", "MIME type {0} not supported by this service", mime
        )

    @staticmethod
    def UnsupportedType(request_type):
        return ProcessingError(
            400, "elg.request.type.unsupported", "Request type {0} not supported by this service", request_type
        )

    def to_json(self):
        return {
            "failure": {
                "errors": [
                    {
                        "code": self.code,
                        "text": self.text,
                        "params": self.params,
                    }
                ]
            }
        }


class QuartService:
    """
    Class to help the creation of an ELG compatible service from a python model using Quart.
    Extra dependencies need to be install to use the QuartService class. Please run: `pip install elg[provider]`.
    """

    requirements = ["elg[quart]"]

    def __init__(self, name: str, request_size_limit: int = None):
        """
        Init function of the QuartService

        Args:
            name (str): Name of the service. It doesn't have any importance.
        """
        self.name = name
        self.app = Quart(name)
        # Don't add an extra "status" property to JSON responses - this would break the API contract
        self.app.config["JSON_ADD_STATUS"] = False
        # Don't sort properties alphabetically in response JSON
        self.app.config["JSON_SORT_KEYS"] = False

        if request_size_limit is not None:
            self.app.config["MAX_CONTENT_LENGTH"] = request_size_limit

        # Exceptions handling
        self.app.register_error_handler(ProcessingError, self.error_message)
        self.app.register_error_handler(BadRequest, lambda err: self.error_message(ProcessingError.InvalidRequest()))
        self.app.register_error_handler(
            RequestEntityTooLarge, lambda err: self.error_message(ProcessingError.TooLarge())
        )

        self.app.before_serving(self.setup)
        self.app.after_serving(self.shutdown)

        self.app.add_url_rule("/health", "health", self.health, methods=["GET"])
        self.app.add_url_rule("/process", "process", self.process, methods=["POST"])

    def run(self):
        """
        Method to start the app.
        """
        self.app.run()

    @staticmethod
    def error_message(err):
        return err.to_json(), err.status_code

    async def setup(self):
        """
        One-time setup tasks that must happen before the first request is
        handled, but require access to the event loop so cannot happen at the top
        level.
        """
        # Create the shared aiohttp session
        self.session = aiohttp.ClientSession()
        # or you may wish to configure things like default headers, e.g.
        # session = aiohttp.ClientSession(headers = {'X-API-Key':os.environ.get('APIKEY')})

    async def shutdown(self):
        """
        Logic that must run at shutdown time, after the last request has been
        handled.
        """
        if self.session is not None:
            await self.session.close()

    def health(self):
        return {"alive": True}

    async def process(self):
        """
        Main request processing logic - accepts a JSON request and returns a JSON response.
        """
        logger.info("Process request")
        if "application/json" in input_request.content_type:
            data = await input_request.get_json()
        elif "multipart/form-data" in input_request.content_type:
            input_request_data = await input_request.get_data()
            decoder = MultipartDecoder(input_request_data, input_request.content_type)
            data = {}
            for part in decoder.parts:
                headers = {k.decode(): v.decode() for k, v in part.headers.items()}
                if "application/json" in headers["Content-Type"]:
                    for k, v in json.loads(part.content.decode()).items():
                        data[k] = v
                elif "audio" in headers["Content-Type"]:
                    data["content"] = part.content
                else:
                    raise ValueError("Unknown Content-Type in multipart request")
        else:
            raise ValueError(f"Content-Type [{input_request.content_type}] not implemented yet.")

        logger.debug(f"Data type: {data.get('type')}")
        if data.get("type") == "audio":
            request = AudioRequest(**data)
        elif data.get("type") == "text":
            request = TextRequest(**data)
        elif data.get("type") == "structuredText":
            request = StructuredTextRequest(**data)
        else:
            raise ProcessingError.InvalidRequest()
        logger.info(f"Call with the input: {request}")
        logger.info("Await for the coroutine...")
        response = await self.process_request(request)
        logger.info(f"Get response: {response}")
        response = {"response": response.dict(by_alias=True)}
        logger.info(f"Return: {response}")
        return response

    async def process_request(self, request):
        """
        Method to process the request object. This method only calls the right process method regarding the type of the request.
        """
        if request.type == "text":
            logger.debug("Process text")
            return await self.process_text(request)
        if request.type == "structuredText":
            logger.debug("Process structured text")
            return await self.process_structured_text(request)
        if request.type == "audio":
            logger.debug("Process audio")
            return await self.process_audio(request)
        raise ProcessingError.InvalidRequest()

    async def process_text(self, request: TextRequest):
        """
        Method to implement if the service takes text as input.

        Args:
            request (TextRequest): TextRequest object.
        """
        raise ProcessingError.UnsupportedType()

    async def process_structured_text(self, request: StructuredTextRequest):
        """
        Method to implement if the service takes structured text as input.

        Args:
            request (StructuredTextRequest): StructuredTextRequest object.
        """
        raise ProcessingError.UnsupportedType()

    async def process_audio(self, request: AudioRequest):
        """
        Method to implement if the service takes audio as input.

        Args:
            request (AudioRequest): AudioRequest object.
        """
        raise ProcessingError.UnsupportedType()

    @classmethod
    def create_requirements(cls, requirements: List = [], path: str = None):
        """
        Class method to create the correct requirements.txt file.

        Args:
            requirements (List, optional): List of required pip packages. Defaults to [].
            path (str, optional): Path where to generate the file. Defaults to None.
        """
        if path == None:
            path = Path(inspect.getsourcefile(cls))
        else:
            path = Path(path)
        requirements = cls.requirements + requirements
        with open(path.parent / "requirements.txt", "w") as f:
            f.write("\n".join(set(requirements)))

    @classmethod
    def create_docker_files(cls, required_files: List = [], required_folders: List = [], path: str = None):
        """Class method to create the correct Dockerfile.

        Args:
            required_files (List, optional): List of files needed for the service. Defaults to [].
            required_folders (List, optional): List of folders needed for the service. Defaults to [].
            path (str, optional): Path where to generate the file. Defaults to None.
        """
        if path == None:
            path = Path(inspect.getsourcefile(cls))
        else:
            path = Path(path)
        required_files = [path.name] + required_files
        required_folders = "\n".join(
            [COPY_FOLDER.format(folder_name=str(Path(folder))) for folder in required_folders]
        )
        service_script = path.name[:-3]  # to remove .py
        # The docker-entrypoint file is a Linux shell script so _must_ be
        # written with Unix-style line endings, even if the build is being done
        # on Windows.  To ensure this we write in binary mode.
        with open(path.parent / "docker-entrypoint.sh", "wb") as f:
            f.write(ENTRYPOINT_QUART.format(service_script=service_script).encode("utf-8"))
        with open(path.parent / "Dockerfile", "w") as f:
            f.write(DOCKERFILE.format(required_files=" ".join(required_files), required_folders=required_folders))

    @classmethod
    def docker_build_image(cls, tag: str, pull: bool = True, path: str = None, **kwargs):
        """
        Class method to do `docker build ...` in python. Better to use the docker cli instead of this method.
        """
        if path == None:
            path = Path(inspect.getsourcefile(cls))
        else:
            path = Path(path)
        client = docker.from_env()
        image, _ = client.images.build(path=str(path.parent), tag=tag, pull=pull, **kwargs)
        return image

    @classmethod
    def docker_push_image(cls, repository: str, tag: str, username: str = None, password: str = None, **kwargs):
        """
        Class method to do `docker push ...` in python. Better to use the docker cli instead of this method.
        """
        client = docker.from_env()
        if username is not None and password is not None:
            auth_config = {"username": username, "password": password}
            client.images.push(repository=repository, tag=tag, auth_config=auth_config, stream=True, **kwargs)
        client.images.push(repository=repository, tag=tag, stream=True, **kwargs)
        return

    @classmethod
    def docker_build_push_image(
        cls,
        repository: str,
        tag: str,
        pull: bool = True,
        username: str = None,
        password: str = None,
        build_kwargs: Dict = {},
        push_kwargs: Dict = {},
    ):
        cls.docker_build_image(tag=f"{repository}:{tag}", pull=pull, **build_kwargs)
        cls.docker_push_image(repository=repository, tag=tag, username=username, password=password, **push_kwargs)
        return None
