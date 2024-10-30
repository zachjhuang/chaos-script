# credit to FabianGoessling for console output redirection to log element
# https://github.com/zauberzeug/nicegui/discussions/1663

import asyncio
import sys
import importlib
from io import StringIO
from logging import StreamHandler, getLogger

import keyboard
from nicegui import app, ui

import test_main

logger = getLogger(__name__)
logger.setLevel("DEBUG")

options = {'do_chaos': False, 'do_kurzan_front': False, 'do_unas': False, 'do_guild': False}

# Backend
def long_sync_func():
    """A synchronous function with a lot of printing or logging."""
    test_main.main(options=options)

async def start_script():
    """Called after button click"""
    importlib.reload(test_main)
    main_task = asyncio.create_task(asyncio.to_thread(long_sync_func))
    
    async def cancel_main():
        await cancel_task(main_task)

    keyboard.add_hotkey("ctrl+page down", lambda: asyncio.run(cancel_main()))

async def cancel_task(task: asyncio.Task):
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Script cancelled")

async def start_stream(log):
    """Start a 'stream' of console outputs."""
    # Create buffer
    console_output_buffer = StringIO()
    # Standard ouput like a print
    sys.stdout = console_output_buffer
    # Errors/Exceptions
    sys.stderr = console_output_buffer
    # Logmessages
    stream_handler = StreamHandler(console_output_buffer)
    stream_handler.setLevel("DEBUG")
    logger.addHandler(stream_handler)
    while 1:
        await asyncio.sleep(1)  # need to update ui
        # Push the log component and reset the buffer
        log.push(console_output_buffer.getvalue())
        console_output_buffer.truncate(0)
        console_output_buffer.seek(0)

def run_page():
    with ui.row(wrap=False).classes('w-full'):
        with ui.column().classes('w-1/6'):
            ui.switch("Chaos").bind_value(options, 'do_chaos')
            ui.switch("Unas").bind_value(options, 'do_unas')
            ui.switch("Kurzan Front (WIP)").bind_value(options, 'do_kurzan_front')
            ui.switch("Guild").bind_value(options, 'do_guild')
            ui.button("Start script", on_click=start_script)
        log = ui.log().classes("w-full").style("height: 500px")
    app.on_startup(start_stream(log))
