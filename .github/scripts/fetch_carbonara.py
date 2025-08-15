#!/usr/bin/env python3
"""Generate Carbonara code snippet image for GitHub profile."""

from pathlib import Path

import httpx


async def generate_carbonara_intro():
    """Generate and save Carbonara code snippet image."""

    # Code content
    code = """console.log("Hi there 👋");

// I'm Rohit!
const developer = {
  name: "Rohit",
  role: "Infrastructure Engineer",
  company: "Academia.edu",
  pronouns: "He/Him",
  currentlyLearning: ["k8s"],
  hobbies: ["reading", "anime", "gaming"],
  funFact: "Red Pandas are not Pandas!"
};

console.log("Welcome to my profile!");"""

    # Carbonara configuration - simplified for testing
    config = {
        "backgroundColor": "#deb563",
        "theme": "duotone-dark",
        "fontFamily": "Fira Code",
        "fontSize": 14,
        "lineNumbers": True,
        "dropShadow": True
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Prepare request data - merge code with config
            request_data = {"code": code}
            request_data.update(config)

            # Make request to Carbonara API
            response = await client.post(
                "https://carbonara.solopov.dev/api/cook",
                json=request_data
            )
            response.raise_for_status()

            # Save the image
            images_dir = Path("../../images")
            images_dir.mkdir(exist_ok=True)

            image_path = images_dir / "intro.png"
            with open(image_path, "wb") as f:
                f.write(response.content)

            print("✅ Carbonara intro image generated successfully")
            print(f"📁 Saved to: {image_path}")

        except httpx.HTTPError as e:
            print(f"❌ HTTP error generating Carbonara image: {e}")
        except Exception as e:
            print(f"❌ Error generating Carbonara image: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(generate_carbonara_intro())
