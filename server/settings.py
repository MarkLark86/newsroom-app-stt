import os
import pathlib

from flask_babel import lazy_gettext
from newsroom.types import AuthProviderType
from newsroom.web.default_settings import (
    ELASTICSEARCH_SETTINGS,
    CONTENTAPI_ELASTICSEARCH_SETTINGS,
    BLUEPRINTS as DEFAULT_BLUEPRINT,
    CORE_APPS as DEFAULT_CORE_APPS,
    CELERY_BEAT_SCHEDULE as CELERY_BEAT_SCHEDULE_DEFAULT,
    CLIENT_LOCALE_FORMATS,
    AUTH_PROVIDERS,
    WIRE_TIME_FILTERS,
    AGENDA_SEARCH_FIELDS,
    CLIENT_CONFIG,
)

SERVER_PATH = pathlib.Path(__file__).resolve().parent
CLIENT_PATH = SERVER_PATH.parent.joinpath("client")
TRANSLATIONS_PATH = SERVER_PATH.joinpath("translations")

SITE_NAME = "Mediapankki"
COPYRIGHT_HOLDER = "STT"

USER_MANUAL = "https://stt.fi/ajankohtaista-tietoa-media-asiakkaille/stt-mediapankki/"
PRIVACY_POLICY = PRIVACY_POLICY_EN = "https://stt.fi/tietosuoja/"
TERMS_AND_CONDITIONS = TERMS_AND_CONDITIONS_EN = "https://stt.fi/kayttoehdot/"
CONTACT_ADDRESS = "https://stt.fi/yhteystiedot/"
CONTACT_ADDRESS_EN = "https://stt.fi/en/contact/"

INSTALLED_APPS = [
    "stt.external_links",
    "stt.filters",
    "stt.signals",
    "newsroom.auth.saml",
]

AGENDA_GROUPS = [
    {
        "field": "sttdepartment",
        "label": lazy_gettext("Department"),
        "nested": {
            "parent": "subject",
            "field": "scheme",
            "value": "sttdepartment",
            "include_planning": True,
        },
        "permissions": [],
    },
    {
        "field": "sttsubj",
        "label": lazy_gettext("Subject"),
        "nested": {
            "parent": "subject",
            "field": "scheme",
            "value": "sttsubj",
            "include_planning": True,
        },
        "permissions": [],
    },
    {
        "field": "event_type",
        "label": lazy_gettext("Event Type"),
        "nested": {
            "parent": "subject",
            "field": "scheme",
            "value": "event_type",
        },
        "permissions": [],
    },
    {
        "field": "stturgency",
        "label": lazy_gettext("Importance"),
        "nested": {
            "parent": "subject",
            "field": "scheme",
            "value": "stturgency",
            "include_planning": True,
        },
        "permissions": ["coverage_info"],
    },
]

WIRE_GROUPS = [
    {
        "field": "sttdepartment",
        "label": lazy_gettext("Department"),
        "nested": {
            "parent": "subject",
            "field": "scheme",
            "value": "sttdepartment",
        },
    },
    {
        "field": "genre",
        "label": lazy_gettext("Genre"),
    },
    {
        "field": "sttversion",
        "label": lazy_gettext("Version"),
        "nested": {
            "parent": "subject",
            "field": "scheme",
            "value": "sttversion",
        },
    },
]

WIRE_AGGS = {
    "genre": {"terms": {"field": "genre.name", "size": 50}},
    "_subject": {
        "terms": {"field": "subject.name", "size": 50}
    },  # it's needed for nested groups
}

CORE_APPS = [
    app
    for app in DEFAULT_CORE_APPS
    if app
    not in [
        "newsroom.monitoring",
        "newsroom.company_expiry_alerts",
    ]
]

BLUEPRINTS = [
    blueprint
    for blueprint in DEFAULT_BLUEPRINT
    if blueprint
    not in [
        "newsroom.monitoring",
    ]
]

LANGUAGES = ["fi", "en"]
DEFAULT_LANGUAGE = "fi"

