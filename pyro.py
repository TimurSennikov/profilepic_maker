import os
import io
import asyncio

from images import VideoParser

from pyrogram import Client

app = Client(name="Zemfirnij", api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"), no_updates=True)

async def tinker_avatars(start: int = 0):
    v = VideoParser("input.mp4", True)
    if start > 0:
        v.skip_to(start)

    c = v.count

    async with app:
        for i in range(c):
            success_upload = False

            img = v.next()

            buf = io.BytesIO()
            img.save(buf, format="PNG")

            while not success_upload:
                try:
                    print(f"Setting photo {v.count} / {v.frames} ... ", end="")
                    await app.set_profile_photo(photo=buf)
                    success_upload = True
                    print("✅")
                    await asyncio.sleep(30)
                except Exception as e:
                    success_upload = False

                    print(f"ERROR ON {v.count} / {v.frames} !")
                    print(e)
                    await asyncio.sleep(5)
