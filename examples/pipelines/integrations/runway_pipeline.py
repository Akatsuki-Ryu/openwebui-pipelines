"""
title: Runway AI Pipeline
author: Akatsuki.Ryu
author_url: https://github.com/akatsuki-ryu
sponsor: Digitalist Open Tech
date: 2024-11-26
version: 1.0
license: MIT
description: Integrate Runway AI Video Generation API
requirements: runwayml
"""

import time
from typing import Any, Dict, Optional, Union, Generator, Iterator,Union,Iterator,List
from pydantic import BaseModel
from runwayml import RunwayML
import os
import json



class Pipeline:
    """Pipeline for generating videos using Runway AI."""

    class Valves(BaseModel):
        RUNWAYML_API_SECRET: str

    def __init__(self):
        self.name = "Runway AI Pipeline"
        self.valves = self.Valves(RUNWAYML_API_SECRET=os.getenv("RUNWAYML_API_SECRET", ""))
        self.client = None

    async def on_startup(self):
        """Initialize the Runway client."""
        print(f"on_startup:{__name__}")
        self.client = RunwayML()

    async def on_shutdown(self):
        """Cleanup resources."""
        print(f"on_shutdown:{__name__}")

    def pipe(
        self,
        user_message: str,
        model_id: str,
        messages: List[dict],
        body: dict,
        polling_interval: int = 10,  # in seconds
        **kwargs: Any,
    ) -> Union[str, Generator, Iterator]:
        """
        Generate a video from an image using Runway AI.

        Args:
            prompt_image: URL or path to the input image
            prompt_text: Text description for the video generation
            model_id: The Runway model to use (default: gen3a_turbo)
            polling_interval: Time in seconds between polling for task status
            **kwargs: Additional arguments to pass to the Runway API

        Returns:
            PipelineResult containing the generated video information
        """
        print(f"pipe:{__name__}")

        try:
            # Hardcoded reference image path - replace with your actual image path
            reference_image_path = "https://freedesignfile.com/upload/2017/06/Women-working-in-the-office-Stock-Photo.jpg"


            # Create image-to-video task
            task = self.client.image_to_video.create(
                model="gen3a_turbo",
                prompt_image=reference_image_path,
                prompt_text="lady working in the office",
            )
            task_id = task.id

            # Poll until task completion
            time.sleep(polling_interval)
            task = self.client.tasks.retrieve(task_id)
            
            while task.status not in ["SUCCEEDED", "FAILED"]:
                time.sleep(polling_interval)
                task = self.client.tasks.retrieve(task_id)
            
            print('Task complete:', task)

            if hasattr(task, "output") and task.output and len(task.output) > 0:
                video_url = task.output[0]  # The video URL is the first item in the output list
                if video_url:
                    return f"{video_url}"
                    # return json.dumps({
                    #     "success": True,
                    #     "data": {
                    #         "task_id": task_id,
                    #         "status": task.status,
                    #         "video_url": video_url
                    #     }
                    # })
            
            return json.dumps({
                        "success": False,
                        "error": "Task completed but no result found.",
                    })
        except Exception as e:
            return json.dumps({
                        "success": False,
                        "error": f"Error generating video: {str(e)}",
                    })

    def validate_config(self) -> Optional[str]:
        """Validate the pipeline configuration."""
        if not self.config:
            return "Configuration is required"
        return None