COMPANY_TYPES = [
    dict(
        id="premium",
        name="Premium",
        # no filter, gets all
    ),
    dict(
        id="non-premium",
        name="Non-premium",
        wire_must_not={
            "bool": {
                "filter": [  # filter out
                    {"term": {"sttdone1": "5"}},  # premium
                    {"range": {"embargoed": {"gte": "now"}}},  # with embargo
                ]
            }
        },
    ),
    dict(
        id="non-media",
        name="Non-media",
        wire_must_not={"range": {"embargoed": {"gte": "now"}}},  # filter out embargo
    ),
]

SHOW_DATE = False

WATERMARK_IMAGE = None

CELERY_BEAT_SCHEDULE = {
    key: val
    for key, val in CELERY_BEAT_SCHEDULE_DEFAULT.items()
    if key == "newsroom.company_expiry"
}

ENABLE_WATCH_LISTS = False

NEWS_API_ENABLED = True

# SDAN-695
ELASTICSEARCH_SETTINGS["settings"]["query_string"] = {"analyze_wildcard": True}

PREPEND_EMBARGOED_TO_WIRE_SEARCH = True

SAML_CLIENTS = [
    "eduskunta",
]

CLIENT_LOCALE_FORMATS["fi"] = {
    "TIME_FORMAT": "H.mm",
    "DATE_FORMAT": "D.M.YYYY",
    "DATETIME_FORMAT": "H.mm D.M.YYYY",
    "COVERAGE_DATE_FORMAT": "D.M.YYYY",
    "COVERAGE_DATE_TIME_FORMAT": "H.mm D.M.YYYY",
    # server formats
    "DATE_FORMAT_HEADER": "d.M.yyyy H.mm",
    "NOTIFICATION_EMAIL_TIME_FORMAT": "H.mm",
    "NOTIFICATION_EMAIL_DATE_FORMAT": "d.M.yyyy",
    "NOTIFICATION_EMAIL_DATETIME_FORMAT": "d.M.yyyy klo H.mm",
}

ELASTICSEARCH_TRACK_TOTAL_HITS = (
    int(os.environ["ELASTICSEARCH_TRACK_TOTAL_HITS"])
    if os.environ.get("ELASTICSEARCH_TRACK_TOTAL_HITS")
    else True
)

AUTH_PROVIDERS.append(
    {
        "_id": "azure",
        "name": lazy_gettext("Azure"),
        "auth_type": AuthProviderType.SAML,
    }
)

CONTENTAPI_ELASTICSEARCH_SETTINGS["settings"]["analysis"]["analyzer"][
    "html_field_analyzer"
]["filter"] = ["lowercase"]

AGENDA_HIDE_COVERAGE_ASSIGNEES = True
AGENDA_DEFAULT_FILTER_HIDE_PLANNING = True

SAML_AUTH_ENABLED = bool(os.environ.get("SAML_PATH", False))

WIRE_TIME_FILTERS.extend(
    [
        {
            "name": "2020-",
            "filter": "2020-2029",
            "default": False,
            "query": {
                "gte": "2019-12-31T22:00:00",
            },
        },
        {
            "name": "2010-2019",
            "filter": "2010-2019",
            "default": False,
            "query": {
                "gte": "2009-12-31T22:00:00",
                "lt": "2019-12-31T22:00:00",
            },
        },
        {
            "name": "2000-2009",
            "filter": "2000-2009",
            "default": False,
            "query": {
                "gte": "1999-12-31T22:00:00",
                "lt": "2009-12-31T22:00:00",
            },
        },
        {
            "name": "1992-1999",
            "filter": "1992-1999",
            "default": False,
            "query": {
                "gte": "1989-12-31T22:00:00",
                "lt": "1999-12-31T22:00:00",
            },
        },
    ]
)

# STTNHUB-375
AGENDA_SEARCH_FIELDS.append("invitation_details")


CLIENT_CONFIG.update(
    {
        "show_coverage_latest_version_only": False,
    },
)
