from rich.console import Console

def rich_print(text: str) -> str:
    console = Console()
    with console.capture() as capt:
        console.print(text)
    return capt.get()[:-1]