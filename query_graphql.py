from base64 import b64decode
import io
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import asyncio


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
    flag = True
    while flag:
        try:
            result = await client.execute_async(query)
        except:
            pass
    img = result["getDaily"]["image"]

    file = io.BytesIO(b64decode(img[9:]))
    return file


async def query_artifact_domains():
    transport = AIOHTTPTransport(
        url="https://painmon-api.herokuapp.com/graphql", headers={"content-type": "application/json"})

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    query = gql(
        """
        query {
            getAllDomainCategory {
                name
                domains {
                    name
                }
                artifacts
            }
        }
        """
    )

    # Execute the query on the transport
    flag = True
    while flag:
        try:
            result = await client.execute_async(query)
            flag = False
        except:
            pass
    ret = {}
    for domain in result["getAllDomainCategory"]:
        ret[domain["name"]] = "/".join(x.replace("_", " ").title()
                                       for x in domain["artifacts"])
    return ret


async def query_weapon_materials_book():
    transport = AIOHTTPTransport(
        url="https://painmon-api.herokuapp.com/graphql", headers={"content-type": "application/json"})

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    query = gql(
        """
        query {
            getDaily {
                materials {
                    name
                    domain
                    type
                    items {
                        name
                    }
                }
            }
        }
        """
    )

    # Execute the query on the transport
    flag = True
    while flag:
        try:
            result = await client.execute_async(query)
            flag = False
        except:
            pass
    weapon = {}
    book = {}
    result = result["getDaily"]['materials']
    for material in result:
        if material["type"] == "book":
            if material["domain"] not in book:
                book[material["domain"]] = []
            book[material["domain"]].append(material["name"])
        elif material["type"] == "weapon":
            if material["domain"] not in weapon:
                weapon[material["domain"]] = []
            weapon[material["domain"]].append(material["name"])
    for key, item in book.items():
        book[key] = "/".join(item)
    for key, item in weapon.items():
        weapon[key] = "/".join(item)
    return weapon, book


if __name__ == "__main__":
    print(asyncio.run(query_weapon_materials_book()))
