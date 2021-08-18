# evb.py

Asynchronous wrapper for the EditVideoBot API https://pigeonburger.xyz/api/docs/

### Example

```python
import asyncio
from evb import AsyncEditVideoBotSession, EditResponse


async def main():
    with open("input.mp4", "rb") as input_file:
        input_bytes = input_file.read()
        
    async with AsyncEditVideoBotSession.from_api_key("your_api_key") as evb_session:
        output_bytes: EditResponse = await evb_session.edit(input_bytes, "tt=smell")

    with open("output.mp4", "xb") as output_media:
        output_media.write(await output_bytes.download())

asyncio.run(main())
```
