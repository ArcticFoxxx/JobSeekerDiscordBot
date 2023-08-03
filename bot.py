import discord
import api.api_client as api_client
from discord.ext import commands
from main import bot

MAX_LIMIT = 10
#TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
TOKEN = "MTEyOTc3NTk0ODM2ODE5MTU2OQ.GyA9y5.rZdav3_CzdZaJr_fTYsq0-TvMbuh59H2yp1obs"

class CustomHelpCommand(commands.DefaultHelpCommand):
    # Override the send_help method to customize the help message format
    async def send_help(self, ctx):
        embed = discord.Embed(
            title='Bot Command Help',
            description='Custom help message',
            color=discord.Color.blue()
        )
        # Customize the embed with relevant information about your bot's commands
        embed.add_field(name='$jobs', value='Description of command1', inline=False)
        embed.add_field(name='$command2', value='Description of command2', inline=False)
        # Add more fields as needed for other commands

        await ctx.send(embed=embed)

# Replace the default help command with your custom help command
def run_discord_bot():
    
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='$', intents=intents, help_command=CustomHelpCommand())

    bot.remove_command('help')

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} is now running!')


    @bot.command(help='Search for job listings based on job type, salary, location, and limit.')
    async def jobs(ctx, job_type: str, location: str, salary: str = '0', limit: int = 1):
        '''
        Search for job listings based on job type, salary, location, and limit.

        Parameters:
            job_type (str): The type of job to search for.
            location (str): The location where the job should be located.
            salary (str, optional): The minimum salary for the job. Defaults to '0'.
            limit (int, optional): The maximum number of job listings to return. Defaults to 1.

        Raises:
            commands.BadArgument: If the specified limit exceeds the maximum limit.
            commands.MissingRequiredArgument: If either job_type or location is missing.

        Returns:
            None
        '''
        
        if limit > MAX_LIMIT:
            raise commands.BadArgument(f"Limit exceeds the maximum of {MAX_LIMIT}")
    
        if not job_type or not location:
            raise commands.MissingRequiredArgument("missing arguments")
        
        jobs = api_client.get_job_listings(job_type, location, salary, limit)

        if jobs and 'results' in jobs and len(jobs['results']) > 0:
            for job in jobs['results']:
                embed = convert_job_listing_to_embed(job)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="ERROR", description="No job listings found", color=discord.Color.red())
            embed.add_field(name='Try again', value="Try search for a different job title", inline=False)
            await ctx.send(embed=embed)

    @jobs.error
    async def jobs_error(ctx, error):
        """
        Handle errors related to the 'jobs' command.

        Parameters:
            ctx (discord.ext.commands.Context): The context of the command.
            error (Exception): The error that occurred during the command execution.

        Returns:
            None
        """
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Missing arguments", description="You are missing required search arguments", color=discord.Color.red())
            embed.add_field(name='Arguments', value=f"Missing required argument: {error.param}", inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Invalid argument", description="Invalid search argument provided", color=discord.Color.red())
            embed.add_field(name='Argument', value=str(error.param), inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandInvokeError):
            original_error = getattr(error, 'original', error)
            if isinstance(original_error, ValueError):
                embed = discord.Embed(title="Value error", description=str(original_error), color=discord.Color.red())
                await ctx.send(embed=embed)


    @bot.command()
    async def hello(ctx):
        embed = discord.Embed(
            title="Find a Job",
            description="Hello! I am here to help you on your job search!.",
            color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
        )
        embed.add_field(name="Job Commans", value="A really nice field with some information. **The description as well as the fields support markdown!**")

        embed.add_field(name="Inline Field 1", value="Inline Field 1", inline=True)
        embed.add_field(name="Inline Field 2", value="Inline Field 2", inline=True)
        embed.add_field(name="Inline Field 3", value="Inline Field 3", inline=True)
    
        embed.set_footer(text="If you notice any mistakes I make, contact Artic Fox.") # footers can have icons too
        embed.set_author(name="Job Search Helper", icon_url="https://example.com/link-to-my-image.png")
        embed.set_thumbnail(url="https://www.inhouserecruitment.co.uk/wp-content/uploads/2020/01/Reed-NEW-LOGO-1000x600-1.png")
        embed.set_image(url="https://images.squarespace-cdn.com/content/v1/5c42569fb98a78e171f10428/1634545592886-X3OITPQ6S1Z2IQ0V01A7/Frame+269.png")
    
        await ctx.send("Hello! Here's a cool embed.", embed=embed) # Send the embed with some text

    bot.run(TOKEN)


def convert_job_listing_to_embed(job_listing):
    title = job_listing['jobTitle'] if job_listing['jobTitle'] is not None else "No Title"
    description = job_listing['jobDescription'] if job_listing['jobDescription'] is not None else "No Description"
    company = job_listing['employerName'] if job_listing['employerName'] is not None else "No Company"
    location = job_listing['locationName'] if job_listing['locationName'] is not None else "No Location"
    salary_min = '{:,}'.format(job_listing['minimumSalary']) if job_listing['minimumSalary'] is not None else "No Minimum Salary"
    salary_max = '{:,}'.format(job_listing['maximumSalary']) if job_listing['maximumSalary'] is not None else "No Maximum Salary"
    currency = job_listing['currency'] if job_listing['currency'] is not None else "No Currency"
    expiration_date = job_listing['expirationDate'] if job_listing['expirationDate'] is not None else "No Expiration Date"
    job_url = job_listing['jobUrl'] if job_listing['jobUrl'] is not None else "No Job URL"

    embed = discord.Embed(title=title, description=description, color=discord.Color.green())
    embed.add_field(name='Company', value=company, inline=False)
    embed.add_field(name='Location', value=location, inline=False)

    if currency == "No currency":
        embed.add_field(name='Salary', value='No salary available', inline=False)
    else:
        embed.add_field(name='Salary', value=f'{currency} {salary_min} - {currency} {salary_max}', inline=False)

    embed.add_field(name='Expiration Date', value=expiration_date, inline=False)
    embed.add_field(name='Job URL', value=job_url, inline=False)

    return embed

