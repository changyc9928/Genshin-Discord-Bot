from base64 import b64decode
import io
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


async def query_image():
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(
        url="https://painmon-api.herokuapp.com/graphql", headers={"content-type": "application/json"})

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    query = gql(
        """
        query {
            getDaily{
                image
            }
        }
        """
    )

    # Execute the query on the transport
    result = await client.execute_async(query)
    img = result["getDaily"]["image"]

    file = io.BytesIO(b64decode(img[9:]))
    return file
