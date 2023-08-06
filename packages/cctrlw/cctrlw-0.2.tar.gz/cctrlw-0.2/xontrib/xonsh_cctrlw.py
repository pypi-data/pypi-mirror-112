from json import loads

import xonsh
from pathlib import Path
import xonsh.built_ins
from cctrlw.algo import get_streak, load_partitions
from cctrlw import CONFIG_DIR, MODES_JSON
from xonsh.events import events

MODE_ENVVAR, CONFIG_FILE_ENVVAR = "CW_MODE", "CW_CONFIG"
setup_done = False


def setup():
    partition_in_use, partition_id, partitions_json = None, None, None

    @events.on_envvar_change
    def configure(name, newvalue, oldvalue=None):
        try:
            nonlocal partition_id, partitions_json, partition_in_use
            if name == MODE_ENVVAR:
                partition_id = newvalue
            elif name == CONFIG_FILE_ENVVAR:
                partitions_json = newvalue
            else:
                raise StopIteration

            with open(partitions_json, "r") as cfg:
                cfg = load_partitions(loads(cfg.read()))
            partition_in_use = cfg[partition_id]
            print(f"loaded {partition_in_use}")
        except StopIteration:
            pass
        except FileNotFoundError as e:
            print(e)
        except KeyError as e:
            print(
                f"partition {e.args} is not defined; partition list is {list(cfg.keys())}"
            )
        except TypeError as e:
            global setup_done
            assert not setup_done
        except BaseException as e:
            print(e.with_traceback())

    @events.on_envvar_new
    def _(name, value):
        configure(name, value)

    configure(MODE_ENVVAR, "Ap")
    configure(
        CONFIG_FILE_ENVVAR, str(Path(__file__).parents[1] / CONFIG_DIR / MODES_JSON)
    )
    setup_done = True

    @events.on_ptk_create
    def _(bindings, completer, history, prompter):

        from prompt_toolkit.application import get_app
        from prompt_toolkit.filters import vi_insert_mode, vi_navigation_mode
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.keys import Keys

        def process(event):
            try:
                buf = event.current_buffer
                text = buf.text
                if not text:
                    raise ValueError()
                cursor = buf.cursor_position
                r = cursor
                text = text[: int(cursor)]
                text = text[::-1]
                text = text.encode("utf8")
                L = get_streak(text, partition_in_use)
                l = r - L
                return buf.text, buf, l, r
            except ValueError:
                return [None] * 4

        def handle(event, only_move):
            text, buf, l, r = process(event)
            if not text:
                return
            buf.cursor_position = l
            if not only_move:
                buf.text = f"{text[:l]}{text[r:]}"

        @bindings.add(Keys.ControlW, filter=vi_insert_mode)
        def _(event):
            handle(event, False)

        @bindings.add(Keys.ControlW, filter=vi_navigation_mode)
        def _(event):
            handle(event, True)


if not setup_done:
    setup()
    setup_done = True
