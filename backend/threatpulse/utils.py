from rich.console import Console

def rich_print(text: str, highlight: bool = True) -> str:
    console = Console()
    with console.capture() as capt:
        console.print(text, highlight=highlight)
    return capt.get()[:-1]