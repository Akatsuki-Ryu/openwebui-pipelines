"""
title: Replicate Flux Pipeline
author: Akatsuki.Ryu
date: 2024-10-07
version: 1.0
license: MIT
description: Integrate Replicate Flux API
requirements: pydantic, replicate
"""

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import replicate
import os
import base64
from io import BytesIO

class Pipeline:
    class Valves(BaseModel):
        REPLICATE_API_TOKEN: str

    def __init__(self):
        self.name = "Replicate Flux Pipeline"
        self.valves = self.Valves(REPLICATE_API_TOKEN=os.getenv("REPLICATE_API_TOKEN",""))

    async def on_startup(self):
        print(f"on_startup:{__name__}")

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        print(f"pipe:{__name__}")

        # Replicateを使用して画像を生成
        try:
            output = replicate.run(
                "black-forest-labs/flux-1.1-pro",
                input={"prompt": user_message}
            )

            # 画像URLを取得
            print(output)
            message = f"![image]({output})\n"
            return message
            

        except Exception as e:
            return f"Error generating image: {str(e)}"
