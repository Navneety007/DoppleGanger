import os
from Doppleganger import Doppleganger
import jishaku
import cogs


os.environ.setdefault("JISHAKU_HIDE", "1")
os.environ.setdefault("JISHAKU_RETAIN", "1")
os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")


if __name__ == "__main__":

    bot = Doppleganger()

    for name in os.listdir("./cogs"):   
        if name.endswith(".py"):
            bot.load_extension("cogs.{}".format(name[:-3]))

    bot.load_extension('jishaku')
    
    bot.run(os.environ["TOKEN"])


