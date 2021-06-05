# EVB-API-py

Asynchronous wrapper for the EditVideoBot API https://pigeonburger.xyz/api/docs/

### Example

```python
import asyncio
from evb import Commands, AsyncEditVideoBotSession


async def main():
    async with AsyncEditVideoBotSession.from_api_key("your_api_key") as evb_session:
        output_bytes = await evb_session.edit(
            open("input.mp4", "rb"), [Commands.TOP_TEXT.value("smellular api wrapper")]
        )

    with open("output.mp4", "xb") as output_media:
        output_media.write(output_bytes)

asyncio.run(main())
```
