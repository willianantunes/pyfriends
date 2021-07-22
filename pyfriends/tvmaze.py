import logging
import os

from dataclasses import dataclass
from datetime import date
from typing import List
from typing import Optional

from bs4 import BeautifulSoup
from requests import RequestException

from pyfriends.http_utils import requests_session

logger = logging.getLogger(__name__)

BASE_ENDPOINT_ADDRESS = os.getenv("TVMAZE_ENDPOINT_API", "https://api.tvmaze.com")
SHOW_INFORMATION_DETAILS = f"{BASE_ENDPOINT_ADDRESS}/shows/{{id}}"
SHOW_SEASONS = f"{BASE_ENDPOINT_ADDRESS}/shows/{{id}}/seasons"
SHOW_CAST = f"{BASE_ENDPOINT_ADDRESS}/shows/{{id}}/cast"
SHOW_EPISODE_DETAILS = f"{BASE_ENDPOINT_ADDRESS}/shows/{{id}}/episodebynumber?season={{season}}&number={{episode}}"
SHOW_EPISODES = f"{BASE_ENDPOINT_ADDRESS}/seasons/{{id}}/episodes"


@dataclass(frozen=True)
class Network:
    name: str
    country: str


@dataclass(frozen=True)
class Show:
    name: str
    genres: List[str]
    premiered: date
    summary: str
    network: Network


@dataclass(frozen=True)
class Episode:
    title: str
    air_date: date
    runtime: int
    summary: str
    type: str


@dataclass(frozen=True)
class Season:
    id: int
    number: int
    number_of_episodes: int
    premiered_date: date
    end_date: date


@dataclass(frozen=True)
class Person:
    id: int
    name: str
    country: str
    birthday: date
    gender: str


@dataclass(frozen=True)
class Character:
    id: int
    name: str


@dataclass(frozen=True)
class Cast:
    character: Character
    person: Person


def show_details(identifier: int) -> Optional[Show]:
    # https://www.tvmaze.com/api#show-main-information
    with requests_session() as r:
        url = SHOW_INFORMATION_DETAILS.format(id=identifier)
        try:
            response = r.get(url)
            status_code = response.status_code

            if status_code == 200:
                body = response.json()
                # Network object
                network_details_from_body = body["network"]
                network = Network(network_details_from_body["name"], network_details_from_body["country"]["name"])
                # Cleaning summary because it comes as HTML
                summary_as_html = body["summary"]
                soup = BeautifulSoup(summary_as_html, "html.parser")
                summary = soup.text
                # The final object
                return Show(body["name"], body["genres"], date.fromisoformat(body["premiered"]), summary, network)
            if status_code == 404:
                return None

            raise UnexpectedBehaviorTVMazeAPIException
        except RequestException as e:
            """
            See more details at: https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
            """
            logger.error(f"A network, time-out or HTTP error was caught. Details: {e}")
            raise e


def episode_details(show_identifier: int, season: int, episode: int) -> Optional[Episode]:
    # https://www.tvmaze.com/api#episode-by-number
    with requests_session() as r:
        url = SHOW_EPISODE_DETAILS.format(id=show_identifier, season=season, episode=episode)
        try:
            response = r.get(url)
            status_code = response.status_code

            if status_code == 200:
                body = response.json()
                # Cleaning summary because it comes as HTML
                summary_as_html = body["summary"]
                soup = BeautifulSoup(summary_as_html, "html.parser")
                summary = soup.text
                # Transform and validation
                runtime = body["runtime"]
                assert type(runtime) is int
                air_date = date.fromisoformat(body["airdate"])
                # Final object
                return Episode(body["name"], air_date, body["runtime"], summary, body["type"])
            if status_code == 404:
                return None

            raise UnexpectedBehaviorTVMazeAPIException
        except RequestException as e:
            """
            See more details at: https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
            """
            logger.error(f"A network, time-out or HTTP error was caught. Details: {e}")
            raise e


def all_seasons(show_identifier: int) -> Optional[List[Season]]:
    # https://www.tvmaze.com/api#show-seasons
    with requests_session() as r:
        url = SHOW_SEASONS.format(id=show_identifier)
        try:
            response = r.get(url)
            status_code = response.status_code

            if status_code == 200:
                body = response.json()
                seasons = []
                for season in body:
                    # Transform and validation
                    premiered_date = date.fromisoformat(season["premiereDate"])
                    end_date = date.fromisoformat(season["endDate"])
                    season_id = season["id"]
                    season_number = season["number"]
                    number_of_episodes = season["episodeOrder"]
                    assert type(season_id) is int
                    assert type(season_number) is int
                    assert type(number_of_episodes) is int
                    # Final object
                    season = Season(season_id, season_number, season["episodeOrder"], premiered_date, end_date)
                    seasons.append(season)
                return seasons
            if status_code == 404:
                return None

            raise UnexpectedBehaviorTVMazeAPIException
        except RequestException as e:
            """
            See more details at: https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
            """
            logger.error(f"A network, time-out or HTTP error was caught. Details: {e}")
            raise e


def all_episodes(season_identifier: int) -> Optional[List[Episode]]:
    # https://www.tvmaze.com/api#season-episodes
    with requests_session() as r:
        url = SHOW_EPISODES.format(id=season_identifier)
        try:
            response = r.get(url)
            status_code = response.status_code

            if status_code == 200:
                body = response.json()
                episodes = []
                for episode in body:
                    # Cleaning summary because it comes as HTML
                    summary_as_html = episode["summary"]
                    soup = BeautifulSoup(summary_as_html, "html.parser")
                    summary = soup.text
                    # Transform and validation
                    runtime = episode["runtime"]
                    assert type(runtime) is int
                    air_date = date.fromisoformat(episode["airdate"])
                    # Final object
                    episode = Episode(episode["name"], air_date, episode["runtime"], summary, episode["type"])
                    episodes.append(episode)
                return episodes
            if status_code == 404:
                return None

            raise UnexpectedBehaviorTVMazeAPIException
        except RequestException as e:
            """
            See more details at: https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
            """
            logger.error(f"A network, time-out or HTTP error was caught. Details: {e}")
            raise e


def main_cast(show_identifier: int):
    # https://www.tvmaze.com/api#show-cast
    with requests_session() as r:
        url = SHOW_CAST.format(id=show_identifier)
        try:
            response = r.get(url)
            status_code = response.status_code

            if status_code == 200:
                body = response.json()
                casts = []
                for cast in body:
                    # Transform and validation
                    character_details = cast["character"]
                    character_id = character_details["id"]
                    assert type(character_id) is int
                    character_name = character_details["name"]
                    person_details = cast["person"]
                    person_id = person_details["id"]
                    assert type(person_id) is int
                    person_birthday = date.fromisoformat(person_details["birthday"])
                    person_country = person_details["country"]["name"]
                    # Building object
                    character = Character(character_id, character_details["name"])
                    person = Person(
                        person_id, person_details["name"], person_country, person_birthday, person_details["gender"]
                    )
                    cast = Cast(character, person)
                    casts.append(cast)

                return casts
            if status_code == 404:
                return None

            raise UnexpectedBehaviorTVMazeAPIException
        except RequestException as e:
            """
            See more details at: https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
            """
            logger.error(f"A network, time-out or HTTP error was caught. Details: {e}")
            raise e


class UnexpectedBehaviorTVMazeAPIException(Exception):
    pass
