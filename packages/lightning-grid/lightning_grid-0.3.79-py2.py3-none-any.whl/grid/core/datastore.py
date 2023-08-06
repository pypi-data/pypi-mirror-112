from __future__ import annotations

import typing
from typing import List, Optional

from grid.core.base import GridObject
from grid.exceptions import ResourceNotFound

if typing.TYPE_CHECKING:
    from grid.client import Grid
    from grid.core import Team


class Datastore(GridObject):
    """
    Datastore object in Grid
    """
    def refresh(self):
        pass

    @classmethod
    def get_all(cls, team: Optional['Team'] = None) -> List['Datastore']:
        client: Grid = cls().client

        query = """
            query GetDatastores ($teamId: ID){
                getDatastores(teamId: $teamId) {
                    id
                    credentialId
                    name
                    version
                    size
                    createdAt
                    snapshotStatus
                    userDetails {
                        username
                    }
                }
            }
        """
        if team:
            params = {'teamId': team.id}  # noqa
        else:
            params = {'teamId': None}
        result = client.query(query, **params)
        if not result['getDatastores']:
            raise ResourceNotFound
        datastores = []
        for detail in result['getDatastores']:
            datastore = cls()
            datastore.data = detail
            datastores.append(datastore)
        return datastores
