from discord import Embed, Colour
def succes(title:str=None, desc:str=None):
    if title is None:
        e= Embed(
            description= desc,
            colour=Colour.green()
        )
        return e
        
    e=Embed(
        title=title,
        description=desc,
        colour=Colour.green()
    )
    
    return e
        

def error(desc:str):
    e=Embed(
        title='Error',
        description=desc,
        colour=Colour.magenta()
    )
    return e

def normal(**kwargs):
    e = Embed(
        description = kwargs.get('desc', "") if kwargs.get('description') is None else kwargs.get('description'),
        colour = Colour.from_rgb(133, 208, 243)
    )

    if (title := kwargs.get('title', None)):
        e.title = title

    if (url := kwargs.get('url', None)) is not None:
        e.url = url
    
    return e


async def select(ctx, content):
    contents = content.split(',')
    content_count = len(contents) + 1

    e = Embed(
        description='\n'.join(f"{i}\U0000fe0f\U000020e3: {content}" for i, content in enumerate(contents, 1)),
        colour=Colour.from_rgb(133, 208, 243)
    )
    e.set_author(name="設定番号のリアクションを押してね")
    m = await ctx.send(embed=e)

    for i in range(1, content_count):
        await m.add_reaction(f'{i}\U0000fe0f\U000020e3')

    return m

async def select_opt(ctx, content):
    contents = content.split(',')
    content_count = len(contents) + 1

    e = Embed(
        description = '\n'.join(f"{i}\U0000fe0f\U000020e3: {content}" for i, content in enumerate(contents, 1)),
        colour=Colour.from_rgb(133, 208, 243)
    )
    e.set_author(name="オプションを選択してね")

    m = await ctx.send(embed=e)

    for i in range(1, content_count):
        await m.add_reaction(f'{i}\U0000fe0f\U000020e3')

    return m


