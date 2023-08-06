"""This module handles all requests concerning the addition of music to the queue."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Union, TYPE_CHECKING, List, Tuple, cast, Type

import ipware
from django.core.handlers.wsgi import WSGIRequest
from django.forms.models import model_to_dict
from django.http import HttpResponseBadRequest
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import URLPattern

import core.musiq.song_utils as song_utils
from core import util
from core.models import CurrentSong
from core.models import QueuedSong
from core.musiq.controller import Controller
from core.musiq.localdrive import LocalSongProvider
from core.musiq.music_provider import MusicProvider, WrongUrlError, ProviderError
from core.musiq.song_provider import SongProvider
from core.musiq.playlist_provider import PlaylistProvider
from core.musiq.playback import Playback
from core.musiq.suggestions import Suggestions
from core.state_handler import Stateful

if TYPE_CHECKING:
    from core.base import Base


class Musiq(Stateful):
    """This class provides endpoints for all music related requests."""

    def __init__(self, base: "Base") -> None:
        self.base = base
        self.urlpatterns: List[URLPattern] = []

        self.suggestions = Suggestions(self)

        self.queue = QueuedSong.objects

        self.playback = Playback(self)
        self.controller = Controller(self)

    def start(self) -> None:
        self.controller.start()
        self.playback.start()

    def do_request_music(
        self,
        request_ip: str,
        query: str,
        key: Optional[int],
        playlist: bool,
        platform: str,
        archive: bool = True,
        manually_requested: bool = True,
    ) -> Tuple[bool, str, Optional[int]]:
        """Performs the actual requesting of the music, not an endpoint.
        Enqueues the requested song or playlist into the queue, using appropriate providers.
        Returns a 3-tuple: successful, message, queue_key"""
        providers: List[MusicProvider] = []

        provider: MusicProvider
        music_provider_class: Union[Type[PlaylistProvider], Type[SongProvider]]
        local_provider_class: Type[MusicProvider]
        jamendo_provider_class: Type[MusicProvider]
        soundcloud_provider_class: Type[MusicProvider]
        spotify_provider_class: Type[MusicProvider]
        youtube_provider_class: Type[MusicProvider]
        if playlist:
            music_provider_class = PlaylistProvider
            local_provider_class = PlaylistProvider
            if self.base.settings.platforms.jamendo_enabled:
                from core.musiq.jamendo import JamendoPlaylistProvider

                jamendo_provider_class = JamendoPlaylistProvider
            if self.base.settings.platforms.soundcloud_enabled:
                from core.musiq.soundcloud import SoundcloudPlaylistProvider

                soundcloud_provider_class = SoundcloudPlaylistProvider
            if self.base.settings.platforms.spotify_enabled:
                from core.musiq.spotify import SpotifyPlaylistProvider

                spotify_provider_class = SpotifyPlaylistProvider
            if self.base.settings.platforms.youtube_enabled:
                from core.musiq.youtube import YoutubePlaylistProvider

                youtube_provider_class = YoutubePlaylistProvider
        else:
            music_provider_class = SongProvider
            local_provider_class = LocalSongProvider
            if self.base.settings.platforms.jamendo_enabled:
                from core.musiq.jamendo import JamendoSongProvider

                jamendo_provider_class = JamendoSongProvider
            if self.base.settings.platforms.soundcloud_enabled:
                from core.musiq.soundcloud import SoundcloudSongProvider

                soundcloud_provider_class = SoundcloudSongProvider
            if self.base.settings.platforms.spotify_enabled:
                from core.musiq.spotify import SpotifySongProvider

                spotify_provider_class = SpotifySongProvider
            if self.base.settings.platforms.youtube_enabled:
                from core.musiq.youtube import YoutubeSongProvider

                youtube_provider_class = YoutubeSongProvider

        if key is not None:
            # an archived entry was requested.
            # The key determines the Provider
            provider = music_provider_class.create(self, query, key)
            if provider is None:
                return False, "No provider found for requested key", None
            providers.append(provider)
        else:
            if platform == "local":
                # local music can only be searched explicitly
                providers.append(local_provider_class(self, query, key))
            if self.base.settings.platforms.soundcloud_enabled:
                try:
                    soundcloud_provider = soundcloud_provider_class(self, query, key)
                    if platform == "soundcloud":
                        providers.insert(0, soundcloud_provider)
                    else:
                        providers.append(soundcloud_provider)
                except WrongUrlError:
                    pass
            if self.base.settings.platforms.spotify_enabled:
                try:
                    spotify_provider = spotify_provider_class(self, query, key)
                    if platform == "spotify":
                        providers.insert(0, spotify_provider)
                    else:
                        providers.append(spotify_provider)
                except WrongUrlError:
                    pass
            if self.base.settings.platforms.jamendo_enabled:
                try:
                    jamendo_provider = jamendo_provider_class(self, query, key)
                    if platform == "jamendo":
                        providers.insert(0, jamendo_provider)
                    else:
                        providers.append(jamendo_provider)
                except WrongUrlError:
                    pass
            if self.base.settings.platforms.youtube_enabled:
                try:
                    youtube_provider = youtube_provider_class(self, query, key)
                    if platform == "youtube":
                        providers.insert(0, youtube_provider)
                    else:
                        providers.append(youtube_provider)
                except WrongUrlError:
                    pass

        if not providers:
            return False, "No backend configured to handle your request.", None

        fallback = False
        for i, provider in enumerate(providers):
            try:
                provider.request(
                    request_ip, archive=archive, manually_requested=manually_requested
                )
                # the current provider could provide the song, don't try the other ones
                break
            except ProviderError:
                # this provider cannot provide this song, use the next provider
                # if this was the last provider, show its error
                # in new music only mode, do not allow fallbacks
                if self.base.settings.basic.new_music_only or i == len(providers) - 1:
                    return False, provider.error, None
                fallback = True
        message = provider.ok_message
        queue_key = None
        if not playlist:
            queued_song = cast(SongProvider, provider).queued_song
            if not queued_song:
                logging.error(
                    "no placeholder was created for query '%s' and key '%s'", query, key
                )
                return False, "No placeholder was created", None
            queue_key = queued_song.id
        if fallback:
            message += " (used fallback)"
        return True, message, queue_key

    def request_music(self, request: WSGIRequest) -> HttpResponse:
        """Endpoint to request music. Calls internal function."""
        key = request.POST.get("key")
        query = request.POST.get("query")
        playlist = request.POST.get("playlist") == "true"
        platform = request.POST.get("platform")

        if query is None or not platform:
            return HttpResponseBadRequest(
                "query, playlist and platform have to be specified."
            )
        ikey = None
        if key:
            ikey = int(key)

        # only get ip on user requests
        if self.base.settings.basic.logging_enabled:
            request_ip, _ = ipware.get_client_ip(request)
            if request_ip is None:
                request_ip = ""
        else:
            request_ip = ""

        successful, message, queue_key = self.do_request_music(
            request_ip, query, ikey, playlist, platform
        )
        if not successful:
            return HttpResponseBadRequest(message)
        return JsonResponse({"message": message, "key": queue_key})

    def request_radio(self, request: WSGIRequest) -> HttpResponse:
        """Endpoint to request radio for the current song."""
        # only get ip on user requests
        if self.base.settings.basic.logging_enabled:
            request_ip, _ = ipware.get_client_ip(request)
            if request_ip is None:
                request_ip = ""
        else:
            request_ip = ""

        try:
            current_song = CurrentSong.objects.get()
        except CurrentSong.DoesNotExist:
            return HttpResponseBadRequest("Need a song to play the radio")
        provider = SongProvider.create(self, external_url=current_song.external_url)
        return provider.request_radio(request_ip)

    def index(self, request: WSGIRequest) -> HttpResponse:
        """Renders the /musiq page."""
        context = self.base.context(request)
        context["urls"] = self.urlpatterns
        context["additional_keywords"] = self.base.settings.basic.additional_keywords
        context["forbidden_keywords"] = self.base.settings.basic.forbidden_keywords
        context["embed_stream"] = self.base.settings.basic.embed_stream
        context[
            "dynamic_embedded_stream"
        ] = self.base.settings.basic.dynamic_embedded_stream
        return render(request, "musiq.html", context)

    def state_dict(self) -> Dict[str, Any]:
        state_dict = self.base.state_dict()

        musiq_state = {}
        current_song: Optional[Dict[str, Any]]
        try:
            current_song = model_to_dict(CurrentSong.objects.get())
            current_song = util.camelize(current_song)
            current_song["durationFormatted"] = song_utils.format_seconds(
                current_song["duration"]
            )
        except CurrentSong.DoesNotExist:
            current_song = None

        song_queue = []
        total_time = 0
        all_songs = self.queue.all()
        if self.base.settings.basic.voting_system:
            all_songs = all_songs.order_by("-votes", "index")
        for song in all_songs:
            song_dict = model_to_dict(song)
            song_dict = util.camelize(song_dict)
            song_dict["durationFormatted"] = song_utils.format_seconds(
                song_dict["duration"]
            )
            song_queue.append(song_dict)
            if song_dict["duration"] < 0:
                # skip duration of placeholders
                continue
            total_time += song_dict["duration"]
        musiq_state["totalTimeFormatted"] = song_utils.format_seconds(total_time)

        if state_dict["alarm"]:
            musiq_state["currentSong"] = {
                "queueKey": -1,
                "manuallyRequested": False,
                "votes": None,
                "internalUrl": "",
                "externalUrl": "",
                "artist": "Raveberry",
                "title": "ALARM!",
                "duration": 10,
                "created": "",
            }
        elif self.playback.backup_playing.is_set():
            musiq_state["currentSong"] = {
                "queueKey": -1,
                "manuallyRequested": False,
                "votes": None,
                "internalUrl": "",
                "externalUrl": self.base.settings.sound.backup_stream,
                "artist": "",
                "title": "Backup Stream",
                "duration": 60 * 60 * 24,
                "created": "",
            }
        else:
            musiq_state["currentSong"] = current_song
        musiq_state["paused"] = self.playback.paused()
        musiq_state["progress"] = self.playback.progress()
        musiq_state["shuffle"] = self.controller.shuffle
        musiq_state["repeat"] = self.controller.repeat
        musiq_state["autoplay"] = self.controller.autoplay
        musiq_state["volume"] = self.controller.volume
        musiq_state["songQueue"] = song_queue

        state_dict["musiq"] = musiq_state
        return state_dict
