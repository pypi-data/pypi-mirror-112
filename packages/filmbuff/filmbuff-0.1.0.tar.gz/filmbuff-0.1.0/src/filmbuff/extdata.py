"""Search for and parse film metadata from an external source.

Copyright (C) 2021 emerac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
from typing import Any, Dict, List, Optional, cast

import requests


def get_cast(data: Dict[str, Any]) -> List[Optional[str]]:
    """Retrieve the top three cast members' names.

    Parameters
    ----------
    data
        Film credits obtained from TMDb.

    Returns
    -------
    list of str, optional
        The top three cast members' names, if they exist in the data.

    """
    top_three: List[Optional[str]] = [None for i in range(3)]
    for index, cast_member in enumerate(data["credits"]["cast"]):
        if index > 2:
            break
        top_three[index] = cast_member.get("name")
    return top_three


def get_director(data: Dict[str, Any]) -> Optional[Any]:
    """Retrieve the director's name.

    Parameters
    ----------
    data
        Film credits obtained from TMDb.

    Returns
    -------
    str, optional
        The director's name, if it exists in the data.

    """
    for member in data["credits"]["crew"]:
        if member["job"] == "Director":
            return member["name"]
    return None


def get_film_info(key: str, film_id: int) -> Dict[str, Any]:
    """Retrieve film details and credits.

    Parameters
    ----------
    key
        A valid TMDb API key.
    film_id
        The TMDb ID for a specific film.

    Returns
    -------
    dict
        JSON film details and credits for a specific film.

    Raises
    ------
    requests.exceptions.HTTPError
        If a bad request (4XX client or 5XX server error) was made
    requests.exceptions.Timeout
        If the server has not responded in N seconds

    """
    url = "https://api.themoviedb.org/3/movie/" + str(film_id)
    query_string = {
        "api_key": key,
        "append_to_response": "credits",
    }
    r = requests.get(url, params=query_string, timeout=3)
    r.raise_for_status()
    return cast(Dict[str, Any], r.json())


def get_genres(data: Dict[str, Any]) -> List[Optional[str]]:
    """Retrieve the top three genres.

    Parameters
    ----------
    data
        Film details obtained from TMDb.

    Returns
    -------
    list of str, optional
        The top three genres' names, if they exist in the data.

    """
    top_three: List[Optional[str]] = [None for i in range(3)]
    for index, genre in enumerate(data["genres"]):
        if index > 2:
            break
        top_three[index] = genre.get("name")
    return top_three


def get_search_results(
    key: str,
    query: str,
    year: str,
    page: int,
) -> Dict[str, Any]:
    """Retrieve search results from TMDb that match a query.

    Parameters
    ----------
    key
        A valid TMDb API key.
    query
        Text that may match against a film's title, description, etc.
    year
        Limit the results to films released in a particular year. If
        `year` is an empty string, all years will be considered.
    page
        Display a particular page of search results.

    Returns
    -------
    dict
        JSON search results for a certain page, with approximately 20
        results per page.

    Raises
    ------
    requests.exceptions.HTTPError
        If a bad request (4XX client or 5XX server error) was made
    requests.exceptions.Timeout
        If the server has not responded in N seconds

    """
    url = "https://api.themoviedb.org/3/search/movie"
    query_string = {
        "api_key": key,
        "query": query,
        "year": year,
        "page": str(page),
    }
    r = requests.get(url, params=query_string, timeout=3)
    r.raise_for_status()
    return cast(Dict[str, Any], r.json())
