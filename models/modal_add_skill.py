import dataclasses
import os.path

import discord
import json
from dataclasses import dataclass
from project.models import Skill
from .user import User


@dataclass(init=False)
class ModalAddSkill(discord.ui.Modal):
    skills: Skill

    def __init__(self, *, title: str = "Add your Skills") -> None:
        super().__init__(title=title)

        self.add_item(discord.ui.InputText(label="Your programming language", style=discord.InputTextStyle.long, placeholder="Python, CSS ..."))
        self.add_item(discord.ui.InputText(label="Your framework/cms and libraries", style=discord.InputTextStyle.long, placeholder="Django, Svelte ..."))
        self.add_item(discord.ui.InputText(label="Your tools", style=discord.InputTextStyle.long, placeholder="Figma, Postman ..."))
        self.add_item(discord.ui.InputText(label="Your system", style=discord.InputTextStyle.long, placeholder="MACOS, Linux, Debian ..."))

    async def callback(self, interaction: discord.Interaction):
        path = f"./json/{interaction.user.id}.json"
        file = open(path, "r")

        if (os.path.getsize(path)) != 0:
            user_data = json.load(file)
            user = User(**user_data)
            setattr(user, 'skill', Skill(f"{self.children[0].value}", f"{self.children[1].value}", f"{self.children[2].value}", f"{self.children[3].value}"))
            file.close()
            file = open(path, "w")
            json.dump(dataclasses.asdict(user), file, indent=11)
            file.close()
        else:
            user = User(id_user=interaction.user.id,
                        skill=Skill(self.children[0].value, self.children[1].value, self.children[2].value,
                                    self.children[3].value))
            json_string = json.dumps(dataclasses.asdict(user), indent=11)
            file.write(json_string)
            file.close()

        await interaction.response.send_message("Hello")
