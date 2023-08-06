"""Prepare SQLite WHERE clauses for use in model filtering.

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
import re
from typing import Dict, List, Pattern


def add_quotes(text: str) -> str:
    """Add double quotes to the start and end of a string.

    Double quotes will not be added to indexes that already contain
    them.

    Parameters
    ----------
    text
        The string to wrap in double quotes.

    Returns
    -------
    str
        The string wrapped in double quotes.

    """
    if not text.startswith("\""):
        text = "\"" + text
    if not text.endswith("\""):
        text = text + "\""
    return text


def escape_query(query: str) -> str:
    """Escape special SQLite characters appearing in the query.

    A backslash will be added before each instance of '%' and '_'
    appearing in the query.

    Parameters
    ----------
    query
        The query potentially containing special characters.

    Returns
    -------
    str
        The query with all instances of '%' and '_' escaped.

    Notes
    -----
    When the final WHERE clause is assembled, any characters preceded
    by the designated ESCAPE character (a backslash), will be treated
    literally.

    See Also
    --------
    handle_regular_query :
        Create a valid SQLite WHERE clause based on the regular query.
    handle_special_query :
        Create a valid SQLite WHERE clause based on the special query.

    """
    return query.replace("%", "\\%").replace("_", "\\_")


def expand_query(query: str) -> str:
    """Convert an unexpanded query into its expanded equivalent.

    The expanded query uses the same search syntax as if each column
    had been explicitly included in the search.

    Parameters
    ----------
    query
        The query containing one or more expansion abbreviations.

    Returns
    -------
    str
        The expanded query.

    Warnings
    --------
    It is not recommended to use expanding and non-expanding queries
    in the same search. When a query is expanded, no parentheses are
    placed around the expansion, which can lead to unexpected results.
    See Example 2.

    Examples
    --------
    Example 1: Standard usage.

    >>> expand_query('"genre":"x"')
    '"genre one":"x" or "genre two":"x" or "genre three":"x"'

    Example 2: Expanding and non-expanding queries should not be used
    in the same query.

    >>> expand_query('"cast":"x" and "runtime":"y"')
    '"cast one":"x" or "cast two":"x" or "cast three":"x" and
    "runtime":"y"'

    The result above is intended behavior. However, one might expect
    the search to operate in the following manner (notice the
    parentheses):

    ("cast one":"x" or "cast two":"x" or "cast three":"x") and
    "runtime":"y"

    See Also
    --------
    is_expanding_query : Determine if the query should be expanded.

    """
    subqueries = get_subqueries(query, True)
    cast_regex = re.compile(r"\"cast\":\"(.*)\"", re.IGNORECASE)
    genre_regex = re.compile(r"\"genre\":\"(.*)\"", re.IGNORECASE)
    operator_regex = re.compile(r"^\"?(and|or)\"?$", re.IGNORECASE)
    for index, subquery in enumerate(subqueries):
        cast_query_mo = cast_regex.search(subquery)
        if cast_query_mo is not None:
            expanded_query = prepare_expansion("cast", cast_regex, subquery)
            subqueries[index] = expanded_query

        genre_query_mo = genre_regex.search(subquery)
        if genre_query_mo is not None:
            expanded_query = prepare_expansion("genre", genre_regex, subquery)
            subqueries[index] = expanded_query

        operator_mo = operator_regex.search(subquery)
        if operator_mo is not None:
            formatted_operator = remove_quotes(operator_mo.group(0))
            subqueries[index] = formatted_operator
    return " ".join(subqueries)


def format_header_name(header_name: str) -> str:
    """Convert a raw header to the correct display format.

    Parameters
    ----------
    header_name
        The header name to format.

    Returns
    -------
    str
        The header name formatted to exactly match a display header
        name.

    """
    if "id" in header_name:
        header_name = header_name.upper()
    else:
        header_name = header_name.capitalize()
    return header_name


def get_special_operators(query: str) -> List[str]:
    """Retrieve instances of 'and' or 'or' in special queries.

    Parameters
    ----------
    query
        A query containing special query syntax.

    Returns
    -------
    list of str
        The operators in order of appearance from left to right.

    """
    operators_regex = re.compile(r"\"\s(and|or)\s\"", re.IGNORECASE)
    operators = operators_regex.findall(query)
    return operators


def get_subqueries(query: str, operators: bool) -> List[str]:
    """Split a query into subqueries, optionally including operators.

    Parameters
    ----------
    query
        A query containing special query syntax.
    operators
        Whether or not to include operators in the list of subqueries.

    Returns
    -------
    list of str
        The individual subqueries that make up `query`.

    """
    subquery_regex = re.compile(r"\"\s(and|or)\s\"", re.IGNORECASE)
    subqueries = subquery_regex.split(query)
    temps = []
    for subquery in subqueries:
        temp = subquery
        temp = add_quotes(temp)
        if temp.lower() == "\"and\"" or temp.lower() == "\"or\"":
            if not operators:
                continue
        temps.append(temp.strip())
    return temps


def handle_regular_query(query: str, headers: Dict[str, str]) -> str:
    """Create a valid SQLite WHERE clause based on a regular query.

    Parameters
    ----------
    query
        A query that does not contain special query syntax.
    headers
        Header names, as displayed in QTableView, mapped to database
        column names.

    Returns
    -------
    str
        A SQLite WHERE clause that searches across all database
        columns. Intended for use with QSqlTableModel.setFilter.

    """
    formatted_query = escape_query(query.strip())
    sql_substrings = [
        f"{column} LIKE \"%{formatted_query}%\" ESCAPE \'\\\' OR "
        for column in headers.values()
    ]
    sql_string = "".join(sql_substrings)[:-4]
    return sql_string


def handle_special_query(query: str, headers: Dict[str, str]) -> str:
    """Create a valid SQLite WHERE clause based on a special query.

    Parameters
    ----------
    query
        A query that contains valid special query syntax.
    headers
        Header names, as displayed in QTableView, mapped to database
        column names.

    Returns
    -------
    str
        A SQLite WHERE clause that searches across only specified
        database columns. Intended for use with
        QSqlTableModel.setFilter.

    """
    formatted_query = escape_query(query.strip())
    subqueries = get_subqueries(formatted_query, False)
    operators = get_special_operators(formatted_query)

    if not is_valid_special_query(subqueries, operators, headers):
        raise ValueError("Expression is not a valid special query.")

    query_regex = re.compile(r"\"(.*)\":\"(.*)\"", re.IGNORECASE)
    noop_sql_substrings = []
    for subquery in subqueries:
        query_mo = query_regex.search(subquery)
        assert query_mo is not None

        header_name = query_mo.group(1).lower()
        formatted_header_name = format_header_name(header_name)
        column = headers[formatted_header_name]
        term = query_mo.group(2)

        noop_sql_substrings.append(
            f"{column} LIKE \"%{term}%\" ESCAPE \'\\\' OPERATOR "
        )

    operator_regex = re.compile(r"OPERATOR")
    sql_substrings = []
    for index, substring in enumerate(noop_sql_substrings):
        if index == len(operators):
            sql_substrings.append(substring)
        else:
            sub = operator_regex.sub(operators[index].upper(), substring)
            sql_substrings.append(sub)
    sql_string = "".join(sql_substrings)[:-10]
    return sql_string


def is_expanding_query(query: str) -> bool:
    """Determine if a query should be expanded.

    Expanding queries are denoted by the syntax '"cast":"x"' or
    '"genre":"x"'.

    Parameters
    ----------
    query
        A raw query.

    Returns
    -------
    bool
        True if the query should be expanded, False if not.

    Notes
    -----
    The database contains three cast columns and three genre columns.
    To avoid having to create a tediously long query to search across
    a category's three columns, two abbreviations ('cast' and 'genre')
    can be used instead. The existence of such abbreviations, along
    with the correct syntax, marks the query as needing to expanded
    into its equivalent long form.

    """
    if "\"cast\":" in query or "\"genre\":" in query:
        return True
    else:
        return False


def is_special_query(query: str, headers: Dict[str, str]) -> bool:
    """Determine if the query contains any special query syntax.

    Special queries are denoted by the syntax: '"x":', where 'x'
    is a header name. Regular queries are those that are not special
    queries.

    Parameters
    ----------
    query
        A query potentially containing special query syntax.
    headers
        Header names, as displayed in QTableView, mapped to database
        column names.

    Returns
    -------
    bool
        True if the query contains any special query syntax, False if
        not.

    Notes
    -----
    This function does not check whether or not any special query
    syntax found is valid.

    See Also
    --------
    is_valid_special_query : Determine if the special query is valid.

    """
    for header in headers.keys():
        if (
            f"\"{header.lower()}\":" in query.lower()
            or "\"cast\":" in query.lower()
            or "\"genre\":" in query.lower()
        ):
            return True
    return False


def is_valid_special_query(
    subqueries: List[str],
    operators: List[str],
    headers: Dict[str, str],
) -> bool:
    """Determine if the special query is valid.

    To be considered valid, a special query must be entirely correct.

    Parameters
    ----------
    subqueries
        The query split on operators.
    operators
        The operators on which the query was split.
    headers
        Header names, as displayed in QTableView, mapped to database
        column names.

    Returns
    -------
    bool
        True if the entire special query is valid, False if not.

    See Also
    --------
    is_special_query :
        Determine if the query contains any special query syntax.

    """
    all_headers = [header.lower() for header in headers.keys()]
    all_headers.append("cast")
    all_headers.append("genre")

    subquery_regex = re.compile(r"\"(.*)\":\"(.*)\"", re.IGNORECASE)
    for subquery in subqueries:
        subquery_mo = subquery_regex.search(subquery)
        if subquery_mo is None:
            return False

        user_header = subquery_mo.group(1).lower()
        if user_header not in all_headers:
            return False

    for operator in operators:
        if operator.lower() not in ["and", "or"]:
            return False
    return True


def prepare_expansion(abbrev: str, regex: Pattern[str], text: str) -> str:
    """Convert unexpanded text into its expanded form.

    Parameters
    ----------
    abbrev: {'cast', 'genre'}
        The display name to expand.
    regex
        The regex used to locate search terms.
    text
        The text to expand.

    Returns
    -------
    str
        The text in its expanded form, suitable for replacement.

    """
    text_mo = regex.search(text)
    assert text_mo is not None
    expansion = (
        f"\"{abbrev} one\":\"{text_mo.group(1)}\" "
        f"or \"{abbrev} two\":\"{text_mo.group(1)}\" "
        f"or \"{abbrev} three\":\"{text_mo.group(1)}\""
    )
    expanded_query = regex.sub(text, expansion)
    return expanded_query


def remove_quotes(text: str) -> str:
    """Remove double quotes from the start and end of a string.

    Quotes will not be removed if the result would be an empty string.

    Parameters
    ----------
    text
        The string from which to remove double quotes.

    Returns
    -------
    str
        The string with no quotes at the beginning or ending indices.

    """
    if text == "\"\"":
        return text
    if text.startswith("\""):
        text = text[1:]
    if text.endswith("\""):
        text = text[:-1]
    return text


def main(query: str, headers: Dict[str, str]) -> str:
    """Create a valid SQLite WHERE clause from a raw query.

    This function will handle a raw query, start-to-finish, performing
    any necessary expansions and formatting.

    Parameters
    ----------
    query
        The raw query.
    headers
        Header names, as displayed in QTableView, mapped to database
        column names.

    Returns
    -------
    str
        A SQLite WHERE clause used to search across database columns.
        Intended for use with QSqlTableModel.setFilter.

    """
    if is_expanding_query(query):
        query = expand_query(query)

    if is_special_query(query, headers):
        sql_string = handle_special_query(query, headers)
    else:
        sql_string = handle_regular_query(query, headers)
    return sql_string
