import logging
from dataclasses import dataclass
from typing import Dict, FrozenSet, List

try:
    from slack_sdk import WebClient
except ImportError:
    print("Please install metaphor[slack] extra\n")
    raise

from metaphor.common.event_util import EventUtil
from metaphor.common.extractor import BaseExtractor, RunConfig
from metaphor.common.metadata_change_event import (
    EntityType,
    MetadataChangeEvent,
    Person,
    PersonLogicalID,
    PersonSlackProfile,
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass
class SlackRunConfig(RunConfig):
    oauth_token: str

    # How many users to fetch per page
    page_size: int = 100

    # Include deleted users
    include_deleted: bool = False

    # Exclude the default Slack bot, which is weirdly not marked as "is_bot".
    excluded_ids: FrozenSet[str] = frozenset(["USLACKBOT"])


class SlackExtractor(BaseExtractor):
    """Slack directory extractor"""

    async def extract(self, config: RunConfig) -> List[MetadataChangeEvent]:
        assert isinstance(config, SlackRunConfig)

        logger.info("Fetching directory data from Slack")

        persons = []
        for user in self.list_all_users(config):
            # Filter out bots & delete users, and specific IDs based on config
            if user["is_bot"]:
                continue

            if user["deleted"] and not config.include_deleted:
                continue

            if user["id"] in config.excluded_ids:
                continue

            slack_profile = PersonSlackProfile(
                slack_id=user["id"],
                team_id=user["team_id"],
                username=user["name"],
                deleted=user["deleted"],
            )

            email = user["profile"].get("email", None)
            if email is None:
                logging.warn(f"Skipping user {user['id']} without email address")
                continue

            persons.append(
                Person(
                    entity_type=EntityType.PERSON,
                    logical_id=PersonLogicalID(email=email),
                    slack_profile=slack_profile,
                )
            )

        return [EventUtil.build_person_event(p) for p in persons]

    def list_all_users(self, config: SlackRunConfig) -> List[Dict]:
        users = []
        next_cursor = None
        while True:
            client = WebClient(token=config.oauth_token)
            response = client.users_list(limit=config.page_size, cursor=next_cursor)
            users.extend(response["members"])
            next_cursor = response["response_metadata"].get("next_cursor", "")
            if next_cursor == "":
                return users
