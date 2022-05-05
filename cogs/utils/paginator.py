import discord


class View(discord.ui.View):
	def __init__(self, embeds):
		super().__init__()
		self.embeds = embeds
		self.current_page = 0

	def loop_pages(self, direction):
		if direction == "next":
			self.current_page += 1
			if self.current_page > len(self.embeds) - 1:
				self.current_page = 0
		elif direction == "previous":
			self.current_page -= 1
			if self.current_page < 0:
				self.current_page = len(self.embeds) - 1

	@discord.ui.button(label="Previous", emoji="\N{BLACK LEFT-POINTING TRIANGLE}")
	async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.loop_pages("previous")
		await interaction.response.edit_message(embed=self.embeds[self.current_page])

	@discord.ui.button(label="Close", emoji="\N{OCTAGONAL SIGN}")
	async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.edit_message(view=None)
		self.stop()

	@discord.ui.button(label="Next", emoji="\N{BLACK RIGHT-POINTING TRIANGLE}")
	async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
		self.loop_pages("next")
		await interaction.response.edit_message(embed=self.embeds[self.current_page])
