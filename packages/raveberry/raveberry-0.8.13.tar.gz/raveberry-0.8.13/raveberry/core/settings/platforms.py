"""This module handles all settings regarding the music platforms."""
from __future__ import annotations

import importlib
import os
import subprocess
from typing import TYPE_CHECKING

from django.conf import settings as conf
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest

from core.models import Setting
from core.settings.library import Library
from core.settings.settings import Settings


class Platforms:
    """This class is responsible for handling setting changes related to music platforms."""

    def __init__(self, settings: Settings):
        self.settings = settings

        self.local_enabled = os.path.islink(Library.get_library_path())

        # in the docker container all dependencies are installed
        self.youtube_available = (
            conf.DOCKER or importlib.util.find_spec("youtube_dl") is not None
        )
        # the _enabled check is the second expression so the databes entry gets created in any case
        self.youtube_enabled = (
            Settings.get_setting("youtube_enabled", "True") == "True"
            and self.youtube_available
        )
        self.youtube_suggestions = int(Settings.get_setting("youtube_suggestions", "2"))

        # Spotify has no python dependencies we could easily check.
        try:
            self.spotify_available = (
                conf.DOCKER
                or "[spotify]"
                in subprocess.check_output(
                    ["mopidy", "config"], stderr=subprocess.DEVNULL
                )
                .decode()
                .splitlines()
            )
        except FileNotFoundError:
            # mopidy is not installed. Disable when mocking, enable otherwise
            self.spotify_available = not conf.MOCK
        self.spotify_enabled = (
            Settings.get_setting("spotify_enabled", "False") == "True"
            and self.spotify_available
        )
        self.spotify_suggestions = int(Settings.get_setting("spotify_suggestions", "2"))
        self.spotify_username = Settings.get_setting("spotify_username", "")
        self.spotify_password = Settings.get_setting("spotify_password", "")
        self.spotify_client_id = Settings.get_setting("spotify_client_id", "")
        self.spotify_client_secret = Settings.get_setting("spotify_client_secret", "")

        self.soundcloud_available = (
            conf.DOCKER or importlib.util.find_spec("soundcloud") is not None
        )
        self.soundcloud_enabled = (
            Settings.get_setting("soundcloud_enabled", "False") == "True"
            and self.soundcloud_available
        )
        self.soundcloud_suggestions = int(
            Settings.get_setting("soundcloud_suggestions", "2")
        )
        self.soundcloud_auth_token = Settings.get_setting("soundcloud_auth_token", "")

        # Jamendo has no python dependencies we could easily check.
        try:
            self.jamendo_available = (
                conf.DOCKER
                or "[jamendo]"
                in subprocess.check_output(
                    ["mopidy", "config"], stderr=subprocess.DEVNULL
                )
                .decode()
                .splitlines()
            )
        except FileNotFoundError:
            # mopidy is not installed. Disable when mocking, enable otherwise
            self.jamendo_available = not conf.MOCK
        self.jamendo_enabled = (
            Settings.get_setting("jamendo_enabled", "False") == "True"
            and self.jamendo_available
        )
        self.jamendo_suggestions = int(Settings.get_setting("jamendo_suggestions", "2"))
        self.jamendo_client_id = Settings.get_setting("jamendo_client_id", "")

    @Settings.option
    def set_youtube_enabled(self, request: WSGIRequest):
        """Enables or disables youtube to be used as a song provider."""
        enabled = request.POST.get("value") == "true"
        Setting.objects.filter(key="youtube_enabled").update(value=enabled)
        self.youtube_enabled = enabled

    @Settings.option
    def set_youtube_suggestions(self, request: WSGIRequest):
        """Sets the number of online suggestions from youtube to be shown."""
        value = int(request.POST.get("value"))  # type: ignore
        Setting.objects.filter(key="youtube_suggestions").update(value=value)
        self.youtube_suggestions = value

    def _set_extension_enabled(self, extension, enabled) -> HttpResponse:
        if enabled:
            if conf.DOCKER:
                response = HttpResponse(
                    "Make sure you provided mopidy with correct credentials."
                )
            else:
                extensions = self.settings.system.check_mopidy_extensions()
                functional, message = extensions[extension]
                if not functional:
                    return HttpResponseBadRequest(message)
                response = HttpResponse(message)
        else:
            response = HttpResponse("Disabled extension")
        Setting.objects.filter(key=f"{extension}_enabled").update(value=enabled)
        setattr(self, f"{extension}_enabled", enabled)
        return response

    @Settings.option
    def set_spotify_enabled(self, request: WSGIRequest) -> HttpResponse:
        """Enables or disables spotify to be used as a song provider.
        Makes sure mopidy has correct spotify configuration."""
        enabled = request.POST.get("value") == "true"
        return self._set_extension_enabled("spotify", enabled)

    @Settings.option
    def set_spotify_suggestions(self, request: WSGIRequest):
        """Sets the number of online suggestions from spotify to be shown."""
        value = int(request.POST.get("value"))  # type: ignore
        Setting.objects.filter(key="spotify_suggestions").update(value=value)
        self.spotify_suggestions = value

    @Settings.option
    def set_spotify_credentials(self, request: WSGIRequest) -> HttpResponse:
        """Update spotify credentials."""
        username = request.POST.get("username")
        password = request.POST.get("password")
        client_id = request.POST.get("client_id")
        client_secret = request.POST.get("client_secret")

        if not username or not password or not client_id or not client_secret:
            return HttpResponseBadRequest("All fields are required")

        self.spotify_username = username
        self.spotify_password = password
        self.spotify_client_id = client_id
        self.spotify_client_secret = client_secret

        Setting.objects.filter(key="spotify_username").update(
            value=self.spotify_username
        )
        Setting.objects.filter(key="spotify_password").update(
            value=self.spotify_password
        )
        Setting.objects.filter(key="spotify_client_id").update(
            value=self.spotify_client_id
        )
        Setting.objects.filter(key="spotify_client_secret").update(
            value=self.spotify_client_secret
        )

        self.settings.system.update_mopidy_config("pulse")
        return HttpResponse("Updated credentials")

    @Settings.option
    def set_soundcloud_enabled(self, request: WSGIRequest) -> HttpResponse:
        """Enables or disables soundcloud to be used as a song provider.
        Makes sure mopidy has correct soundcloud configuration."""
        enabled = request.POST.get("value") == "true"
        return self._set_extension_enabled("soundcloud", enabled)

    @Settings.option
    def set_soundcloud_suggestions(self, request: WSGIRequest):
        """Sets the number of online suggestions from soundcloud to be shown."""
        value = int(request.POST.get("value"))  # type: ignore
        Setting.objects.filter(key="soundcloud_suggestions").update(value=value)
        self.soundcloud_suggestions = value

    @Settings.option
    def set_soundcloud_credentials(self, request: WSGIRequest) -> HttpResponse:
        """Update soundcloud credentials."""
        auth_token = request.POST.get("auth_token")

        if not auth_token:
            return HttpResponseBadRequest("All fields are required")

        self.soundcloud_auth_token = auth_token

        Setting.objects.filter(key="soundcloud_auth_token").update(
            value=self.soundcloud_auth_token
        )

        self.settings.system.update_mopidy_config("pulse")
        return HttpResponse("Updated credentials")

    @Settings.option
    def set_jamendo_enabled(self, request: WSGIRequest) -> HttpResponse:
        """Enables or disables jamendo to be used as a song provider.
        Makes sure mopidy has correct jamendo configuration."""
        enabled = request.POST.get("value") == "true"
        return self._set_extension_enabled("jamendo", enabled)

    @Settings.option
    def set_jamendo_suggestions(self, request: WSGIRequest):
        """Sets the number of online suggestions from jamendo to be shown."""
        value = int(request.POST.get("value"))  # type: ignore
        Setting.objects.filter(key="jamendo_suggestions").update(value=value)
        self.jamendo_suggestions = value

    @Settings.option
    def set_jamendo_credentials(self, request: WSGIRequest) -> HttpResponse:
        """Update jamendo credentials."""
        client_id = request.POST.get("client_id")

        if not client_id:
            return HttpResponseBadRequest("All fields are required")

        self.jamendo_client_id = client_id

        Setting.objects.filter(key="jamendo_client_id").update(
            value=self.jamendo_client_id
        )

        self.settings.system.update_mopidy_config("pulse")
        return HttpResponse("Updated credentials")
