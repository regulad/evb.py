# EVB-API-py

Asynchronous wrapper for the EditVideoBot API https://pigeonburger.xyz/api/docs/

### Example

```python
import asyncio
from evb import Commands, AsyncEditVideoBotSession


async def main():
    with open("input.mp4", "rb") as input_media:
        input_bytes = input_media.read()

    async with AsyncEditVideoBotSession.from_api_key("your_api_key") as evb_session:
        output_bytes = await evb_session.edit(input_bytes, [Commands.TOP_TEXT.value("smellular api wrapper")])

    with open("output.mp4", "xb") as output_media:
        output_media.write(output_bytes)

asyncio.run(main())
```
